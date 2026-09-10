"""Ejecuta pruebas de integridad reales y revierte todos los datos de prueba."""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

import psycopg

from configuracion_bd import obtener_database_url


def esperar_rechazo(
    cursor: psycopg.Cursor,
    nombre: str,
    operacion,
    estados_sql: set[str],
    resultados: list[str],
) -> None:
    cursor.execute("SAVEPOINT caso_rechazado")
    try:
        operacion()
    except psycopg.Error as exc:
        cursor.execute("ROLLBACK TO SAVEPOINT caso_rechazado")
        if exc.sqlstate not in estados_sql:
            raise AssertionError(
                f"{nombre}: SQLSTATE inesperado {exc.sqlstate}"
            ) from exc
        resultados.append(f"[OK] {nombre}")
    else:
        cursor.execute("ROLLBACK TO SAVEPOINT caso_rechazado")
        raise AssertionError(f"{nombre}: la base de datos aceptó un dato inválido")
    finally:
        cursor.execute("RELEASE SAVEPOINT caso_rechazado")


def insertar_y_obtener_id(cursor: psycopg.Cursor, consulta: str, parametros: tuple) -> int:
    return cursor.execute(consulta, parametros).fetchone()[0]


def probar_concurrencia(database_url: str, resultados: list[str]) -> None:
    """Confirma con dos conexiones simultáneas que solo un préstamo se confirma."""
    sufijo = uuid4().hex[:10]
    ids: dict[str, object] = {}

    try:
        with psycopg.connect(database_url, connect_timeout=15) as conn:
            cursor = conn.cursor()
            cursor.execute("SET LOCAL TIME ZONE 'America/Lima'")
            ids["usuario"] = insertar_y_obtener_id(
                cursor,
                """
                INSERT INTO usuarios (username, password_hash, nombre_completo, rol)
                VALUES (%s, 'hash_solo_para_prueba', 'Usuario concurrencia', 'admin')
                RETURNING id
                """,
                (f"concurrencia_{sufijo}",),
            )
            ids["materia"] = insertar_y_obtener_id(
                cursor,
                "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                (f"Materia concurrencia {sufijo}",),
            )
            ids["libro"] = insertar_y_obtener_id(
                cursor,
                """
                INSERT INTO libros (titulo, autor, materia_id, nivel)
                VALUES (%s, 'Autor de prueba', %s, 'Ambos') RETURNING id
                """,
                (f"Libro concurrencia {sufijo}", ids["materia"]),
            )
            ids["ejemplar"] = insertar_y_obtener_id(
                cursor,
                """
                INSERT INTO ejemplares (libro_id, codigo_qr)
                VALUES (%s, %s) RETURNING id
                """,
                (ids["libro"], f"CON-{sufijo}-1"),
            )
            ids["lectores"] = [
                insertar_y_obtener_id(
                    cursor,
                    """
                    INSERT INTO lectores (nombres, apellidos)
                    VALUES (%s, %s) RETURNING id
                    """,
                    (f"Concurrente {numero}", f"Integridad {sufijo}"),
                )
                for numero in (1, 2)
            ]
            conn.commit()

        barrera = Barrier(2)

        def intentar_prestamo(lector_id: int) -> str:
            with psycopg.connect(database_url, connect_timeout=15) as conn:
                conn.execute("SET TIME ZONE 'America/Lima'")
                barrera.wait(timeout=15)
                try:
                    conn.execute(
                        """
                        INSERT INTO prestamos
                            (lector_id, ejemplar_id, registrado_por_usuario_id,
                             nivel_alumno, grado_seccion_alumno, fecha_limite)
                        VALUES (%s, %s, %s, 'Primaria', '6 A',
                                (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                        """,
                        (lector_id, ids["ejemplar"], ids["usuario"]),
                    )
                except psycopg.errors.UniqueViolation:
                    conn.rollback()
                    return "rechazado"
                conn.commit()
                return "aceptado"

        with ThreadPoolExecutor(max_workers=2) as executor:
            estados = sorted(executor.map(intentar_prestamo, ids["lectores"]))

        if estados != ["aceptado", "rechazado"]:
            raise AssertionError(
                f"concurrencia: se esperaban un éxito y un rechazo; resultado {estados}"
            )
        resultados.append("[OK] concurrencia real: solo un préstamo fue confirmado")
    finally:
        if ids:
            with psycopg.connect(database_url, connect_timeout=15) as conn:
                with conn.transaction():
                    if ids.get("ejemplar"):
                        conn.execute(
                            "DELETE FROM prestamos WHERE ejemplar_id = %s",
                            (ids["ejemplar"],),
                        )
                    if ids.get("lectores"):
                        conn.execute(
                            "DELETE FROM lectores WHERE id = ANY(%s)",
                            (ids["lectores"],),
                        )
                    if ids.get("ejemplar"):
                        conn.execute(
                            "DELETE FROM ejemplares WHERE id = %s", (ids["ejemplar"],)
                        )
                    if ids.get("libro"):
                        conn.execute("DELETE FROM libros WHERE id = %s", (ids["libro"],))
                    if ids.get("materia"):
                        conn.execute(
                            "DELETE FROM materias WHERE id = %s", (ids["materia"],)
                        )
                    if ids.get("usuario"):
                        conn.execute("DELETE FROM usuarios WHERE id = %s", (ids["usuario"],))


def main() -> int:
    database_url = obtener_database_url()
    sufijo = uuid4().hex[:10]
    resultados: list[str] = []

    with psycopg.connect(database_url, connect_timeout=15) as conn:
        cursor = conn.cursor()
        cursor.execute("SET LOCAL TIME ZONE 'America/Lima'")

        usuario_id = insertar_y_obtener_id(
            cursor,
            """
            INSERT INTO usuarios (username, password_hash, nombre_completo, rol)
            VALUES (%s, %s, %s, 'admin') RETURNING id
            """,
            (f"integridad_{sufijo}", "hash_solo_para_prueba", "Usuario de integridad"),
        )
        materia_id = insertar_y_obtener_id(
            cursor,
            "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
            (f"Materia integridad {sufijo}",),
        )
        libro_id = insertar_y_obtener_id(
            cursor,
            """
            INSERT INTO libros (titulo, autor, materia_id, nivel)
            VALUES (%s, 'Autor de prueba', %s, 'Ambos') RETURNING id
            """,
            (f"Libro integridad {sufijo}", materia_id),
        )

        ejemplares: list[int] = []
        for numero in range(1, 6):
            estado = "Dañado" if numero == 5 else "Operativo"
            ejemplares.append(
                insertar_y_obtener_id(
                    cursor,
                    """
                    INSERT INTO ejemplares (libro_id, codigo_qr, estado_fisico)
                    VALUES (%s, %s, %s) RETURNING id
                    """,
                    (libro_id, f"INT-{sufijo}-{numero}", estado),
                )
            )

        lectores = [
            insertar_y_obtener_id(
                cursor,
                """
                INSERT INTO lectores (nombres, apellidos)
                VALUES (%s, %s) RETURNING id
                """,
                (f"Lector {numero}", f"Integridad {sufijo}"),
            )
            for numero in range(1, 4)
        ]

        cursor.execute(
            """
            INSERT INTO prestamos
                (lector_id, ejemplar_id, registrado_por_usuario_id,
                 nivel_alumno, grado_seccion_alumno, fecha_limite)
            VALUES (%s, %s, %s, 'Primaria', '5 A',
                    (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
            """,
            (lectores[0], ejemplares[0], usuario_id),
        )
        resultados.append("[OK] préstamo válido aceptado")

        cursor.execute(
            """
            INSERT INTO prestamos
                (lector_id, ejemplar_id, registrado_por_usuario_id,
                 nivel_alumno, grado_seccion_alumno, fecha_limite)
            VALUES (%s, %s, %s, 'Primaria', '5 A',
                    (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 14)
            """,
            (lectores[0], ejemplares[1], usuario_id),
        )
        resultados.append("[OK] segundo préstamo activo aceptado")

        esperar_rechazo(
            cursor,
            "tercer préstamo activo rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO prestamos
                    (lector_id, ejemplar_id, registrado_por_usuario_id,
                     nivel_alumno, grado_seccion_alumno, fecha_limite)
                VALUES (%s, %s, %s, 'Primaria', '5 A',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                """,
                (lectores[0], ejemplares[2], usuario_id),
            ),
            {"23514"},
            resultados,
        )

        esperar_rechazo(
            cursor,
            "segundo préstamo activo del mismo ejemplar rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO prestamos
                    (lector_id, ejemplar_id, registrado_por_usuario_id,
                     nivel_alumno, grado_seccion_alumno, fecha_limite)
                VALUES (%s, %s, %s, 'Secundaria', '2 B',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                """,
                (lectores[1], ejemplares[0], usuario_id),
            ),
            {"23505"},
            resultados,
        )

        cursor.execute(
            """
            INSERT INTO prestamos
                (lector_id, ejemplar_id, registrado_por_usuario_id,
                 nivel_alumno, grado_seccion_alumno,
                 fecha_prestamo, fecha_limite)
            VALUES (%s, %s, %s, 'Secundaria', '3 C',
                    (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima') - interval '10 days',
                    (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date - 5)
            """,
            (lectores[2], ejemplares[2], usuario_id),
        )
        esperar_rechazo(
            cursor,
            "nuevo préstamo con mora rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO prestamos
                    (lector_id, ejemplar_id, registrado_por_usuario_id,
                     nivel_alumno, grado_seccion_alumno, fecha_limite)
                VALUES (%s, %s, %s, 'Secundaria', '3 C',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                """,
                (lectores[2], ejemplares[3], usuario_id),
            ),
            {"23514"},
            resultados,
        )

        esperar_rechazo(
            cursor,
            "ejemplar dañado rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO prestamos
                    (lector_id, ejemplar_id, registrado_por_usuario_id,
                     nivel_alumno, grado_seccion_alumno, fecha_limite)
                VALUES (%s, %s, %s, 'Primaria', '4 A',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                """,
                (lectores[1], ejemplares[4], usuario_id),
            ),
            {"23514"},
            resultados,
        )

        esperar_rechazo(
            cursor,
            "código QR duplicado rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO ejemplares (libro_id, codigo_qr)
                VALUES (%s, %s)
                """,
                (libro_id, f"INT-{sufijo}-1"),
            ),
            {"23505"},
            resultados,
        )

        esperar_rechazo(
            cursor,
            "rol fuera del dominio rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO usuarios
                    (username, password_hash, nombre_completo, rol)
                VALUES (%s, 'hash', 'Rol inválido', 'lector')
                """,
                (f"rol_invalido_{sufijo}",),
            ),
            {"23514"},
            resultados,
        )

        materia_inactiva_id = insertar_y_obtener_id(
            cursor,
            "INSERT INTO materias (nombre, activo) VALUES (%s, FALSE) RETURNING id",
            (f"Materia inactiva {sufijo}",),
        )
        esperar_rechazo(
            cursor,
            "libro con materia inactiva rechazado",
            lambda: cursor.execute(
                """
                INSERT INTO libros (titulo, autor, materia_id, nivel)
                VALUES (%s, 'Autor de prueba', %s, 'Primaria')
                """,
                (f"Libro inválido {sufijo}", materia_inactiva_id),
            ),
            {"23514"},
            resultados,
        )

        esperar_rechazo(
            cursor,
            "devolución sin usuario responsable rechazada",
            lambda: cursor.execute(
                """
                INSERT INTO prestamos
                    (lector_id, ejemplar_id, registrado_por_usuario_id,
                     nivel_alumno, grado_seccion_alumno,
                     fecha_prestamo, fecha_limite, fecha_devolucion)
                VALUES (%s, %s, %s, 'Secundaria', '1 A',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima') - interval '1 day',
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 6,
                        CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')
                """,
                (lectores[1], ejemplares[3], usuario_id),
            ),
            {"23514"},
            resultados,
        )

        conn.rollback()

    probar_concurrencia(database_url, resultados)

    print("\n".join(resultados))
    print(f"Resultado: {len(resultados)}/{len(resultados)} pruebas correctas.")
    print("Todos los datos creados por esta prueba fueron revertidos o eliminados.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, RuntimeError, psycopg.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
