# Resultados de pruebas de la Semana 7

Fecha: 15 de septiembre de 2026. Entornos: aplicación local conectada a Neon y servicio público Render por HTTPS. Las pruebas funcionales de esta semana son de humo y regresión; el QA integral permanece reservado para la Semana 8.

| Comprobación ejecutada | Resultado real |
|---|---|
| `python -m unittest discover -s tests -v` | 34/34 correctas en 216,053 s |
| `python scripts/probar_integridad_bd.py` | 11/11 correctas; datos temporales revertidos o limpiados |
| `python scripts/verificar_bd.py` | 7/7: tablas, constraints, índices, triggers, seed y limpieza |
| `python -m compileall -q app.py utils scripts tests` | Correcto; sin errores de sintaxis |
| `python -m pip check` | Correcto; sin incompatibilidades declaradas |
| `python scripts/verificar_produccion.py` | Correcto: catálogo HTTPS, login admin/asistente, sesiones, cookie Secure y HttpOnly, CSRF, rutas por rol, reportes, QR/PDF protegidos, logout |
| Revisión de archivos versionados y `.gitignore` | `.env` ignorado y no versionado; `.env.example` contiene marcadores; búsqueda de patrones de URL/clave real sin coincidencias |
| Consulta de solo lectura a Neon | Host Neon confirmado; 2 usuarios con hashes Werkzeug, 5 materias iniciales, 0 libros, ejemplares, lectores y préstamos, 0 residuos `TEMP-SEMANA-%` |
| Redeploy manual de `0ae60c9` | `Deploy succeeded | Live` en 48,9 s; Render ejecutó `gunicorn app:app` |
| Humo posterior al redeploy | 32/32 comprobaciones correctas por HTTPS |
| Persistencia posterior al redeploy | 2 usuarios y 5 materias; huella de identificadores/nombres igual a la línea base; Neon 7/7 |
| Reinicio controlado del servicio | Gunicorn volvió a iniciar sin errores relevantes en los logs recientes |
| Humo y persistencia posteriores al reinicio | 32/32 comprobaciones correctas; misma huella de registros Neon |
| Deployment documental final `a0b935c` | Manual, `Deploy succeeded | Live`, 45,7 s; Gunicorn ejecutado |
| Humo HTTPS después del deployment final | 32/32 comprobaciones correctas |
| Neon después del deployment final | 7/7 y huella de datos existentes igual a la línea base |
| Nueva comprobación antes del cierre documental | Humo HTTPS 32/32 y Neon 7/7 correctos |
| Capturas finales de PC | 4/4 PNG abiertos y revisados visualmente; metadata sin valores sensibles |

La suite cubrió catálogo, materias, libros, ejemplares, QR, PDF A4, terminal, ingreso manual, préstamos, devoluciones, listados, reportes, CSRF, permisos y concurrencia. En Render se comprobó que el público recibe 401 al consultar la API interna y que el asistente recibe 403 en las rutas administrativas. Los endpoints QR/PDF devolvieron 404 para un ejemplar inexistente con sesión admin; la generación real de archivos quedó respaldada por la suite automática, sin crear datos temporales en producción para esta prueba de humo.

La primera ejecución de `verificar_bd.py` dentro del entorno restringido no pudo conectarse por el permiso de red local. La misma orden con acceso de red autorizado pasó 7/7. No fue un fallo de Neon ni de la aplicación.

El script de humo toma las contraseñas de prueba del entorno local y nunca las imprime. No se guardaron cookies, tokens CSRF, cabeceras completas ni cadenas de conexión en esta evidencia.

Auto-Deploy siguió configurado en `On Commit`, pero no inició un deployment tras el push `0ae60c9`; el panel continuó mostrando el commit anterior después de la ventana de observación. Se utilizó `Deploy latest commit` y el nuevo commit pasó a `Live`. Los Build Filters están vacíos, Root Directory está vacío, y repositorio/rama son correctos; no se identificó una causa segura del fallo de detección.

El push documental `a0b935c` tampoco activó Auto-Deploy. La misma contingencia lo dejó Live. La revisión visual final confirmó Build y Start Command, `On Commit`, el commit definitivo y el catálogo visible; la captura de Build deja fuera del encuadre Ignored Paths, que se verificó directamente en el panel. La captura del catálogo muestra la barra de dirección activa, por lo que la negociación HTTPS queda respaldada por la prueba de humo en red.
