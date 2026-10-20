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
    "ck_libros_anio_publicacion",
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

        materias_iniciales = {
            "Comunicación",
            "Matemática",
            "Ciencia y Tecnología",
            "Ciencias Sociales",
            "Inglés",
        }
        materias = {
            fila[0] for fila in conn.execute("SELECT nombre FROM materias")
        }
        usuarios = conn.execute(
            """
            SELECT username, rol, activo
              FROM usuarios
             WHERE username IN (
                       'AdminJAQ',
                       'AsistJAQ1',
                       'admin_prueba',
                       'asistente_prueba'
                   )
             ORDER BY username
            """
        ).fetchall()
        registrar(
            resultados,
            materias_iniciales.issubset(materias) and len(materias) >= 22,
            "materias iniciales e institucionales conservadas",
        )
        registrar(
            resultados,
            usuarios
            == [
                ("AdminJAQ", "admin", True),
                ("AsistJAQ1", "asistente", True),
                ("asistente_prueba", "asistente", False),
            ],
            "cuentas institucionales activas y cuenta asistente de prueba inactiva",
        )

        conteos_catalogo = conn.execute(
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
            conteos_catalogo[0] >= 6 and conteos_catalogo[1] >= 7,
            (
                "catálogo institucional conservado "
                f"({conteos_catalogo[0]} libros, {conteos_catalogo[1]} ejemplares, "
                f"{conteos_catalogo[2]} lectores, {conteos_catalogo[3]} préstamos)"
            ),
        )

        residuos_temporales = conn.execute(
            """
            SELECT
                (SELECT count(*) FROM libros
                  WHERE titulo ILIKE 'TEMP-%' OR titulo ILIKE '%PRUEBA%'),
                (SELECT count(*) FROM ejemplares
                  WHERE codigo_qr ILIKE 'TEMP-%' OR codigo_qr ILIKE '%PRUEBA%'),
                (SELECT count(*) FROM lectores
                  WHERE nombres ILIKE 'TEMP-%' OR apellidos ILIKE 'TEMP-%'
                     OR nombres ILIKE '%PRUEBA%' OR apellidos ILIKE '%PRUEBA%')
            """
        ).fetchone()
        registrar(
            resultados,
            residuos_temporales == (0, 0, 0),
            "no existen marcadores de datos temporales en catálogo o lectores",
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
