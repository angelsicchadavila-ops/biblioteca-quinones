# Análisis de impacto de la versión 1.1

## Base estable y rollback

La versión 1.1 se construye sobre el commit estable `a629694aae199a00a55ae34009fe60f1326c9b49`, protegido mediante la etiqueta `v1.0-final`. Antes de la migración se registró el punto de Neon `2026-09-24 14:27:10 UTC`, LSN `0/2317358`.

## Cambios aprobados

- Añadir `libros.anio_publicacion` como `SMALLINT NULL`, con rango 1000–9999.
- Exigir año para libros nuevos y conservar `NULL` al editar libros legados sin año.
- Incorporar filtro público combinable por año.
- Permitir al asistente listar, crear y editar libros, sin ampliar permisos de estado, materias o ejemplares.
- Añadir un módulo exclusivo de administrador para crear, listar, desactivar, reactivar y restablecer contraseñas de asistentes.
- Añadir recuperación técnica de contraseña del administrador mediante un script interactivo y `getpass`.

## Compatibilidad

La migración es aditiva y no actualiza registros existentes. La tabla `usuarios` ya dispone de `activo`, y los préstamos conservan referencias `ON DELETE RESTRICT` a los usuarios responsables. No se modifican las reglas de préstamos, devoluciones, QR, mora, lectores, reportes, disponibilidad ni trazabilidad.

## Riesgos y mitigaciones

- Migración de año: riesgo bajo; columna nullable y constraint validado.
- Permisos de libros: riesgo medio; autorización de backend y pruebas de URL/POST directo.
- Gestión de cuentas y contraseñas: riesgo alto; rol fijado en servidor, hash Werkzeug, CSRF y consultas parametrizadas.
- Deployment: riesgo medio; migración previa al código y rollback de código compatible con la columna adicional.

## Pruebas requeridas

Se requiere cobertura de año, permisos del asistente, gestión de usuarios, recuperación administrativa y regresión completa de la v1.0. La validación final incluye suite `unittest`, integridad y concurrencia, verificación Neon, smoke Render, compilación, dependencias, secretos y diferencias Git.
