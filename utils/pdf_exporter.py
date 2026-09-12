"""Exportación A4 de etiquetas QR en una cuadrícula de 21 unidades."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from utils.qr_generator import generar_qr_png


COLUMNAS = 3
FILAS = 7
ETIQUETAS_POR_PAGINA = COLUMNAS * FILAS
MARGEN_X = 10 * mm
MARGEN_Y = 10 * mm
TAMANO_QR = 25 * mm


def _ajustar_texto(texto: str, ancho_maximo: float, fuente: str, tamano: float) -> str:
    """Acorta una línea para que no invada otra etiqueta."""
    if pdfmetrics.stringWidth(texto, fuente, tamano) <= ancho_maximo:
        return texto
    sufijo = "..."
    recortado = texto
    while recortado and pdfmetrics.stringWidth(
        recortado + sufijo, fuente, tamano
    ) > ancho_maximo:
        recortado = recortado[:-1]
    return recortado.rstrip() + sufijo


def generar_pdf_etiquetas(ejemplares: Sequence[Mapping[str, object]]) -> BytesIO:
    """Genera etiquetas uniformes en A4, tres columnas por siete filas."""
    if not ejemplares:
        raise ValueError("Se requiere al menos un ejemplar para generar etiquetas.")

    salida = BytesIO()
    documento = canvas.Canvas(salida, pagesize=A4, pageCompression=1)
    documento.setTitle("Etiquetas QR de ejemplares")
    documento.setAuthor("Biblioteca Quiñones")

    ancho_pagina, alto_pagina = A4
    ancho_util = ancho_pagina - (2 * MARGEN_X)
    alto_util = alto_pagina - (2 * MARGEN_Y)
    ancho_etiqueta = ancho_util / COLUMNAS
    alto_etiqueta = alto_util / FILAS

    for indice, ejemplar in enumerate(ejemplares):
        posicion = indice % ETIQUETAS_POR_PAGINA
        if posicion == 0 and indice:
            documento.showPage()

        columna = posicion % COLUMNAS
        fila = posicion // COLUMNAS
        x = MARGEN_X + (columna * ancho_etiqueta)
        y = alto_pagina - MARGEN_Y - ((fila + 1) * alto_etiqueta)

        documento.setStrokeColor(colors.HexColor("#D9D9D9"))
        documento.setLineWidth(0.35)
        documento.rect(x, y, ancho_etiqueta, alto_etiqueta, stroke=1, fill=0)

        codigo = str(ejemplar["codigo_qr"])
        titulo = str(ejemplar.get("titulo", ""))
        qr_x = x + ((ancho_etiqueta - TAMANO_QR) / 2)
        qr_y = y + alto_etiqueta - TAMANO_QR - (2.2 * mm)
        documento.drawImage(
            ImageReader(generar_qr_png(codigo)),
            qr_x,
            qr_y,
            width=TAMANO_QR,
            height=TAMANO_QR,
            preserveAspectRatio=True,
            mask="auto",
        )

        centro_x = x + (ancho_etiqueta / 2)
        ancho_texto = ancho_etiqueta - (6 * mm)
        documento.setFillColor(colors.black)
        documento.setFont("Helvetica-Bold", 8)
        documento.drawCentredString(centro_x, y + (7.2 * mm), codigo)
        documento.setFont("Helvetica", 6.5)
        documento.drawCentredString(
            centro_x,
            y + (3.8 * mm),
            _ajustar_texto(titulo, ancho_texto, "Helvetica", 6.5),
        )

    documento.save()
    salida.seek(0)
    return salida
