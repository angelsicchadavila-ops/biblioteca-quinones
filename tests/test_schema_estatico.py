"""Pruebas estáticas del alcance y la seguridad del esquema de Semana 2."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SCHEMA = (RAIZ / "sql" / "schema.sql").read_text(encoding="utf-8")
SEED = (RAIZ / "sql" / "seed.sql").read_text(encoding="utf-8")


class SchemaEstaticoTest(unittest.TestCase):
    def test_contiene_exclusivamente_las_seis_tablas_del_der(self) -> None:
        tablas = set(re.findall(r"CREATE TABLE\s+(\w+)", SCHEMA, re.IGNORECASE))
        self.assertEqual(
            tablas,
            {"usuarios", "materias", "libros", "ejemplares", "lectores", "prestamos"},
        )

    def test_dominios_aprobados_tienen_check(self) -> None:
        for valores in (
            "'admin', 'asistente'",
            "'Primaria', 'Secundaria', 'Ambos'",
            "'Operativo', 'Dañado'",
            "'Primaria', 'Secundaria'",
        ):
            self.assertIn(valores, SCHEMA)

    def test_unicidades_esenciales(self) -> None:
        for nombre in (
            "uq_usuarios_username",
            "uq_materias_nombre",
            "uq_ejemplares_codigo_qr",
            "uq_prestamos_ejemplar_activo",
        ):
            self.assertIn(nombre, SCHEMA)
        self.assertRegex(
            SCHEMA,
            r"(?is)CREATE UNIQUE INDEX\s+uq_prestamos_ejemplar_activo.*?WHERE\s+fecha_devolucion IS NULL",
        )

    def test_disponibilidad_no_se_almacena_en_ejemplares(self) -> None:
        bloque = re.search(
            r"(?is)CREATE TABLE ejemplares\s*\((.*?)\);", SCHEMA
        ).group(1)
        self.assertNotRegex(bloque, r"(?im)^\s*estado\s+")

    def test_anio_publicacion_es_nullable_y_tiene_rango_v1_1(self) -> None:
        bloque = re.search(
            r"(?is)CREATE TABLE libros\s*\((.*?)\);", SCHEMA
        ).group(1)
        self.assertRegex(bloque, r"(?im)^\s*anio_publicacion\s+SMALLINT")
        self.assertIn("ck_libros_anio_publicacion", bloque)
        self.assertRegex(
            bloque,
            r"anio_publicacion\s+IS\s+NULL\s+OR\s+anio_publicacion\s+BETWEEN\s+1000\s+AND\s+9999",
        )

    def test_indices_de_busqueda_y_operacion(self) -> None:
        for nombre in (
            "idx_libros_titulo_lower",
            "idx_libros_autor_lower",
            "idx_libros_materia_nivel_activo",
            "idx_prestamos_lector_activo",
            "idx_prestamos_fecha_limite_activos",
        ):
            self.assertIn(nombre, SCHEMA)

    def test_reglas_criticas_tienen_triggers(self) -> None:
        self.assertIn("trg_validar_materia_activa_libro", SCHEMA)
        self.assertIn("trg_validar_prestamo_activo", SCHEMA)
        self.assertIn("America/Lima", SCHEMA)

    def test_seed_no_inserta_credenciales(self) -> None:
        self.assertNotRegex(SEED, r"(?is)INSERT\s+INTO\s+usuarios")
        self.assertNotIn("password_hash", SEED.lower())
        self.assertIn("Ciencia y Tecnología", SEED)

    def test_env_esta_ignorado_y_el_ejemplo_no_tiene_url_real(self) -> None:
        gitignore = (RAIZ / ".gitignore").read_text(encoding="utf-8")
        env_example = (RAIZ / ".env.example").read_text(encoding="utf-8")
        self.assertRegex(gitignore, r"(?m)^\.env$")
        self.assertNotIn("neon.tech", env_example.lower())
        for variable in (
            "DATABASE_URL=",
            "SEED_ADMIN_PASSWORD=",
            "SEED_ASISTENTE_PASSWORD=",
        ):
            self.assertIn(variable, env_example)


if __name__ == "__main__":
    unittest.main()
