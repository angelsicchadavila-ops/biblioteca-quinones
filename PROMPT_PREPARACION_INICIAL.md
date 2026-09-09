# Prompt — Preparación Inicial del Proyecto

Pega este prompt en un chat nuevo de Codex después de abrir la carpeta raíz `biblioteca_quinones/`.

---

Realiza exclusivamente la **Preparación Inicial** del proyecto “Sistema Web de Gestión Bibliotecaria con Control QR”. Esta preparación no corresponde todavía a la Semana 1.

Antes de modificar cualquier archivo:

1. Lee `AGENTS.md` completo.
2. Revisa `docs/Documento_Maestro_Biblioteca_v1.0.docx`.
3. Lee `docs/ESTADO_PROYECTO.md`.
4. Lee `docs/REGISTRO_CAMBIOS.md`.
5. Inspecciona la estructura actual de la carpeta.
6. Comprueba si Git está instalado y revisa si esta carpeta ya es un repositorio Git.

Después realiza lo siguiente:

### A. Validación de estructura
- Verifica que existan las carpetas `docs/` y `docs/evidencias/semana_01` hasta `semana_09`.
- Verifica que estén presentes el Documento Maestro v1.0 y el modelo lógico.
- No crees todavía `app.py`, `templates/`, `static/`, `utils/` ni dependencias de la aplicación si no son necesarias para esta preparación; esas estructuras se crearán cuando corresponda al cronograma.

### B. Git local
- Si la carpeta aún no es un repositorio Git, inicialízala.
- Configura la rama principal como `main` si corresponde.
- Revisa `.gitignore` y asegúrate de que al menos ignore `.env`, entornos virtuales, cachés de Python, archivos temporales y secretos.
- No añadas credenciales reales a ningún archivo versionado.

### C. GitHub
- Comprueba si existe un remote `origin`.
- Si existe, valida su configuración sin modificarlo innecesariamente.
- Si no existe, comprueba si GitHub CLI (`gh`) está instalado y autenticado.
- Si `gh` está autenticado y puedes crear un repositorio remoto de forma segura, pregúntame antes de crear/publicar un repositorio nuevo.
- Si no hay autenticación o no puede hacerse automáticamente, indícame exactamente la única acción manual que debo realizar.
- No solicites ni muestres mi contraseña o token de GitHub.

### D. Estado y documentación
- Revisa si `docs/ESTADO_PROYECTO.md` refleja correctamente la situación real y actualízalo si es necesario.
- No modifiques el Documento Maestro salvo que detectes una contradicción real; si la detectas, solo repórtala y espera aprobación.

### E. Commit inicial
Cuando la estructura esté validada y no haya secretos expuestos:
- prepara un commit inicial descriptivo con la documentación y estructura base;
- antes de hacer `push`, verifica que el repositorio remoto y la autenticación sean correctos;
- si falta alguna acción manual mía, detente solo en ese punto y explícame exactamente qué debo hacer;
- no hagas `push` de forma insegura ni publiques secretos.

### F. Evidencia
Crea `docs/evidencias/semana_01/` únicamente como carpeta preparada; no registres todavía la Semana 1 como completada.

Para esta preparación, crea además `docs/EVIDENCIA_PREPARACION_INICIAL.md` con:
- estructura validada;
- estado de Git;
- estado del remote de GitHub;
- commit inicial si se realizó;
- acciones manuales pendientes;
- confirmación de que no se detectaron secretos versionados.

### Al finalizar
Dame un resumen breve y comprensible indicando:
- qué configuraste;
- qué archivos modificaste;
- estado de Git;
- estado de GitHub;
- commit creado, si corresponde;
- si hiciste `push` o por qué no;
- dónde quedó la evidencia;
- cuál es mi única siguiente acción manual, si existe;
- si el proyecto está listo para iniciar la Semana 1.

No inicies la Semana 1 hasta que yo la solicite explícitamente.
