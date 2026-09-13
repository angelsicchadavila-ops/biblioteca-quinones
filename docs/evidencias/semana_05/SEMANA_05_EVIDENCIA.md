# Evidencia de la Semana 5

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 05 — QR, PDF y escáner móvil.
- Fecha de inicio: 12 de septiembre de 2026.
- Estado: completa y lista para revisión y aprobación expresa del usuario.
- Documento oficial: `docs/Documento_Maestro_Biblioteca_v1.0.docx`.

## Resumen técnico

La Semana 5 implementa el flujo técnico de identificación de ejemplares sin incorporar préstamos ni devoluciones:

```text
ejemplar existente → codigo_qr estable → QR → PDF A4 → cámara o código manual → ficha del ejemplar
```

No se modificaron el esquema PostgreSQL, las reglas de negocio, los roles ni la convención `LIB-XXX-EJYY`.

## Generación y reimpresión QR

- `utils/qr_generator.py` crea el QR en memoria con `qrcode` y `BytesIO`.
- El contenido se compara con el código recibido antes de producir la imagen.
- La ruta administrativa entrega el PNG del ejemplar existente.
- La reimpresión consulta el registro existente y no crea ejemplares ni modifica `codigo_qr`, condición física, activación o historial.
- El QR contiene únicamente el código alfanumérico del ejemplar.

## PDF de etiquetas

- `utils/pdf_exporter.py` usa ReportLab y tamaño A4.
- La cuadrícula tiene 3 columnas y 7 filas, con capacidad de 21 etiquetas por página.
- El QR se dibuja a 25 mm por 25 mm, sin deformación.
- Cada etiqueta incluye código y título con recorte controlado cuando el ancho no es suficiente.
- Las rutas administrativas permiten descargar una etiqueta individual o un PDF con varios ejemplares seleccionados.
- La evidencia `ETIQUETAS_QR_SEMANA_05.pdf` contiene tres etiquetas reales del conjunto controlado.

## Endpoint de identificación

`GET /api/ejemplar/<codigo_qr>` requiere una sesión válida de `admin` o `asistente`, normaliza el ingreso, valida la convención y devuelve una ficha JSON limitada. Diferencia:

- código válido y existente: HTTP 200;
- formato inválido: HTTP 400;
- sesión ausente: HTTP 401;
- código no registrado: HTTP 404.

El estado visible se deriva con prioridad para inactivo, dañado, prestado y disponible. No se exponen lectores, historial, claves internas ni secretos.

## Terminal móvil

- `/escaneo` sigue protegido para usuarios autenticados.
- La cámara se solicita únicamente al pulsar `Iniciar cámara`.
- `html5-qrcode` usa preferentemente `facingMode: environment`.
- Se puede detener y reiniciar la cámara.
- Los errores de permiso, cámara ausente, cámara ocupada y carga del lector muestran alternativas comprensibles.
- Una lectura se bloquea mientras la consulta está activa y el mismo código se ignora durante 3 segundos.
- El ingreso manual llama a la misma función y al mismo endpoint que la cámara.
- La interfaz fue revisada a 390 x 844 px sin desbordamiento horizontal.
- No existen botones ni endpoints de préstamo o devolución de Semana 6.

## Seguridad y permisos

- Administrador: terminal, QR individual, reimpresión y PDF múltiple.
- Asistente: terminal y API de identificación; HTTP 403 en rutas QR administrativas.
- Público: redirección al login en `/escaneo`, HTTP 401 JSON en la API y sin acceso a QR/PDF administrativos.
- Las operaciones administrativas conservan la validación CSRF donde corresponde.

## Pruebas

- Suite completa final: 30 de 30 pruebas correctas en 170,628 segundos, ejecutada después de limpiar los datos de prueba.
- Pruebas nuevas de Semana 5: 10 de 10 correctas.
- PDF: A4 confirmado con `pdfinfo` e inspección visual de la página renderizada.
- Responsive e ingreso manual: comprobados en navegador real local a 390 x 844 px.
- Neon: 7 de 7 verificaciones correctas y sin datos temporales residuales.

El detalle reproducible se encuentra en `RESULTADOS_PRUEBAS.md`.

## Evidencias disponibles

- `QR_LIB-011-EJ01.png`: QR real del ejemplar operativo temporal.
- `ETIQUETAS_QR_SEMANA_05.pdf`: PDF A4 real con los tres ejemplares temporales.
- `RESULTADOS_PRUEBAS.md`: resultados, contrato API y control de datos.
- `capturas/01_modulo_admin_qr.png`: módulo administrativo de QR y PDF.
- `capturas/02_pdf_etiquetas_a4.png`: PDF A4 abierto y legible.
- `capturas/03_terminal_escaneo_movil.png`: terminal responsive en teléfono.
- `capturas/04_ingreso_manual_correcto.png`: identificación manual correcta.
- `capturas/05_codigo_no_registrado.png`: manejo de código inexistente.
- `capturas/06_camara_activa_movil.png`: cámara real activa.
- `capturas/07_qr_leido_correctamente.png`: lectura real de `LIB-011-EJ01`.
- `capturas/08_render_deploy_semana05.png`: deployment `Live` del commit técnico.
- `capturas/INSTRUCCIONES_CAPTURAS.md`: procedimiento utilizado para obtener las evidencias.

Todas las capturas fueron revisadas individualmente y no exponen contraseñas, variables de entorno, tokens ni Deploy Hook.

## Deployment, prueba móvil y limpieza

- Commit técnico `1c2f46f` y push correcto a `origin/main`.
- Auto-Deploy comprobado en `On Commit` sin modificarlo; Render no reaccionó al push, por lo que se documentó la reincidencia.
- Contingencia `Deploy latest commit` ejecutada: `Deploy succeeded | Live` en 44,7 segundos.
- Aplicación verificada por HTTPS; el catálogo respondió y el acceso anónimo a `/escaneo` redirigió al login.
- Prueba móvil real completada en Render HTTPS: cámara iniciada por acción del usuario y lectura correcta de `LIB-011-EJ01`.
- Ingreso manual correcto y código inexistente documentados desde el teléfono.
- Ocho capturas obligatorias revisadas y almacenadas en `capturas/`.
- Conjunto `TEMP-SEMANA-05` eliminado de Neon después de conservar las evidencias.
- Verificación posterior: suite 30/30 y base de datos 7/7.

La Semana 5 está técnicamente completa. No se iniciará la Semana 6 hasta recibir la aprobación expresa del usuario.
