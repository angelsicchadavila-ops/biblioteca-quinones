"""Consulta única para identificar ejemplares por QR o código manual."""

from __future__ import annotations

import re

import psycopg


PATRON_CODIGO_EJEMPLAR = re.compile(r"^LIB-\d{3,}-EJ\d{2,}$")


def normalizar_codigo(valor: str) -> str:
    """Normaliza el ingreso humano sin alterar la convención almacenada."""
    return valor.strip().upper()


def codigo_valido(codigo: str) -> bool:
    return len(codigo) <= 50 and PATRON_CODIGO_EJEMPLAR.fullmatch(codigo) is not None


def consultar_ejemplar_por_codigo(
    conexion: psycopg.Connection, codigo: str
) -> dict | None:
    """Devuelve solo la ficha necesaria para el terminal interno."""
    return conexion.execute(
        """
        SELECT e.codigo_qr, e.estado_fisico, e.activo,
               l.titulo, l.autor, l.nivel, l.activo AS libro_activo,
               m.nombre AS materia,
               CASE
                   WHEN NOT e.activo OR NOT l.activo OR NOT m.activo THEN 'Inactivo'
                   WHEN e.estado_fisico = 'Dañado' THEN 'Dañado'
                   WHEN p.id IS NOT NULL THEN 'Prestado'
                   ELSE 'Disponible'
               END AS disponibilidad
          FROM ejemplares e
          JOIN libros l ON l.id = e.libro_id
          JOIN materias m ON m.id = l.materia_id
          LEFT JOIN prestamos p
            ON p.ejemplar_id = e.id
           AND p.fecha_devolucion IS NULL
         WHERE e.codigo_qr = %s
        """,
        (codigo,),
    ).fetchone()
