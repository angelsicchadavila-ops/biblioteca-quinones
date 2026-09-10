"""Verifica tablas, restricciones, índices, trigger y datos iniciales."""

from __future__ import annotations

import sys

import psycopg

from configuracion_bd import obtener_database_url


TABLAS_ESPERADAS = {
    "usuarios",
    "materias",
    "libros",
    "ejemplares",
    "lectores",
    "prestamos",
}

RESTRICCIONES_ESPERADAS = {
    "uq_usuarios_username",
    "ck_usuarios_rol",
    "uq_materias_nombre",
    "fk_libros_materia",
    "ck_libros_nivel",
    "fk_ejemplares_libro",
    "uq_ejemplares_codigo_qr",
    "ck_ejemplares_estado_fisico",
    "fk_prestamos_lector",
    "fk_prestamos_ejemplar",
    "fk_prestamos_usuario_registro",
    "fk_prestamos_usuario_devolucion",
    "ck_prestamos_nivel_alumno",
    "ck_prestamos_fecha_limite",
    "ck_prestamos_devolucion",
}

INDICES_ESPERADOS = {
    "uq_prestamos_ejemplar_activo",
    "idx_libros_titulo_lower",
    "idx_libros_autor_lower",
    "idx_libros_materia_nivel_activo",
    "idx_ejemplares_libro_activo",
    "idx_prestamos_lector_activo",
    "idx_prestamos_fecha_limite_activos",
    "idx_prestamos_fecha_prestamo",
    "idx_prestamos_usuario_registro",
    "idx_prestamos_usuario_devolucion",
}


def registrar(resultado: list[str], condicion: bool, descripcion: str) -> None:
    marca = "OK" if condicion else "FALLO"
    resultado.append(f"[{marca}] {descripcion}")


def main() -> int:
    resultados: list[str] = []
    with psycopg.connect(obtener_database_url(), connect_timeout=15) as conn:
        conn.execute("SET TIME ZONE 'America/Lima'")

        tablas = {
            fila[0]
            for fila in conn.execute(
                """
                SELECT table_name
                  FROM information_schema.tables
                 WHERE table_schema = 'public'
                """
            )
        }
        registrar(
            resultados,
            TABLAS_ESPERADAS.issubset(tablas),
            "están creadas las 6 tablas del DER",
        )

        restricciones = {
            fila[0]
            for fila in conn.execute(
                """
                SELECT c.conname
                  FROM pg_constraint c
                  JOIN pg_class t ON t.oid = c.conrelid
                  JOIN pg_namespace n ON n.oid = t.relnamespace
                 WHERE n.nspname = 'public'
                """
            )
        }
        faltantes = sorted(RESTRICCIONES_ESPERADAS - restricciones)
        registrar(
            resultados,
            not faltantes,
            "restricciones esenciales presentes"
            + (f"; faltan: {', '.join(faltantes)}" if faltantes else ""),
        )

        indices = {
            fila[0]
            for fila in conn.execute(
                "SELECT indexname FROM pg_indexes WHERE schemaname = 'public'"
            )
        }
        faltantes = sorted(INDICES_ESPERADOS - indices)
        registrar(
            resultados,
            not faltantes,
            "índices funcionales y de búsqueda presentes"
            + (f"; faltan: {', '.join(faltantes)}" if faltantes else ""),
        )

        triggers = {
            fila[0]
            for fila in conn.execute(
                """
                SELECT tgname
                  FROM pg_trigger
                 WHERE tgname IN (
                           'trg_validar_materia_activa_libro',
                           'trg_validar_prestamo_activo'
                       )
                   AND NOT tgisinternal
                """
            )
        }
        registrar(
            resultados,
            triggers
            == {
                "trg_validar_materia_activa_libro",
                "trg_validar_prestamo_activo",
            },
            "triggers de materia activa y préstamos presentes",
        )

        materias = conn.execute("SELECT count(*) FROM materias").fetchone()[0]
        usuarios = conn.execute(
            """
            SELECT username, rol
              FROM usuarios
             WHERE username IN ('admin_prueba', 'asistente_prueba')
             ORDER BY username
            """
        ).fetchall()
        registrar(resultados, materias == 5, "cinco materias iniciales cargadas")
        registrar(
            resultados,
            usuarios == [("admin_prueba", "admin"), ("asistente_prueba", "asistente")],
            "cuentas de prueba cargadas con roles válidos",
        )

        conteos_operativos = conn.execute(
            """
            SELECT
                (SELECT count(*) FROM libros),
                (SELECT count(*) FROM ejemplares),
                (SELECT count(*) FROM lectores),
                (SELECT count(*) FROM prestamos)
            """
        ).fetchone()
        registrar(
            resultados,
            conteos_operativos == (0, 0, 0, 0),
            "no quedaron datos temporales de las pruebas de integridad",
        )

    print("\n".join(resultados))
    correctos = sum(linea.startswith("[OK]") for linea in resultados)
    print(f"Resultado: {correctos}/{len(resultados)} verificaciones correctas.")
    return 0 if correctos == len(resultados) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, psycopg.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
