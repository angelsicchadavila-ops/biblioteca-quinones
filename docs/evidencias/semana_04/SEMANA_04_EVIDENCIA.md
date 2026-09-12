# Evidencia de la Semana 4

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 04 — Catálogo, materias y ejemplares.
- Fecha de cierre técnico: 12 de septiembre de 2026.
- Estado: Implementación, pruebas y deployment completados; capturas manuales pendientes de guardar.
- Documento oficial: `docs/Documento_Maestro_Biblioteca_v1.0.docx`.

## Resumen técnico

La Semana 4 incorpora el catálogo bibliográfico público y la administración de materias, libros y ejemplares físicos sobre las seis tablas PostgreSQL creadas en la Semana 2. No se modificó el esquema ni se agregaron estados redundantes.

La disponibilidad se deriva en cada consulta con esta prioridad:

1. Ejemplar inactivo: `Inactivo`.
2. Ejemplar activo con estado físico `Dañado`: `Dañado`.
3. Ejemplar activo y operativo con un préstamo sin devolución: `Prestado`.
4. Ejemplar activo y operativo sin préstamo activo: `Disponible`.

## Módulo de materias

- Listado de materias activas e inactivas con conteo de libros.
- Creación desde la propia interfaz administrativa.
- Edición del nombre.
- Normalización de espacios y validación de duplicados sin distinguir mayúsculas.
- Desactivación y reactivación lógica.
- Bloqueo de la desactivación cuando la materia conserva libros activos, para respetar RN-01.
- Rutas protegidas en backend para el rol `admin`.

## Módulo de libros

- Listado de libros activos e inactivos.
- Creación y edición de título, autor, materia, nivel académico e ISBN/editorial opcional.
- Niveles permitidos: `Primaria`, `Secundaria` y `Ambos`.
- Asignación exclusiva a materias activas.
- Desactivación y reactivación sin eliminación física.
- Resumen de inventario asociado con total, disponibles, prestados, dañados e inactivos.

## Módulo de ejemplares

- Creación de uno o varios ejemplares por título.
- Generación transaccional de códigos estables con el formato `LIB-XXX-EJYY`.
- Bloqueo de la fila del libro durante la numeración para evitar colisiones entre altas concurrentes.
- Listado individual con código, fecha, condición física y disponibilidad derivada.
- Cambio entre `Operativo` y `Dañado`.
- Desactivación y reactivación lógica.
- No se generaron imágenes QR ni PDF; esas actividades permanecen reservadas para la Semana 5.

## Catálogo público

- Ruta `/` accesible sin autenticación.
- Búsqueda parametrizada por título o autor.
- Escape de `%`, `_` y barra inversa para tratarlos como texto literal.
- Filtro por materia.
- Filtro por nivel; `Primaria` y `Secundaria` incluyen títulos clasificados como `Ambos`.
- Combinación simultánea de texto, materia y nivel.
- Exposición exclusiva de títulos activos asociados a materias activas.
- Conteos de inventario sin nombres de lectores, historial ni información interna del préstamo.
- Interfaz Bootstrap 5 revisada en escritorio; la captura móvil debe guardarse manualmente.

## Control de acceso

- Público: catálogo y login.
- `admin`: materias, libros, ejemplares, catálogo y rutas ya autorizadas.
- `asistente`: catálogo y terminal de escaneo; recibe HTTP 403 en rutas administrativas de catálogo, tanto GET como POST.
- Todas las operaciones de escritura conservan la validación CSRF de Semana 3.

## Pruebas y resultados

- Suite completa: 20 de 20 pruebas correctas en 111,707 segundos.
- Flujo compuesto de Semana 4: correcto; cubrió las 20 comprobaciones funcionales locales solicitadas para catálogo, inventario y permisos.
- Verificación de Neon posterior: 7 de 7 controles correctos.
- Limpieza posterior: no quedaron libros, ejemplares, lectores ni préstamos temporales.
- `compileall`: correcto.
- `pip check`: sin dependencias incompatibles.
- `git diff --check`: correcto.

El detalle está en `docs/evidencias/semana_04/RESULTADOS_PRUEBAS.md`.

## Deployment en Render

- Repositorio y rama: `angelsicchadavila-ops/biblioteca-quinones`, `main`.
- Commit de implementación: `a190a88` (`feat: implementar catalogo y ejemplares`).
- Auto-Deploy configurado: `On Commit`.
- Incidencia observada: el webhook no inició el deployment después del push.
- Acción aplicada: `Manual Deploy` → `Deploy latest commit`, sin cambiar configuración ni secretos.
- Resultado: `Deploy succeeded | Live`.
- Duración mostrada por Render: 39,7 segundos.
- Inicio de Gunicorn: correcto con `gunicorn app:app`.
- Health check `/`: HTTP 200.
- Verificación funcional HTTPS: HTTP 200 y título `Catálogo · Biblioteca Quiñones`.
- URL: https://biblioteca-quinones.onrender.com

## Criterios de aceptación comprobados

- CA-01: libro con materia y nivel; filtros individuales y combinados.
- CA-02: múltiples ejemplares y códigos únicos.
- CA-07: disponibilidad derivada para disponible, prestado, dañado e inactivo.
- CA-09: público sin autenticación, asistente bloqueado y administrador autorizado.
- CA-11: desactivación/reactivación sin borrado físico.

También se comprobaron RN-01, RN-02, RN-09, RN-10, RN-11, RN-13 y RN-16.

## Archivos principales

- `app.py`.
- `utils/catalogo.py`.
- `templates/index.html`.
- `templates/admin_dashboard.html`.
- `templates/materias.html` y `templates/materia_form.html`.
- `templates/libros.html` y `templates/libro_form.html`.
- `templates/ejemplares.html`.
- `static/css/style.css`.
- `tests/test_catalogo_semana4.py`.
- `README.md`.

## Evidencia visual pendiente

La interfaz pública y el estado `Live` de Render fueron inspeccionados visualmente durante la ejecución. La herramienta de navegador no puede guardar sus capturas directamente dentro del repositorio, por lo que las imágenes enumeradas en `capturas/INSTRUCCIONES_CAPTURAS.md` requieren intervención manual del usuario.

No se deben escribir credenciales antes de tomar las capturas ni incluir el archivo `.env`.

## Alcance y pendientes

- No se modificó el Documento Maestro ni `docs/REGISTRO_CAMBIOS.md` porque no hubo cambios estructurales.
- No se avanzó a QR, PDF, escaneo, préstamos/devoluciones completos ni reportes.
- Queda pendiente guardar las capturas manuales y revisar por qué el webhook de Render no inició el Auto-Deploy, aunque el servicio final está actualizado y operativo.
