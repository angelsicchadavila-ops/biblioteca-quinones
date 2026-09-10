# Esquema PostgreSQL implementado en Neon

## Resultado

El 09 de septiembre de 2026 se inicializó correctamente la base `neondb` de la rama `production` del proyecto Neon `biblioteca-quinones`. La ejecución se realizó con Psycopg 3 mediante una conexión directa con SSL y sin registrar la cadena de conexión en Git ni en esta evidencia.

## Tablas creadas

| Tabla | Propósito | Relaciones principales |
|---|---|---|
| `usuarios` | Cuentas internas y roles | Registra altas y devoluciones de préstamos |
| `materias` | Clasificación controlada | Tiene muchos libros |
| `libros` | Información del título | Pertenece a una materia y tiene ejemplares |
| `ejemplares` | Copia física con QR | Pertenece a un libro y conserva historial de préstamos |
| `lectores` | Identidad persistente del lector | Conserva historial de préstamos sin datos académicos permanentes |
| `prestamos` | Operación, fechas y trazabilidad | Relaciona lector, ejemplar y usuarios responsables |

La vista `Tables` de Neon confirmó visualmente las seis tablas en el esquema `public`.

## Restricciones principales

- Claves primarias `SERIAL` en las seis tablas.
- Claves foráneas con `ON DELETE RESTRICT` para preservar historial.
- `UNIQUE` para `usuarios.username`, `materias.nombre` y `ejemplares.codigo_qr`.
- Dominios `CHECK` para roles, niveles académicos y estado físico.
- Verificación de textos obligatorios no vacíos.
- Coherencia entre `fecha_prestamo`, `fecha_limite`, `fecha_devolucion` y el usuario responsable de la devolución.
- Trigger que exige una materia activa al crear o reclasificar un libro.
- Trigger transaccional que bloquea préstamos a lectores inactivos, lectores morosos, lectores con dos préstamos activos y ejemplares inactivos o dañados.
- Índice único parcial `uq_prestamos_ejemplar_activo`, que impide dos préstamos simultáneos sin devolución para el mismo ejemplar.
- No existe un campo redundante que almacene el estado `Prestado` en `ejemplares`.

## Índices explícitos

- `uq_prestamos_ejemplar_activo`
- `idx_libros_titulo_lower`
- `idx_libros_autor_lower`
- `idx_libros_materia_nivel_activo`
- `idx_ejemplares_libro_activo`
- `idx_prestamos_lector_activo`
- `idx_prestamos_fecha_limite_activos`
- `idx_prestamos_fecha_prestamo`
- `idx_prestamos_usuario_registro`
- `idx_prestamos_usuario_devolucion`

## Datos iniciales

- Materias: Comunicación, Matemática, Ciencia y Tecnología, Ciencias Sociales e Inglés.
- Dos cuentas de prueba: una con rol `admin` y otra con rol `asistente`.
- Las contraseñas no forman parte del repositorio; el inicializador recibió valores locales y almacenó únicamente hashes generados con Werkzeug.
