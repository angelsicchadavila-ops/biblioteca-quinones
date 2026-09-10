-- Esquema PostgreSQL oficial de la Biblioteca Quiñones v1.0.
-- Debe ejecutarse sobre una base de datos vacía mediante scripts/inicializar_bd.py.

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_usuarios_username UNIQUE (username),
    CONSTRAINT ck_usuarios_username_no_vacio CHECK (btrim(username) <> ''),
    CONSTRAINT ck_usuarios_password_hash_no_vacio CHECK (btrim(password_hash) <> ''),
    CONSTRAINT ck_usuarios_nombre_no_vacio CHECK (btrim(nombre_completo) <> ''),
    CONSTRAINT ck_usuarios_rol CHECK (rol IN ('admin', 'asistente'))
);

CREATE TABLE materias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_materias_nombre UNIQUE (nombre),
    CONSTRAINT ck_materias_nombre_no_vacio CHECK (btrim(nombre) <> '')
);

CREATE TABLE libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    materia_id INT NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    isbn_editorial VARCHAR(100),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_libros_materia
        FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE RESTRICT,
    CONSTRAINT ck_libros_titulo_no_vacio CHECK (btrim(titulo) <> ''),
    CONSTRAINT ck_libros_autor_no_vacio CHECK (btrim(autor) <> ''),
    CONSTRAINT ck_libros_nivel CHECK (nivel IN ('Primaria', 'Secundaria', 'Ambos')),
    CONSTRAINT ck_libros_isbn_editorial_no_vacio
        CHECK (isbn_editorial IS NULL OR btrim(isbn_editorial) <> '')
);

CREATE TABLE ejemplares (
    id SERIAL PRIMARY KEY,
    libro_id INT NOT NULL,
    codigo_qr VARCHAR(50) NOT NULL,
    estado_fisico VARCHAR(20) NOT NULL DEFAULT 'Operativo',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ejemplares_libro
        FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE RESTRICT,
    CONSTRAINT uq_ejemplares_codigo_qr UNIQUE (codigo_qr),
    CONSTRAINT ck_ejemplares_codigo_qr_no_vacio CHECK (btrim(codigo_qr) <> ''),
    CONSTRAINT ck_ejemplares_estado_fisico
        CHECK (estado_fisico IN ('Operativo', 'Dañado'))
);

CREATE TABLE lectores (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_lectores_nombres_no_vacio CHECK (btrim(nombres) <> ''),
    CONSTRAINT ck_lectores_apellidos_no_vacio CHECK (btrim(apellidos) <> '')
);

CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    lector_id INT NOT NULL,
    ejemplar_id INT NOT NULL,
    registrado_por_usuario_id INT NOT NULL,
    devuelto_por_usuario_id INT,
    nivel_alumno VARCHAR(20) NOT NULL,
    grado_seccion_alumno VARCHAR(50) NOT NULL,
    fecha_prestamo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_limite DATE NOT NULL,
    fecha_devolucion TIMESTAMP,
    CONSTRAINT fk_prestamos_lector
        FOREIGN KEY (lector_id) REFERENCES lectores(id) ON DELETE RESTRICT,
    CONSTRAINT fk_prestamos_ejemplar
        FOREIGN KEY (ejemplar_id) REFERENCES ejemplares(id) ON DELETE RESTRICT,
    CONSTRAINT fk_prestamos_usuario_registro
        FOREIGN KEY (registrado_por_usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    CONSTRAINT fk_prestamos_usuario_devolucion
        FOREIGN KEY (devuelto_por_usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    CONSTRAINT ck_prestamos_nivel_alumno
        CHECK (nivel_alumno IN ('Primaria', 'Secundaria')),
    CONSTRAINT ck_prestamos_grado_seccion_no_vacio
        CHECK (btrim(grado_seccion_alumno) <> ''),
    CONSTRAINT ck_prestamos_fecha_limite
        CHECK (fecha_limite >= fecha_prestamo::date),
    CONSTRAINT ck_prestamos_devolucion
        CHECK (
            (fecha_devolucion IS NULL AND devuelto_por_usuario_id IS NULL)
            OR
            (fecha_devolucion IS NOT NULL
             AND devuelto_por_usuario_id IS NOT NULL
             AND fecha_devolucion >= fecha_prestamo)
        )
);

-- RN-15 / CA-13: la unicidad parcial también protege ante concurrencia.
CREATE UNIQUE INDEX uq_prestamos_ejemplar_activo
    ON prestamos (ejemplar_id)
    WHERE fecha_devolucion IS NULL;

-- Índices para catálogo, relaciones, préstamos activos, mora e historial.
CREATE INDEX idx_libros_titulo_lower ON libros (lower(titulo));
CREATE INDEX idx_libros_autor_lower ON libros (lower(autor));
CREATE INDEX idx_libros_materia_nivel_activo
    ON libros (materia_id, nivel, activo);
CREATE INDEX idx_ejemplares_libro_activo
    ON ejemplares (libro_id, activo);
CREATE INDEX idx_prestamos_lector_activo
    ON prestamos (lector_id)
    WHERE fecha_devolucion IS NULL;
CREATE INDEX idx_prestamos_fecha_limite_activos
    ON prestamos (fecha_limite)
    WHERE fecha_devolucion IS NULL;
CREATE INDEX idx_prestamos_fecha_prestamo ON prestamos (fecha_prestamo);
CREATE INDEX idx_prestamos_usuario_registro
    ON prestamos (registrado_por_usuario_id);
CREATE INDEX idx_prestamos_usuario_devolucion
    ON prestamos (devuelto_por_usuario_id)
    WHERE devuelto_por_usuario_id IS NOT NULL;

-- RN-01: un libro nuevo o reclasificado solo puede usar una materia activa.
CREATE OR REPLACE FUNCTION fn_validar_materia_activa_libro()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM materias
         WHERE id = NEW.materia_id
           AND activo
    ) THEN
        RAISE EXCEPTION 'La materia no existe o está inactiva'
            USING ERRCODE = '23514';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validar_materia_activa_libro
BEFORE INSERT OR UPDATE OF materia_id ON libros
FOR EACH ROW
EXECUTE FUNCTION fn_validar_materia_activa_libro();

-- Protege las reglas críticas al crear o reactivar un préstamo. La aplicación
-- volverá a validarlas dentro de su transacción cuando se implemente en Semana 6.
CREATE OR REPLACE FUNCTION fn_validar_prestamo_activo()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_lector_activo BOOLEAN;
    v_ejemplar_activo BOOLEAN;
    v_estado_fisico VARCHAR(20);
    v_usuario_activo BOOLEAN;
    v_prestamos_activos INTEGER;
BEGIN
    IF NEW.fecha_devolucion IS NOT NULL THEN
        RETURN NEW;
    END IF;

    -- Serializa préstamos simultáneos del mismo lector y del mismo ejemplar.
    SELECT activo
      INTO v_lector_activo
      FROM lectores
     WHERE id = NEW.lector_id
     FOR UPDATE;

    IF NOT FOUND OR NOT v_lector_activo THEN
        RAISE EXCEPTION 'El lector no existe o está inactivo'
            USING ERRCODE = '23514';
    END IF;

    SELECT activo, estado_fisico
      INTO v_ejemplar_activo, v_estado_fisico
      FROM ejemplares
     WHERE id = NEW.ejemplar_id
     FOR UPDATE;

    IF NOT FOUND OR NOT v_ejemplar_activo OR v_estado_fisico <> 'Operativo' THEN
        RAISE EXCEPTION 'El ejemplar no está activo y operativo'
            USING ERRCODE = '23514';
    END IF;

    SELECT activo
      INTO v_usuario_activo
      FROM usuarios
     WHERE id = NEW.registrado_por_usuario_id;

    IF NOT FOUND OR NOT v_usuario_activo THEN
        RAISE EXCEPTION 'El usuario responsable no existe o está inactivo'
            USING ERRCODE = '23514';
    END IF;

    IF EXISTS (
        SELECT 1
          FROM prestamos
         WHERE lector_id = NEW.lector_id
           AND fecha_devolucion IS NULL
           AND id <> NEW.id
           AND fecha_limite < (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
    ) THEN
        RAISE EXCEPTION 'El lector tiene al menos un préstamo vencido'
            USING ERRCODE = '23514';
    END IF;

    SELECT count(*)
      INTO v_prestamos_activos
      FROM prestamos
     WHERE lector_id = NEW.lector_id
       AND fecha_devolucion IS NULL
       AND id <> NEW.id;

    IF v_prestamos_activos >= 2 THEN
        RAISE EXCEPTION 'El lector ya tiene dos préstamos activos'
            USING ERRCODE = '23514';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validar_prestamo_activo
BEFORE INSERT OR UPDATE ON prestamos
FOR EACH ROW
EXECUTE FUNCTION fn_validar_prestamo_activo();
