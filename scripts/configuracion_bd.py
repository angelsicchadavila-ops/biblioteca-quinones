"""Configuración compartida para los scripts de PostgreSQL de la Semana 2."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_ENV = RAIZ_PROYECTO / ".env"


def cargar_entorno() -> None:
    """Carga el archivo .env local sin sobrescribir variables ya exportadas."""
    load_dotenv(RUTA_ENV, override=False)


def obtener_variable(nombre: str) -> str:
    """Obtiene una variable obligatoria sin revelar su valor en los errores."""
    valor = os.getenv(nombre, "").strip()
    if not valor:
        raise RuntimeError(
            f"Falta la variable {nombre}. Configúrala localmente en {RUTA_ENV.name}."
        )
    return valor


def obtener_database_url() -> str:
    cargar_entorno()
    return obtener_variable("DATABASE_URL")
