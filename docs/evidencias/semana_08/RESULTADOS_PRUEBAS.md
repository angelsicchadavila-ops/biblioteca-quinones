# Resultados de pruebas Semana 8

Estado del documento: cierre técnico completo y listo para revisión del usuario. No se ha iniciado la Semana 9. La prueba presencial con bibliotecaria no se realizó y queda registrada como `NO APLICA` para este cierre, sin inventar participación.

La matriz contiene 167 casos con estado final: 160 `APROBADO`, 4 `CORREGIDO`, 3 `NO APLICA`, 0 `FALLIDO` y 0 pendientes.

## Precondiciones verificadas

| Comprobación | Resultado real |
|---|---|
| Semana 7 | Cierre técnico completo; la orden de iniciar oficialmente Semana 8 constituye la aprobación expresa que faltaba registrar |
| Git antes de cambios | `main` limpia, `HEAD` y `origin/main` en `f1f1515`, divergencia 0/0 después de `fetch` |
| Render antes de cambios | HTTPS operativo; smoke 32/32; commit `f1f1515` Live |
| Neon antes de cambios | Accesible; verificación 7/7 |
| Documento Maestro | Revisado: 242 párrafos, 32 tablas, RN-01 a RN-18, CA-01 a CA-14 y alcance de Semana 8 |
| Cierres Semanas 1 a 7 | Revisados junto con resultados y evidencias principales |

El render interno del DOCX no pudo repetirse porque el runtime disponible no incluye `soffice.exe`. El contenido completo se revisó mediante extracción estructural; la evidencia de Semana 1 ya registra una inspección visual correcta de sus 16 páginas.

## Línea base de regresión

| Prueba | Resultado |
|---|---|
| Suite existente antes de cambios | 34/34 correctas en 238,617 s |
| Integridad y concurrencia Neon | 11/11 correctas; datos revertidos o eliminados |
| Verificación de esquema Neon | 7/7 correctas |
| Smoke Render HTTPS | 32/32 correctas |
| `compileall` | Correcto |
| `pip check` | Sin dependencias incompatibles |
| `git diff --check` | Correcto; solo avisos informativos LF/CRLF |
| Secretos versionados | `.env` ignorado y no versionado; solo marcadores en `.env.example`; aplicación lee variables sin valores por defecto secretos |

## Incidencia reproducida y corrección

La nueva prueba `test_04_no_se_crean_ejemplares_en_libro_inactivo` falló antes de la corrección. La respuesta confirmó que el sistema creó `LIB-037-EJ01` para un libro desactivado y lo mostró como Disponible. Los datos temporales de esa reproducción fueron eliminados por `finally`.

Después de la corrección:

| Verificación | Resultado |
|---|---|
| Prueba puntual corregida | 1/1 correcta en 7,735 s |
| Pruebas QA nuevas | 4/4 correctas en 36,887 s |
| Suite completa ampliada | 38/38 correctas en 269,008 s |
| Neon posterior a la suite | 7/7 correctas; sin residuos de la suite |
| Compilación posterior | Correcta |
| `pip check` posterior | Correcto |
| `git diff --check` posterior | Correcto |

Las pruebas nuevas cubren sesión inválida, catálogo sin coincidencias y sin controles administrativos, matriz ampliada de URLs directas por rol, y bloqueo de altas en libros inactivos con conservación de inventario histórico.

## Git y Render de la corrección

- Commit técnico: `83d1677` (`fix: corregir inventario inactivo en QA semana 8`).
- Push: correcto a `origin/main`.
- Auto-Deploy: no reaccionó al push; el panel seguía mostrando `f1f1515`.
- Contingencia: `Manual Deploy` → `Deploy latest commit`.
- Resultado: `83d1677`, `Deploy succeeded | Live`, 38,4 s.
- Gunicorn: `gunicorn app:app`; Gunicorn 23.0.0 inició, escuchó en el puerto asignado y arrancó un worker sin errores relevantes.
- Health check visible: `GET /` HTTP 200.
- Smoke posterior: 32/32 por HTTPS.
- Revisión de navegador: catálogo responsive visible, Bootstrap cargado y sin errores o advertencias en la consola del navegador.
- Después del commit documental `f985761` y su push, Auto-Deploy volvió a no reaccionar. Se aplicó nuevamente `Deploy latest commit`.
- Deployment final: `dep-dalcirnf3r2c738pi5ag`, fuente `f985761`, `Deploy succeeded | Live`, duración 1 min 07 s.
- Logs finales: build correcto, `gunicorn app:app`, Gunicorn 23.0.0, worker iniciado y comprobaciones `HEAD /` y `GET /` con HTTP 200, sin errores relevantes.
- Smoke posterior al deployment final: 32/32 por HTTPS.

## Datos y validación móvil

El conjunto controlado se preparó con estos datos antes de la intervención del responsable:

| Dato | Estado |
|---|---|
| Materia | `TEMP-SEMANA-08 QA` |
| Libro | `TEMP-SEMANA-08 QA MOVIL` |
| `LIB-044-EJ01` | Operativo, activo y disponible; ciclo principal |
| `LIB-044-EJ02` | Operativo, activo y disponible; reserva |
| `LIB-044-EJ03` | Dañado; préstamo debe quedar bloqueado |
| `LIB-044-EJ04` | Operativo e inactivo; préstamo debe quedar bloqueado |
| Préstamos temporales | 0 antes de la prueba móvil |
| Lectores temporales | 0 antes de la prueba móvil |

Se generaron `QR_TEMP_SEMANA_08.png` y `ETIQUETAS_QA_SEMANA_08.pdf`. `pdfinfo` confirmó 1 página A4 (595,276 x 841,89 pt) y el PDF se renderizó a PNG a 150 dpi: las cuatro etiquetas quedaron nítidas, alineadas, sin recortes ni superposiciones. El QR individual también se revisó a resolución original. Render confirmó 1 título, 4 ejemplares, 2 disponibles, 1 dañado y 1 inactivo.

La validación se realizó desde un teléfono real con Samsung Internet; el modelo exacto no fue informado. El responsable comunicó como aprobados catálogo, login, inicio/detención/reinicio de cámara, QR con iluminación normal y baja, código inexistente e ingreso manual, préstamo y devolución, mensajes, botones, formularios y ausencia de desbordamiento horizontal. La bibliotecaria no participó.

Las cinco capturas recibidas fueron revisadas visualmente:

- `01_catalogo_movil_semana08.png`: catálogo responsive y conteos coherentes.
- `02_bloqueo_permisos_semana08.png`: asistente bloqueado al abrir una ruta administrativa directa.
- `03_camara_qr_semana08.png`: cámara real y `LIB-044-EJ01` identificado correctamente.
- `04_ciclo_prestamo_semana08.png`: mensaje de préstamo registrado correctamente.
- `05_reporte_movil_semana08.png`: RPT-01 legible en orientación horizontal.

La primera limpieza controlada dejó la materia, libro, cuatro ejemplares y préstamo temporal en cero, pero `verificar_bd.py` detectó un lector `LECTOR TEMP / SEMANA 08` porque el auxiliar comparaba mayúsculas de forma exacta. Se registró INC-08-002, se normalizó la comparación sin ampliar el alcance de borrado, se confirmó que el lector no tenía préstamos ajenos y se eliminó únicamente ese residuo. Estado final `TEMP-SEMANA-08`: materias 0, libros 0, ejemplares 0, préstamos 0 y lectores 0.

## Verificación final posterior a la prueba móvil

| Comprobación | Resultado final |
|---|---|
| Suite oficial `unittest` | 38/38 correctas en 303,407 s |
| Integridad y concurrencia Neon | 11/11; datos revertidos o eliminados |
| Verificación Neon | Primera ejecución 6/7 por INC-08-002; corrección aplicada; final 7/7 |
| Smoke Render HTTPS | 32/32 |
| Compilación | Correcta |
| `pip check` | Sin dependencias incompatibles |
| `git diff --check` | Correcto; únicamente avisos informativos LF/CRLF |
| Secretos | `.env` ignorado y no versionado; sin secretos reales en Git |
| Matriz QA | 167/167 con estado final; 0 fallidos y 0 pendientes |

Se intentó inicialmente invocar `pytest`, pero el proyecto no incluye esa dependencia porque su ejecutor oficial es `unittest`; no se contabilizó como prueba funcional. A continuación se ejecutó el comando documentado en `README.md`, que completó las 38 pruebas correctamente.

No quedan bloqueos técnicos para el cierre de Semana 8. La ejecución con bibliotecaria queda como acción presencial opcional pendiente del responsable. La Semana 9 no debe iniciarse hasta la aprobación expresa del usuario.
