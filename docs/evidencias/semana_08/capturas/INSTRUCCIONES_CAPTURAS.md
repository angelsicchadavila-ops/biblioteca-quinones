# Instrucciones de validación móvil y capturas Semana 8

## Objetivo

Completar la parte de QA que requiere un teléfono real sobre Render HTTPS. Se solicitan solo cinco evidencias representativas. No incluyas contraseñas, cookies, tokens, variables privadas, datos de alumnos reales ni la pantalla de inicio con la clave escrita.

## Datos que debes comunicar antes de empezar

Indica al responsable del QA:

- modelo del teléfono;
- versión de Android o iOS si la conoces;
- navegador utilizado;
- si la prueba será solo del responsable o también participará la bibliotecaria.

## Preparación

1. Usa la URL `https://biblioteca-quinones.onrender.com/`.
2. Abre el archivo `docs/evidencias/semana_08/QR_TEMP_SEMANA_08.png` en otra pantalla o imprime el PDF `ETIQUETAS_QA_SEMANA_08.pdf`.
3. Usa una cuenta de prueba recibida por un canal privado.
4. Usa nombres temporales; no escribas el nombre de un alumno real.
5. Si Render demora por arranque en frío, espera hasta 90 segundos antes de repetir una vez.

Datos temporales preparados en Neon:

- `LIB-044-EJ01`: operativo, activo y disponible; úsalo para el ciclo principal.
- `LIB-044-EJ02`: operativo, activo y disponible; reserva para una prueba adicional.
- `LIB-044-EJ03`: dañado; debe identificarse y bloquear el préstamo.
- `LIB-044-EJ04`: inactivo; debe identificarse y bloquear el préstamo.
- lector nuevo sugerido: nombres `Lector TEMP`, apellidos `SEMANA 08`.

## Secuencia exacta de prueba

### A Catálogo y login

1. Abre el catálogo sin sesión.
2. Confirma visualmente que no haya desplazamiento horizontal.
3. Busca el libro `TEMP-SEMANA-08` y prueba los filtros indicados por el responsable.
4. Abre Iniciar sesión e ingresa con una cuenta de prueba sin capturar la contraseña.
5. Comprueba que textos, campos y botones se vean completos.

### B Cámara

1. Abre Escaneo.
2. Comprueba que la cámara esté apagada al cargar.
3. Pulsa Iniciar cámara.
4. Acepta el permiso de cámara para este sitio.
5. Confirma que aparezca el visor.
6. Pulsa Detener cámara y verifica que el visor se detenga.
7. Pulsa Iniciar cámara y verifica que se pueda reiniciar.
8. Lee el QR temporal con iluminación normal.
9. Repite la lectura con menor iluminación, sin poner en riesgo el dispositivo.
10. Confirma que el código mostrado coincida exactamente con la etiqueta.

### C Código y estados

1. Escribe manualmente el mismo código en minúsculas y con espacios exteriores.
2. Confirma que el sistema lo normalice e identifique el mismo ejemplar.
3. Prueba `LIB-999999-EJ99` y confirma Código no registrado.
4. Si el responsable proporciona códigos dañados o inactivos, comprueba que se identifiquen y no permitan prestar.
5. Presenta dos veces rápidamente el mismo QR y confirma que no se duplique la operación ni aparezcan dos fichas simultáneas.

### D Préstamo y devolución

1. Con el ejemplar disponible, busca el lector temporal.
2. Si no existe, pulsa Crear lector nuevo y usa `Lector TEMP` y `SEMANA 08`.
3. Registra un préstamo de 7 días.
4. Confirma que el mensaje de éxito, el formulario y los botones sean legibles.
5. Vuelve a leer el código y confirma que aparezca el préstamo activo.
6. Registra la devolución.
7. Confirma que el ejemplar vuelva a Disponible.
8. No repitas Confirmar si hay demora; primero vuelve a consultar el estado.

## Cinco capturas solicitadas

Guarda las imágenes en `docs/evidencias/semana_08/capturas/` con estos nombres:

1. `01_catalogo_movil_semana08.png`: catálogo y controles visibles sin desbordamiento.
2. `02_bloqueo_permisos_semana08.png`: asistente bloqueado al abrir directamente una ruta `/admin`.
3. `03_camara_qr_semana08.png`: cámara activa o QR temporal identificado; no debe aparecer la contraseña.
4. `04_ciclo_prestamo_semana08.png`: mensaje de préstamo o devolución correctamente confirmado.
5. `05_reporte_movil_semana08.png`: un reporte básico legible; puede mostrar desplazamiento dentro de la tabla, pero no de toda la página.

Si se ve la barra de dirección, confirma que muestre el dominio correcto y HTTPS. Recorta solo lo necesario para no exponer notificaciones personales del teléfono.

## Respuesta que debe enviar el responsable

Después de realizar la prueba, responde con este formato:

```text
Teléfono y navegador:
Catálogo móvil: APROBADO o FALLIDO — detalle
Login móvil: APROBADO o FALLIDO — detalle
Cámara iniciar detener reiniciar: APROBADO o FALLIDO — detalle
QR válido e iluminación baja: APROBADO o FALLIDO — detalle
Código inexistente y manual: APROBADO o FALLIDO — detalle
Préstamo y devolución: APROBADO o FALLIDO — detalle
Mensajes botones formularios: APROBADO o FALLIDO — detalle
Sin desbordamiento horizontal: APROBADO o FALLIDO — detalle
Participó bibliotecaria: SÍ o NO
Archivos adjuntos: lista de nombres
```

Si un paso falla, no intentes corregir datos manualmente en Neon. Detén esa parte, conserva el mensaje exacto y comunícalo para reproducirlo de forma segura.
