"""Generación en memoria de códigos QR estables para ejemplares."""

from __future__ import annotations

from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_M


def construir_qr(codigo: str) -> qrcode.QRCode:
    """Construye un QR cuyo único contenido es el código recibido."""
    if not codigo or len(codigo) > 50:
        raise ValueError("El código QR debe contener entre 1 y 50 caracteres.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(codigo, optimize=0)
    qr.make(fit=True)

    contenido = b"".join(segmento.data for segmento in qr.data_list).decode("utf-8")
    if contenido != codigo:
        raise ValueError("El contenido generado no coincide con el código del ejemplar.")
    return qr


def generar_qr_png(codigo: str) -> BytesIO:
    """Devuelve una imagen PNG del QR sin crear archivos temporales."""
    imagen = construir_qr(codigo).make_image(fill_color="black", back_color="white")
    salida = BytesIO()
    imagen.save(salida, format="PNG")
    salida.seek(0)
    return salida
