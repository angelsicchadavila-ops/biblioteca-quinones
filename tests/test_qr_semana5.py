"""Pruebas de generación QR, PDF A4 e identificación de la Semana 5."""

from __future__ import annotations

import os
import re
import secrets
import unittest
from io import BytesIO
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from PIL import Image


load_dotenv(override=False)
CLAVE_PRUEBAS = secrets.token_hex(32)
os.environ.setdefault("SECRET_KEY", CLAVE_PRUEBAS)

from app import crear_app  # noqa: E402
from utils.pdf_exporter import A4, ETIQUETAS_POR_PAGINA, generar_pdf_etiquetas  # noqa: E402
from utils.qr_generator import construir_qr, generar_qr_png  # noqa: E402


PATRON_CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')
RAIZ = Path(__file__).resolve().parents[1]


class GeneracionQrPdfTest(unittest.TestCase):
    def test_01_qr_contiene_exactamente_el_codigo_y_es_png_cuadrado(self) -> None:
        codigo = "LIB-123-EJ45"
        qr = construir_qr(codigo)
        contenido = b"".join(segmento.data for segmento in qr.data_list).decode("utf-8")
        self.assertEqual(contenido, codigo)

        png = generar_qr_png(codigo)
        imagen = Image.open(png)
        self.assertEqual(imagen.format, "PNG")
        self.assertEqual(imagen.width, imagen.height)
        self.assertGreaterEqual(imagen.width, 250)

    def test_02_pdf_individual_es_valido_y_a4(self) -> None:
        pdf = generar_pdf_etiquetas(
            [{"codigo_qr": "LIB-123-EJ45", "titulo": "Libro de prueba"}]
        ).getvalue()
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn(b"/MediaBox [ 0 0 595.2756 841.8898 ]", pdf)
        self.assertEqual(len(re.findall(rb"/Type\s*/Page\b", pdf)), 1)
        self.assertEqual(A4, (595.2755905511812, 841.8897637795277))

    def test_03_pdf_multiple_respeta_21_etiquetas_por_pagina(self) -> None:
        ejemplares = [
            {"codigo_qr": f"LIB-123-EJ{numero:02d}", "titulo": "Libro múltiple"}
            for numero in range(1, ETIQUETAS_POR_PAGINA + 2)
        ]
        pdf = generar_pdf_etiquetas(ejemplares).getvalue()
        self.assertEqual(ETIQUETAS_POR_PAGINA, 21)
        self.assertEqual(len(re.findall(rb"/Type\s*/Page\b", pdf)), 2)
        self.assertEqual(pdf.count(b"/MediaBox [ 0 0 595.2756 841.8898 ]"), 2)


class FlujoQrSemana5Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database_url = os.getenv("DATABASE_URL", "")
        cls.admin_password = os.getenv("SEED_ADMIN_PASSWORD", "")
        cls.asistente_password = os.getenv("SEED_ASISTENTE_PASSWORD", "")
        if not all((cls.database_url, cls.admin_password, cls.asistente_password)):
            raise unittest.SkipTest("Faltan variables locales para las pruebas reales en Neon.")

        cls.app = crear_app(
            {
                "TESTING": True,
                "SECRET_KEY": CLAVE_PRUEBAS,
                "SESSION_COOKIE_SECURE": False,
            }
        )
        cls.sufijo = secrets.token_hex(5)
        with psycopg.connect(cls.database_url, autocommit=True) as conexion:
            cls.materia_id = conexion.execute(
                "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                (f"Materia QR {cls.sufijo}",),
            ).fetchone()[0]
            cls.libro_id = conexion.execute(
                """
                INSERT INTO libros (titulo, autor, materia_id, nivel)
                VALUES (%s, 'Autor Semana 5', %s, 'Secundaria') RETURNING id
                """,
                (f"Libro QR {cls.sufijo}", cls.materia_id),
            ).fetchone()[0]
            cls.codigos = [
                f"LIB-{cls.libro_id:03d}-EJ{numero:02d}" for numero in range(1, 4)
            ]
            filas = conexion.execute(
                """
                INSERT INTO ejemplares (libro_id, codigo_qr, estado_fisico, activo)
                VALUES (%s, %s, 'Operativo', TRUE),
                       (%s, %s, 'Dañado', TRUE),
                       (%s, %s, 'Operativo', FALSE)
                RETURNING id
                """,
                (
                    cls.libro_id,
                    cls.codigos[0],
                    cls.libro_id,
                    cls.codigos[1],
                    cls.libro_id,
                    cls.codigos[2],
                ),
            ).fetchall()
            cls.ejemplar_ids = [fila[0] for fila in filas]

    @classmethod
    def tearDownClass(cls) -> None:
        if not hasattr(cls, "libro_id"):
            return
        with psycopg.connect(cls.database_url, autocommit=True) as conexion:
            conexion.execute("DELETE FROM ejemplares WHERE libro_id = %s", (cls.libro_id,))
            conexion.execute("DELETE FROM libros WHERE id = %s", (cls.libro_id,))
            conexion.execute("DELETE FROM materias WHERE id = %s", (cls.materia_id,))

    def setUp(self) -> None:
        self.cliente = self.app.test_client()

    def obtener_csrf(self, ruta: str = "/login") -> str:
        respuesta = self.cliente.get(ruta)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, usuario: str, clave: str) -> None:
        token = self.obtener_csrf()
        respuesta = self.cliente.post(
            "/login",
            data={"username": usuario, "password": clave, "csrf_token": token},
        )
        self.assertEqual(respuesta.status_code, 302)

    def test_04_publico_no_accede_a_terminal_api_ni_qr_admin(self) -> None:
        self.assertEqual(self.cliente.get("/escaneo").status_code, 302)
        respuesta = self.cliente.get(f"/api/ejemplar/{self.codigos[0]}")
        self.assertEqual(respuesta.status_code, 401)
        self.assertEqual(respuesta.json["error"]["codigo"], "autenticacion_requerida")
        self.assertEqual(
            self.cliente.get(
                f"/admin/ejemplares/{self.ejemplar_ids[0]}/qr.png"
            ).status_code,
            302,
        )

    def test_05_admin_genera_reimprime_y_no_modifica_codigo(self) -> None:
        self.login("admin_prueba", self.admin_password)
        with psycopg.connect(self.database_url) as conexion:
            codigo_antes = conexion.execute(
                "SELECT codigo_qr FROM ejemplares WHERE id = %s",
                (self.ejemplar_ids[0],),
            ).fetchone()[0]

        qr = self.cliente.get(f"/admin/ejemplares/{self.ejemplar_ids[0]}/qr.png")
        self.assertEqual(qr.status_code, 200)
        self.assertEqual(qr.mimetype, "image/png")
        self.assertEqual(Image.open(BytesIO(qr.data)).format, "PNG")

        pdf_1 = self.cliente.get(
            f"/admin/ejemplares/{self.ejemplar_ids[0]}/etiqueta.pdf"
        )
        pdf_2 = self.cliente.get(
            f"/admin/ejemplares/{self.ejemplar_ids[0]}/etiqueta.pdf"
        )
        self.assertEqual(pdf_1.status_code, 200)
        self.assertTrue(pdf_1.data.startswith(b"%PDF-"))
        self.assertEqual(pdf_2.status_code, 200)

        with psycopg.connect(self.database_url) as conexion:
            codigo_despues = conexion.execute(
                "SELECT codigo_qr FROM ejemplares WHERE id = %s",
                (self.ejemplar_ids[0],),
            ).fetchone()[0]
            prestamos = conexion.execute(
                "SELECT count(*) FROM prestamos WHERE ejemplar_id = %s",
                (self.ejemplar_ids[0],),
            ).fetchone()[0]
        self.assertEqual(codigo_antes, codigo_despues)
        self.assertEqual(prestamos, 0)

    def test_06_admin_genera_pdf_con_multiples_etiquetas(self) -> None:
        self.login("admin_prueba", self.admin_password)
        ruta = f"/admin/libros/{self.libro_id}/ejemplares"
        token = self.obtener_csrf(ruta)
        respuesta = self.cliente.post(
            "/admin/etiquetas-qr.pdf",
            data={
                "csrf_token": token,
                "libro_id": str(self.libro_id),
                "ejemplar_id": [str(valor) for valor in self.ejemplar_ids],
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.mimetype, "application/pdf")
        self.assertTrue(respuesta.data.startswith(b"%PDF-"))

    def test_07_endpoint_identifica_operativo_danado_inactivo_e_inexistente(self) -> None:
        self.login("asistente_prueba", self.asistente_password)
        esperados = ("Disponible", "Dañado", "Inactivo")
        for codigo, esperado in zip(self.codigos, esperados, strict=True):
            with self.subTest(codigo=codigo):
                respuesta = self.cliente.get(f"/api/ejemplar/{codigo}")
                self.assertEqual(respuesta.status_code, 200)
                self.assertTrue(respuesta.json["ok"])
                self.assertEqual(respuesta.json["ejemplar"]["codigo_qr"], codigo)
                self.assertEqual(respuesta.json["ejemplar"]["disponibilidad"], esperado)
                self.assertEqual(
                    set(respuesta.json["ejemplar"]),
                    {
                        "codigo_qr",
                        "titulo",
                        "autor",
                        "materia",
                        "nivel",
                        "estado_fisico",
                        "activo",
                        "libro_activo",
                        "disponibilidad",
                    },
                )

        inexistente = self.cliente.get("/api/ejemplar/LIB-999999-EJ99")
        self.assertEqual(inexistente.status_code, 404)
        self.assertEqual(inexistente.json["error"]["mensaje"], "Código no registrado.")
        invalido = self.cliente.get("/api/ejemplar/CODIGO-INVALIDO")
        self.assertEqual(invalido.status_code, 400)

    def test_08_ingreso_manual_normalizado_usa_el_mismo_endpoint(self) -> None:
        self.login("asistente_prueba", self.asistente_password)
        respuesta = self.cliente.get(f"/api/ejemplar/%20{self.codigos[0].lower()}%20")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json["ejemplar"]["codigo_qr"], self.codigos[0])

        scanner_js = (RAIZ / "static" / "js" / "qr_scanner.js").read_text(
            encoding="utf-8"
        )
        self.assertIn('procesarCodigo(entradaManual.value, "Ingreso manual")', scanner_js)
        self.assertIn('procesarCodigo(textoDecodificado, "QR leído")', scanner_js)
        self.assertEqual(scanner_js.count("fetch(`/api/ejemplar/"), 1)

    def test_09_asistente_usa_terminal_pero_no_generacion_admin(self) -> None:
        self.login("asistente_prueba", self.asistente_password)
        terminal = self.cliente.get("/escaneo")
        contenido = terminal.get_data(as_text=True)
        self.assertEqual(terminal.status_code, 200)
        self.assertIn("Iniciar cámara", contenido)
        self.assertIn("Ingreso manual", contenido)
        self.assertIn("html5-qrcode@2.3.8", contenido)
        self.assertIn("Confirmar préstamo", contenido)
        self.assertIn("Confirmar devolución", contenido)
        self.assertEqual(
            self.cliente.get(
                f"/admin/ejemplares/{self.ejemplar_ids[0]}/qr.png"
            ).status_code,
            403,
        )

    def test_10_doble_lectura_y_errores_de_camara_estan_controlados(self) -> None:
        scanner_js = (RAIZ / "static" / "js" / "qr_scanner.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("BLOQUEO_LECTURA_MS = 3000", scanner_js)
        self.assertIn("if (procesando ||", scanner_js)
        self.assertIn('{ facingMode: "environment" }', scanner_js)
        self.assertIn("NotAllowed|PermissionDenied", scanner_js)
        self.assertIn("NotFound|DevicesNotFound", scanner_js)
        self.assertIn("await lector.stop()", scanner_js)


if __name__ == "__main__":
    unittest.main()
