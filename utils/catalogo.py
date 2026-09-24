"""Consultas y reglas auxiliares del catálogo bibliográfico."""

from __future__ import annotations

import re

import psycopg


NIVELES_LIBRO = ("Primaria", "Secundaria", "Ambos")
ESTADOS_FISICOS = ("Operativo", "Dañado")


def normalizar_texto(valor: str) -> str:
    """Quita espacios exteriores y reduce espacios consecutivos."""
    return " ".join(valor.split())


def escapar_patron_like(valor: str) -> str:
    """Convierte %, _ y la barra inversa en texto literal para ILIKE."""
    return valor.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def consultar_catalogo(
    conexion: psycopg.Connection,
    texto: str = "",
    materia_id: int | None = None,
    nivel: str = "",
    anio_publicacion: int | None = None,
) -> list[dict]:
    """Devuelve títulos activos y su inventario calculado."""
    condiciones = ["l.activo", "m.activo"]
    parametros: list[object] = []

    if texto:
        patron = f"%{escapar_patron_like(texto)}%"
        condiciones.append(
            "(l.titulo ILIKE %s ESCAPE '\\' OR l.autor ILIKE %s ESCAPE '\\')"
        )
        parametros.extend((patron, patron))

    if materia_id is not None:
        condiciones.append("l.materia_id = %s")
        parametros.append(materia_id)

    if nivel in {"Primaria", "Secundaria"}:
        condiciones.append("l.nivel IN (%s, 'Ambos')")
        parametros.append(nivel)
    elif nivel == "Ambos":
        condiciones.append("l.nivel = 'Ambos'")

    if anio_publicacion is not None:
        condiciones.append("l.anio_publicacion = %s")
        parametros.append(anio_publicacion)

    consulta = f"""
        SELECT l.id, l.titulo, l.autor, l.nivel, l.anio_publicacion,
               l.isbn_editorial,
               m.id AS materia_id, m.nombre AS materia,
               count(e.id) AS total_ejemplares,
               count(e.id) FILTER (
                   WHERE e.activo
                     AND e.estado_fisico = 'Operativo'
                     AND p.id IS NULL
               ) AS disponibles,
               count(e.id) FILTER (
                   WHERE e.activo
                     AND e.estado_fisico = 'Operativo'
                     AND p.id IS NOT NULL
               ) AS prestados,
               count(e.id) FILTER (
                   WHERE e.activo AND e.estado_fisico = 'Dañado'
               ) AS danados,
               count(e.id) FILTER (WHERE NOT e.activo) AS inactivos
          FROM libros l
          JOIN materias m ON m.id = l.materia_id
          LEFT JOIN ejemplares e ON e.libro_id = l.id
          LEFT JOIN prestamos p
            ON p.ejemplar_id = e.id
           AND p.fecha_devolucion IS NULL
         WHERE {" AND ".join(condiciones)}
         GROUP BY l.id, m.id, m.nombre
         ORDER BY lower(l.titulo), lower(l.autor), l.id
    """
    return conexion.execute(consulta, parametros).fetchall()


def consultar_libros_admin(conexion: psycopg.Connection) -> list[dict]:
    """Lista todos los libros con un resumen exclusivo de sus ejemplares."""
    return conexion.execute(
        """
        SELECT l.id, l.titulo, l.autor, l.nivel, l.anio_publicacion,
               l.isbn_editorial, l.activo,
               m.id AS materia_id, m.nombre AS materia, m.activo AS materia_activa,
               count(e.id) AS total_ejemplares,
               count(e.id) FILTER (
                   WHERE e.activo
                     AND e.estado_fisico = 'Operativo'
                     AND p.id IS NULL
               ) AS disponibles,
               count(e.id) FILTER (
                   WHERE e.activo
                     AND e.estado_fisico = 'Operativo'
                     AND p.id IS NOT NULL
               ) AS prestados,
               count(e.id) FILTER (
                   WHERE e.activo AND e.estado_fisico = 'Dañado'
               ) AS danados,
               count(e.id) FILTER (WHERE NOT e.activo) AS inactivos
          FROM libros l
          JOIN materias m ON m.id = l.materia_id
          LEFT JOIN ejemplares e ON e.libro_id = l.id
          LEFT JOIN prestamos p
            ON p.ejemplar_id = e.id
           AND p.fecha_devolucion IS NULL
         GROUP BY l.id, m.id, m.nombre, m.activo
         ORDER BY l.activo DESC, lower(l.titulo), l.id
        """
    ).fetchall()


def consultar_ejemplares(
    conexion: psycopg.Connection, libro_id: int
) -> list[dict]:
    """Lista ejemplares y deriva un estado visible sin guardar redundancias."""
    return conexion.execute(
        """
        SELECT e.id, e.codigo_qr, e.estado_fisico, e.activo, e.fecha_registro,
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
         WHERE e.libro_id = %s
         ORDER BY e.id
        """,
        (libro_id,),
    ).fetchall()


def crear_ejemplares(
    conexion: psycopg.Connection, libro_id: int, cantidad: int
) -> list[str]:
    """Genera códigos estables LIB-XXX-EJYY dentro de una transacción segura."""
    codigos: list[str] = []
    with conexion.transaction():
        libro = conexion.execute(
            "SELECT id FROM libros WHERE id = %s FOR UPDATE", (libro_id,)
        ).fetchone()
        if libro is None:
            raise LookupError("El libro no existe.")

        prefijo = f"LIB-{libro_id:03d}-EJ"
        existentes = conexion.execute(
            "SELECT codigo_qr FROM ejemplares WHERE libro_id = %s", (libro_id,)
        ).fetchall()
        patron = re.compile(rf"^{re.escape(prefijo)}(\d+)$")
        numeros = [
            int(coincidencia.group(1))
            for fila in existentes
            if (coincidencia := patron.fullmatch(fila["codigo_qr"]))
        ]
        siguiente = max(numeros, default=0) + 1

        for numero in range(siguiente, siguiente + cantidad):
            codigo = f"{prefijo}{numero:02d}"
            conexion.execute(
                """
                INSERT INTO ejemplares (libro_id, codigo_qr)
                VALUES (%s, %s)
                """,
                (libro_id, codigo),
            )
            codigos.append(codigo)
    return codigos
