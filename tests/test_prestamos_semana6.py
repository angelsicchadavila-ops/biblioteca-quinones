"""Pruebas integrales del núcleo operativo de la Semana 6 contra Neon."""

from __future__ import annotations

import os
import re
import secrets
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


load_dotenv(override=False)
CLAVE_PRUEBAS = secrets.token_hex(32)
os.environ.setdefault("SECRET_KEY", CLAVE_PRUEBAS)

from app import crear_app  # noqa: E402
from utils.prestamos import ReglaOperacionError, registrar_prestamo  # noqa: E402


PATRON_CSRF = re.compile(r'name="csrf_token" value="([^"]+)"')


class PrestamosSemana6Test(unittest.TestCase):
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
        cls.apellido_temporal = f"TEMPSEMANA6{cls.sufijo}"
        with psycopg.connect(
            cls.database_url, autocommit=True, row_factory=dict_row
        ) as conexion:
            conexion.execute("SET TIME ZONE 'America/Lima'")
            usuarios = conexion.execute(
                """
                SELECT id, username FROM usuarios
                 WHERE username IN ('admin_prueba', 'asistente_prueba')
                """
            ).fetchall()
            cls.usuarios = {fila["username"]: fila["id"] for fila in usuarios}
            if len(cls.usuarios) != 2:
                raise unittest.SkipTest("No existen las cuentas de prueba aprobadas.")

            cls.materia_id = conexion.execute(
                "INSERT INTO materias (nombre) VALUES (%s) RETURNING id",
                (f"TEMP-SEMANA-06-{cls.sufijo}",),
            ).fetchone()["id"]
            cls.libro_id = conexion.execute(
                """
                INSERT INTO libros (titulo, autor, materia_id, nivel)
                VALUES (%s, 'Autor Temporal Semana 6', %s, 'Ambos')
                RETURNING id
                """,
                (f"Libro TEMP Semana 6 {cls.sufijo}", cls.materia_id),
            ).fetchone()["id"]
            cls.codigos = [
                f"LIB-{cls.libro_id:03d}-EJ{numero:02d}" for numero in range(1, 9)
            ]
            for numero, codigo in enumerate(cls.codigos, start=1):
                estado = "Dañado" if numero == 7 else "Operativo"
                activo = numero != 8
                conexion.execute(
                    """
                    INSERT INTO ejemplares (libro_id, codigo_qr, estado_fisico, activo)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (cls.libro_id, codigo, estado, activo),
                )

    @classmethod
    def tearDownClass(cls) -> None:
        if not hasattr(cls, "libro_id"):
            return
        with psycopg.connect(cls.database_url, autocommit=True) as conexion:
            conexion.execute(
                """
                DELETE FROM prestamos
                 WHERE ejemplar_id IN (SELECT id FROM ejemplares WHERE libro_id = %s)
                """,
                (cls.libro_id,),
            )
            conexion.execute(
                "DELETE FROM lectores WHERE apellidos = %s", (cls.apellido_temporal,)
            )
            conexion.execute("DELETE FROM ejemplares WHERE libro_id = %s", (cls.libro_id,))
            conexion.execute("DELETE FROM libros WHERE id = %s", (cls.libro_id,))
            conexion.execute("DELETE FROM materias WHERE id = %s", (cls.materia_id,))

    def setUp(self) -> None:
        self.cliente = self.app.test_client()
        with psycopg.connect(self.database_url, autocommit=True) as conexion:
            conexion.execute(
                """
                DELETE FROM prestamos
                 WHERE ejemplar_id IN (SELECT id FROM ejemplares WHERE libro_id = %s)
                """,
                (self.libro_id,),
            )
            conexion.execute(
                "DELETE FROM lectores WHERE apellidos = %s", (self.apellido_temporal,)
            )

    def obtener_csrf(self, ruta: str = "/login", cliente=None) -> str:
        cliente = cliente or self.cliente
        respuesta = cliente.get(ruta)
        coincidencia = PATRON_CSRF.search(respuesta.get_data(as_text=True))
        self.assertIsNotNone(coincidencia)
        return coincidencia.group(1)

    def login(self, usuario: str, clave: str, cliente=None) -> None:
        cliente = cliente or self.cliente
        token = self.obtener_csrf(cliente=cliente)
        respuesta = cliente.post(
            "/login",
            data={"username": usuario, "password": clave, "csrf_token": token},
        )
        self.assertEqual(respuesta.status_code, 302)

    def prestar(
        self,
        codigo: str,
        *,
        lector_id: int | None = None,
        nombres: str = "Lector",
        tipo_plazo: str = "7",
        fecha_personalizada: str = "",
        cliente=None,
    ):
        cliente = cliente or self.cliente
        token = self.obtener_csrf("/escaneo", cliente)
        return cliente.post(
            "/api/prestamos",
            data={
                "csrf_token": token,
                "codigo_qr": codigo,
                "lector_id": str(lector_id or ""),
                "lector_nombres": nombres if lector_id is None else "",
                "lector_apellidos": self.apellido_temporal if lector_id is None else "",
                "nivel_alumno": "Secundaria",
                "grado_seccion_alumno": "2 A",
                "tipo_plazo": tipo_plazo,
                "fecha_personalizada": fecha_personalizada,
            },
        )

    def devolver(self, codigo: str, cliente=None):
        cliente = cliente or self.cliente
        token = self.obtener_csrf("/escaneo", cliente)
        return cliente.post(
            "/api/devoluciones",
            data={"csrf_token": token, "codigo_qr": codigo},
        )

    def test_01_lector_plazos_limite_devolucion_e_historial(self) -> None:
        self.login("admin_prueba", self.admin_password)

        primero = self.prestar(self.codigos[0], nombres="Lector Nuevo")
        self.assertEqual(primero.status_code, 201)
        self.assertTrue(primero.json["prestamo"]["lector_creado"])
        lector_id = primero.json["prestamo"]["lector_id"]
        self.assertEqual(
            date.fromisoformat(primero.json["prestamo"]["fecha_limite"]),
            date.today() + timedelta(days=7),
        )

        busqueda = self.cliente.get(
            "/api/lectores", query_string={"q": f"  nuevo   {self.apellido_temporal.lower()} "}
        )
        self.assertEqual(busqueda.status_code, 200)
        self.assertEqual(busqueda.json["lectores"][0]["id"], lector_id)
        self.assertEqual(busqueda.json["lectores"][0]["prestamos_activos"], 1)

        segundo = self.prestar(self.codigos[1], lector_id=lector_id, tipo_plazo="14")
        self.assertEqual(segundo.status_code, 201)
        self.assertFalse(segundo.json["prestamo"]["lector_creado"])
        self.assertEqual(
            date.fromisoformat(segundo.json["prestamo"]["fecha_limite"]),
            date.today() + timedelta(days=14),
        )

        tercero = self.prestar(self.codigos[2], lector_id=lector_id)
        self.assertEqual(tercero.status_code, 409)
        self.assertEqual(tercero.json["error"]["codigo"], "limite_prestamos")
        self.assertIn("dos préstamos activos", tercero.json["error"]["mensaje"])

        asistente = self.app.test_client()
        self.login("asistente_prueba", self.asistente_password, asistente)
        devuelto = self.devolver(self.codigos[0], asistente)
        self.assertEqual(devuelto.status_code, 200)
        self.assertEqual(devuelto.json["devolucion"]["disponibilidad"], "Disponible")

        personalizada = (date.today() + timedelta(days=3)).isoformat()
        tercero_valido = self.prestar(
            self.codigos[2],
            lector_id=lector_id,
            tipo_plazo="personalizada",
            fecha_personalizada=personalizada,
            cliente=asistente,
        )
        self.assertEqual(tercero_valido.status_code, 201)
        self.assertEqual(tercero_valido.json["prestamo"]["fecha_limite"], personalizada)

        invalida = self.prestar(
            self.codigos[3],
            lector_id=lector_id,
            tipo_plazo="personalizada",
            fecha_personalizada=(date.today() - timedelta(days=1)).isoformat(),
        )
        self.assertEqual(invalida.status_code, 400)
        self.assertEqual(invalida.json["error"]["codigo"], "fecha_invalida")

        self.devolver(self.codigos[1], asistente)
        self.devolver(self.codigos[2], asistente)
        with psycopg.connect(self.database_url, row_factory=dict_row) as conexion:
            filas = conexion.execute(
                """
                SELECT registrado_por_usuario_id, devuelto_por_usuario_id,
                       fecha_devolucion
                  FROM prestamos
                 WHERE lector_id = %s
                 ORDER BY id
                """,
                (lector_id,),
            ).fetchall()
        self.assertEqual(len(filas), 3)
        self.assertTrue(all(fila["fecha_devolucion"] is not None for fila in filas))
        self.assertEqual(
            [fila["registrado_por_usuario_id"] for fila in filas],
            [
                self.usuarios["admin_prueba"],
                self.usuarios["admin_prueba"],
                self.usuarios["asistente_prueba"],
            ],
        )
        self.assertTrue(
            all(
                fila["devuelto_por_usuario_id"]
                == self.usuarios["asistente_prueba"]
                for fila in filas
            )
        )

    def test_02_mora_estado_dinamico_y_desbloqueo(self) -> None:
        self.login("admin_prueba", self.admin_password)
        with psycopg.connect(
            self.database_url, autocommit=True, row_factory=dict_row
        ) as conexion:
            lector_id = conexion.execute(
                """
                INSERT INTO lectores (nombres, apellidos)
                VALUES ('Lector Mora', %s) RETURNING id
                """,
                (self.apellido_temporal,),
            ).fetchone()["id"]
            ejemplar_id = conexion.execute(
                "SELECT id FROM ejemplares WHERE codigo_qr = %s", (self.codigos[0],)
            ).fetchone()["id"]
            conexion.execute(
                """
                INSERT INTO prestamos (
                    lector_id, ejemplar_id, registrado_por_usuario_id,
                    nivel_alumno, grado_seccion_alumno,
                    fecha_prestamo, fecha_limite
                ) VALUES (%s, %s, %s, 'Primaria', '5 B',
                          CURRENT_TIMESTAMP - INTERVAL '8 days',
                          (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date - 1)
                """,
                (lector_id, ejemplar_id, self.usuarios["admin_prueba"]),
            )

        ficha = self.cliente.get(f"/api/ejemplar/{self.codigos[0]}")
        self.assertEqual(ficha.status_code, 200)
        self.assertEqual(ficha.json["operacion"], "devolucion")
        self.assertEqual(ficha.json["prestamo_activo"]["estado"], "Vencido")
        self.assertEqual(ficha.json["prestamo_activo"]["dias_atraso"], 1)

        bloqueado = self.prestar(self.codigos[1], lector_id=lector_id)
        self.assertEqual(bloqueado.status_code, 409)
        self.assertEqual(bloqueado.json["error"]["codigo"], "lector_con_mora")

        self.assertEqual(self.devolver(self.codigos[0]).status_code, 200)
        habilitado = self.prestar(self.codigos[1], lector_id=lector_id)
        self.assertEqual(habilitado.status_code, 201)
        self.assertEqual(self.devolver(self.codigos[1]).status_code, 200)

    def test_03_estados_permisos_listado_y_reportes(self) -> None:
        publico = self.app.test_client()
        self.assertEqual(publico.get("/api/lectores", query_string={"q": "x"}).status_code, 401)
        self.assertEqual(publico.get("/admin/prestamos").status_code, 302)
        self.assertEqual(publico.get("/admin/reportes").status_code, 302)

        self.login("asistente_prueba", self.asistente_password)
        self.assertEqual(self.cliente.get("/escaneo").status_code, 200)
        self.assertEqual(self.cliente.get("/admin/prestamos").status_code, 403)
        self.assertEqual(self.cliente.get("/admin/reportes").status_code, 403)

        danado = self.cliente.get(f"/api/ejemplar/{self.codigos[6]}")
        inactivo = self.cliente.get(f"/api/ejemplar/{self.codigos[7]}")
        self.assertEqual(danado.json["operacion"], "bloqueado")
        self.assertEqual(danado.json["ejemplar"]["disponibilidad"], "Dañado")
        self.assertEqual(inactivo.json["operacion"], "bloqueado")
        self.assertEqual(inactivo.json["ejemplar"]["disponibilidad"], "Inactivo")
        self.assertEqual(self.prestar(self.codigos[6]).json["error"]["codigo"], "ejemplar_danado")
        self.assertEqual(self.prestar(self.codigos[7]).json["error"]["codigo"], "ejemplar_inactivo")
        self.assertEqual(self.cliente.get("/api/ejemplar/LIB-999999-EJ99").status_code, 404)

        with psycopg.connect(
            self.database_url, autocommit=True, row_factory=dict_row
        ) as conexion:
            lectores = []
            for nombre in ("Activo", "Vencido", "Devuelto"):
                lectores.append(
                    conexion.execute(
                        "INSERT INTO lectores (nombres, apellidos) VALUES (%s, %s) RETURNING id",
                        (nombre, self.apellido_temporal),
                    ).fetchone()["id"]
                )
            ids = [
                conexion.execute(
                    "SELECT id FROM ejemplares WHERE codigo_qr = %s", (codigo,)
                ).fetchone()["id"]
                for codigo in self.codigos[:3]
            ]
            conexion.execute(
                """
                INSERT INTO prestamos (
                    lector_id, ejemplar_id, registrado_por_usuario_id,
                    nivel_alumno, grado_seccion_alumno, fecha_limite
                ) VALUES (%s, %s, %s, 'Secundaria', '1 A',
                          (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 7)
                """,
                (lectores[0], ids[0], self.usuarios["asistente_prueba"]),
            )
            conexion.execute(
                """
                INSERT INTO prestamos (
                    lector_id, ejemplar_id, registrado_por_usuario_id,
                    nivel_alumno, grado_seccion_alumno,
                    fecha_prestamo, fecha_limite
                ) VALUES (%s, %s, %s, 'Primaria', '6 C',
                          CURRENT_TIMESTAMP - INTERVAL '8 days',
                          (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date - 2)
                """,
                (lectores[1], ids[1], self.usuarios["admin_prueba"]),
            )
            conexion.execute(
                """
                INSERT INTO prestamos (
                    lector_id, ejemplar_id, registrado_por_usuario_id,
                    devuelto_por_usuario_id, nivel_alumno,
                    grado_seccion_alumno, fecha_prestamo,
                    fecha_limite, fecha_devolucion
                ) VALUES (%s, %s, %s, %s, 'Secundaria', '3 B',
                          CURRENT_TIMESTAMP - INTERVAL '5 days',
                          (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date + 2,
                          CURRENT_TIMESTAMP - INTERVAL '1 day')
                """,
                (
                    lectores[2],
                    ids[2],
                    self.usuarios["admin_prueba"],
                    self.usuarios["asistente_prueba"],
                ),
            )

        admin = self.app.test_client()
        self.login("admin_prueba", self.admin_password, admin)
        listado = admin.get("/admin/prestamos").get_data(as_text=True)
        self.assertIn("fila-prestamo-activo", listado)
        self.assertIn("fila-prestamo-vencido", listado)
        self.assertIn("fila-prestamo-devuelto", listado)
        self.assertIn("Registró:", listado)
        self.assertIn("Devolvió:", listado)

        for reporte, texto in (
            ("inventario", "RPT-01 Inventario"),
            ("activos", "RPT-02 Préstamos activos"),
            ("vencidos", "RPT-03 Préstamos vencidos"),
            ("historial", "RPT-04 Historial de préstamos"),
        ):
            with self.subTest(reporte=reporte):
                respuesta = admin.get("/admin/reportes", query_string={"reporte": reporte})
                self.assertEqual(respuesta.status_code, 200)
                contenido = respuesta.get_data(as_text=True)
                self.assertIn(texto, contenido)
                marcador = (
                    f"Libro TEMP Semana 6 {self.sufijo}"
                    if reporte == "inventario"
                    else self.apellido_temporal
                )
                self.assertIn(marcador, contenido)
                if reporte == "inventario":
                    self.assertRegex(
                        contenido,
                        r"<td>7</td><td>4</td><td>2</td><td>1</td>",
                    )

        hoy = date.today().isoformat()
        historial = admin.get(
            "/admin/reportes",
            query_string={"reporte": "historial", "desde": hoy, "hasta": hoy},
        )
        self.assertEqual(historial.status_code, 200)
        rango_invalido = admin.get(
            "/admin/reportes",
            query_string={
                "reporte": "historial",
                "desde": (date.today() + timedelta(days=1)).isoformat(),
                "hasta": hoy,
            },
        )
        self.assertEqual(rango_invalido.status_code, 400)

    def test_04_doble_prestamo_simultaneo_solo_confirma_uno(self) -> None:
        with psycopg.connect(
            self.database_url, autocommit=True, row_factory=dict_row
        ) as conexion:
            lectores = [
                conexion.execute(
                    "INSERT INTO lectores (nombres, apellidos) VALUES (%s, %s) RETURNING id",
                    (f"Concurrente {numero}", self.apellido_temporal),
                ).fetchone()["id"]
                for numero in (1, 2)
            ]

        barrera = threading.Barrier(2)

        def intentar(lector_id: int):
            with psycopg.connect(
                self.database_url, autocommit=True, row_factory=dict_row
            ) as conexion:
                conexion.execute("SET TIME ZONE 'America/Lima'")
                barrera.wait(timeout=10)
                try:
                    registrar_prestamo(
                        conexion,
                        codigo_qr=self.codigos[0],
                        usuario_id=self.usuarios["admin_prueba"],
                        lector_id=lector_id,
                        lector_nombres="",
                        lector_apellidos="",
                        nivel_alumno="Secundaria",
                        grado_seccion_alumno="4 A",
                        tipo_plazo="7",
                        fecha_personalizada="",
                    )
                    return "creado"
                except ReglaOperacionError as error:
                    return error.codigo

        with ThreadPoolExecutor(max_workers=2) as ejecutor:
            resultados = list(ejecutor.map(intentar, lectores))

        self.assertEqual(resultados.count("creado"), 1)
        self.assertEqual(resultados.count("ejemplar_prestado"), 1)
        with psycopg.connect(self.database_url) as conexion:
            cantidad = conexion.execute(
                """
                SELECT count(*) FROM prestamos p
                JOIN ejemplares e ON e.id = p.ejemplar_id
                WHERE e.codigo_qr = %s AND p.fecha_devolucion IS NULL
                """,
                (self.codigos[0],),
            ).fetchone()[0]
        self.assertEqual(cantidad, 1)


if __name__ == "__main__":
    unittest.main()
