"""Crea el esquema y carga datos iniciales en una base PostgreSQL vacía."""

from __future__ import annotations

import sys

import psycopg
from werkzeug.security import generate_password_hash

from configuracion_bd import RAIZ_PROYECTO, cargar_entorno, obtener_database_url, obtener_variable


TABLAS_PROYECTO = {
    "usuarios",
    "materias",
    "libros",
    "ejemplares",
    "lectores",
    "prestamos",
}


def tablas_existentes(conn: psycopg.Connection) -> set[str]:
    filas = conn.execute(
        """
        SELECT table_name
          FROM information_schema.tables
         WHERE table_schema = 'public'
           AND table_name = ANY(%s)
        """,
        (list(TABLAS_PROYECTO),),
    ).fetchall()
    return {fila[0] for fila in filas}


def main() -> int:
    cargar_entorno()
    database_url = obtener_database_url()
    admin_password = obtener_variable("SEED_ADMIN_PASSWORD")
    asistente_password = obtener_variable("SEED_ASISTENTE_PASSWORD")

    schema_sql = (RAIZ_PROYECTO / "sql" / "schema.sql").read_text(encoding="utf-8")
    seed_sql = (RAIZ_PROYECTO / "sql" / "seed.sql").read_text(encoding="utf-8")

    with psycopg.connect(database_url, autocommit=True, connect_timeout=15) as conn:
        existentes = tablas_existentes(conn)
        if existentes:
            nombres = ", ".join(sorted(existentes))
            raise RuntimeError(
                "La inicialización se detuvo porque ya existen tablas del proyecto: "
                f"{nombres}. Usa verificar_bd.py; no se sobrescribió nada."
            )

        with conn.transaction():
            conn.execute("SET LOCAL TIME ZONE 'America/Lima'")
            conn.execute(schema_sql)
            conn.execute(seed_sql)
            conn.execute(
                """
                INSERT INTO usuarios
                    (username, password_hash, nombre_completo, rol)
                VALUES
                    (%s, %s, %s, %s),
                    (%s, %s, %s, %s)
                """,
                (
                    "admin_prueba",
                    generate_password_hash(admin_password),
                    "Administrador de prueba",
                    "admin",
                    "asistente_prueba",
                    generate_password_hash(asistente_password),
                    "Asistente de prueba",
                    "asistente",
                ),
            )

    print("Inicialización completada: 6 tablas, materias iniciales y 2 cuentas de prueba.")
    print("No se mostraron ni almacenaron contraseñas en archivos versionados.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, psycopg.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
