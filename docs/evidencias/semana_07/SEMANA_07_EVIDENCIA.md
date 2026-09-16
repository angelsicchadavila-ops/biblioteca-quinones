# Evidencia técnica de la Semana 7

Estado: Semana 7 completa y aprobada expresamente el 16/09/2026 al autorizarse el inicio oficial de la Semana 8.

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

El registro documental final se publicó en `a0b935c`. Auto-Deploy tampoco reaccionó a ese push, por lo que se utilizó nuevamente `Deploy latest commit`. La captura final muestra `a0b935c` en estado `Live`, con disparador manual y duración de 45,7 s. El detalle del deployment mostró `Deploy succeeded | Live` y la ejecución de `gunicorn app:app`. Después, la prueba de humo HTTPS pasó 32/32, Neon pasó 7/7 y la huella de los registros existentes permaneció igual. `HEAD`, `origin/main` y la referencia remota coincidieron al terminar la publicación técnica.

## Capturas finales verificadas

Se abrieron individualmente los cuatro PNG reales de `capturas/`, se revisaron nombre, resolución, legibilidad, contenido y metadata. Todos son capturas de PC; sus tamaños son suficientes para leer el dato que respaldan. No contienen contraseñas, tokens, cadenas de conexión, Deploy Hook ni metadata sensible.

| Archivo | Evidencia visual verificada | Límite de la captura |
|---|---|---|
| `01_render_live_semana07.png` | Servicio correcto, fuente GitHub, rama `main`, `a0b935c` Live y deployment manual final. | El arranque Gunicorn se verificó en el detalle del deployment y en la prueba HTTPS. |
| `02_render_build_semana07.png` | Repositorio, rama `main`, Root Directory vacío, Build Command correcto e Included Paths sin entradas. | Ignored Paths queda fuera del recorte; se comprobó directamente en Settings. Es visible el identificador de la cuenta Git, ya presente en la metadata pública de commits, sin clave ni token. |
| `03_render_deploy_semana07.png` | Start Command `gunicorn app:app` y Auto-Deploy `On Commit`. | El bloque Deploy Hook queda fuera de la imagen. |
| `04_https_catalogo_semana07.png` | Página pública cargada y URL HTTPS visible. | La barra de dirección está activa; la conexión HTTPS efectiva se respaldó además con la prueba de humo real. |

Las capturas no sustituyen la verificación de Neon, variables privadas o persistencia; esos controles constan en `RESULTADOS_PRUEBAS.md` sin revelar valores secretos. Las capturas funcionales de Semanas 4 a 6 no se repitieron.

## Estado para aprobación

No queda un pendiente técnico identificado de Semana 7. Auto-Deploy continúa en `On Commit` y su falta de reacción a pushes se mantiene como observación no bloqueante, con `Deploy latest commit` probado como contingencia. La Semana 7 fue aprobada expresamente el 16/09/2026 cuando el usuario autorizó el inicio oficial de la Semana 8.

El campo `Responsable` del Documento Maestro conserva `[Nombre del estudiante]`; se mantiene como dato administrativo pendiente del estudiante, sin bloquear la Semana 7.
