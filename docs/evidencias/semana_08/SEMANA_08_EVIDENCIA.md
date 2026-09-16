# Evidencia técnica Semana 8

## Estado

Semana 8 completa técnicamente y lista para revisión del usuario. El QA integral, regresión, validación móvil real, correcciones, limpieza, seguridad, Neon, Render y evidencias están completos. La bibliotecaria no participó en esta ejecución y no se afirma lo contrario. No se ha iniciado la Semana 9.

## Alcance ejecutado

- Revisión de `AGENTS.md`, Documento Maestro v1.0, `ESTADO_PROYECTO.md`, `REGISTRO_CAMBIOS.md`, cierres de Semanas 1 a 7, código e historial Git.
- Confirmación remota de sincronización Git antes de cambios.
- Línea base completa de regresión, integridad Neon, smoke HTTPS, compilación, dependencias, secretos y diferencias.
- Revisión funcional de catálogo, autenticación, materias, libros, ejemplares, QR/PDF, escáner, lectores, préstamos, devoluciones, semáforo, reportes y permisos con las pruebas existentes.
- Ampliación de cobertura para sesión inválida, catálogo sin coincidencias, URLs directas por rol y altas en libros inactivos.
- Corrección mínima de INC-08-001 sin cambiar arquitectura, esquema, roles ni reglas del Documento Maestro.
- Deployment manual del commit técnico después de confirmarse nuevamente que Auto-Deploy no reaccionó.
- Preparación de la guía de prueba de campo, instrucciones móviles y datos `TEMP-SEMANA-08`.
- Validación desde teléfono real en Samsung Internet y revisión visual de cinco capturas representativas.
- Limpieza controlada completa de los datos temporales y corrección del auxiliar para reconocer el lector marcado sin depender de mayúsculas.
- Repetición final de suite, integridad, Neon, smoke HTTPS, compilación, dependencias, secretos y diferencias.

## Resultados actuales

- Suite completa: 38/38.
- Integridad Neon: 11/11.
- Verificación Neon tras la suite: 7/7.
- Smoke Render después del deployment: 32/32.
- Incidencias encontradas: 2 —una funcional de severidad media y una del auxiliar de QA de severidad baja—.
- Incidencias corregidas: 2.
- Incidencias pendientes: 0.
- Matriz QA: 167/167 casos con estado final.
- Estados finales: 160 `APROBADO`, 4 `CORREGIDO`, 3 `NO APLICA`, 0 `FALLIDO` y 0 pendientes.
- Validación móvil: aprobada; cinco capturas revisadas; navegador Samsung Internet; modelo no informado.
- Prueba de campo con bibliotecaria: no realizada; guía lista.
- Datos temporales: materias 0, libros 0, ejemplares 0, préstamos 0 y lectores 0.
- Render: `83d1677` Live por HTTPS, Gunicorn 23.0.0, logs del deployment sin errores relevantes.
- Auto-Deploy: continúa en `On Commit` según la configuración previamente verificada, pero no reaccionó al push; contingencia manual correcta.
- Verificación final: suite 38/38 en 303,407 s, integridad 11/11, Neon final 7/7 y smoke HTTPS 32/32.

## Archivos principales

- `app.py`.
- `utils/catalogo.py`.
- `templates/ejemplares.html`.
- `tests/test_qa_semana8.py`.
- `scripts/datos_qa_semana8.py`.
- `docs/evidencias/semana_08/RESULTADOS_PRUEBAS.md`.
- `docs/evidencias/semana_08/INCIDENCIAS_QA.md`.
- `docs/evidencias/semana_08/GUIA_PRUEBA_CAMPO.md`.
- `docs/evidencias/semana_08/capturas/INSTRUCCIONES_CAPTURAS.md`.
- `docs/evidencias/semana_08/capturas/01_catalogo_movil_semana08.png`.
- `docs/evidencias/semana_08/capturas/02_bloqueo_permisos_semana08.png`.
- `docs/evidencias/semana_08/capturas/03_camara_qr_semana08.png`.
- `docs/evidencias/semana_08/capturas/04_ciclo_prestamo_semana08.png`.
- `docs/evidencias/semana_08/capturas/05_reporte_movil_semana08.png`.

## Evidencias de QR/PDF y limpieza

- `QR_TEMP_SEMANA_08.png`.
- `ETIQUETAS_QA_SEMANA_08.pdf`.
- El conjunto Neon controlado fue usado para la prueba móvil y posteriormente eliminado por completo.
- INC-08-002 documenta y corrige el lector temporal residual detectado por la primera verificación 6/7; la repetición terminó 7/7.

## Criterios de aceptación revalidados automáticamente

CA-01 a CA-14 conservan cobertura en la suite acumulada. La prueba nueva refuerza CA-09 y CA-11 y elimina una inconsistencia de activación lógica observada durante QA. Las reglas RN-04, RN-05, RN-06, RN-07, RN-09, RN-12, RN-13, RN-14, RN-15 y RN-18 permanecen cubiertas por regresión e integridad.

## Acción manual pendiente

No queda una acción técnica obligatoria para Semana 8. La guía para una persona no técnica está lista; si posteriormente se coordina una sesión con la bibliotecaria, su resultado podrá añadirse como evidencia complementaria. En este cierre se registra expresamente que no participó.

## Condición de cierre

Se cumplen las once condiciones de cierre definidas para Semana 8: pruebas automáticas, matriz completa, incidencias resueltas, datos temporales limpios, Neon íntegro, Render Live, smoke correcto, seguridad verificada, prueba móvil validada, guía de campo preparada y evidencias completas. La semana queda completa para revisión y aprobación expresa del usuario. No iniciar Semana 9.
