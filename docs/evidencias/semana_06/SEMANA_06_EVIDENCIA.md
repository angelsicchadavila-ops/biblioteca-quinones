# Evidencia técnica de la Semana 6

## Estado

Semana 6 completa y aprobada expresamente por el responsable del proyecto el 15 de septiembre de 2026, con observaciones menores de encuadre visual. Implementación, pruebas, ciclo móvil, evidencias, limpieza temporal y deployment verificados. No se avanzó a la Semana 7.

## Funcionalidad implementada

- Búsqueda tolerante de lectores por nombres y apellidos, con referencia del último grado/sección y resumen de préstamos activos o vencidos.
- Creación de lector dentro del flujo de préstamo, almacenando únicamente nombres, apellidos, activación y fecha de registro.
- Salvaguarda contra duplicados evidentes por coincidencia normalizada de nombres y apellidos.
- Préstamos con plazos de 7 días, 14 días o fecha personalizada no anterior al día de préstamo.
- Bloqueo claro por mora, por máximo de dos préstamos, por ejemplar prestado, dañado o inactivo.
- Devolución desde la misma ficha del terminal, con fecha/hora y usuario responsable.
- Estado dinámico `Activo`, `Vencido` o `Devuelto`, sin agregar columnas redundantes.
- Semáforo verde, amarillo y rojo en el listado administrativo.
- Listado de préstamos con lector, libro, ejemplar, fechas y ambos usuarios responsables.
- Reportes RPT-01 Inventario, RPT-02 Préstamos activos, RPT-03 Préstamos vencidos y RPT-04 Historial por rango.
- Rutas de operación disponibles para `admin` y `asistente`; listados y reportes exclusivos de `admin`.

## Integración con Semana 5

El escaneo y el ingreso manual conservan una única función JavaScript `procesarCodigo` y consultan el mismo endpoint `GET /api/ejemplar/<codigo_qr>`. El endpoint ahora indica una de tres acciones: préstamo, devolución o bloqueo, y solo expone la ficha privada del préstamo a una sesión autenticada.

## Transacciones y fuente de verdad

`utils/prestamos.py` ejecuta préstamo y devolución dentro de transacciones. El préstamo bloquea primero al lector y luego al ejemplar, igual que el trigger de Semana 2. La disponibilidad sigue derivándose de activación, estado físico y existencia de un préstamo sin devolución. No se agregó un campo `Prestado` ni un campo `Vencido`.

## Pruebas

La suite completa terminó con **34/34 pruebas correctas**. La prueba concurrente confirmó que dos solicitudes simultáneas sobre un ejemplar producen un préstamo creado y un rechazo explicativo. Tras la limpieza manual, Neon terminó con **7/7 verificaciones correctas** y sin datos TEMP-SEMANA-06.

Detalle: `RESULTADOS_PRUEBAS.md`.

## Archivos principales

- `utils/prestamos.py`
- `utils/escaneo.py`
- `app.py`
- `templates/scanner.html`
- `static/js/qr_scanner.js`
- `templates/prestamos.html`
- `templates/reportes.html`
- `templates/admin_dashboard.html`
- `static/css/style.css`
- `tests/test_prestamos_semana6.py`

## Criterios de aceptación verificados

CA-03, CA-04, CA-05, CA-06, CA-07, CA-08, CA-09, CA-10, CA-12, CA-13 y CA-14 quedaron cubiertos automáticamente. El responsable confirmó además la validación física del ciclo móvil y de las funciones mostradas en las capturas.

## Evidencia móvil y visual aceptada

- `capturas/CICLO_MOVIL_SEMANA_06.mp4`: grabación real desde teléfono, de aproximadamente 1 min 56 s, que muestra identificación manual del ejemplar temporal, creación de lector, préstamo de 7 días, nueva identificación, devolución y disponibilidad final. La grabación comienza con sesión ya iniciada para no exponer credenciales; la autenticación y permisos estaban comprobados en semanas anteriores y en las pruebas automáticas de esta semana.
- `capturas/01_lector_nuevo_en_flujo.png` a `capturas/13_render_deploy_semana06.png`: trece PNG reales, revisados por existencia, nombres, apertura, legibilidad y privacidad. No se observaron credenciales, secretos ni datos personales reales. Cubren lector nuevo y existente, préstamo, límite de dos, mora, devolución vencida, semáforo, RPT-01 a RPT-04, trazabilidad y deployment.
- Observación visual: 01 no encuadra simultáneamente la disponibilidad del ejemplar; 03 muestra el mensaje de éxito pero no la ficha posterior; 09 y 10 recortan parte de la columna del lector; 11 no muestra un rango aplicado y recorta columnas; 12 deja fuera del encuadre las columnas de usuarios responsables. Estas limitaciones **no se presentan como prueba visual de los datos omitidos**. El responsable del proyecto verificó personalmente en la interfaz completa la disponibilidad, creación de lector, préstamo y devolución, columnas y datos de RPT-02/RPT-03, funcionamiento y filtro de RPT-04, y las columnas `Registró`/`Devolvió`; aceptó expresamente las evidencias sin repetir pruebas solo por encuadre. La suite automática respalda esos comportamientos.
- `capturas/13_render_deploy_semana06.png` muestra el deployment manual del commit documental `ecfd370` con estado `Deploy succeeded | Live`.

## Limpieza controlada y verificación final

El 15 de septiembre de 2026 se identificó el conjunto aislado TEMP-SEMANA-06 y se eliminó en una única transacción: 7 préstamos (IDs 56-62), 3 lectores (44-46), 7 ejemplares (95-101), 1 libro (24) y 1 materia (36). Antes de borrar se verificó que ninguno de los lectores tuviera préstamos sobre otros ejemplares y que la materia no contuviera otros libros. No se modificaron usuarios, materias iniciales, datos reales ni el esquema. Después, `scripts/verificar_bd.py` dio **7/7**; las tablas quedaron con 2 usuarios y 5 materias iniciales, 0 registros TEMP-SEMANA-06, 0 préstamos activos duplicados y 0 lectores sobre el límite. Las capturas y el video se conservaron.

El catálogo público de `https://biblioteca-quinones.onrender.com/` respondió por HTTPS con HTTP 200 después de la limpieza. No queda pendiente técnico real de la Semana 6.

## Git y deployment

- Commit técnico: `861a89a`.
- Commit de evidencia automática: `7db4cd7`.
- Commit documental del deployment manual: `ecfd370`.
- Push a `origin/main`: correcto.
- Auto-Deploy: no reaccionó al push, por tercera semana consecutiva.
- Contingencia: `Deploy latest commit` ejecutada sin cambiar configuración.
- Resultado posterior: `ecfd370` en estado `Deploy succeeded | Live`, según la captura 13; aplicación HTTPS operativa al cierre.
