# Evidencia de la Semana 3

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 03 — Flask, autenticación y deployment técnico temprano.
- Fecha de inicio: 09 de septiembre de 2026.
- Estado: En curso; implementación y pruebas locales completadas, deployment en Render pendiente.

## Arquitectura Flask creada

- `app.py`: fábrica de aplicación, rutas, carga de usuario, sesiones, autenticación, control por rol, CSRF y páginas de error.
- `utils/db.py`: conexión Psycopg 3 por solicitud, cierre automático y zona horaria `America/Lima`.
- `templates/`: vistas mínimas para inicio, login, administración, escaneo y errores.
- `static/css/style.css`: ajustes mínimos de presentación responsive.
- `tests/test_core.py`: pruebas reales de autenticación y permisos contra Neon.
- `render.yaml`: build, inicio Gunicorn, health check y variables privadas de Render.

No se modificó el esquema PostgreSQL ni se desarrollaron catálogo, QR, préstamos, devoluciones o reportes.

## Autenticación y permisos

- `/` y `/login` permanecen públicos.
- `/escaneo` exige una cuenta activa con rol `admin` o `asistente`.
- `/admin` exige una cuenta activa con rol `admin`; un `asistente` recibe HTTP 403.
- Los usuarios no autenticados son redirigidos a `/login`.
- El login consulta `usuarios` con SQL parametrizado y verifica `password_hash` con Werkzeug.
- El logout usa POST, valida CSRF, elimina la sesión y vuelve a proteger las rutas privadas.
- La cuenta se vuelve a consultar en cada solicitud privada, por lo que una cuenta desactivada pierde el acceso.

## Resultado local

La verificación previa de Neon obtuvo 7 de 7 comprobaciones. La suite completa obtuvo 19 de 19 pruebas correctas. El detalle está en `RESULTADOS_PRUEBAS.md`.

## Deployment y evidencias visuales pendientes

El deployment requiere vincular el repositorio de GitHub con una cuenta de Render y configurar `DATABASE_URL` como variable privada. `SECRET_KEY` queda configurada para generación automática por Render.

Cuando el servicio esté publicado se deben guardar estas capturas en `docs/evidencias/semana_03/capturas/`:

1. `01_login_render.png`: URL HTTPS visible y formulario de login completo, sin credenciales escritas.
2. `02_admin_render.png`: panel administrativo con el texto `Rol verificado: admin`; no mostrar contraseña.
3. `03_asistente_render.png`: terminal de escaneo con el texto `Rol verificado: asistente`; no mostrar contraseña.
4. `04_bloqueo_asistente_admin.png`: página de acceso denegado al abrir `/admin` como asistente.
5. `05_render_https_pc.png`: página de inicio en escritorio con el candado o URL `https://` visible.
6. `06_render_https_movil.png`: la misma URL abierta en un teléfono real, con la página completa y sin datos sensibles.

La URL pública y los resultados definitivos de HTTPS y móvil se registrarán después de completar la configuración externa.
