# Evidencia técnica de la Semana 7

Estado: verificaciones técnicas completadas; pendientes las capturas del estado final y la revisión del usuario. La Semana 7 no está cerrada ni aprobada.

## Alcance y fuente

Se revisaron `AGENTS.md`, el Documento Maestro v1.0, `docs/ESTADO_PROYECTO.md`, los cierres de Semanas 1 a 6, el código y Git antes de modificar archivos. La Semana 6 consta como completa y aprobada. Esta semana consolida Render, Neon, Gunicorn, variables privadas y seguridad básica; no incorpora nuevas funciones de negocio ni modifica el modelo de datos.

## Estado previo comprobado

- Árbol Git local limpio en `main`; `HEAD`, `origin/main` y la referencia descargada desde GitHub coincidían en `e249cbf`.
- Render mostraba `biblioteca-quinones` como servicio Python 3 Free, fuente `angelsicchadavila-ops/biblioteca-quinones`, rama `main`, estado `Live` y último commit desplegado `ecfd370`. El cierre documental local `e249cbf` todavía no figuraba desplegado.
- URL pública `https://biblioteca-quinones.onrender.com/` operativa; catálogo cargó y consultó materias de Neon.
- Build Command: `pip install -r requirements.txt`; Start Command: `gunicorn app:app`; Root Directory vacío; sin Included Paths ni Ignored Paths configurados.
- Auto-Deploy: `On Commit`. Los deployments previos de Semanas 4 a 6 aparecían con disparador manual. No se identificó un filtro de rutas, rama o repositorio incorrecto que explique de forma segura el fallo intermitente. El Deploy Hook no se mostró, copió ni utilizó.
- Variables presentes en el panel privado: `DATABASE_URL`, `SECRET_KEY`, `SESSION_COOKIE_SECURE`. Se comprobó internamente que la primera utiliza PostgreSQL en Neon y la última está activa; sus valores no se registraron. `SECRET_KEY` no se regeneró.
- Health Check Path del servicio actual vacío. La ruta pública `/` respondió 200 y puede emplearse como comprobación de disponibilidad si en el futuro se decide configurarla. `render.yaml` declara `/`, sin que sea necesario cambiar el servicio operativo esta semana.

## Seguridad y estabilidad

- Los dos usuarios existentes tienen `password_hash` con formato Werkzeug; la autenticación utiliza `check_password_hash` y el inicializador `generate_password_hash`. No se hallaron contraseñas en texto plano en el seed ni secretos reales en archivos versionados.
- Flask utiliza sesión, vuelve a consultar el usuario activo por solicitud, exige CSRF en POST y distingue permisos `admin`/`asistente` en el backend. El logout invalida la sesión.
- El catálogo público no muestra datos de lectores ni préstamos internos. La API de ejemplar bloquea al público; los endpoints QR/PDF y las rutas de listados/reportes son administrativos.
- La cookie de sesión de Render se observó con atributos `Secure` y `HttpOnly` por HTTPS; la configuración declara también `SameSite=Lax`.
- Los errores 403, 404 y de PostgreSQL muestran páginas genéricas; los mensajes de validación no publican cadenas de conexión. Los archivos frontend no incluyen URLs de Neon, claves o tokens persistentes.
- `requirements.txt` declara Flask, Psycopg 3, Gunicorn, python-dotenv, qrcode/Pillow, ReportLab y Werkzeug, todos utilizados. `pip check` pasó. No se detectaron rutas absolutas de la laptop ni archivos locales no versionados requeridos por Render; `.env` solo se carga cuando existe y las variables privadas del servicio suministran la configuración.
- El visor de logs de aplicación de Render, en su muestra visible reciente, mostró respuestas 200 y ningún HTTP 500, excepción o error repetitivo de conexión. No se copiaron logs a documentación.

## Neon y pruebas

El verificador existente confirmó 6 tablas, constraints, índices, triggers, cinco materias y las dos cuentas aprobadas: 7/7. La integridad transaccional y de concurrencia pasó 11/11. La suite completa terminó 34/34. Tras estas pruebas se observaron 0 libros, ejemplares, lectores y préstamos, y 0 residuos `TEMP-SEMANA-%`. El detalle está en `RESULTADOS_PRUEBAS.md`. No se recreó la base, no se ejecutó DROP y no se modificaron datos reales.

## Redeploy, reinicio y persistencia

El commit legítimo `0ae60c9` se publicó en `origin/main` después de las pruebas y revisión de secretos. Durante la ventana de observación Render no creó un deployment automático, pese a conservar `On Commit`; el panel seguía en `ecfd370`. Se ejecutó `Manual Deploy` → `Deploy latest commit`. Render construyó e instaló las dependencias de `requirements.txt`, ejecutó `gunicorn app:app` y completó el deployment manual en 48,9 s con `Deploy succeeded | Live` para `0ae60c9`. No se utilizó el Deploy Hook ni se modificaron variables o configuración crítica.

Después del redeploy, la prueba HTTPS de solo lectura superó 32 comprobaciones, incluidas ambos logins y las consultas a Neon a través de Render. La verificación de Neon volvió a pasar 7/7. Antes y después se compararon conteos y una huella calculada de identificadores/nombres de las cinco materias y de los dos usuarios; ambas coincidieron. Los datos existentes persistieron y no hubo registros operativos o temporales residuales.

Se ejecutó además `Restart service`. Los logs recientes mostraron un nuevo arranque de Gunicorn sin errores relevantes. La prueba de humo volvió a pasar 32/32 y la huella de los registros Neon siguió igual. Render continuó Live en `0ae60c9`. El plan Free puede suspender una instancia por inactividad y demorar su primera solicitud; la comprobación controlada cubrió arranque tras redeploy y reinicio, no una espera prolongada de inactividad.

## Pendientes para completar la evidencia

- Incorporar las capturas puntuales del deployment documental final indicadas en `capturas/INSTRUCCIONES_CAPTURAS.md` y permitir revisión del usuario antes de declarar el cierre.

El campo `Responsable` del Documento Maestro conserva `[Nombre del estudiante]`; se mantiene como dato administrativo pendiente del estudiante, sin bloquear la Semana 7.
