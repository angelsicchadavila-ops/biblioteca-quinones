# Evidencia de Preparación Inicial

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR
- Fecha de verificación: 09 de septiembre de 2026
- Alcance: preparación inicial previa a la Semana 1
- Resultado: preparación inicial completada y publicada en GitHub

## Estructura validada

Se verificó la existencia de los siguientes elementos:

- `docs/`
- `docs/Documento_Maestro_Biblioteca_v1.0.docx`
- `docs/Modelo_Logico_Biblioteca_v1.0.png`
- `docs/ESTADO_PROYECTO.md`
- `docs/REGISTRO_CAMBIOS.md`
- `docs/evidencias/semana_01/` hasta `docs/evidencias/semana_09/`

Las carpetas de evidencia fueron normalizadas desde `semana_1` a `semana_9` al formato de dos dígitos definido por la documentación. Cada carpeta conserva su archivo `.gitkeep` y está preparada, sin registrar actividades semanales.

No se crearon `app.py`, `templates/`, `static/`, `utils/`, dependencias ni otros componentes de la aplicación. La Semana 1 permanece sin iniciar.

## Documento Maestro y modelo lógico

Se revisaron el Documento Maestro v1.0 y el modelo lógico. La estructura base, las decisiones técnicas y el estado del proyecto son coherentes con la preparación solicitada. No se detectó una contradicción que requiera modificar la especificación ni registrar un cambio en `REGISTRO_CAMBIOS.md`.

## Estado de Git

- Git disponible: sí
- Versión verificada: 2.54.0.windows.1
- Repositorio local: inicializado durante esta preparación
- Rama principal: `main`
- Identidad Git disponible en la configuración del usuario: sí
- Commit inicial local: `c643a90`
- Mensaje del commit: `chore: preparar estructura inicial del proyecto`

## Estado de GitHub

- Remote `origin`: `https://github.com/angelsicchadavila-ops/biblioteca-quinones.git`
- Remotes adicionales: ninguno
- GitHub CLI (`gh`): no instalado
- Autenticación de GitHub: completada mediante Git Credential Manager sin exponer credenciales
- Push inicial: realizado correctamente
- Rama publicada: `main`, configurada para seguir `origin/main`

Antes del primer push se verificó que no existiera un remote anterior, que no hubiera reglas globales de redirección de URL y que el repositorio remoto indicado estuviera accesible y vacío.

## Revisión de seguridad

Se revisó `.gitignore` y se confirmó que excluye:

- archivos `.env`, excepto `.env.example`;
- entornos virtuales;
- cachés y artefactos de Python;
- archivos temporales y logs;
- archivos comunes de secretos, credenciales y claves privadas.

La búsqueda de patrones sensibles no detectó credenciales reales en los archivos que se prepararon para versionar. La única coincidencia fue la cadena de ejemplo de `.env.example`, cuyos valores son marcadores no operativos.

## Acción manual pendiente

No queda ninguna acción manual pendiente para completar la preparación inicial.

## Confirmación final

El proyecto queda preparado localmente y publicado en GitHub para iniciar la Semana 1 cuando sea solicitada expresamente. Esta preparación no inició ninguna actividad semanal.
