# Biblioteca Quiñones — Guía de Inicio con Codex

## Objetivo
Esta carpeta está preparada para iniciar el proyecto de Prácticas Pre-Profesionales II de forma ordenada, con continuidad entre chats y evidencias por semana.

## Paso 1 — Coloca la carpeta en tu laptop
Puedes usar directamente la carpeta `biblioteca_quinones/` incluida en este paquete.

Ubicación sugerida:
- Windows: `C:\Proyectos\biblioteca_quinones\`
- O cualquier carpeta personal de proyectos que prefieras.

Evita carpetas sincronizadas o temporales si no son necesarias.

## Paso 2 — Abre la carpeta en Codex
Abre Codex y selecciona la carpeta raíz `biblioteca_quinones/`.

Concede acceso únicamente a la carpeta del proyecto y a las operaciones que sean necesarias.

## Paso 3 — No empieces Semana 1 todavía
Primero abre un chat llamado, por ejemplo:

`00 - Preparación Inicial`

Pega el contenido de `PROMPT_PREPARACION_INICIAL.md`.

Ese chat verificará:
- estructura;
- Git local;
- `.gitignore`;
- GitHub/remote;
- commit inicial;
- estado del proyecto.

## Paso 4 — GitHub
Recomendación:
- usa una cuenta/repositorio bajo tu control;
- autentícate con GitHub mediante el navegador, GitHub CLI o el gestor de credenciales;
- no entregues contraseñas ni tokens dentro del chat.

El flujo será:

`Laptop/Codex -> Git local -> GitHub -> Render`

## Paso 5 — Chats por semana
Usa un chat separado por semana:

- `00 - Preparación Inicial`
- `01 - Semana 1 - Análisis y diseño`
- `02 - Semana 2 - Base de datos`
- `03 - Semana 3 - Flask, autenticación y deployment técnico`
- `04 - Semana 4 - Catálogo y búsqueda`
- `05 - Semana 5 - QR, PDF y escáner`
- `06 - Semana 6 - Préstamos, devoluciones, mora y reportes`
- `07 - Semana 7 - Deployment de producción`
- `08 - Semana 8 - QA y pruebas de campo`
- `09 - Semana 9 - Manuales y cierre`

Para cada chat utiliza `PROMPT_SEMANA_BASE.md` cambiando el número de semana.

## Paso 6 — Neon (Semana 2)
No necesitas instalar PostgreSQL en tu laptop.

En Semana 2 tú realizarás normalmente esta parte manual:
1. Crear tu cuenta/proyecto en Neon.
2. Obtener la cadena de conexión.
3. Guardarla localmente como `DATABASE_URL` en `.env`.

Nunca publiques el contenido de `.env` en GitHub.

Codex podrá usar esa conexión para crear/probar las tablas mediante Psycopg 3 y scripts SQL.

## Paso 7 — Render (Semana 3 y 7)
Render se conectará al repositorio GitHub.

Cuando el servicio esté configurado, un flujo habitual será:

`Codex modifica -> pruebas -> commit -> push -> GitHub -> Render despliega`

Las variables privadas (`DATABASE_URL`, `SECRET_KEY`) se configurarán en Render y no se incluirán en Git.

## Paso 8 — Evidencias
Cada semana debe terminar con evidencia real en:

`docs/evidencias/semana_XX/`

La evidencia debe incluir, cuando aplique:
- resumen Markdown;
- capturas;
- pruebas;
- scripts;
- PDF generado;
- commit;
- URL del deployment;
- incidencias y correcciones.

## Regla principal
El Documento Maestro v1.0 es la fuente oficial de verdad; los chats ayudan a ejecutar el proyecto, pero el estado real debe quedar reflejado en archivos y en Git.
