# Evidencia técnica de la Semana 6

## Estado

Implementación técnica y pruebas automáticas completas. Pendientes: deployment del commit de Semana 6, ciclo real desde teléfono, capturas obligatorias y limpieza del conjunto temporal que se prepare para esa validación.

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

La suite completa terminó con **34/34 pruebas correctas**. La prueba concurrente confirmó que dos solicitudes simultáneas sobre un ejemplar producen un préstamo creado y un rechazo explicativo. Neon terminó con **7/7 verificaciones correctas** y sin datos temporales de la suite.

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

CA-03, CA-04, CA-05, CA-06, CA-07, CA-08, CA-09, CA-10, CA-12, CA-13 y CA-14 quedaron cubiertos automáticamente. CA-08, CA-10 y la operación móvil requieren además la validación física final solicitada.

## Pendientes antes del cierre

1. Publicar el commit técnico en `origin/main`.
2. Verificar Auto-Deploy de Render y aplicar `Deploy latest commit` si vuelve a fallar.
3. Completar el ciclo real desde teléfono por HTTPS.
4. Guardar capturas y video reales según las instrucciones.
5. Eliminar los datos temporales manuales después de conservar la evidencia.
6. Actualizar este documento y `docs/ESTADO_PROYECTO.md` con el resultado final.
