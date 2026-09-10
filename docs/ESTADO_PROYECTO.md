# Estado del Proyecto — Biblioteca Quiñones

## Identificación
- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR
- Documento Maestro: v1.0
- Estado general: Semana 3 completada; pendiente de revisión del usuario
- Semana actual: Semana 3 — Flask, autenticación y deployment técnico temprano (completada)
- Última actualización: 10 de septiembre de 2026

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

## Pendientes abiertos
- No existen pendientes técnicos ni decisiones estructurales de la Semana 1.
- No existen pendientes técnicos ni decisiones estructurales de la Semana 2.
- La implementación, las pruebas locales y el deployment técnico en Render de la Semana 3 están completos.
- Render ejecutó correctamente `gunicorn app:app` y publicó `https://biblioteca-quinones.onrender.com` desde el commit `5096cf4`.
- Las pruebas remotas HTTPS de autenticación, sesiones y permisos finalizaron correctamente.
- El acceso desde un dispositivo móvil real fue validado y se guardó `06_render_https_movil.png`.
- El campo `Responsable` del Documento Maestro conserva el marcador `[Nombre del estudiante]`; es un dato administrativo no bloqueante que deberá completarse cuando el usuario proporcione el nombre.

## Fase actual

Semana 3 completada. Esperar la revisión y aprobación expresa del usuario antes de iniciar la Semana 4.

## Historial semanal
| Semana | Estado | Fecha | Evidencia principal | Commit |
|---|---|---|---|---|
| 01 | Completa | 09/09/2026 | `docs/evidencias/semana_01/SEMANA_01_EVIDENCIA.md` | `docs: completar análisis y diseño de semana 1` |
| 02 | Completa | 09/09/2026 | `docs/evidencias/semana_02/SEMANA_02_EVIDENCIA.md` | `db: completar base de datos de semana 2` |
| 03 | Completa | 10/09/2026 | `docs/evidencias/semana_03/SEMANA_03_EVIDENCIA.md` | `5096cf4` (implementación) + `docs: cerrar semana 3 y registrar deployment` |
| 04 | Pendiente | — | — | — |
| 05 | Pendiente | — | — | — |
| 06 | Pendiente | — | — | — |
| 07 | Pendiente | — | — | — |
| 08 | Pendiente | — | — | — |
| 09 | Pendiente | — | — | — |
