# Evidencia de la Semana 3

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 03 — Flask, autenticación y deployment técnico temprano.
- Fecha de inicio: 09 de septiembre de 2026.
- Estado: Completada; pendiente únicamente de revisión y aprobación del usuario.

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

## Deployment técnico en Render

- Servicio: `biblioteca-quinones`.
- Plan: Free, 0.1 CPU y 512 MB RAM.
- Región: Oregon (US West).
- Fuente: rama `main` del repositorio GitHub.
- Commit desplegado: `5096cf4` (`feat: implementar base Flask y autenticacion`).
- Build: `pip install -r requirements.txt`.
- Inicio: `gunicorn app:app`.
- Variables privadas configuradas: `DATABASE_URL`, `SECRET_KEY` y `SESSION_COOKIE_SECURE=true`.
- Resultado del primer deployment: `Deploy succeeded | Live`.
- URL pública: https://biblioteca-quinones.onrender.com
- Validación del health check `/`: HTTP 200.
- HTTPS: correcto en navegador de escritorio y en pruebas HTTP automatizadas.

Render registró el arranque de Gunicorn, la escucha en el puerto asignado y respuestas HTTP 200 sin exponer secretos. La aplicación desplegada autenticó correctamente contra las cuentas existentes en Neon, lo que comprueba la conexión funcional con la base de datos de Semana 2.

## Evidencias visuales

Capturas guardadas en `docs/evidencias/semana_03/capturas/`:

1. `01_login_render.png`: formulario de login de la instancia pública, sin credenciales escritas.
2. `02_admin_render.png`: panel con `Rol verificado: admin`.
3. `03_asistente_render.png`: terminal con `Rol verificado: asistente`.
4. `04_bloqueo_asistente_admin.png`: respuesta de acceso denegado al intentar abrir `/admin` como asistente.
5. `05_render_https_pc.png`: página pública desplegada, validada mediante la URL HTTPS registrada en este documento.
6. `06_render_https_movil.png`: login abierto desde un teléfono Android real; se observa el dominio público, el indicador de conexión segura y el formulario completo sin credenciales.

## Cierre de la semana

Los criterios técnicos de la Semana 3 quedaron cubiertos: aplicación Flask operativa, conexión a Neon, autenticación por hash, sesiones, logout, rutas protegidas, autorización por rol, ejecución con Gunicorn, deployment público por HTTPS y acceso desde escritorio y móvil real.

No se inició ninguna funcionalidad de la Semana 4.
