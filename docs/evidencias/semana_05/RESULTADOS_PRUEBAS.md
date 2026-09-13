# Resultados de pruebas de QR PDF y escáner móvil

## Estado de la validación

- Fecha: 12 de septiembre de 2026.
- Resultado automatizado final posterior a la limpieza: 30 de 30 pruebas correctas en 170,628 segundos.
- Estado: validación técnica, deployment HTTPS, prueba móvil real, evidencias visuales y limpieza de datos temporales completas.
- Base de datos: PostgreSQL en Neon, con conexión Psycopg 3 y zona horaria `America/Lima`.

## Suite automatizada

Comando ejecutado:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

La suite completa cubrió:

- 10 pruebas nuevas de Semana 5.
- 1 prueba integral de catálogo e inventario de Semana 4.
- 11 pruebas de autenticación y permisos de Semana 3.
- 8 pruebas estáticas de esquema y seguridad de Semana 2.

No quedaron fallos después de corregir una regresión de texto en el encabezado del terminal. La prueba puntual corregida y la suite completa posterior finalizaron correctamente.

## Casos de Semana 5

| N.º | Caso | Resultado |
|---:|---|---|
| 1 | Generar QR para ejemplar existente | Correcto; ruta administrativa devuelve PNG válido |
| 2 | Contenido QR igual a `codigo_qr` | Correcto; comparación exacta con `LIB-123-EJ45` y evidencia real `LIB-011-EJ01` |
| 3 | Reimprimir sin cambiar identificador | Correcto; dos descargas y código antes/después idéntico |
| 4 | PDF válido | Correcto; encabezado `%PDF-1.4` |
| 5 | PDF con múltiples etiquetas | Correcto; ruta con tres ejemplares y prueba directa con 22 etiquetas |
| 6 | Estructura A4 | Correcto; `595,276 x 841,890 pt`, una página en la evidencia |
| 7 | Legibilidad y proporción | Correcto; inspección visual sin deformación, solapamiento ni recorte |
| 8 | Endpoint con ejemplar válido | Correcto; HTTP 200 y contrato JSON mínimo |
| 9 | Código inexistente | Correcto; HTTP 404 y mensaje `Código no registrado.` |
| 10 | Ejemplar operativo | Correcto; estado visible `Disponible` |
| 11 | Ejemplar dañado | Correcto; identificado con estado `Dañado` |
| 12 | Ejemplar inactivo | Correcto; identificado con estado `Inactivo` |
| 13 | Ingreso manual correcto | Correcto; normaliza espacios y mayúsculas y usa el mismo endpoint |
| 14 | Ingreso manual inexistente | Correcto; mismo HTTP 404 y mensaje del escaneo |
| 15 | Acceso administrador | Correcto; genera QR y PDF individual/múltiple |
| 16 | Acceso asistente | Correcto; usa terminal y API; recibe HTTP 403 en generación administrativa |
| 17 | Público/no autenticado | Correcto; terminal redirige y API responde JSON HTTP 401 |
| 18 | Doble lectura rápida | Correcto; bloqueo de 3 segundos y exclusión mientras una consulta está en curso |
| 19 | Responsive | Correcto en vista local real de 390 x 844 px, sin desbordamiento horizontal |
| 20 | Deployment de Semana 5 | Correcto; commit `1c2f46f`, build correcto y estado `Live` en 44,7 s |
| 21 | HTTPS de Semana 5 | Correcto; catálogo HTTP 200 y `/escaneo` protegido redirige al login |
| 22 | Cámara real desde teléfono | Correcto; permiso concedido, cámara activa y visor visible sobre Render HTTPS |
| 23 | Lectura de QR real desde teléfono | Correcto; lectura de `LIB-011-EJ01` y mensaje de identificación correcta |

## Contrato del endpoint

Ruta interna:

```text
GET /api/ejemplar/<codigo_qr>
```

Respuesta correcta, HTTP 200:

```json
{
  "ok": true,
  "ejemplar": {
    "codigo_qr": "LIB-011-EJ01",
    "titulo": "Prueba controlada QR Semana 5",
    "autor": "Dato temporal de prueba",
    "materia": "Comunicación",
    "nivel": "Ambos",
    "estado_fisico": "Operativo",
    "activo": true,
    "libro_activo": true,
    "disponibilidad": "Disponible"
  }
}
```

Errores previstos:

- HTTP 400: `codigo_invalido`.
- HTTP 401: `autenticacion_requerida`.
- HTTP 404: `codigo_no_registrado` con el mensaje `Código no registrado.`.

La respuesta no incluye identificadores internos, lectores, préstamos, credenciales ni información sensible.

## PDF y QR

- Generación en memoria con `BytesIO`.
- QR con corrección de errores M, borde de cuatro módulos y forma cuadrada.
- ReportLab usa A4, 3 columnas y 7 filas: 21 etiquetas por página.
- Cada etiqueta contiene QR cuadrado de 25 mm, código alfanumérico y título abreviado si no cabe.
- `pdfinfo` confirmó una página A4, sin cifrado, formularios ni JavaScript embebido.
- La imagen renderizada a 180 DPI fue revisada visualmente; los tres QR, códigos y título son legibles.

## Verificación responsive e ingreso manual

La vista local autenticada se revisó en un navegador real con viewport temporal de 390 x 844 px. Se comprobó:

- controles grandes y apilados;
- cámara apagada al cargar;
- ingreso manual siempre disponible;
- normalización de `lib-011-ej01` a `LIB-011-EJ01`;
- ficha completa del ejemplar operativo;
- desaparición de la ficha y mensaje `Código no registrado.` ante `LIB-999999-EJ99`;
- ausencia de controles de préstamo o devolución.

La prueba posterior desde un teléfono sobre Render HTTPS confirmó que la cámara permanece apagada hasta pulsar `Iniciar cámara`, que el permiso activa el visor y que el QR real identifica `LIB-011-EJ01`. Las capturas 03, 06 y 07 documentan el flujo móvil; la captura 04 muestra la ficha devuelta para el mismo ejemplar.

## Neon y datos temporales

La suite automatizada crea datos con sufijos aleatorios y los elimina en `tearDownClass` o bloques `finally`.

Para la prueba móvil se creó deliberadamente el siguiente conjunto controlado:

| Registro | Valor | Estado |
|---|---|---|
| Libro | ID 11, marcador `TEMP-SEMANA-05` | Temporal |
| Ejemplar | `LIB-011-EJ01` | Activo y Operativo |
| Ejemplar | `LIB-011-EJ02` | Activo y Dañado |
| Ejemplar | `LIB-011-EJ03` | Inactivo y Operativo |

Antes de eliminarlo se confirmó exactamente 1 libro, 3 ejemplares, 0 lectores y 0 préstamos asociados. Finalizada la prueba móvil, se eliminaron el libro ID 11 y sus tres ejemplares mediante una transacción limitada al marcador `TEMP-SEMANA-05`.

La suite completa se ejecutó nuevamente después de la limpieza y finalizó 30/30. `scripts/verificar_bd.py` confirmó 7/7 controles y ausencia de datos temporales.

## Deployment y HTTPS

- Commit técnico: `1c2f46f` (`feat: implementar QR PDF y escaner movil semana 5`).
- Push: correcto a `origin/main`.
- Auto-Deploy: configurado en `On Commit`, verificado sin modificar la opción.
- Incidencia: Render no creó un deployment automático después del push, repitiendo el comportamiento observado en Semana 4.
- Contingencia aplicada: `Deploy latest commit`, sin revelar ni usar el Deploy Hook.
- Resultado: `Deploy succeeded | Live` en 44,7 segundos.
- Dependencias nuevas instaladas correctamente en Render: `qrcode 8.2`, `reportlab 4.5.1` y `Pillow 12.3.0`.
- URL verificada: `https://biblioteca-quinones.onrender.com/` respondió por HTTPS y mostró el catálogo temporal correcto.
- Protección verificada: el acceso anónimo a `/escaneo` redirigió a `/login`.

## Revisión de evidencias visuales

Las ocho capturas fueron abiertas y revisadas individualmente. No muestran contraseñas, variables privadas, `DATABASE_URL`, `SECRET_KEY`, tokens ni Deploy Hook.

| Archivo | Evidencia verificada |
|---|---|
| `01_modulo_admin_qr.png` | Administración de ejemplares, selección múltiple, Ver QR y Reimprimir PDF |
| `02_pdf_etiquetas_a4.png` | PDF A4 con tres QR cuadrados, códigos y título legibles |
| `03_terminal_escaneo_movil.png` | Terminal responsive con cámara inicialmente apagada e ingreso manual disponible |
| `04_ingreso_manual_correcto.png` | Código `LIB-011-EJ01`, ficha correcta y estado Disponible |
| `05_codigo_no_registrado.png` | Mensaje `Código no registrado.` sin operación adicional |
| `06_camara_activa_movil.png` | Cámara real activa después de la acción y permiso del usuario |
| `07_qr_leido_correctamente.png` | Lectura real y confirmación de `LIB-011-EJ01` |
| `08_render_deploy_semana05.png` | Commit `1c2f46f` con `Deploy succeeded | Live` |

## Controles complementarios

- `compileall`: correcto.
- `pip check`: dependencias compatibles.
- `git diff --check`: correcto; solo avisos informativos de conversión LF/CRLF en Windows.
- Revisión de secretos: `.env` excluido; no se incorporaron credenciales, tokens, cadenas reales de PostgreSQL ni Deploy Hook.
- Verificación final de Neon: 7/7 controles correctos y ningún dato temporal residual.
