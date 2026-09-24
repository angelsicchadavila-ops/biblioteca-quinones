"""Pruebas funcionales del catálogo y el inventario de la Semana 4."""

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


class CatalogoSemana4Test(unittest.TestCase):
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

    def obtener_csrf(self, ruta: str) -> str:
        respuesta = self.cliente.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, usuario: str, clave: str) -> None:
        token = self.obtener_csrf("/login")
        respuesta = self.cliente.post(
            "/login",
            data={"username": usuario, "password": clave, "csrf_token": token},
        )
        self.assertEqual(respuesta.status_code, 302)

    def publicar(self, ruta: str, datos: dict, seguir: bool = True):
        token = self.obtener_csrf("/admin")
        return self.cliente.post(
            ruta,
            data={**datos, "csrf_token": token},
            follow_redirects=seguir,
        )

    def limpiar_datos(self) -> None:
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
                """,
                (patron,),
            )
            conexion.execute(
                "DELETE FROM lectores WHERE apellidos LIKE %s", (patron,)
            )
            conexion.execute(
                """
                DELETE FROM ejemplares
                 WHERE libro_id IN (SELECT id FROM libros WHERE titulo LIKE %s)
                """,
                (patron,),
            )
            conexion.execute("DELETE FROM libros WHERE titulo LIKE %s", (patron,))
            conexion.execute("DELETE FROM materias WHERE nombre LIKE %s", (patron,))

    def test_01_flujo_completo_catalogo_inventario_y_filtros(self) -> None:
        materia_inicial = f"  Materia   Semana4 {self.sufijo}  "
        materia_editada = f"Materia Editada {self.sufijo}"
        materia_filtro = f"Materia Filtro {self.sufijo}"
        titulo_inicial = f"Libro Inicial {self.sufijo}"
        titulo = f"Aventuras Revisadas {self.sufijo}"
        autor = f"Autora Catálogo {self.sufijo}"

        try:
            self.login("admin_prueba", self.admin_password)

            # 1. Crear materia y normalizar espacios.
            respuesta = self.publicar(
                "/admin/materias", {"nombre": materia_inicial}
            )
            self.assertIn("Materia creada correctamente", respuesta.get_data(as_text=True))
            with psycopg.connect(self.database_url) as conexion:
                materia = conexion.execute(
                    "SELECT id, nombre, activo FROM materias WHERE nombre LIKE %s",
                    (f"%{self.sufijo}%",),
                ).fetchone()
            self.assertEqual(materia[1], f"Materia Semana4 {self.sufijo}")
            self.assertTrue(materia[2])
            materia_id = materia[0]

            # La comparación de nombres es insensible a mayúsculas.
            respuesta = self.publicar(
                "/admin/materias",
                {"nombre": f"materia semana4 {self.sufijo}"},
            )
            self.assertIn("Ya existe una materia", respuesta.get_data(as_text=True))

            # 2. Editar materia.
            respuesta = self.publicar(
                f"/admin/materias/{materia_id}/editar",
                {"nombre": materia_editada},
            )
            self.assertIn("Materia actualizada correctamente", respuesta.get_data(as_text=True))

            # 3 y 4. Desactivar y reactivar materia.
            respuesta = self.publicar(
                f"/admin/materias/{materia_id}/estado", {}
            )
            self.assertIn("Materia desactivada correctamente", respuesta.get_data(as_text=True))
            respuesta = self.publicar(
                f"/admin/materias/{materia_id}/estado", {}
            )
            self.assertIn("Materia reactivada correctamente", respuesta.get_data(as_text=True))

            # Segunda materia controlada para probar edición y filtros.
            self.publicar("/admin/materias", {"nombre": materia_filtro})
            with psycopg.connect(self.database_url) as conexion:
                materia_filtro_id = conexion.execute(
                    "SELECT id FROM materias WHERE nombre = %s", (materia_filtro,)
                ).fetchone()[0]

            # 5. Crear libro.
            respuesta = self.publicar(
                "/admin/libros/nuevo",
                {
                    "titulo": titulo_inicial,
                    "autor": "Autor inicial",
                    "materia_id": str(materia_id),
                    "nivel": "Primaria",
                    "anio_publicacion": "2021",
                    "isbn_editorial": "Editorial de prueba",
                },
                seguir=False,
            )
            self.assertEqual(respuesta.status_code, 302)
            with psycopg.connect(self.database_url) as conexion:
                libro_id = conexion.execute(
                    "SELECT id FROM libros WHERE titulo = %s", (titulo_inicial,)
                ).fetchone()[0]

            # 6 y 7. Editar libro, materia y nivel.
            respuesta = self.publicar(
                f"/admin/libros/{libro_id}/editar",
                {
                    "titulo": titulo,
                    "autor": autor,
                    "materia_id": str(materia_filtro_id),
                    "nivel": "Secundaria",
                    "anio_publicacion": "2022",
                    "isbn_editorial": "ISBN 978-TEST",
                },
            )
            self.assertIn("Libro actualizado correctamente", respuesta.get_data(as_text=True))

            # Una materia con libros activos no puede quedar inconsistente.
            respuesta = self.publicar(
                f"/admin/materias/{materia_filtro_id}/estado", {}
            )
            self.assertIn("mientras tenga libros activos", respuesta.get_data(as_text=True))

            # 8 y 9. Crear un ejemplar y luego varios; códigos únicos y consecutivos.
            self.publicar(
                f"/admin/libros/{libro_id}/ejemplares", {"cantidad": "1"}
            )
            respuesta = self.publicar(
                f"/admin/libros/{libro_id}/ejemplares", {"cantidad": "3"}
            )
            self.assertIn("Se crearon 3 ejemplar", respuesta.get_data(as_text=True))
            with psycopg.connect(self.database_url) as conexion:
                ejemplares = conexion.execute(
                    """
                    SELECT id, codigo_qr
                      FROM ejemplares
                     WHERE libro_id = %s
                     ORDER BY id
                    """,
                    (libro_id,),
                ).fetchall()
            codigos = [fila[1] for fila in ejemplares]
            self.assertEqual(len(codigos), 4)
            self.assertEqual(len(set(codigos)), 4)
            self.assertEqual(
                codigos,
                [f"LIB-{libro_id:03d}-EJ{numero:02d}" for numero in range(1, 5)],
            )

            # 10 y 11. Marcar dañado y devolver a operativo.
            ejemplar_disponible, ejemplar_prestado, ejemplar_danado, ejemplar_inactivo = [
                fila[0] for fila in ejemplares
            ]
            respuesta = self.publicar(
                f"/admin/ejemplares/{ejemplar_danado}/estado-fisico",
                {"estado_fisico": "Dañado"},
            )
            self.assertIn("actualizado a Dañado", respuesta.get_data(as_text=True))
            respuesta = self.publicar(
                f"/admin/ejemplares/{ejemplar_danado}/estado-fisico",
                {"estado_fisico": "Operativo"},
            )
            self.assertIn("actualizado a Operativo", respuesta.get_data(as_text=True))

            # 12. Desactivar y reactivar ejemplar.
            respuesta = self.publicar(
                f"/admin/ejemplares/{ejemplar_inactivo}/estado", {}
            )
            self.assertIn("Ejemplar desactivado", respuesta.get_data(as_text=True))
            respuesta = self.publicar(
                f"/admin/ejemplares/{ejemplar_inactivo}/estado", {}
            )
            self.assertIn("Ejemplar reactivado", respuesta.get_data(as_text=True))

            # Dejar un ejemplar en cada estado visible para validar disponibilidad.
            self.publicar(
                f"/admin/ejemplares/{ejemplar_danado}/estado-fisico",
                {"estado_fisico": "Dañado"},
            )
            self.publicar(f"/admin/ejemplares/{ejemplar_inactivo}/estado", {})
            with psycopg.connect(self.database_url, autocommit=True) as conexion:
                usuario_id = conexion.execute(
                    "SELECT id FROM usuarios WHERE username = 'admin_prueba'"
                ).fetchone()[0]
                lector_id = conexion.execute(
                    """
                    INSERT INTO lectores (nombres, apellidos)
                    VALUES ('Lector Semana 4', %s) RETURNING id
                    """,
                    (f"Prueba {self.sufijo}",),
                ).fetchone()[0]
                conexion.execute(
                    """
                    INSERT INTO prestamos
                        (lector_id, ejemplar_id, registrado_por_usuario_id,
                         nivel_alumno, grado_seccion_alumno, fecha_limite)
                    VALUES (%s, %s, %s, 'Secundaria', '2 A',
                            (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                    """,
                    (lector_id, ejemplar_prestado, usuario_id),
                )

            # 13 a 18 y 20. Consulta pública, búsquedas, filtros y stock calculado.
            publico = self.app.test_client()
            respuesta = publico.get("/")
            contenido = respuesta.get_data(as_text=True)
            self.assertEqual(respuesta.status_code, 200)
            self.assertIn(titulo, contenido)
            self.assertNotIn("Administración del catálogo", contenido)
            for cantidad, etiqueta in (
                ("4", "Total"),
                ("1", "Disponibles"),
                ("1", "Prestados"),
                ("1", "Dañados"),
                ("1", "Inactivos"),
            ):
                self.assertRegex(contenido, rf">{cantidad}</strong><span>{etiqueta}")

            self.assertIn(
                titulo,
                publico.get("/", query_string={"q": "Aventuras Revisadas"}).get_data(as_text=True),
            )
            self.assertIn(
                titulo,
                publico.get("/", query_string={"q": "Autora Catálogo"}).get_data(as_text=True),
            )
            self.assertIn(
                titulo,
                publico.get(
                    "/", query_string={"materia": materia_filtro_id}
                ).get_data(as_text=True),
            )
            self.assertNotIn(
                titulo,
                publico.get("/", query_string={"materia": materia_id}).get_data(as_text=True),
            )
            self.assertIn(
                titulo,
                publico.get("/", query_string={"nivel": "Secundaria"}).get_data(as_text=True),
            )
            self.assertNotIn(
                titulo,
                publico.get("/", query_string={"nivel": "Primaria"}).get_data(as_text=True),
            )
            combinada = publico.get(
                "/",
                query_string={
                    "q": self.sufijo,
                    "materia": materia_filtro_id,
                    "nivel": "Secundaria",
                },
            ).get_data(as_text=True)
            self.assertIn(titulo, combinada)

            # Activación lógica de libro y visibilidad pública.
            self.publicar(f"/admin/libros/{libro_id}/estado", {})
            self.assertNotIn(titulo, publico.get("/").get_data(as_text=True))
            self.publicar(f"/admin/libros/{libro_id}/estado", {})
            self.assertIn(titulo, publico.get("/").get_data(as_text=True))

            # 19. El asistente recibe 403 en GET y POST administrativos.
            asistente = self.app.test_client()
            self.cliente = asistente
            self.login("asistente_prueba", self.asistente_password)
            for ruta in ("/admin/libros", "/admin/libros/nuevo", f"/admin/libros/{libro_id}/editar"):
                with self.subTest(ruta=ruta):
                    self.assertEqual(asistente.get(ruta).status_code, 200)
            for ruta in ("/admin/materias", f"/admin/libros/{libro_id}/ejemplares"):
                with self.subTest(ruta=ruta):
                    self.assertEqual(asistente.get(ruta).status_code, 403)
            token = self.obtener_csrf("/escaneo")
            self.assertEqual(
                asistente.post(
                    f"/admin/libros/{libro_id}/estado",
                    data={"csrf_token": token},
                ).status_code,
                403,
            )
        finally:
            self.limpiar_datos()


if __name__ == "__main__":
    unittest.main()
