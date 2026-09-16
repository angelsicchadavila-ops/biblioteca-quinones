"""Pruebas de regresión adicionales para el QA integral de la Semana 8."""

from __future__ import annotations

import os
import re
import secrets
import unittest
from uuid import uuid4

import psycopg
from dotenv import load_dotenv


load_dotenv(override=False)
CLAVE_PRUEBAS = secrets.token_hex(32)
os.environ.setdefault("SECRET_KEY", CLAVE_PRUEBAS)

from app import crear_app  # noqa: E402


PATRON_CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')


class QaSemana8Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database_url = os.getenv("DATABASE_URL", "")
        cls.admin_password = os.getenv("SEED_ADMIN_PASSWORD", "")
        cls.asistente_password = os.getenv("SEED_ASISTENTE_PASSWORD", "")
        if not all(
            (cls.database_url, cls.admin_password, cls.asistente_password)
        ):
            raise unittest.SkipTest(
                "Faltan DATABASE_URL o contraseñas de prueba en el entorno local."
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
        self.sufijo = uuid4().hex[:10]

    def obtener_csrf(self, cliente=None, ruta: str = "/login") -> str:
        cliente = cliente or self.cliente
        respuesta = cliente.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, usuario: str, clave: str, cliente=None) -> None:
        cliente = cliente or self.cliente
        token = self.obtener_csrf(cliente)
        respuesta = cliente.post(
            "/login",
            data={"username": usuario, "password": clave, "csrf_token": token},
        )
        self.assertEqual(respuesta.status_code, 302)

    def limpiar_catalogo_temporal(self) -> None:
        patron = f"%{self.sufijo}%"
        with psycopg.connect(self.database_url, autocommit=True) as conexion:
            conexion.execute(
                """
                DELETE FROM ejemplares
                 WHERE libro_id IN (SELECT id FROM libros WHERE titulo LIKE %s)
                """,
                (patron,),
            )
            conexion.execute("DELETE FROM libros WHERE titulo LIKE %s", (patron,))
            conexion.execute("DELETE FROM materias WHERE nombre LIKE %s", (patron,))

    def test_01_sesion_invalida_se_descarta_y_protege_rutas(self) -> None:
        with self.cliente.session_transaction() as sesion:
            sesion["usuario_id"] = 2_147_483_647
            sesion["csrf_token"] = "token-temporal"

        respuesta = self.cliente.get("/admin")
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.headers["Location"], "/login")
        self.assertEqual(
            self.cliente.get("/api/ejemplar/LIB-000-EJ00").status_code, 401
        )
        with self.cliente.session_transaction() as sesion:
            self.assertNotIn("usuario_id", sesion)

    def test_02_catalogo_sin_coincidencias_no_expone_controles_admin(self) -> None:
        respuesta = self.cliente.get(
            "/", query_string={"q": f"SIN-COINCIDENCIAS-{self.sufijo}"}
        )
        contenido = respuesta.get_data(as_text=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("No se encontraron títulos", contenido)
        self.assertNotIn("Administración", contenido)
        self.assertNotIn("Escaneo", contenido)
        self.assertNotIn("Cerrar sesión", contenido)

    def test_03_urls_directas_respetan_la_matriz_de_roles(self) -> None:
        publico = self.app.test_client()
        for ruta in (
            "/admin",
            "/admin/materias",
            "/admin/libros",
            "/admin/libros/nuevo",
            "/admin/prestamos",
            "/admin/reportes",
            "/escaneo",
        ):
            with self.subTest(rol="publico", ruta=ruta):
                self.assertEqual(publico.get(ruta).status_code, 302)
        self.assertEqual(publico.get("/api/lectores?q=x").status_code, 401)
        self.assertEqual(publico.get("/api/ejemplar/LIB-000-EJ00").status_code, 401)

        asistente = self.app.test_client()
        self.login("asistente_prueba", self.asistente_password, asistente)
        self.assertEqual(asistente.get("/escaneo").status_code, 200)
        self.assertEqual(asistente.get("/api/lectores?q=x").status_code, 200)
        for ruta in (
            "/admin",
            "/admin/materias",
            "/admin/materias/999999/editar",
            "/admin/libros",
            "/admin/libros/nuevo",
            "/admin/libros/999999/editar",
            "/admin/libros/999999/ejemplares",
            "/admin/ejemplares/999999/qr.png",
            "/admin/ejemplares/999999/etiqueta.pdf",
            "/admin/prestamos",
            "/admin/reportes",
        ):
            with self.subTest(rol="asistente", ruta=ruta):
                self.assertEqual(asistente.get(ruta).status_code, 403)

        admin = self.app.test_client()
        self.login("admin_prueba", self.admin_password, admin)
        for ruta in (
            "/admin",
            "/admin/materias",
            "/admin/libros",
            "/admin/libros/nuevo",
            "/admin/prestamos",
            "/admin/reportes",
            "/escaneo",
            "/api/lectores?q=x",
        ):
            with self.subTest(rol="admin", ruta=ruta):
                self.assertEqual(admin.get(ruta).status_code, 200)

    def test_04_no_se_crean_ejemplares_en_libro_inactivo(self) -> None:
        materia = f"TEMP-SEMANA-08-MATERIA-{self.sufijo}"
        titulo = f"TEMP-SEMANA-08-LIBRO-{self.sufijo}"
        try:
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                materia_id = conexion.execute(
                    "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                    (materia,),
                ).fetchone()[0]
                libro_id = conexion.execute(
                    """
                    INSERT INTO libros (titulo, autor, materia_id, nivel)
                    VALUES (%s, 'Autor temporal', %s, 'Primaria')
                    RETURNING id
                    """,
                    (titulo, materia_id),
                ).fetchone()[0]
                conexion.execute(
                    "INSERT INTO ejemplares (libro_id, codigo_qr) VALUES (%s, %s)",
                    (libro_id, f"LIB-{libro_id:03d}-EJ01"),
                )
                conexion.execute(
                    "UPDATE libros SET activo = FALSE WHERE id = %s", (libro_id,)
                )

            self.login("admin_prueba", self.admin_password)
            token = self.obtener_csrf(self.cliente, "/admin")
            respuesta = self.cliente.post(
                f"/admin/libros/{libro_id}/ejemplares",
                data={"cantidad": "1", "csrf_token": token},
                follow_redirects=True,
            )
            contenido = respuesta.get_data(as_text=True)
            self.assertIn("libro está inactivo", contenido)
            self.assertIn("text-bg-secondary\">Inactivo", contenido)
            with psycopg.connect(self.database_url) as conexion:
                total = conexion.execute(
                    "SELECT count(*) FROM ejemplares WHERE libro_id = %s",
                    (libro_id,),
                ).fetchone()[0]
            self.assertEqual(total, 1)
        finally:
            self.limpiar_catalogo_temporal()


if __name__ == "__main__":
    unittest.main()
