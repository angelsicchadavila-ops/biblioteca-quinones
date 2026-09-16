"""Prepara, consulta o limpia el conjunto controlado TEMP-SEMANA-08."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from configuracion_bd import obtener_database_url


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))
CARPETA_EVIDENCIA = RAIZ_PROYECTO / "docs" / "evidencias" / "semana_08"
MATERIA_TEMPORAL = "TEMP-SEMANA-08 QA"
LIBRO_TEMPORAL = "TEMP-SEMANA-08 QA MOVIL"
LECTOR_NOMBRES = "Lector TEMP"
LECTOR_APELLIDOS = "SEMANA 08"


def _estado(conexion: psycopg.Connection) -> dict:
    return conexion.execute(
        """
        SELECT
            (SELECT count(*) FROM materias WHERE nombre = %s) AS materias,
            (SELECT count(*) FROM libros WHERE titulo = %s) AS libros,
            (SELECT count(*)
               FROM ejemplares e
               JOIN libros l ON l.id = e.libro_id
              WHERE l.titulo = %s) AS ejemplares,
            (SELECT count(*)
               FROM prestamos p
               JOIN ejemplares e ON e.id = p.ejemplar_id
               JOIN libros l ON l.id = e.libro_id
              WHERE l.titulo = %s) AS prestamos,
            (SELECT count(*)
               FROM lectores
              WHERE lower(btrim(nombres)) = lower(%s)
                AND lower(btrim(apellidos)) = lower(%s)) AS lectores
        """,
        (
            MATERIA_TEMPORAL,
            LIBRO_TEMPORAL,
            LIBRO_TEMPORAL,
            LIBRO_TEMPORAL,
            LECTOR_NOMBRES,
            LECTOR_APELLIDOS,
        ),
    ).fetchone()


def mostrar_estado(conexion: psycopg.Connection) -> None:
    estado = _estado(conexion)
    print(
        "Estado TEMP-SEMANA-08: "
        f"materias={estado['materias']}, libros={estado['libros']}, "
        f"ejemplares={estado['ejemplares']}, prestamos={estado['prestamos']}, "
        f"lectores={estado['lectores']}"
    )
    codigos = conexion.execute(
        """
        SELECT e.codigo_qr, e.estado_fisico, e.activo
          FROM ejemplares e
          JOIN libros l ON l.id = e.libro_id
         WHERE l.titulo = %s
         ORDER BY e.id
        """,
        (LIBRO_TEMPORAL,),
    ).fetchall()
    for fila in codigos:
        estado_fisico = fila["estado_fisico"]
        activacion = "Activo" if fila["activo"] else "Inactivo"
        print(f"- {fila['codigo_qr']}: {estado_fisico}, {activacion}")


def preparar(conexion: psycopg.Connection) -> None:
    estado = _estado(conexion)
    if any(estado.values()):
        raise RuntimeError(
            "Ya existen datos TEMP-SEMANA-08. Consulta el estado o límpialos antes de preparar otro conjunto."
        )

    with conexion.transaction():
        materia_id = conexion.execute(
            "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
            (MATERIA_TEMPORAL,),
        ).fetchone()["id"]
        libro_id = conexion.execute(
            """
            INSERT INTO libros (titulo, autor, materia_id, nivel, isbn_editorial)
            VALUES (%s, 'Dato temporal de QA', %s, 'Ambos', 'TEMP-SEMANA-08')
            RETURNING id
            """,
            (LIBRO_TEMPORAL, materia_id),
        ).fetchone()["id"]
        prefijo = f"LIB-{libro_id:03d}-EJ"
        filas = []
        for numero, estado_fisico, activo in (
            (1, "Operativo", True),
            (2, "Operativo", True),
            (3, "Dañado", True),
            (4, "Operativo", False),
        ):
            filas.append(
                conexion.execute(
                    """
                    INSERT INTO ejemplares (libro_id, codigo_qr, estado_fisico, activo)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, codigo_qr
                    """,
                    (libro_id, f"{prefijo}{numero:02d}", estado_fisico, activo),
                ).fetchone()
            )

    from utils.pdf_exporter import generar_pdf_etiquetas
    from utils.qr_generator import generar_qr_png

    CARPETA_EVIDENCIA.mkdir(parents=True, exist_ok=True)
    ruta_qr = CARPETA_EVIDENCIA / "QR_TEMP_SEMANA_08.png"
    ruta_pdf = CARPETA_EVIDENCIA / "ETIQUETAS_QA_SEMANA_08.pdf"
    ruta_qr.write_bytes(generar_qr_png(filas[0]["codigo_qr"]).getvalue())
    etiquetas = [
        {"codigo_qr": fila["codigo_qr"], "titulo": LIBRO_TEMPORAL}
        for fila in filas
    ]
    ruta_pdf.write_bytes(generar_pdf_etiquetas(etiquetas).getvalue())
    print(f"Conjunto preparado. QR disponible: {filas[0]['codigo_qr']}")
    print(f"Archivo QR: {ruta_qr}")
    print(f"Archivo PDF: {ruta_pdf}")


def limpiar(conexion: psycopg.Connection) -> None:
    estado = _estado(conexion)
    if not any(estado.values()):
        print("No existen datos TEMP-SEMANA-08 para limpiar.")
        return
    if estado["materias"] not in (0, 1) or estado["libros"] not in (0, 1):
        raise RuntimeError(
            "La cantidad de materias o libros TEMP-SEMANA-08 no coincide con el conjunto controlado."
        )
    if bool(estado["materias"]) != bool(estado["libros"]):
        raise RuntimeError(
            "La materia y el libro TEMP-SEMANA-08 no forman un conjunto coherente."
        )

    with conexion.transaction():
        ejemplares = conexion.execute(
            """
            SELECT e.id
              FROM ejemplares e
              JOIN libros l ON l.id = e.libro_id
             WHERE l.titulo = %s
             FOR UPDATE OF e
            """,
            (LIBRO_TEMPORAL,),
        ).fetchall()
        ejemplar_ids = [fila["id"] for fila in ejemplares]

        lectores = conexion.execute(
            """
            SELECT id
              FROM lectores
             WHERE lower(btrim(nombres)) = lower(%s)
               AND lower(btrim(apellidos)) = lower(%s)
             FOR UPDATE
            """,
            (LECTOR_NOMBRES, LECTOR_APELLIDOS),
        ).fetchall()
        lector_ids = [fila["id"] for fila in lectores]
        if lector_ids:
            prestamos_ajenos = conexion.execute(
                """
                SELECT count(*) AS total
                  FROM prestamos
                 WHERE lector_id = ANY(%s)
                   AND NOT (ejemplar_id = ANY(%s))
                """,
                (lector_ids, ejemplar_ids or [0]),
            ).fetchone()["total"]
            if prestamos_ajenos:
                raise RuntimeError(
                    "El lector temporal tiene préstamos ajenos al conjunto; se canceló la limpieza."
                )

        if ejemplar_ids:
            conexion.execute(
                "DELETE FROM prestamos WHERE ejemplar_id = ANY(%s)",
                (ejemplar_ids,),
            )
        if lector_ids:
            conexion.execute("DELETE FROM lectores WHERE id = ANY(%s)", (lector_ids,))
        conexion.execute(
            """
            DELETE FROM ejemplares
             WHERE libro_id IN (SELECT id FROM libros WHERE titulo = %s)
            """,
            (LIBRO_TEMPORAL,),
        )
        conexion.execute("DELETE FROM libros WHERE titulo = %s", (LIBRO_TEMPORAL,))
        conexion.execute("DELETE FROM materias WHERE nombre = %s", (MATERIA_TEMPORAL,))
    print("Datos TEMP-SEMANA-08 eliminados de forma controlada.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("accion", choices=("preparar", "estado", "limpiar"))
    argumentos = parser.parse_args()

    with psycopg.connect(
        obtener_database_url(), autocommit=True, row_factory=dict_row
    ) as conexion:
        conexion.execute("SET TIME ZONE 'America/Lima'")
        if argumentos.accion == "preparar":
            preparar(conexion)
        elif argumentos.accion == "limpiar":
            limpiar(conexion)
        mostrar_estado(conexion)


if __name__ == "__main__":
    main()
