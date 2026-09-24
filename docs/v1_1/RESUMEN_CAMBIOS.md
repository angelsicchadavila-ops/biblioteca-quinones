# Resumen de cambios v1.1

## Alcance implementado

La versión 1.1 extiende la base estable v1.0 sin reconstruir el sistema ni modificar las reglas de préstamos, devoluciones, QR, mora, lectores, reportes, disponibilidad o trazabilidad.

- Libros: campo `anio_publicacion`, obligatorio para altas nuevas, editable y nullable para libros legados.
- Catálogo: filtro por año combinable con texto, materia y nivel.
- Asistente: acceso al listado administrativo, alta y edición bibliográfica de libros.
- Restricciones del asistente: sin activar/desactivar libros, gestionar materias, ejemplares o usuarios.
- Usuarios: módulo exclusivo de admin para listar asistentes, crear cuentas, cambiar contraseña, desactivar y reactivar.
- Recuperación admin: script técnico interactivo con `getpass`, hash Werkzeug y consultas parametrizadas.

## Base de datos y rollback

- Base protegida: `a629694aae199a00a55ae34009fe60f1326c9b49`.
- Etiqueta inmutable de referencia: `v1.0-final`.
- Punto previo de Neon: `2026-09-24 14:27:10 UTC`, LSN `0/2317358`.
- Migración: `sql/migracion_v1_1.sql`.
- Cambio aplicado: `libros.anio_publicacion SMALLINT NULL` y constraint de rango 1000–9999.
- No se añadieron índices, tablas ni cambios a `usuarios`; su columna `activo` existente se reutilizó.

La migración es aditiva y el código v1.0 ignora la columna nueva, por lo que el rollback de código consiste en desplegar el commit etiquetado `v1.0-final`. No se recomienda retirar la columna para volver al código anterior: conservarla evita pérdida de datos v1.1. Cualquier restauración temporal de Neon debe realizarse desde el punto registrado y solo ante una incidencia confirmada.

## Seguridad

- El rol de las cuentas creadas desde web se fija como `asistente` en el SQL del backend.
- Las operaciones sobre cuentas se restringen por ID y `rol = 'asistente'`.
- Las contraseñas requieren al menos 12 caracteres y confirmación.
- Solo se persisten hashes Werkzeug; las plantillas y listados nunca consultan ni muestran `password_hash`.
- La desactivación es lógica mediante `activo = FALSE`; no existe borrado físico desde la interfaz.
- La carga de usuario en cada solicitud invalida una sesión ya abierta cuando la cuenta pasa a inactiva.

## Archivos principales

- Backend: `app.py`, `utils/catalogo.py`.
- Esquema y migración: `sql/schema.sql`, `sql/migracion_v1_1.sql`.
- Interfaz: `templates/index.html`, `templates/libro_form.html`, `templates/libros.html`, `templates/admin_dashboard.html`, `templates/base.html`, `templates/usuarios.html`, `templates/usuario_form.html`, `templates/usuario_contrasena.html`.
- Operación: `scripts/restablecer_password_admin.py`, `scripts/verificar_bd.py`, `scripts/verificar_produccion.py`.
- Pruebas: `tests/test_v1_1.py` y ajustes legítimos de expectativas v1.1 en la regresión histórica.

## Commit de implementación

La implementación probada quedó registrada en `e0283aaf428933e06ae05e3f830057d216aea970` (`feat: implementar version 1.1`).
