# Estado del Proyecto — Biblioteca Quiñones

## Identificación
- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR
- Documento Maestro: v1.0
- Estado general: Semana 6 aprobada; Semana 7 completa en implementación, pruebas y evidencias, pendiente aprobación expresa
- Semana actual: Semana 7 — producción y endurecimiento; no iniciar Semana 8 sin aprobación
- Última actualización: 15 de septiembre de 2026

## Fuente de verdad
- `docs/Documento_Maestro_Biblioteca_v1.0.docx`
- `AGENTS.md`

## Preparación completada
- Documento Maestro v1.0 creado.
- Modelo lógico v1.0 creado.
- Estructura inicial de evidencias validada con carpetas `semana_01` a `semana_09`.
- Reglas persistentes para Codex definidas en `AGENTS.md`.
- Git 2.54.0 instalado y repositorio local inicializado en la rama `main`.
- `.gitignore` revisado para excluir variables de entorno, secretos, entornos virtuales, cachés y temporales.
- Commit inicial local creado para la documentación y la estructura base.
- Evidencia de preparación inicial registrada.
- Remote `origin` configurado con `https://github.com/angelsicchadavila-ops/biblioteca-quinones.git`.
- Rama `main` publicada en GitHub y configurada para seguir `origin/main`.

## Preparación pendiente
- Ninguna acción pendiente para la preparación inicial.

## Última fase completada
### Semana 1 — Análisis de Requerimientos y Diseño Arquitectónico
- Reglas de negocio RN-01 a RN-18 revisadas y validadas sin cambios estructurales.
- Casos de uso CU-01 a CU-10 detallados con flujos, alternativas y trazabilidad.
- Criterios CA-01 a CA-14 consolidados en la matriz de trazabilidad.
- Matriz de permisos para Público, `admin` y `asistente` completada.
- DER definitivo contrastado con el capítulo 8 y el Anexo A del Documento Maestro.
- Cuatro wireframes iniciales completados y verificados visualmente.
- Evidencia de cierre guardada en `docs/evidencias/semana_01/SEMANA_01_EVIDENCIA.md`.

## Semana 2 completada
### Base de datos PostgreSQL en Neon
- Esquema relacional de las seis entidades preparado en `sql/schema.sql`.
- Restricciones, índices y triggers de integridad preparados conforme al DER definitivo.
- Seeder de materias y creación segura de cuentas de prueba preparados.
- Scripts Psycopg 3 de inicialización, verificación e integridad preparados.
- Ocho pruebas estáticas ejecutadas correctamente.
- Entorno virtual local preparado con Psycopg 3, python-dotenv y Werkzeug.
- Proyecto Neon configurado y esquema inicializado en la rama `production`.
- Verificación final del esquema: 7 de 7 comprobaciones correctas.
- Pruebas reales de integridad: 11 de 11 casos correctos, incluida concurrencia con dos conexiones.
- Captura de la vista `Tables` incorporada y verificada sin credenciales visibles.
- Evidencias técnicas completadas en `docs/evidencias/semana_02/`.

## Decisiones vigentes
- Backend: Python + Flask.
- Base de datos: PostgreSQL en Neon.
- Conexión: Psycopg 3.
- Frontend: HTML5 + CSS + Bootstrap 5 + JavaScript.
- Escáner QR: html5-qrcode.
- Generador QR: qrcode.
- PDF: ReportLab.
- Hosting: Render + Gunicorn.
- Repositorio: GitHub.
- Roles: `admin` y `asistente`.
- No existe carga anual obligatoria de alumnos; los lectores se crean dentro del flujo operativo.
- El grado/sección se registra por préstamo.
- La mora se calcula a partir de `fecha_limite` y `fecha_devolucion`.
- La disponibilidad se deriva del préstamo activo y del estado físico/activo del ejemplar.
- Se preserva historial mediante desactivación en lugar de borrado físico desde la interfaz.

## Semana 4 completada

### Catálogo, materias y ejemplares

- Gestión administrativa de materias con normalización, validación, edición y activación lógica.
- Gestión administrativa de libros con autor, materia, nivel e ISBN/editorial opcional.
- Gestión individual y por lotes de ejemplares físicos.
- Códigos automáticos y estables con formato `LIB-XXX-EJYY`.
- Disponibilidad derivada sin agregar campos al esquema.
- Catálogo público con búsqueda por título/autor y filtros combinables por materia y nivel.
- Inventario diferenciado en disponibles, prestados, dañados e inactivos.
- Rutas administrativas protegidas para `admin`; el `asistente` recibe HTTP 403.
- Suite completa: 20 de 20 pruebas correctas.
- Neon verificado: 7 de 7 controles y sin datos temporales residuales.
- Deployment del commit `a190a88` completado en Render con estado `Deploy succeeded | Live`.
- URL pública verificada por HTTPS con HTTP 200.
- Evidencias técnicas guardadas en `docs/evidencias/semana_04/`.
- Seis capturas obligatorias guardadas con los nombres previstos, revisadas visualmente y sin secretos visibles.

## Semana 5 completada

### QR PDF y escáner móvil

- Generación QR en memoria con `qrcode`, contenido idéntico al código estable del ejemplar y sin archivos temporales de servidor.
- Reimpresión administrativa individual sin crear registros ni modificar `codigo_qr`, estado físico o historial.
- PDF ReportLab en A4 con cuadrícula de 3 x 7 y capacidad de 21 etiquetas por página.
- Selección administrativa de uno o varios ejemplares para generar PDF.
- Endpoint autenticado `GET /api/ejemplar/<codigo_qr>` con respuestas JSON 200, 400, 401 y 404.
- Terminal `/escaneo` con `html5-qrcode`, cámara trasera preferida, inicio bajo acción del usuario, detención/reinicio, ingreso manual y bloqueo de doble lectura.
- Ficha de identificación para estados Disponible, Prestado, Dañado e Inactivo, sin acciones de Semana 6.
- Suite completa final: 30 de 30 pruebas correctas en 170,628 segundos después de la limpieza.
- PDF real generado y verificado como A4; interfaz comprobada a 390 x 844 px.
- Prueba real desde teléfono completada sobre Render HTTPS con cámara activa y lectura correcta de `LIB-011-EJ01`.
- Ingreso manual correcto y código inexistente comprobados en móvil.
- Ocho capturas obligatorias revisadas individualmente y guardadas en `docs/evidencias/semana_05/capturas/` sin secretos visibles.
- Conjunto temporal `TEMP-SEMANA-05` eliminado; Neon volvió a 7 de 7 verificaciones correctas.
- Commit técnico `1c2f46f` publicado correctamente en `origin/main`.
- Render no reaccionó al push pese a conservar Auto-Deploy en `On Commit`; la contingencia `Deploy latest commit` dejó `1c2f46f` en estado `Live`.
- Aplicación verificada por HTTPS; catálogo operativo y terminal protegido frente a acceso anónimo.
- Evidencias técnicas disponibles en `docs/evidencias/semana_05/`.

## Pendientes abiertos
- No existen pendientes técnicos ni decisiones estructurales de la Semana 1.
- No existen pendientes técnicos ni decisiones estructurales de la Semana 2.
- La implementación, las pruebas locales y el deployment técnico en Render de la Semana 3 están completos.
- La implementación, las pruebas, las evidencias y el deployment de la Semana 4 están completos.
- No existen pendientes bloqueantes dentro del alcance de la Semana 4.
- Observación no bloqueante: el Auto-Deploy de Render está configurado como `On Commit`, pero el webhook no reaccionó al push de Semana 4; el deployment se completó correctamente mediante `Deploy latest commit`.
- No existen pendientes técnicos ni documentales dentro del alcance de la Semana 5.
- La Semana 5 fue aprobada expresamente al solicitar el inicio oficial de la Semana 6.
- Semana 6 completa y aprobada expresamente el 15/09/2026: 34/34 pruebas automáticas, ciclo móvil real y 13 capturas aceptadas, conjunto TEMP-SEMANA-06 eliminado, Neon 7/7 y Render HTTP 200 por HTTPS.
- Observación menor no bloqueante: algunas capturas recortan información o no muestran un filtro aplicado; el responsable verificó esas funciones en la interfaz completa y aceptó las evidencias. El video comienza con la sesión ya iniciada para evitar exponer credenciales.
- Semana 7 completa en verificación técnica y documental, con cuatro capturas revisadas; pendiente únicamente de aprobación expresa del usuario. No se identificó un pendiente técnico bloqueante. Auto-Deploy sigue en `On Commit` y `Deploy latest commit` funciona como contingencia.
- El campo `Responsable` del Documento Maestro conserva el marcador `[Nombre del estudiante]`; es un dato administrativo no bloqueante que deberá completarse cuando el usuario proporcione el nombre.

## Fase actual

Semana 7 completa en implementación, verificaciones y evidencias, pendiente aprobación expresa del usuario. Render dejó `a0b935c` Live mediante `Deploy latest commit` después de otro fallo de detección de Auto-Deploy; Build, Gunicorn, HTTPS y variables privadas fueron comprobados. Neon terminó 7/7, la suite 34/34, integridad 11/11 y el humo final HTTPS 32/32. Redeploy y reinicio conservaron la huella de los datos existentes. Las cuatro capturas de producción se revisaron individualmente y sus límites de encuadre se documentaron sin presentarlos como prueba de información no visible. No queda pendiente técnico identificado de Semana 7. Auto-Deploy se mantiene como observación no bloqueante con contingencia manual validada. No iniciar la Semana 8 sin nueva autorización.

## Historial semanal
| Semana | Estado | Fecha | Evidencia principal | Commit |
|---|---|---|---|---|
| 01 | Completa | 09/09/2026 | `docs/evidencias/semana_01/SEMANA_01_EVIDENCIA.md` | `docs: completar análisis y diseño de semana 1` |
| 02 | Completa | 09/09/2026 | `docs/evidencias/semana_02/SEMANA_02_EVIDENCIA.md` | `db: completar base de datos de semana 2` |
| 03 | Completa | 10/09/2026 | `docs/evidencias/semana_03/SEMANA_03_EVIDENCIA.md` | `5096cf4` (implementación) + `docs: cerrar semana 3 y registrar deployment` |
| 04 | Completa; pendiente de aprobación del usuario | 12/09/2026 | `docs/evidencias/semana_04/SEMANA_04_EVIDENCIA.md` | `a190a88` + `c30945d` + cierre visual |
| 05 | Completa; aprobada al iniciar Semana 6 | 14/09/2026 | `docs/evidencias/semana_05/SEMANA_05_EVIDENCIA.md` | `1c2f46f` + `798b45c` + `e0f83ff` |
| 06 | Completa y aprobada; observaciones visuales menores | 15/09/2026 | `docs/evidencias/semana_06/SEMANA_06_EVIDENCIA.md` | `861a89a` + `7db4cd7` + `ecfd370` + cierre documental y visual |
| 07 | Completa; pendiente aprobación expresa | 15/09/2026 | `docs/evidencias/semana_07/SEMANA_07_EVIDENCIA.md` | `0ae60c9` + `a0b935c` + cierre visual/documental |
| 08 | Pendiente | — | — | — |
| 09 | Pendiente | — | — | — |
