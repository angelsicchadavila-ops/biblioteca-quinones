-- Materias iniciales de referencia para el entorno de desarrollo.
-- Las cuentas de prueba se insertan de forma parametrizada desde
-- scripts/inicializar_bd.py para no guardar contraseñas en Git.

INSERT INTO materias (nombre)
VALUES
    ('Comunicación'),
    ('Matemática'),
    ('Ciencia y Tecnología'),
    ('Ciencias Sociales'),
    ('Inglés')
ON CONFLICT (nombre) DO NOTHING;
