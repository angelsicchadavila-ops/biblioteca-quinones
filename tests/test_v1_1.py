"""Pruebas funcionales y de seguridad específicas de la versión 1.1."""

from __future__ import annotations

import os
import re
import secrets
import unittest
from unittest.mock import patch
from uuid import uuid4

import psycopg
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash


load_dotenv(override=False)
CLAVE_PRUEBAS = secrets.token_hex(32)
os.environ.setdefault("SECRET_KEY", CLAVE_PRUEBAS)

from app import crear_app  # noqa: E402
from scripts.restablecer_password_admin import (  # noqa: E402
    actualizar_password_admin,
    solicitar_nueva_password,
)


PATRON_CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')


class FuncionalidadV11Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database_url = os.getenv("DATABASE_URL", "")
        cls.admin_password = os.getenv("SEED_ADMIN_PASSWORD", "")
        cls.asistente_password = os.getenv("SEED_ASISTENTE_PASSWORD", "")
        if not all((cls.database_url, cls.admin_password, cls.asistente_password)):
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
        self.sufijo = uuid4().hex[:10]

    def obtener_csrf(self, cliente, ruta: str) -> str:
        respuesta = cliente.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, cliente, username: str, password: str, seguir: bool = False):
        token = self.obtener_csrf(cliente, "/login")
        return cliente.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "csrf_token": token,
            },
            follow_redirects=seguir,
        )

    def crear_materia(self) -> int:
        with psycopg.connect(self.database_url, autocommit=True) as conexion:
            return conexion.execute(
                "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                (f"TEMP-V11-MATERIA-{self.sufijo}",),
            ).fetchone()[0]

    def limpiar(self) -> None:
        patron = f"%{self.sufijo}%"
        with psycopg.connect(self.database_url, autocommit=True) as conexion:
            conexion.execute(
                """
                DELETE FROM prestamos
                 WHERE ejemplar_id IN (
                       SELECT e.id
                         FROM ejemplares e
                         JOIN libros l ON l.id = e.libro_id
                        WHERE l.titulo LIKE %s
                 )
                    OR lector_id IN (
                       SELECT id FROM lectores WHERE apellidos LIKE %s
                 )
                    OR registrado_por_usuario_id IN (
                       SELECT id FROM usuarios WHERE username LIKE %s
                 )
                    OR devuelto_por_usuario_id IN (
                       SELECT id FROM usuarios WHERE username LIKE %s
                 )
                """,
                (patron, patron, patron, patron),
            )
            conexion.execute(
                "DELETE FROM lectores WHERE apellidos LIKE %s", (patron,)
            )
            conexion.execute(
                """
                DELETE FROM ejemplares
                 WHERE libro_id IN (
                       SELECT id FROM libros WHERE titulo LIKE %s
                 )
                """,
                (patron,),
            )
            conexion.execute("DELETE FROM libros WHERE titulo LIKE %s", (patron,))
            conexion.execute("DELETE FROM materias WHERE nombre LIKE %s", (patron,))
            conexion.execute("DELETE FROM usuarios WHERE username LIKE %s", (patron,))

    def test_01_anio_creacion_edicion_filtros_y_legado(self) -> None:
        materia_id = self.crear_materia()
        cliente = self.app.test_client()
        self.login(cliente, "admin_prueba", self.admin_password)
        titulo_2022 = f"TEMP-V11-LIBRO-2022-{self.sufijo}"
        titulo_2021 = f"TEMP-V11-LIBRO-2021-{self.sufijo}"
        titulo_legado = f"TEMP-V11-LIBRO-LEGADO-{self.sufijo}"
        try:
            token = self.obtener_csrf(cliente, "/admin")
            respuesta = cliente.post(
                "/admin/libros/nuevo",
                data={
                    "titulo": titulo_2022,
                    "autor": "Autor v1.1",
                    "materia_id": str(materia_id),
                    "nivel": "Secundaria",
                    "anio_publicacion": "2022",
                    "isbn_editorial": "Editorial v1.1",
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                libro_id, anio = conexion.execute(
                    """
                    SELECT id, anio_publicacion
                      FROM libros
                     WHERE titulo = %s
                    """,
                    (titulo_2022,),
                ).fetchone()
                self.assertEqual(anio, 2022)
                conexion.execute(
                    """
                    INSERT INTO libros
                        (titulo, autor, materia_id, nivel, anio_publicacion)
                    VALUES (%s, 'Autor v1.1', %s, 'Secundaria', 2021)
                    """,
                    (titulo_2021, materia_id),
                )
                legado_id = conexion.execute(
                    """
                    INSERT INTO libros (titulo, autor, materia_id, nivel)
                    VALUES (%s, 'Autor legado', %s, 'Primaria')
                    RETURNING id
                    """,
                    (titulo_legado, materia_id),
                ).fetchone()[0]

            token = self.obtener_csrf(cliente, f"/admin/libros/{libro_id}/editar")
            respuesta = cliente.post(
                f"/admin/libros/{libro_id}/editar",
                data={
                    "titulo": titulo_2022,
                    "autor": "Autor actualizado",
                    "materia_id": str(materia_id),
                    "nivel": "Secundaria",
                    "anio_publicacion": "2023",
                    "isbn_editorial": "Editorial actualizada",
                    "csrf_token": token,
                },
                follow_redirects=True,
            )
            self.assertIn("Libro actualizado correctamente", respuesta.get_data(as_text=True))

            publico = self.app.test_client()
            respuesta = publico.get(
                "/",
                query_string={
                    "q": self.sufijo,
                    "materia": materia_id,
                    "nivel": "Secundaria",
                    "anio": "2023",
                },
            )
            contenido = respuesta.get_data(as_text=True)
            self.assertIn(titulo_2022, contenido)
            self.assertNotIn(titulo_2021, contenido)
            self.assertIn('value="2023"', contenido)
            self.assertIn("Año 2023", contenido)

            token = self.obtener_csrf(cliente, f"/admin/libros/{legado_id}/editar")
            respuesta = cliente.post(
                f"/admin/libros/{legado_id}/editar",
                data={
                    "titulo": f"{titulo_legado} EDITADO",
                    "autor": "Autor legado actualizado",
                    "materia_id": str(materia_id),
                    "nivel": "Primaria",
                    "anio_publicacion": "",
                    "isbn_editorial": "",
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            with psycopg.connect(self.database_url) as conexion:
                self.assertIsNone(
                    conexion.execute(
                        "SELECT anio_publicacion FROM libros WHERE id = %s",
                        (legado_id,),
                    ).fetchone()[0]
                )

            for indice, anio_invalido in enumerate(("", "999", "0999", "10000", "abcd")):
                token = self.obtener_csrf(cliente, "/admin/libros/nuevo")
                respuesta = cliente.post(
                    "/admin/libros/nuevo",
                    data={
                        "titulo": f"TEMP-V11-INVALIDO-{indice}-{self.sufijo}",
                        "autor": "Autor inválido",
                        "materia_id": str(materia_id),
                        "nivel": "Primaria",
                        "anio_publicacion": anio_invalido,
                        "isbn_editorial": "",
                        "csrf_token": token,
                    },
                )
                self.assertEqual(respuesta.status_code, 200)
            with psycopg.connect(self.database_url) as conexion:
                total = conexion.execute(
                    "SELECT count(*) FROM libros WHERE titulo LIKE %s",
                    (f"TEMP-V11-INVALIDO-%-{self.sufijo}",),
                ).fetchone()[0]
                self.assertEqual(total, 0)
        finally:
            self.limpiar()

    def test_02_asistente_gestiona_libros_sin_estado_materias_ni_ejemplares(self) -> None:
        materia_id = self.crear_materia()
        asistente = self.app.test_client()
        self.login(asistente, "asistente_prueba", self.asistente_password)
        titulo = f"TEMP-V11-ASISTENTE-{self.sufijo}"
        try:
            self.assertEqual(asistente.get("/admin/libros").status_code, 200)
            self.assertEqual(asistente.get("/admin/libros/nuevo").status_code, 200)
            token = self.obtener_csrf(asistente, "/admin/libros/nuevo")
            respuesta = asistente.post(
                "/admin/libros/nuevo",
                data={
                    "titulo": titulo,
                    "autor": "Autor asistente",
                    "materia_id": str(materia_id),
                    "nivel": "Primaria",
                    "anio_publicacion": "2024",
                    "isbn_editorial": "Editorial asistente",
                    "rol": "admin",
                    "activo": "false",
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            self.assertTrue(respuesta.headers["Location"].endswith("/admin/libros"))
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                libro_id, activo = conexion.execute(
                    "SELECT id, activo FROM libros WHERE titulo = %s", (titulo,)
                ).fetchone()
                self.assertTrue(activo)

            token = self.obtener_csrf(asistente, f"/admin/libros/{libro_id}/editar")
            respuesta = asistente.post(
                f"/admin/libros/{libro_id}/editar",
                data={
                    "titulo": f"{titulo} EDITADO",
                    "autor": "Autor editado",
                    "materia_id": str(materia_id),
                    "nivel": "Ambos",
                    "anio_publicacion": "2025",
                    "isbn_editorial": "ISBN editado",
                    "activo": "false",
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                fila = conexion.execute(
                    """
                    SELECT titulo, autor, nivel, anio_publicacion,
                           isbn_editorial, activo
                      FROM libros WHERE id = %s
                    """,
                    (libro_id,),
                ).fetchone()
                self.assertEqual(
                    fila[:5],
                    (f"{titulo} EDITADO", "Autor editado", "Ambos", 2025, "ISBN editado"),
                )
                self.assertTrue(fila[5])

            token = self.obtener_csrf(asistente, "/admin/libros")
            self.assertEqual(
                asistente.post(
                    f"/admin/libros/{libro_id}/estado",
                    data={"csrf_token": token},
                ).status_code,
                403,
            )
            for ruta in (
                "/admin/materias",
                f"/admin/libros/{libro_id}/ejemplares",
                "/admin/usuarios/nuevo",
            ):
                with self.subTest(ruta=ruta, metodo="POST"):
                    self.assertEqual(
                        asistente.post(
                            ruta,
                            data={
                                "csrf_token": token,
                                "nombre": "Manipulado",
                                "cantidad": "1",
                                "rol": "admin",
                            },
                        ).status_code,
                        403,
                    )
            for ruta in (
                "/admin/materias",
                f"/admin/libros/{libro_id}/ejemplares",
                "/admin/usuarios",
                "/admin/usuarios/nuevo",
            ):
                with self.subTest(ruta=ruta):
                    self.assertEqual(asistente.get(ruta).status_code, 403)
            self.assertEqual(
                asistente.post(
                    "/admin/usuarios/999999/estado",
                    data={"csrf_token": token},
                ).status_code,
                403,
            )
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                conexion.execute(
                    "UPDATE libros SET activo = FALSE WHERE id = %s", (libro_id,)
                )
            listado = asistente.get("/admin/libros").get_data(as_text=True)
            self.assertIn(f"{titulo} EDITADO", listado)
            self.assertNotIn("Reactivar", listado)
        finally:
            self.limpiar()

    def test_03_admin_gestiona_asistente_y_conserva_trazabilidad(self) -> None:
        admin = self.app.test_client()
        self.login(admin, "admin_prueba", self.admin_password)
        username = f"temp_v11_{self.sufijo}"
        password_inicial = secrets.token_urlsafe(18)
        password_nueva = secrets.token_urlsafe(20)
        try:
            token = self.obtener_csrf(admin, "/admin/usuarios/nuevo")
            respuesta = admin.post(
                "/admin/usuarios/nuevo",
                data={
                    "username": username,
                    "nombre_completo": "",
                    "password": password_inicial,
                    "confirmar_password": password_inicial,
                    "csrf_token": token,
                },
            )
            self.assertIn("nombre completo es obligatorio", respuesta.get_data(as_text=True))

            for password, confirmacion in (("corta", "corta"), (password_inicial, "distinta")):
                token = self.obtener_csrf(admin, "/admin/usuarios/nuevo")
                respuesta = admin.post(
                    "/admin/usuarios/nuevo",
                    data={
                        "username": username,
                        "nombre_completo": f"Asistente Temporal {self.sufijo}",
                        "password": password,
                        "confirmar_password": confirmacion,
                        "csrf_token": token,
                    },
                )
                self.assertEqual(respuesta.status_code, 200)

            token = self.obtener_csrf(admin, "/admin/usuarios/nuevo")
            respuesta = admin.post(
                "/admin/usuarios/nuevo",
                data={
                    "username": username,
                    "nombre_completo": f"Asistente Temporal {self.sufijo}",
                    "password": password_inicial,
                    "confirmar_password": password_inicial,
                    "rol": "admin",
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                usuario_id, rol, hash_guardado = conexion.execute(
                    """
                    SELECT id, rol, password_hash
                      FROM usuarios WHERE username = %s
                    """,
                    (username,),
                ).fetchone()
                self.assertEqual(rol, "asistente")
                self.assertNotEqual(hash_guardado, password_inicial)
                self.assertTrue(check_password_hash(hash_guardado, password_inicial))

                listado = admin.get("/admin/usuarios").get_data(as_text=True)
                self.assertIn(username, listado)
                self.assertNotIn("admin_prueba", listado)

                materia_id = conexion.execute(
                    "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                    (f"TEMP-V11-MATERIA-{self.sufijo}",),
                ).fetchone()[0]
                libro_id = conexion.execute(
                    """
                    INSERT INTO libros
                        (titulo, autor, materia_id, nivel, anio_publicacion)
                    VALUES (%s, 'Autor', %s, 'Primaria', 2024)
                    RETURNING id
                    """,
                    (f"TEMP-V11-TRAZA-{self.sufijo}", materia_id),
                ).fetchone()[0]
                ejemplar_id = conexion.execute(
                    """
                    INSERT INTO ejemplares (libro_id, codigo_qr)
                    VALUES (%s, %s) RETURNING id
                    """,
                    (libro_id, f"LIB-{libro_id:03d}-EJ01"),
                ).fetchone()[0]
                lector_id = conexion.execute(
                    """
                    INSERT INTO lectores (nombres, apellidos)
                    VALUES ('Lector', %s) RETURNING id
                    """,
                    (f"TEMP-V11-{self.sufijo}",),
                ).fetchone()[0]
                conexion.execute(
                    """
                    INSERT INTO prestamos
                        (lector_id, ejemplar_id, registrado_por_usuario_id,
                         nivel_alumno, grado_seccion_alumno, fecha_limite)
                    VALUES (%s, %s, %s, 'Primaria', '1 A',
                            (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                    """,
                    (lector_id, ejemplar_id, usuario_id),
                )

            asistente_sesion = self.app.test_client()
            self.assertEqual(
                self.login(asistente_sesion, username, password_inicial).status_code, 302
            )

            token = self.obtener_csrf(
                admin, f"/admin/usuarios/{usuario_id}/contrasena"
            )
            respuesta = admin.post(
                f"/admin/usuarios/{usuario_id}/contrasena",
                data={
                    "password": password_nueva,
                    "confirmar_password": password_nueva,
                    "csrf_token": token,
                },
            )
            self.assertEqual(respuesta.status_code, 302)
            self.assertEqual(
                self.login(self.app.test_client(), username, password_inicial).status_code,
                401,
            )
            nueva_sesion = self.app.test_client()
            self.assertEqual(
                self.login(nueva_sesion, username, password_nueva).status_code, 302
            )

            token = self.obtener_csrf(admin, "/admin/usuarios")
            self.assertEqual(
                admin.post(
                    f"/admin/usuarios/{usuario_id}/estado",
                    data={"csrf_token": token},
                ).status_code,
                302,
            )
            respuesta = nueva_sesion.get("/escaneo")
            self.assertEqual(respuesta.status_code, 302)
            self.assertTrue(respuesta.headers["Location"].endswith("/login"))
            self.assertEqual(
                self.login(self.app.test_client(), username, password_nueva).status_code,
                401,
            )
            with psycopg.connect(self.database_url) as conexion:
                traza = conexion.execute(
                    """
                    SELECT u.username, u.nombre_completo, u.activo
                      FROM prestamos p
                      JOIN usuarios u ON u.id = p.registrado_por_usuario_id
                     WHERE u.id = %s
                    """,
                    (usuario_id,),
                ).fetchone()
                self.assertEqual(traza[0], username)
                self.assertFalse(traza[2])
                admin_id = conexion.execute(
                    "SELECT id FROM usuarios WHERE username = 'admin_prueba'"
                ).fetchone()[0]

            self.assertEqual(
                admin.post(
                    f"/admin/usuarios/{admin_id}/estado",
                    data={"csrf_token": token},
                ).status_code,
                404,
            )
            self.assertEqual(
                admin.get(f"/admin/usuarios/{admin_id}/contrasena").status_code, 404
            )

            token = self.obtener_csrf(admin, "/admin/usuarios")
            self.assertEqual(
                admin.post(
                    f"/admin/usuarios/{usuario_id}/estado",
                    data={"csrf_token": token},
                ).status_code,
                302,
            )
            self.assertEqual(
                self.login(self.app.test_client(), username, password_nueva).status_code,
                302,
            )
        finally:
            self.limpiar()

    def test_04_recuperacion_tecnica_admin_segura(self) -> None:
        username = f"temp_admin_{self.sufijo}"
        password_anterior = secrets.token_urlsafe(18)
        password_nueva = secrets.token_urlsafe(20)
        try:
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                conexion.execute(
                    """
                    INSERT INTO usuarios
                        (username, password_hash, nombre_completo, rol)
                    VALUES (%s, %s, %s, 'admin')
                    """,
                    (
                        username,
                        generate_password_hash(password_anterior),
                        f"Admin Temporal {self.sufijo}",
                    ),
                )

            with patch(
                "scripts.restablecer_password_admin.getpass.getpass",
                side_effect=(password_nueva, password_nueva),
            ):
                self.assertEqual(solicitar_nueva_password(), password_nueva)
            with patch(
                "scripts.restablecer_password_admin.getpass.getpass",
                side_effect=("corta", "corta"),
            ):
                with self.assertRaises(ValueError):
                    solicitar_nueva_password()
            with patch(
                "scripts.restablecer_password_admin.getpass.getpass",
                side_effect=(password_nueva, "diferente"),
            ):
                with self.assertRaises(ValueError):
                    solicitar_nueva_password()

            with psycopg.connect(self.database_url) as conexion:
                with self.assertRaises(ValueError):
                    actualizar_password_admin(conexion, username, "corta")
                self.assertTrue(
                    actualizar_password_admin(conexion, username, password_nueva)
                )
            with psycopg.connect(self.database_url) as conexion:
                rol, activo, hash_guardado = conexion.execute(
                    """
                    SELECT rol, activo, password_hash
                      FROM usuarios WHERE username = %s
                    """,
                    (username,),
                ).fetchone()
                self.assertEqual(rol, "admin")
                self.assertTrue(activo)
                self.assertFalse(check_password_hash(hash_guardado, password_anterior))
                self.assertTrue(check_password_hash(hash_guardado, password_nueva))
                self.assertFalse(
                    actualizar_password_admin(
                        conexion, "asistente_prueba", password_nueva
                    )
                )

            self.assertEqual(
                self.login(self.app.test_client(), username, password_nueva).status_code,
                302,
            )
        finally:
            self.limpiar()


if __name__ == "__main__":
    unittest.main()
