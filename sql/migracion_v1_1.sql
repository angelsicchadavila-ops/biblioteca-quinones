-- Migración aditiva v1.1: año de publicación opcional para compatibilidad.
-- No elimina ni reescribe datos existentes y puede ejecutarse nuevamente.

BEGIN;

ALTER TABLE public.libros
    ADD COLUMN IF NOT EXISTS anio_publicacion SMALLINT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
          FROM pg_constraint
         WHERE conrelid = 'public.libros'::regclass
           AND conname = 'ck_libros_anio_publicacion'
    ) THEN
        ALTER TABLE public.libros
            ADD CONSTRAINT ck_libros_anio_publicacion
            CHECK (
                anio_publicacion IS NULL
                OR anio_publicacion BETWEEN 1000 AND 9999
            ) NOT VALID;
    END IF;
END;
$$;

ALTER TABLE public.libros
    VALIDATE CONSTRAINT ck_libros_anio_publicacion;

COMMIT;
