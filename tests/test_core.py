"""Pruebas funcionales de autenticación y permisos de la Semana 3."""

from __future__ import annotations

import os
import re
import secrets
import unittest

from dotenv import load_dotenv


load_dotenv(override=False)
CLAVE_PRUEBAS = secrets.token_hex(32)
os.environ.setdefault("SECRET_KEY", CLAVE_PRUEBAS)

from app import crear_app  # noqa: E402
from utils.db import obtener_bd  # noqa: E402


PATRON_CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')


class AplicacionSemana3Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_password = os.getenv("SEED_ADMIN_PASSWORD", "")
        cls.asistente_password = os.getenv("SEED_ASISTENTE_PASSWORD", "")
        if not cls.admin_password or not cls.asistente_password:
            raise unittest.SkipTest(
                "Faltan las contraseñas de prueba en variables de entorno locales."
            )

        cls.app = crear_app(
            {
                "TESTING": True,
                "SECRET_KEY": CLAVE_PRUEBAS,
                "SESSION_COOKIE_SECURE": False,
            }
        )

    def setUp(self) -> None:
        self.cliente = self.app.test_client()

    def obtener_csrf(self, ruta: str = "/login") -> str:
        respuesta = self.cliente.get(ruta)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, username: str, password: str, seguir: bool = False):
        token = self.obtener_csrf()
        return self.cliente.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "csrf_token": token,
            },
            follow_redirects=seguir,
        )

    def test_01_aplicacion_y_conexion_neon(self) -> None:
        with self.app.app_context():
            resultado = obtener_bd().execute("SELECT 1 AS valor").fetchone()
        self.assertEqual(resultado["valor"], 1)

    def test_02_rutas_publicas(self) -> None:
        self.assertEqual(self.cliente.get("/").status_code, 200)
        self.assertEqual(self.cliente.get("/login").status_code, 200)

    def test_03_usuario_no_autenticado_es_redirigido(self) -> None:
        for ruta in ("/admin", "/escaneo"):
            with self.subTest(ruta=ruta):
                respuesta = self.cliente.get(ruta)
                self.assertEqual(respuesta.status_code, 302)
                self.assertEqual(respuesta.headers["Location"], "/login")

    def test_04_login_invalido(self) -> None:
        respuesta = self.login("usuario_inexistente", "credencial_invalida", True)
        self.assertEqual(respuesta.status_code, 401)
        self.assertIn("Usuario o contraseña incorrectos", respuesta.get_data(as_text=True))

    def test_05_login_admin_valido(self) -> None:
        respuesta = self.login("admin_prueba", self.admin_password)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/admin")

    def test_06_admin_accede_a_admin_y_escaneo(self) -> None:
        self.login("admin_prueba", self.admin_password)
        self.assertEqual(self.cliente.get("/admin").status_code, 200)
        self.assertEqual(self.cliente.get("/escaneo").status_code, 200)

    def test_07_login_asistente_valido(self) -> None:
        respuesta = self.login("asistente_prueba", self.asistente_password)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/escaneo")

    def test_08_asistente_accede_a_escaneo(self) -> None:
        self.login("asistente_prueba", self.asistente_password)
        respuesta = self.cliente.get("/escaneo")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Rol verificado: asistente", respuesta.get_data(as_text=True))

    def test_09_asistente_no_accede_a_admin(self) -> None:
        self.login("asistente_prueba", self.asistente_password)
        respuesta = self.cliente.get("/admin")
        self.assertEqual(respuesta.status_code, 403)

    def test_10_logout_invalida_la_sesion(self) -> None:
        self.login("admin_prueba", self.admin_password)
        token = self.obtener_csrf("/admin")
        respuesta = self.cliente.post(
            "/logout", data={"csrf_token": token}, follow_redirects=True
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("La sesión se cerró correctamente", respuesta.get_data(as_text=True))
        self.assertEqual(self.cliente.get("/admin").status_code, 302)

    def test_11_post_sin_csrf_es_rechazado(self) -> None:
        respuesta = self.cliente.post(
            "/login", data={"username": "admin_prueba", "password": "x"}
        )
        self.assertEqual(respuesta.status_code, 400)


if __name__ == "__main__":
    unittest.main()
