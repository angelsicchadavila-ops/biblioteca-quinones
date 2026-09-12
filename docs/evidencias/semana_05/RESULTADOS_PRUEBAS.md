# Resultados de pruebas de QR PDF y escáner móvil

## Estado de la validación

- Fecha: 12 de septiembre de 2026.
- Resultado automatizado final: 30 de 30 pruebas correctas en 163,202 segundos.
- Estado: validación técnica local completa; quedan pendientes el deployment de esta versión y la prueba real de cámara y lectura QR desde un teléfono.
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
| 20 | Deployment de Semana 5 | Pendiente de push y verificación en Render |
| 21 | HTTPS de Semana 5 | Pendiente de verificar después del deployment |
| 22 | Cámara real desde teléfono | Pendiente de intervención del usuario |
| 23 | Lectura de QR real desde teléfono | Pendiente de intervención del usuario |

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

El permiso de cámara no se concedió en esta validación local porque la prueba obligatoria debe realizarse desde el teléfono sobre Render HTTPS.

## Neon y datos temporales

La suite automatizada crea datos con sufijos aleatorios y los elimina en `tearDownClass` o bloques `finally`.

Para la prueba móvil se conserva deliberadamente un conjunto controlado:

| Registro | Valor | Estado |
|---|---|---|
| Libro | ID 11, marcador `TEMP-SEMANA-05` | Temporal |
| Ejemplar | `LIB-011-EJ01` | Activo y Operativo |
| Ejemplar | `LIB-011-EJ02` | Activo y Dañado |
| Ejemplar | `LIB-011-EJ03` | Inactivo y Operativo |

La comprobación posterior confirmó exactamente 1 libro, 3 ejemplares, 0 lectores y 0 préstamos. El verificador histórico de Semana 2 informa 6/7 porque fue diseñado para una base sin catálogo; su único control no cumplido corresponde a estos datos temporales intencionales, no a residuos de la suite.

El conjunto temporal se eliminará después de completar y documentar la prueba móvil.

## Controles complementarios

- `compileall`: correcto.
- `pip check`: dependencias compatibles.
- `git diff --check`: correcto; solo avisos informativos de conversión LF/CRLF en Windows.
- Revisión de secretos: `.env` excluido; no se incorporaron credenciales, tokens, cadenas reales de PostgreSQL ni Deploy Hook.
