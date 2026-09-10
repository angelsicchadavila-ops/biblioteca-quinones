# Evidencia de la Semana 2

## Identificación

- Proyecto: Sistema Web de Gestión Bibliotecaria con Control QR.
- Semana: 02 — Base de datos PostgreSQL en Neon.
- Fecha de inicio: 09 de septiembre de 2026.
- Estado: Completa; pendiente de revisión y aprobación del usuario antes de iniciar la Semana 3.

## Fuente de verdad revisada

- `AGENTS.md`.
- `docs/Documento_Maestro_Biblioteca_v1.0.docx`.
- `docs/ESTADO_PROYECTO.md`.
- `docs/analisis/semana_01/DER_DEFINITIVO.md`.
- `docs/analisis/semana_01/VALIDACION_REQUERIMIENTOS.md`.
- `docs/analisis/semana_01/MATRIZ_TRAZABILIDAD.md`.

La Semana 1 figura como completa y el usuario autorizó expresamente el inicio oficial de la Semana 2.

## Entregables preparados

- `sql/schema.sql`: seis tablas del DER, claves, restricciones, índices y protección de préstamos activos.
- `sql/seed.sql`: materias iniciales de referencia sin credenciales.
- `scripts/inicializar_bd.py`: creación transaccional del esquema y cuentas de prueba con hashes.
- `scripts/verificar_bd.py`: inventario verificable de tablas, restricciones, índices, trigger y seed.
- `scripts/probar_integridad_bd.py`: pruebas reales con reversión total de los datos temporales.
- `tests/test_schema_estatico.py`: comprobaciones locales de alcance, restricciones y secretos.
- `.env.example` y `requirements.txt`: configuración segura y dependencias de Semana 2.

## Restricciones respaldadas

- Roles limitados a `admin` y `asistente`.
- Niveles de libro limitados a `Primaria`, `Secundaria` y `Ambos`.
- Nivel del alumno limitado a `Primaria` o `Secundaria`.
- Estado físico limitado a `Operativo` o `Dañado`.
- Unicidad de usuario, materia y código QR.
- Claves foráneas con borrado restringido para preservar historial.
- Coherencia entre fecha de préstamo, fecha límite, devolución y usuario responsable.
- Máximo de dos préstamos activos por lector.
- Bloqueo de nuevos préstamos por mora.
- Bloqueo de lectores inactivos y ejemplares inactivos o dañados.
- Un único préstamo activo por ejemplar mediante índice único parcial.
- Disponibilidad derivada: no existe un campo redundante de estado Prestado en `ejemplares`.

## Pruebas ejecutadas

| Prueba | Resultado real |
|---|---|
| Pruebas estáticas con `unittest` | Correcto: 8 de 8 pruebas superadas |
| Compilación de scripts con `compileall` | Correcto: sin errores de sintaxis |
| Importación de dependencias | Correcto: Psycopg 3.3.5, python-dotenv y Werkzeug disponibles en `.venv` |
| `git diff --check` | Correcto: sin errores de espacios ni marcadores de conflicto |
| Manejo de configuración ausente | Correcto: `verificar_bd.py` se detuvo con un mensaje seguro al no existir `DATABASE_URL` |
| Inicialización real en Neon | Correcto: 6 tablas, 5 materias y 2 cuentas de prueba |
| Verificación final del esquema | Correcto: 7 de 7 comprobaciones |
| Pruebas reales de integridad | Correcto: 11 de 11 casos, incluida concurrencia real |
| Limpieza de datos temporales | Correcto: 0 libros, ejemplares, lectores y préstamos de prueba restantes |

El detalle reproducible está registrado en `docs/evidencias/semana_02/RESULTADOS_PRUEBAS.md` y `docs/evidencias/semana_02/ESQUEMA_IMPLEMENTADO.md`.

## Evidencia visual

La captura [`capturas/01_tablas_neon.png`](capturas/01_tablas_neon.png) muestra la rama `production`, la base `neondb`, el esquema `public` y las tablas `ejemplares`, `lectores`, `libros`, `materias`, `prestamos` y `usuarios`. Fue inspeccionada visualmente y no contiene cadenas de conexión ni contraseñas.

## Seguridad

El repositorio no contiene una cadena de conexión real ni contraseñas. `.env` está ignorado y las cuentas de prueba reciben sus contraseñas exclusivamente desde variables locales, almacenándose solo el hash en PostgreSQL.

## Criterios y reglas respaldados

- RN-01 y CA-01: todo libro exige nivel válido y materia activa.
- RN-02, RN-13 y CA-02: cada ejemplar posee un código QR único.
- RN-04 y CA-03: nivel y grado/sección pertenecen al préstamo, no al lector.
- RN-05 y CA-04: se aceptan hasta dos préstamos activos y se rechaza el tercero.
- RN-06, RN-07, RN-18 y CA-05: la mora se calcula por fecha y bloquea nuevos préstamos.
- RN-09, RN-10 y CA-07: disponibilidad derivada y bloqueo de ejemplares dañados o inactivos.
- RN-11 y CA-11: claves foráneas restringen el borrado de registros con historial.
- RN-12 y CA-12: préstamo y devolución conservan usuarios responsables y fechas coherentes.
- RN-15 y CA-13: dos solicitudes simultáneas no pueden confirmar dos préstamos activos del mismo ejemplar.

## Commit y publicación

El cierre se prepara con el mensaje `db: completar base de datos de semana 2`. El resultado definitivo del push se comprobará en Git antes de entregar el resumen al usuario.

## Acción manual realizada

El usuario creó el proyecto Neon, guardó las variables privadas en `.env` y proporcionó la captura de la vista `Tables` sin exponer credenciales en el repositorio.
