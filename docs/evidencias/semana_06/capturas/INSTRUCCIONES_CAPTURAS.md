# Instrucciones de capturas y prueba móvil de la Semana 6

Guarda todos los archivos en `docs/evidencias/semana_06/capturas/`. Usa únicamente lectores y libros identificados como `TEMP-SEMANA-06`. No muestres contraseñas, correos, tokens, variables de entorno, barras de notificaciones, nombres reales de alumnos ni datos personales.

## Ciclo móvil obligatorio

Graba `CICLO_MOVIL_SEMANA_06.mp4` desde un teléfono real en `https://biblioteca-quinones.onrender.com`.

Debe verse, en este orden:

1. Inicio de sesión con la contraseña fuera del encuadre o pausando la grabación durante su escritura.
2. Apertura del terminal de escaneo.
3. Escaneo o ingreso manual del ejemplar temporal indicado al preparar la prueba.
4. Creación de un lector `PRUEBA MOVIL SEMANA 6` dentro del flujo.
5. Registro de préstamo con plazo de 7 días.
6. Nueva identificación del mismo ejemplar, mostrando lector, préstamo, límite y estado.
7. Confirmación de devolución.
8. Ficha final del ejemplar nuevamente disponible.

## Capturas exactas

### 01 Lector nuevo

- Archivo: `01_lector_nuevo_en_flujo.png`
- Pantalla: terminal con el formulario “Crear lector nuevo” visible.
- Debe aparecer: ejemplar temporal disponible, nombres y apellidos ficticios, nivel, grado/sección y plazo.

### 02 Búsqueda de lector existente

- Archivo: `02_busqueda_lector_existente.png`
- Pantalla: resultados de búsqueda dentro del terminal.
- Debe aparecer: el lector temporal, último nivel/grado y cantidad de préstamos activos o vencidos.

### 03 Préstamo registrado

- Archivo: `03_prestamo_registrado_movil.png`
- Pantalla: resultado posterior al préstamo desde teléfono.
- Debe aparecer: mensaje “Préstamo registrado correctamente”, ejemplar y opción de devolución.

### 04 Límite de dos préstamos

- Archivo: `04_bloqueo_tercer_prestamo.png`
- Pantalla: intento del tercer préstamo para el mismo lector.
- Debe aparecer: mensaje que indique que ya tiene dos préstamos activos.

### 05 Bloqueo por mora

- Archivo: `05_bloqueo_por_mora.png`
- Pantalla: intento de préstamo al lector temporal con vencimiento preparado.
- Debe aparecer: mensaje que exige devolver el préstamo vencido.

### 06 Devolución vencida

- Archivo: `06_devolucion_vencida.png`
- Pantalla: ficha de devolución del ejemplar vencido.
- Debe aparecer: lector ficticio, fecha límite, estado rojo y días de atraso.

### 07 Semáforo

- Archivo: `07_semaforo_listado_prestamos.png`
- Pantalla: `/admin/prestamos`.
- Debe aparecer: al menos una fila amarilla activa, una roja vencida y una verde devuelta.

### 08 a 11 Reportes

- `08_rpt01_inventario.png`: RPT-01 con título, materia, total, disponibles, prestados y dañados.
- `09_rpt02_activos.png`: RPT-02 con lector, libro, ejemplar y fechas.
- `10_rpt03_vencidos.png`: RPT-03 con grado/sección y días de atraso.
- `11_rpt04_historial.png`: RPT-04 con un rango aplicado, devolución, estado y responsables.

### 12 Trazabilidad

- Archivo: `12_trazabilidad_prestamo_devolucion.png`
- Pantalla: `/admin/prestamos?estado=devueltos`.
- Debe aparecer: columnas “Registró” y “Devolvió” para el registro temporal.

### 13 Deployment

- Archivo: `13_render_deploy_semana06.png`
- Pantalla: detalle del deployment de Render.
- Debe aparecer: commit técnico de Semana 6, estado `Live` o `Deploy succeeded` y fecha/hora.
- Evita mostrar: Deploy Hook, variables privadas, logs con URLs de base de datos o datos de la cuenta.

## Después de capturar

Informa que el ciclo móvil terminó y conserva los archivos con los nombres exactos. No elimines manualmente registros en Neon; la limpieza controlada se realizará después de revisar las evidencias.
