"""Prueba de humo de solo lectura sobre la aplicación desplegada."""

from __future__ import annotations

import os
import re
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

from dotenv import load_dotenv


URL = "https://biblioteca-quinones.onrender.com"
RAIZ = Path(__file__).resolve().parents[1]
TOKEN_CSRF = re.compile(rb'name="csrf_token" value="([^"]+)"')


def solicitar(opener, ruta: str, datos: dict[str, str] | None = None):
    """Devuelve estado, contenido y cabeceras sin imprimir cookies ni credenciales."""
    cuerpo = urlencode(datos).encode() if datos is not None else None
    solicitud = Request(URL + ruta, data=cuerpo, method="POST" if cuerpo else "GET")
    try:
        with opener.open(solicitud, timeout=90) as respuesta:
            return respuesta.status, respuesta.read(), respuesta.headers
    except HTTPError as error:
        return error.code, error.read(), error.headers


def comprobar(condicion: bool, descripcion: str) -> None:
    if not condicion:
        raise RuntimeError(f"FALLO: {descripcion}")
    print(f"[OK] {descripcion}")


def sesion_usuario(usuario: str, clave: str):
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    estado, pagina, cabeceras = solicitar(opener, "/login")
    comprobar(estado == 200, f"login público disponible para {usuario}")
    cookie = cabeceras.get("Set-Cookie", "")
    comprobar("Secure" in cookie and "HttpOnly" in cookie, "cookie de sesión segura")
    coincidencia = TOKEN_CSRF.search(pagina)
    comprobar(coincidencia is not None, "formulario de login con CSRF")
    estado, _, _ = solicitar(
        opener,
        "/login",
        {
            "username": usuario,
            "password": clave,
            "csrf_token": coincidencia.group(1).decode(),
        },
    )
    comprobar(estado == 200, f"autenticación de {usuario}")
    return opener


def main() -> None:
    load_dotenv(RAIZ / ".env", override=False)
    admin_clave = os.getenv("SEED_ADMIN_PASSWORD", "")
    asistente_clave = os.getenv("SEED_ASISTENTE_PASSWORD", "")
    if not admin_clave or not asistente_clave:
        raise RuntimeError("Faltan contraseñas de prueba en el entorno local.")

    publico = build_opener(HTTPCookieProcessor(CookieJar()))
    estado, pagina, _ = solicitar(publico, "/")
    comprobar(estado == 200 and "Catálogo".encode() in pagina, "catálogo público por HTTPS")
    estado, _, _ = solicitar(publico, "/api/ejemplar/LIB-000-EJ00")
    comprobar(estado == 401, "público sin acceso a API interna")

    admin = sesion_usuario("admin_prueba", admin_clave)
    rutas_admin = (
        "/admin",
        "/admin/materias",
        "/admin/libros",
        "/admin/prestamos",
        "/admin/reportes?reporte=inventario",
        "/admin/reportes?reporte=activos",
        "/admin/reportes?reporte=vencidos",
        "/admin/reportes?reporte=historial",
        "/escaneo",
        "/api/lectores?q=",
    )
    for ruta in rutas_admin:
        estado, _, _ = solicitar(admin, ruta)
        comprobar(estado == 200, f"admin: {ruta}")
    for ruta in ("/admin/ejemplares/0/qr.png", "/admin/ejemplares/0/etiqueta.pdf"):
        estado, _, _ = solicitar(admin, ruta)
        comprobar(estado == 404, f"endpoint QR/PDF protegido y sin ejemplar inexistente: {ruta}")

    asistente = sesion_usuario("asistente_prueba", asistente_clave)
    for ruta in ("/escaneo", "/api/lectores?q="):
        estado, _, _ = solicitar(asistente, ruta)
        comprobar(estado == 200, f"asistente: {ruta}")
    for ruta in ("/admin", "/admin/materias", "/admin/libros", "/admin/prestamos", "/admin/reportes"):
        estado, _, _ = solicitar(asistente, ruta)
        comprobar(estado == 403, f"asistente bloqueado: {ruta}")

    estado, pagina, _ = solicitar(admin, "/admin")
    token = TOKEN_CSRF.search(pagina)
    comprobar(estado == 200 and token is not None, "CSRF presente en sesión admin")
    estado, _, _ = solicitar(admin, "/logout", {"csrf_token": token.group(1).decode()})
    comprobar(estado == 200, "logout admin completado")
    estado, pagina, _ = solicitar(admin, "/admin")
    comprobar(estado == 200 and "Iniciar sesión".encode() in pagina, "sesión cerrada sin acceso admin")


if __name__ == "__main__":
    main()
