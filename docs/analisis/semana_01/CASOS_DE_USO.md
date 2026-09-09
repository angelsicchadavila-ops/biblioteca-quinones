# Casos de uso de la versión 1.0

## Convenciones

- Los actores internos son `admin` y `asistente`.
- Las validaciones se ejecutan nuevamente en el backend antes de guardar.
- Los flujos alternativos no cambian el resultado esperado definido por el Documento Maestro.

## CU-01 Consultar catálogo

**Actor:** Público.

**Precondición:** Ninguna autenticación requerida.

**Flujo principal:**

1. El visitante abre el catálogo público.
2. Busca por título o autor y, si lo desea, filtra por nivel académico y materia.
3. El sistema muestra los títulos coincidentes y la cantidad disponible por título.

**Flujos alternativos:** Sin coincidencias, se muestra un resultado vacío sin error. Los filtros pueden utilizarse de forma individual o combinada.

**Postcondición:** No se modifica información y no se exponen lectores, historial ni datos internos.

**Trazabilidad:** RN-01, RN-09, RN-16; CA-01, CA-07.

## CU-02 Autenticarse

**Actores:** `admin`, `asistente`.

**Precondición:** El usuario interno existe y está activo.

**Flujo principal:**

1. El usuario abre `/login` e ingresa sus credenciales.
2. El backend verifica la contraseña almacenada como hash y el estado activo.
3. El sistema crea la sesión y habilita únicamente las funciones del rol.

**Flujos alternativos:** Credenciales inválidas o usuario inactivo producen un rechazo sin revelar información sensible.

**Postcondición:** Existe una sesión autenticada con permisos de `admin` o `asistente`.

**Trazabilidad:** CA-09; requisitos de seguridad 14.1.

## CU-03 Gestionar catálogo

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`; existe al menos una materia activa para registrar libros.

**Flujo principal:**

1. El administrador consulta los libros y ejemplares.
2. Crea o edita un libro con título, autor, nivel y materia.
3. Agrega uno o más ejemplares físicos con código QR único.
4. Puede desactivar o reactivar libros y ejemplares sin borrar historial.

**Flujos alternativos:** Se rechazan datos obligatorios ausentes, una materia no válida o un código QR duplicado. Un ejemplar dañado o inactivo queda no prestable.

**Postcondición:** El catálogo conserva la clasificación y la identidad individual de cada ejemplar.

**Trazabilidad:** RN-01, RN-02, RN-10, RN-11, RN-13; CA-01, CA-02, CA-07, CA-11.

## CU-04 Gestionar materias

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`.

**Flujo principal:**

1. El administrador consulta las materias.
2. Crea o edita una materia con nombre único.
3. Desactiva o reactiva una materia cuando corresponda.

**Flujos alternativos:** Se rechaza un nombre duplicado o vacío. Una materia con historial no se elimina físicamente desde la interfaz.

**Postcondición:** El catálogo dispone de una lista controlada de materias.

**Trazabilidad:** RN-01, RN-11; CA-01, CA-11.

## CU-05 Gestionar usuarios

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`.

**Flujo principal:**

1. El administrador consulta las cuentas internas.
2. Crea o edita nombre, usuario y rol `admin` o `asistente`.
3. Define una contraseña que se almacena únicamente como hash.
4. Desactiva o reactiva cuentas sin borrar su trazabilidad.

**Flujos alternativos:** Se rechazan nombres de usuario duplicados, roles no permitidos y datos obligatorios ausentes.

**Postcondición:** Las cuentas quedan disponibles conforme a su rol y estado activo.

**Trazabilidad:** RN-11, RN-12; CA-09, CA-11, CA-12; requisitos de seguridad 14.1.

## CU-06 Generar o reimprimir QR

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`; existe al menos un ejemplar.

**Flujo principal:**

1. El administrador selecciona uno o más ejemplares.
2. El sistema genera una imagen QR a partir de cada `codigo_qr`.
3. El administrador exporta las etiquetas en PDF A4.
4. Si una etiqueta se pierde, vuelve a imprimirla.

**Flujo alternativo:** Una reimpresión reutiliza el código existente y nunca crea una identidad distinta para el ejemplar.

**Postcondición:** Cada etiqueta representa de forma estable a un único ejemplar.

**Trazabilidad:** RN-02, RN-13; CA-02.

## CU-07 Registrar préstamo

**Actores:** `admin`, `asistente`.

**Precondición:** Sesión autenticada; el terminal recibe un código por cámara o ingreso manual.

**Flujo principal:**

1. El sistema consulta el ejemplar por `codigo_qr`.
2. Verifica que exista, esté activo, sea Operativo y no tenga préstamo activo.
3. El operador busca al lector sin distinguir mayúsculas/minúsculas ni espacios significativos.
4. Selecciona una coincidencia o crea un lector dentro del mismo flujo.
5. Registra nivel, grado/sección y un plazo de 7 días, 14 días o fecha personalizada válida.
6. El backend comprueba que el lector esté activo, no tenga mora y tenga menos de dos préstamos activos.
7. Se registra el préstamo y el usuario responsable dentro de una transacción.

**Flujos alternativos:** Código inexistente, ejemplar dañado/inactivo/prestado, lector inactivo, mora, dos préstamos activos o fecha inválida producen rechazo explicativo y no modifican la base. Ante dos solicitudes simultáneas, solo una puede confirmar el préstamo.

**Postcondición:** Existe un préstamo activo y el ejemplar se muestra Prestado.

**Trazabilidad:** RN-03 a RN-06, RN-08 a RN-10, RN-12, RN-14, RN-15, RN-18; CA-03 a CA-07, CA-10, CA-12, CA-13.

## CU-08 Registrar devolución

**Actores:** `admin`, `asistente`.

**Precondición:** Sesión autenticada; el código corresponde a un ejemplar con préstamo activo.

**Flujo principal:**

1. El terminal consulta el ejemplar por cámara o código manual.
2. El sistema muestra el préstamo activo.
3. El operador confirma la devolución.
4. El backend registra `fecha_devolucion` y `devuelto_por_usuario_id`.
5. Se recalculan la disponibilidad del ejemplar y la elegibilidad del lector.

**Flujos alternativos:** Si no existe un préstamo activo, no se registra devolución. Ante error de red, no se asume éxito y se permite verificar el estado antes de reintentar.

**Postcondición:** El préstamo queda Devuelto; el ejemplar aparece Disponible si continúa activo y Operativo.

**Trazabilidad:** RN-07, RN-09, RN-10, RN-12, RN-14, RN-18; CA-05, CA-07, CA-08, CA-10, CA-12.

## CU-09 Consultar préstamos

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`.

**Flujo principal:**

1. El administrador abre la consulta de préstamos.
2. Filtra o revisa préstamos activos, vencidos y devueltos.
3. El sistema calcula el estado en tiempo real con `fecha_limite`, `fecha_devolucion` y la fecha de `America/Lima`.

**Flujo alternativo:** Si no existen registros para el filtro, se muestra un resultado vacío sin modificar información.

**Postcondición:** El administrador obtiene una vista operativa sin crear estados redundantes.

**Trazabilidad:** RN-09, RN-12, RN-18; CA-05, CA-12.

## CU-10 Consultar reportes

**Actor:** `admin`.

**Precondición:** Sesión activa con rol `admin`.

**Flujo principal:**

1. El administrador selecciona Inventario, Préstamos activos, Préstamos vencidos o Historial.
2. Para Historial, define un rango de fechas válido.
3. El sistema muestra las columnas mínimas establecidas para RPT-01 a RPT-04.

**Flujos alternativos:** Un rango inválido se rechaza; un reporte sin registros muestra un resultado vacío.

**Postcondición:** Se presenta información tabular sin alterar datos.

**Trazabilidad:** RN-17, RN-18; CA-14.
