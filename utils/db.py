"""Conexión PostgreSQL por solicitud para la aplicación Flask."""

from __future__ import annotations

import psycopg
from flask import current_app, g
from psycopg.rows import dict_row


def obtener_bd() -> psycopg.Connection:
    """Abre una conexión a Neon y la reutiliza durante la solicitud actual."""
    if "bd" not in g:
        g.bd = psycopg.connect(
            current_app.config["DATABASE_URL"],
            autocommit=True,
            connect_timeout=15,
            row_factory=dict_row,
        )
        g.bd.execute("SET TIME ZONE 'America/Lima'")
    return g.bd


def cerrar_bd(_error: BaseException | None = None) -> None:
    """Cierra la conexión asociada a la solicitud, si existe."""
    conexion = g.pop("bd", None)
    if conexion is not None:
        conexion.close()


def iniciar_bd(app) -> None:
    """Registra el cierre automático de conexiones en la aplicación."""
    app.teardown_appcontext(cerrar_bd)
