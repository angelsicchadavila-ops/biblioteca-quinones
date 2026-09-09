# Evidencia de la Semana 1

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 01 — Análisis de Requerimientos y Diseño Arquitectónico.
- Fecha de cierre: 09 de septiembre de 2026.
- Documento oficial: [`Documento_Maestro_Biblioteca_v1.0.docx`](../../Documento_Maestro_Biblioteca_v1.0.docx).
- Estado: Completa, pendiente únicamente de revisión y aprobación del usuario antes de iniciar la Semana 2.

## Actividades realizadas

1. Se revisaron y validaron las reglas RN-01 a RN-18 sin modificar la especificación.
2. Se detallaron CU-01 a CU-10 con actor, precondición, flujo principal, alternativas, postcondición y trazabilidad.
3. Se consolidó la relación entre las 18 reglas, los 10 casos de uso y CA-01 a CA-14.
4. Se formalizaron los permisos de Público, `admin` y `asistente` por recurso, ruta y caso de uso.
5. Se contrastó el DER definitivo con las seis entidades, relaciones y restricciones del Documento Maestro.
6. Se prepararon y revisaron cuatro wireframes de baja fidelidad para catálogo/login, administración, préstamo y devolución/reportes.
7. Se comprobó que no se crearon archivos Flask, SQL, Neon o Render correspondientes a semanas posteriores.

## Entregables definitivos

- [`VALIDACION_REQUERIMIENTOS.md`](../../analisis/semana_01/VALIDACION_REQUERIMIENTOS.md): cierre de reglas, alcance y decisiones vigentes.
- [`CASOS_DE_USO.md`](../../analisis/semana_01/CASOS_DE_USO.md): especificación detallada de CU-01 a CU-10.
- [`MATRIZ_TRAZABILIDAD.md`](../../analisis/semana_01/MATRIZ_TRAZABILIDAD.md): cobertura RN–CU–CA.
- [`MATRIZ_PERMISOS.md`](../../analisis/semana_01/MATRIZ_PERMISOS.md): permisos por actor, recurso y caso de uso.
- [`DER_DEFINITIVO.md`](../../analisis/semana_01/DER_DEFINITIVO.md) y [`Modelo_Logico_Biblioteca_v1.0.png`](../../Modelo_Logico_Biblioteca_v1.0.png): definición y representación del modelo definitivo.
- [`WIREFRAMES_INICIALES.md`](../../analisis/semana_01/WIREFRAMES_INICIALES.md): índice, alcance y criterios de los wireframes.
- SVG editables en `docs/analisis/semana_01/wireframes/`.
- Capturas PNG verificadas en [`capturas/`](capturas/).

## Verificaciones ejecutadas

| Verificación | Resultado real |
|---|---|
| Apertura del DOCX con `python-docx` | Correcto: 242 párrafos y 32 tablas |
| Exportación del DOCX mediante Microsoft Word | Correcto: PDF de 16 páginas |
| Inspección visual del Documento Maestro | Correcto: 16 páginas legibles, sin cortes, solapes ni tablas truncadas |
| Inventario de identificadores del Documento Maestro | Correcto: 18 RN, 10 CU, 14 CA y 4 RPT, sin saltos |
| Apertura del DER | Correcto: PNG de 2581 × 1395 píxeles |
| Validación estructural de wireframes | Correcto: 4 archivos SVG con XML válido |
| Render de wireframes | Correcto: 4 PNG de 1440 × 900 píxeles |
| Inspección visual de wireframes | Correcto después de ajustar una colisión de texto en la tabla administrativa |
| Enlaces locales de los documentos de análisis | Correcto: sin referencias rotas |
| Control de alcance | Correcto: no existen `app.py`, `schema.sql`, `seed.sql` ni `requirements.txt` de semanas posteriores |
| Política de secretos | Correcto: `.env` ignorado y no versionado; `.env.example` contiene solo marcadores |
| Búsqueda de valores sensibles | Correcto: no se detectaron URL de conexión ni claves reales |
| `git diff --check` | Correcto: sin errores de espacios ni marcadores de conflicto |

## Evidencias visuales

- [`01_catalogo_login.png`](capturas/01_catalogo_login.png)
- [`02_panel_gestion.png`](capturas/02_panel_gestion.png)
- [`03_terminal_prestamo.png`](capturas/03_terminal_prestamo.png)
- [`04_devolucion_reportes.png`](capturas/04_devolucion_reportes.png)

## Criterios de aceptación relacionados

- CA-09 quedó completamente especificado a nivel de diseño mediante la matriz de permisos y la asignación de casos de uso.
- CA-01 a CA-14 quedaron cubiertos documentalmente en la matriz de trazabilidad y vinculados con sus reglas y casos de uso.
- Los estados de CA-05 y CA-07 se reflejaron en los wireframes sin crear campos redundantes.
- CA-10 se representó mediante la alternativa de ingreso manual en el terminal.
- CA-14 se representó con RPT-01 a RPT-04 y el filtro por fechas del historial.
- La validación funcional de CA-01 a CA-14 se realizará en las semanas donde se implemente cada módulo; la Semana 1 valida su definición, consistencia y cobertura.

## Control de cambios y alcance

No se modificaron reglas de negocio, arquitectura, tecnologías, roles, modelo de datos, alcance ni criterios de aceptación. Por ello, `docs/REGISTRO_CAMBIOS.md` permanece sin nuevas entradas. No se realizó ninguna actividad de la Semana 2.

## Commit y publicación

El cierre corresponde al commit con mensaje `docs: completar análisis y diseño de semana 1`. El identificador y el resultado del push quedan verificables en el historial Git del repositorio.

## Acción manual

El usuario debe revisar y aprobar la Semana 1 antes de autorizar la Semana 2. Como dato administrativo no bloqueante, el Documento Maestro mantiene `[Nombre del estudiante]` en el campo `Responsable` hasta que se proporcione el nombre definitivo.
