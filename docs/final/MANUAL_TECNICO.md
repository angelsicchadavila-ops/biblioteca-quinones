# Manual técnico del Sistema Web de Gestión Bibliotecaria con Control QR

## Propósito

Este documento permite comprender, desplegar y mantener la versión 1.0 del sistema de la Biblioteca Quiñones. Describe la solución existente; no sustituye las políticas internas de seguridad de la institución ni contiene secretos.

Datos de referencia:

- Producción: <https://biblioteca-quinones.onrender.com/>
- Repositorio: <https://github.com/angelsicchadavila-ops/biblioteca-quinones>
- Rama de producción: `main`
- Zona horaria de negocio: `America/Lima`
- Responsable técnico: **[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]**

## Arquitectura general

La solución sigue una arquitectura web sencilla de tres partes:

1. El navegador de PC o móvil carga HTML, CSS, Bootstrap y JavaScript por HTTPS.
2. Render ejecuta la aplicación Flask mediante Gunicorn y valida sesión, rol, formularios y reglas de negocio.
3. Flask se conecta mediante Psycopg 3 a PostgreSQL alojado en Neon.

GitHub conserva el código fuente y es la fuente del despliegue de Render. La aplicación y la base de datos están separadas. El navegador nunca recibe la cadena de conexión ni las credenciales de Neon.

```text
Navegador HTTPS
      |
      v
Render: Gunicorn -> Flask
      |
      v
Psycopg 3 -> Neon PostgreSQL

GitHub main -> Render deployment
```

## Tecnologías utilizadas

| Componente | Tecnología | Uso |
|---|---|---|
| Backend | Python 3 y Flask 3 | Rutas, sesión, permisos, validación y plantillas. |
| Producción | Gunicorn 23 | Servidor WSGI en Render. |
| Base de datos | PostgreSQL en Neon | Persistencia relacional, restricciones, índices y triggers. |
| Conector | Psycopg 3 | SQL parametrizado y transacciones. |
| Frontend | HTML5, CSS, Bootstrap 5 y JavaScript | Interfaz responsive para PC y móvil. |
| Escaneo | html5-qrcode 2.3.8 | Lectura por cámara desde el navegador. |
| QR | qrcode y Pillow | PNG en memoria a partir del código estable. |
| PDF | ReportLab | Etiquetas QR en A4, 21 por página. |
| Seguridad de contraseñas | Werkzeug | `generate_password_hash` y `check_password_hash`. |
| Hosting | Render | Servicio web HTTPS. |
| Control de versiones | Git y GitHub | Historial, revisión y fuente de despliegue. |

Las versiones permitidas se encuentran en `requirements.txt`. Antes de actualizar una dependencia, ejecute la suite y revise compatibilidad.

## Estructura del repositorio

```text
biblioteca_quinones/
|-- app.py                     # Fábrica Flask, rutas, sesión, roles y errores
|-- render.yaml                # Configuración declarativa de Render
|-- requirements.txt           # Dependencias Python
|-- .env.example               # Nombres y marcadores, nunca secretos
|-- sql/
|   |-- schema.sql             # Tablas, constraints, índices y triggers
|   `-- seed.sql               # Materias iniciales, sin contraseñas
|-- scripts/
|   |-- inicializar_bd.py      # Inicialización segura de una BD vacía
|   |-- verificar_bd.py        # Verificación de esquema y estado base
|   |-- probar_integridad_bd.py# Pruebas transaccionales y concurrencia
|   |-- verificar_produccion.py# Smoke HTTPS de solo lectura
|   `-- datos_qa_semana8.py    # Utilidad controlada de QA histórico
|-- utils/
|   |-- db.py                  # Ciclo de conexión Psycopg en Flask
|   |-- catalogo.py            # Consultas y códigos de ejemplares
|   |-- escaneo.py             # Normalización e identificación por código
|   |-- prestamos.py           # Reglas, transacciones y reportes
|   |-- qr_generator.py        # QR PNG en memoria
|   `-- pdf_exporter.py        # PDF A4 de etiquetas
|-- templates/                 # Plantillas Jinja2
|-- static/
|   |-- css/style.css
|   `-- js/qr_scanner.js
|-- tests/                     # Pruebas acumuladas de Semanas 2 a 8
`-- docs/                      # Especificación, estado, manuales y evidencias
```

## Configuración de Flask

`crear_app()` en `app.py` implementa el patrón de fábrica. La aplicación:

- carga `.env` solo cuando existe en el entorno local;
- exige `DATABASE_URL` y `SECRET_KEY`;
- usa cookies de sesión `HttpOnly`, `SameSite=Lax` y `Secure` en Render;
- vuelve a consultar el usuario en cada solicitud y descarta sesiones de cuentas inactivas;
- exige token CSRF en todas las solicitudes `POST`;
- protege rutas mediante `login_requerido`, `rol_requerido` y `api_login_requerido`;
- usa consultas SQL parametrizadas;
- presenta páginas genéricas para 403, 404 y errores de base de datos.

## Variables de entorno

| Variable | Obligatoria | Propósito |
|---|---|---|
| `DATABASE_URL` | Sí | Cadena privada de conexión a Neon con SSL. |
| `SECRET_KEY` | Sí | Firma de la sesión Flask. Debe ser larga, aleatoria y privada. |
| `SESSION_COOKIE_SECURE` | Producción | Debe ser `true` para enviar la cookie solo por HTTPS. |
| `SEED_ADMIN_PASSWORD` | Inicialización/pruebas | Contraseña temporal usada para generar el hash de la cuenta admin de prueba. |
| `SEED_ASISTENTE_PASSWORD` | Inicialización/pruebas | Contraseña temporal usada para generar el hash de la cuenta asistente de prueba. |

No registre valores reales en Git, documentación, capturas, incidencias ni logs compartidos. `.env` está ignorado; `.env.example` contiene únicamente marcadores.

## Base de datos PostgreSQL en Neon

### Tablas principales

| Tabla | Responsabilidad |
|---|---|
| `usuarios` | Cuenta interna, hash, nombre, rol, activación y fecha de registro. |
| `materias` | Clasificación controlada de libros. |
| `libros` | Título, autor, materia, nivel, dato bibliográfico opcional y activación. |
| `ejemplares` | Copia física, `codigo_qr`, condición física y activación. |
| `lectores` | Identidad persistente simplificada y activación. |
| `prestamos` | Lector, ejemplar, datos académicos por operación, fechas y usuarios responsables. |

### Relaciones

- `materias` 1:N `libros`.
- `libros` 1:N `ejemplares`.
- `lectores` 1:N `prestamos`.
- `ejemplares` 1:N `prestamos` históricos, con máximo uno activo.
- `usuarios` 1:N préstamos registrados y 1:N devoluciones confirmadas.

Las claves foráneas usan `ON DELETE RESTRICT`. La aplicación desactiva registros con historial en lugar de eliminarlos desde la interfaz.

### Restricciones importantes

- `username`, nombre de materia y `codigo_qr` son únicos.
- Roles permitidos: `admin`, `asistente`.
- Nivel de libro: `Primaria`, `Secundaria`, `Ambos`.
- Nivel del alumno: `Primaria`, `Secundaria`.
- Estado físico: `Operativo`, `Dañado`.
- La fecha límite no puede ser anterior al préstamo.
- Una devolución requiere fecha y usuario responsable.
- El índice parcial `uq_prestamos_ejemplar_activo` impide dos préstamos sin devolución para un mismo ejemplar.
- Existen índices para búsqueda de libros, relaciones, activos, mora, historial y usuarios responsables.

### Triggers

`trg_validar_materia_activa_libro` ejecuta `fn_validar_materia_activa_libro` y rechaza altas o reclasificaciones hacia una materia inexistente o inactiva.

`trg_validar_prestamo_activo` ejecuta `fn_validar_prestamo_activo`. Bloquea y valida lector y ejemplar, confirma que el usuario esté activo, rechaza ejemplares dañados/inactivos, lectores con mora y lectores con dos préstamos activos. El orden de bloqueos ayuda a serializar solicitudes simultáneas.

## Reglas de negocio críticas

- Máximo dos préstamos activos por lector.
- Mora si `fecha_devolucion IS NULL` y `fecha_limite` es anterior a la fecha actual en Lima.
- Desbloqueo al devolver todos los vencidos, sujeto al límite de dos.
- La disponibilidad no se almacena: se deriva de activación, condición física y préstamo activo.
- `Vencido` no se almacena: se calcula a partir de las fechas.
- El nivel y grado/sección del alumno pertenecen al préstamo, no al lector.
- QR único y estable por ejemplar; reimprimir no cambia el código.
- Cámara e ingreso manual utilizan la misma API y reglas.
- Préstamo y devolución se ejecutan en transacciones.
- Cada operación registra al usuario responsable.
- Fechas y comparaciones de negocio usan `America/Lima`.

## Rutas principales

| Método y ruta | Acceso | Función |
|---|---|---|
| `GET /` | Público | Catálogo, búsqueda y filtros. |
| `GET/POST /login` | Público | Autenticación. |
| `POST /logout` | Autenticado | Cierre de sesión. |
| `GET /admin` | Admin | Resumen administrativo. |
| `GET/POST /admin/materias` | Admin | Listado y alta de materias. |
| `GET/POST /admin/materias/<id>/editar` | Admin | Edición de materia. |
| `POST /admin/materias/<id>/estado` | Admin | Activación lógica. |
| `GET /admin/libros` | Admin | Listado de libros. |
| `GET/POST /admin/libros/nuevo` | Admin | Alta de libro. |
| `GET/POST /admin/libros/<id>/editar` | Admin | Edición de libro. |
| `POST /admin/libros/<id>/estado` | Admin | Activación lógica. |
| `GET/POST /admin/libros/<id>/ejemplares` | Admin | Inventario y altas por lote. |
| `POST /admin/ejemplares/<id>/estado-fisico` | Admin | Operativo/dañado. |
| `POST /admin/ejemplares/<id>/estado` | Admin | Activación lógica. |
| `GET /admin/ejemplares/<id>/qr.png` | Admin | QR individual. |
| `GET /admin/ejemplares/<id>/etiqueta.pdf` | Admin | PDF individual. |
| `POST /admin/etiquetas-qr.pdf` | Admin | PDF de varios ejemplares. |
| `GET /escaneo` | Admin/asistente | Terminal QR y manual. |
| `GET /api/ejemplar/<codigo>` | Admin/asistente | Identificación y acción disponible. |
| `GET /api/lectores` | Admin/asistente | Búsqueda de lectores. |
| `POST /api/prestamos` | Admin/asistente | Registro transaccional. |
| `POST /api/devoluciones` | Admin/asistente | Devolución transaccional. |
| `GET /admin/prestamos` | Admin | Listado y semáforo. |
| `GET /admin/reportes` | Admin | RPT-01 a RPT-04. |

## Roles, permisos y provisión de cuentas

`admin` accede a gestión completa, QR, terminal, préstamos y reportes. `asistente` accede al terminal y a las APIs operativas; las rutas administrativas responden 403. El público solo accede a catálogo y login.

La versión desplegada mantiene cuentas en la tabla `usuarios`, pero no incluye una pantalla de autogestión de usuarios. Para la entrega institucional, un responsable técnico autorizado debe sustituir o desactivar las cuentas de prueba y crear o actualizar cuentas definitivas mediante una operación controlada en PostgreSQL:

1. acordar nombre de usuario, nombre visible y rol;
2. generar el hash con `werkzeug.security.generate_password_hash` fuera de la documentación;
3. insertar o actualizar mediante consulta parametrizada dentro de una transacción;
4. verificar inicio de sesión y permisos;
5. entregar la contraseña solo por canal privado;
6. desactivar las cuentas de prueba cuando ya no sean necesarias.

Nunca inserte una contraseña en texto plano. Si no existe una persona técnica autorizada, complete esta tarea con el responsable original antes de la entrega formal.

## Generación QR y PDF

`utils/qr_generator.py` normaliza el código y genera PNG en memoria. El contenido codificado es exactamente `codigo_qr`; no contiene URL, contraseña ni datos personales.

`utils/pdf_exporter.py` utiliza ReportLab y tamaño A4. Distribuye 3 columnas por 7 filas, es decir, 21 etiquetas por página. Cada etiqueta incluye título, código legible y QR. Los endpoints devuelven archivos en memoria, sin temporales persistentes del servidor.

## Escáner con html5-qrcode

`templates/scanner.html` carga html5-qrcode y `static/js/qr_scanner.js` coordina la cámara y el ingreso manual. El usuario inicia la cámara explícitamente. Se solicita preferentemente `facingMode: environment`, se controlan errores de permiso o ausencia de cámara y se ofrece siempre el código manual.

La función de frontend que procesa el código consulta `/api/ejemplar/<codigo>`. El backend decide si corresponde préstamo, devolución o bloqueo. Existe una ventana de bloqueo de lectura para evitar dobles solicitudes rápidas.

## Reportes

- RPT-01: inventario por título y materia.
- RPT-02: préstamos activos sin devolver.
- RPT-03: vencidos y días de atraso.
- RPT-04: historial por rango con estado y trazabilidad.

Son consultas tabulares. No generan gráficos ni exportaciones adicionales en la versión 1.0.

## Ejecución local

Ejemplo en PowerShell, después de crear un `.env` privado:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

La aplicación escucha normalmente en `http://127.0.0.1:5000`. En local puede usarse `SESSION_COOKIE_SECURE=false`; en producción debe ser `true`.

## Inicialización y verificación de base de datos

`scripts/inicializar_bd.py` solo funciona en una base sin tablas del proyecto. Se detiene sin sobrescribir si detecta tablas existentes. Ejecuta `schema.sql`, `seed.sql` y crea dos cuentas iniciales con hashes obtenidos de variables privadas.

Comandos de mantenimiento habituales:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_bd.py
.\.venv\Scripts\python.exe scripts\probar_integridad_bd.py
```

La segunda prueba crea datos aislados, prueba restricciones y concurrencia, y los revierte o elimina. No debe ejecutarse durante una ventana de mantenimiento sensible sin respaldo y supervisión.

## Deployment en Render

Configuración esperada:

- repositorio GitHub: `angelsicchadavila-ops/biblioteca-quinones`;
- rama: `main`;
- build: `pip install -r requirements.txt`;
- start: `gunicorn app:app`;
- health check: `/`;
- variables privadas: `DATABASE_URL`, `SECRET_KEY`, `SESSION_COOKIE_SECURE=true`.

`render.yaml` contiene esta definición sin valores secretos. Render proporciona HTTPS. El plan gratuito puede suspender la instancia y provocar un *cold start*.

En las Semanas 4 a 8, Auto-Deploy figuró como `On Commit`, pero no reaccionó de forma consistente. El procedimiento probado de contingencia es **Manual Deploy > Deploy latest commit**. No use Deploy Hook en documentación ni revele su valor.

## Proceso de actualización

1. Leer `AGENTS.md`, Documento Maestro y `docs/ESTADO_PROYECTO.md`.
2. Crear o editar únicamente el cambio aprobado.
3. Revisar `git status` y `git diff`.
4. Ejecutar pruebas proporcionales al cambio.
5. Ejecutar escaneo de secretos y `git diff --check`.
6. Crear un commit descriptivo, sin secretos.
7. Hacer `git push origin main` solo con pruebas aprobadas.
8. Verificar el deployment en Render; si Auto-Deploy no reacciona, usar la contingencia documentada.
9. Ejecutar `scripts/verificar_produccion.py` y, cuando corresponda, `scripts/verificar_bd.py`.
10. Registrar el cambio, pruebas y evidencia.

No use `force push`, no reescriba el historial y no ejecute cambios estructurales de BD sin aprobación y respaldo.

## Respaldo y recuperación

### Código y documentación

GitHub conserva el historial, pero no sustituye una política institucional de respaldo. Mantenga acceso administrativo al repositorio y, antes de cambios mayores, confirme que `main` esté publicada y sincronizada.

### Base de datos

Antes de una migración o entrega importante:

1. revise las opciones de respaldo y restauración vigentes del plan de Neon;
2. genere un respaldo lógico con herramientas PostgreSQL compatibles, en un equipo seguro, si la política institucional lo permite;
3. cifre y proteja cualquier archivo que contenga datos personales;
4. pruebe la restauración en una rama o base separada, nunca sobre producción sin plan de reversión;
5. documente fecha, responsable y alcance, sin copiar secretos.

No almacene respaldos de producción dentro del repositorio Git.

## Seguridad operativa

- Mantener `.env` fuera de Git.
- Rotar credenciales cuando cambie el responsable.
- Conservar `SECRET_KEY` estable durante la operación; cambiarla cierra sesiones existentes.
- Entregar credenciales institucionales por un canal privado.
- Revisar que los hashes de `usuarios.password_hash` tengan formato Werkzeug.
- Desactivar cuentas que ya no correspondan.
- No publicar nombres reales de lectores en evidencias.
- Mantener HTTPS para la cámara y la cookie segura.
- No mostrar `DATABASE_URL`, claves, tokens, Deploy Hook ni respaldos en tickets o capturas.

## Solución de problemas

| Problema | Diagnóstico y acción |
|---|---|
| Render tarda al primer acceso | Esperar el *cold start* y revisar `/` por HTTPS. |
| HTTP 500 o página de error de BD | Revisar logs de Render sin copiarlos públicamente; comprobar `DATABASE_URL` y estado de Neon. |
| Falta una variable | Configurarla en `.env` local o Environment de Render; no añadir valor por defecto secreto. |
| Login falla para todos | Verificar Neon, cuenta activa, rol válido y hash; no restablecer con texto plano. |
| Asistente recibe 403 | Es el comportamiento esperado en rutas exclusivas de admin. |
| Cámara no funciona | Confirmar HTTPS, permiso del navegador, disponibilidad de cámara y carga de html5-qrcode; usar ingreso manual. |
| QR no se identifica | Confirmar normalización y existencia exacta de `codigo_qr`; revisar activación y condición del ejemplar. |
| Préstamo rechazado | Revisar mora, cantidad de activos, lector, ejemplar, fecha límite y posible operación simultánea. |
| PDF no abre | Confirmar ReportLab, endpoint autenticado y selección válida de ejemplares. |
| Auto-Deploy no inicia | Confirmar rama y commit; usar `Deploy latest commit` y documentar el deployment. |
| Neon no conecta | Confirmar servicio, SSL, cadena privada y acceso de red; ejecutar `verificar_bd.py`. |

## Procedimiento general de mantenimiento

1. Identificar el incidente y registrar fecha, ambiente y alcance.
2. Reproducir de forma segura, sin datos personales reales.
3. Confirmar si afecta una regla del Documento Maestro.
4. Si exige cambio estructural, solicitar aprobación y actualizar control de cambios.
5. Aplicar el cambio mínimo en una rama o entorno controlado.
6. Probar flujo principal, restricciones y regresión relevante.
7. Revisar seguridad y secretos.
8. Publicar con Git y verificar Render/Neon.
9. Registrar evidencia real y comunicar el resultado.

## Límites y mejoras futuras

La versión 1.0 no incluye multas, reservas, notificaciones, integración académica, modo offline, múltiples sedes, analítica avanzada ni aplicación móvil nativa. Estas funciones corresponden a una versión 1.1, 2.0 o posterior.

También se recomienda evaluar en una versión aprobada una interfaz administrativa para gestionar cuentas internas y una solución definitiva para Auto-Deploy. Hasta entonces, la provisión de cuentas es una tarea técnica controlada.
