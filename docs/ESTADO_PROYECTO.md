# Estado del Proyecto — Biblioteca Quiñones

## Identificación
- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR
- Documento Maestro: v1.0
- Estado general: Preparación inicial completada localmente
- Semana actual: Aún no iniciada
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
Ninguna semana de desarrollo ha sido completada todavía.

## Próxima fase
### Semana 1 — Análisis de Requerimientos y Diseño Arquitectónico
Objetivos principales:
- revisar y validar reglas de negocio;
- elaborar casos de uso;
- consolidar criterios de aceptación;
- preparar DER definitivo;
- preparar wireframes iniciales;
- generar evidencias de análisis y diseño.

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
- No existen decisiones estructurales ni tareas de preparación abiertas que impidan iniciar la Semana 1 cuando sea solicitada.

## Historial semanal
| Semana | Estado | Fecha | Evidencia principal | Commit |
|---|---|---|---|---|
| 01 | Pendiente | — | — | — |
| 02 | Pendiente | — | — | — |
| 03 | Pendiente | — | — | — |
| 04 | Pendiente | — | — | — |
| 05 | Pendiente | — | — | — |
| 06 | Pendiente | — | — | — |
| 07 | Pendiente | — | — | — |
| 08 | Pendiente | — | — | — |
| 09 | Pendiente | — | — | — |
