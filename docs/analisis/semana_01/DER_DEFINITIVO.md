# DER definitivo de la versión 1.0

## Diagrama oficial

El diagrama definitivo es [`docs/Modelo_Logico_Biblioteca_v1.0.png`](../../Modelo_Logico_Biblioteca_v1.0.png). Fue contrastado con el capítulo 8 y el Anexo A del Documento Maestro v1.0.

```mermaid
erDiagram
    MATERIAS ||--o{ LIBROS : clasifica
    LIBROS ||--o{ EJEMPLARES : contiene
    LECTORES ||--o{ PRESTAMOS : realiza
    EJEMPLARES ||--o{ PRESTAMOS : registra_historial
    USUARIOS ||--o{ PRESTAMOS : registra
    USUARIOS ||--o{ PRESTAMOS : devuelve

    USUARIOS {
        SERIAL id PK
        VARCHAR username UK
        VARCHAR password_hash
        VARCHAR nombre_completo
        VARCHAR rol
        BOOLEAN activo
        TIMESTAMP fecha_registro
    }
    MATERIAS {
        SERIAL id PK
        VARCHAR nombre UK
        BOOLEAN activo
    }
    LIBROS {
        SERIAL id PK
        VARCHAR titulo
        VARCHAR autor
        INT materia_id FK
        VARCHAR nivel
        VARCHAR isbn_editorial
        BOOLEAN activo
        TIMESTAMP fecha_registro
    }
    EJEMPLARES {
        SERIAL id PK
        INT libro_id FK
        VARCHAR codigo_qr UK
        VARCHAR estado_fisico
        BOOLEAN activo
        TIMESTAMP fecha_registro
    }
    LECTORES {
        SERIAL id PK
        VARCHAR nombres
        VARCHAR apellidos
        BOOLEAN activo
        TIMESTAMP fecha_registro
    }
    PRESTAMOS {
        SERIAL id PK
        INT lector_id FK
        INT ejemplar_id FK
        INT registrado_por_usuario_id FK
        INT devuelto_por_usuario_id FK
        VARCHAR nivel_alumno
        VARCHAR grado_seccion_alumno
        TIMESTAMP fecha_prestamo
        DATE fecha_limite
        TIMESTAMP fecha_devolucion
    }
```

## Relaciones validadas

- Una materia tiene muchos libros; cada libro pertenece a una materia.
- Un libro tiene muchos ejemplares; cada ejemplar pertenece a un libro.
- Un lector puede tener muchos préstamos históricos.
- Un ejemplar puede tener muchos préstamos históricos, pero solo uno activo simultáneamente.
- Un usuario puede registrar préstamos y confirmar devoluciones.

## Restricciones que deberá materializar la Semana 2

- `usuarios.username`, `materias.nombre` y `ejemplares.codigo_qr` son únicos.
- `prestamos.fecha_devolucion IS NULL` identifica un préstamo activo.
- Un índice o restricción única parcial impedirá más de un préstamo activo por ejemplar.
- Las operaciones de préstamo y devolución serán transaccionales.
- Los valores de rol, nivel y estado físico se limitarán a los dominios definidos.

Estas restricciones se documentan aquí para cerrar el diseño. El archivo `schema.sql` no se crea durante la Semana 1.
