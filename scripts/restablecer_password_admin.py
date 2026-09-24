"""Restablece de forma interactiva la contraseña de una cuenta administradora."""

from __future__ import annotations

import getpass
import sys

import psycopg
from werkzeug.security import generate_password_hash

try:
    from configuracion_bd import obtener_database_url
except ModuleNotFoundError:  # Permite importar el script desde las pruebas.
    from scripts.configuracion_bd import obtener_database_url


LONGITUD_MINIMA = 12


def solicitar_nueva_password() -> str:
    """Solicita y confirma una contraseña sin mostrarla ni recibirla por CLI."""
    password = getpass.getpass("Nueva contraseña: ")
    confirmacion = getpass.getpass("Confirmar nueva contraseña: ")
    if len(password) < LONGITUD_MINIMA:
        raise ValueError(
            f"La contraseña debe tener al menos {LONGITUD_MINIMA} caracteres."
        )
    if password != confirmacion:
        raise ValueError("La confirmación de contraseña no coincide.")
    return password


def actualizar_password_admin(
    conexion: psycopg.Connection, username: str, password: str
) -> bool:
    """Actualiza solo el hash de una cuenta cuyo rol continúa siendo admin."""
    if len(password) < LONGITUD_MINIMA:
        raise ValueError(
            f"La contraseña debe tener al menos {LONGITUD_MINIMA} caracteres."
        )
    with conexion.transaction():
        usuario = conexion.execute(
            """
            SELECT id
              FROM usuarios
             WHERE username = %s AND rol = 'admin'
             FOR UPDATE
            """,
            (username,),
        ).fetchone()
        if usuario is None:
            return False
        fila = conexion.execute(
            """
            UPDATE usuarios
               SET password_hash = %s
             WHERE id = %s AND rol = 'admin'
             RETURNING id
            """,
            (generate_password_hash(password), usuario[0]),
        ).fetchone()
        return fila is not None


def main() -> int:
    username = input("Username del administrador: ").strip()
    if not username:
        print("ERROR: debes indicar una cuenta administradora.", file=sys.stderr)
        return 1

    try:
        password = solicitar_nueva_password()
        with psycopg.connect(obtener_database_url(), connect_timeout=15) as conexion:
            actualizado = actualizar_password_admin(conexion, username, password)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except (RuntimeError, psycopg.Error):
        print("ERROR: no fue posible completar la operación.", file=sys.stderr)
        return 1

    if not actualizado:
        print("ERROR: no se encontró una cuenta con rol admin.", file=sys.stderr)
        return 1

    print("Contraseña administrativa actualizada correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
