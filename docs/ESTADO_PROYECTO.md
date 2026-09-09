# Estado del Proyecto — Biblioteca Quiñones

## Identificación
- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR
- Documento Maestro: v1.0
- Estado general: Semana 1 completada
- Semana actual: Semana 1 — Análisis de Requerimientos y Diseño Arquitectónico
- Última actualización: 09 de septiembre de 2026

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

## Próxima fase
Revisión y aprobación del usuario. No iniciar la Semana 2 hasta recibir aprobación expresa.

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
- Queda pendiente la revisión y aprobación del usuario antes de iniciar la Semana 2.
- El campo `Responsable` del Documento Maestro conserva el marcador `[Nombre del estudiante]`; es un dato administrativo no bloqueante que deberá completarse cuando el usuario proporcione el nombre.

## Historial semanal
| Semana | Estado | Fecha | Evidencia principal | Commit |
|---|---|---|---|---|
| 01 | Completa | 09/09/2026 | `docs/evidencias/semana_01/SEMANA_01_EVIDENCIA.md` | `docs: completar análisis y diseño de semana 1` |
| 02 | Pendiente | — | — | — |
| 03 | Pendiente | — | — | — |
| 04 | Pendiente | — | — | — |
| 05 | Pendiente | — | — | — |
| 06 | Pendiente | — | — | — |
| 07 | Pendiente | — | — | — |
| 08 | Pendiente | — | — | — |
| 09 | Pendiente | — | — | — |
