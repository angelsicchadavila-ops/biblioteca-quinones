# Memoria final del Sistema Web de Gestión Bibliotecaria con Control QR

## Datos generales

| Campo | Información |
|---|---|
| Proyecto | Sistema Web de Gestión Bibliotecaria con Control QR |
| Institución | Colegio Privado José Abelardo Quiñones |
| Finalidad académica | Prácticas Pre-Profesionales II |
| Versión | 1.0 |
| Periodo de ejecución | 9 semanas |
| Fecha de cierre técnico documental | 17 de septiembre de 2026 |
| Responsable | **[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]** |
| Docente o supervisor | **[PENDIENTE DE COMPLETAR]** |
| Responsable receptor | **[PENDIENTE DE COMPLETAR]** |

Esta memoria presenta la base académica del proyecto, sus decisiones, construcción, pruebas y resultados. La entrega formal a la institución y la firma de conformidad no se consideran realizadas hasta que existan evidencia y firma correspondientes.

## Resumen

El proyecto desarrolló una aplicación web para digitalizar el catálogo e inventario de una biblioteca escolar, identificar cada copia física mediante QR y registrar préstamos y devoluciones desde computadora o teléfono. La versión 1.0 aplica un máximo de dos préstamos activos, bloqueo por mora, disponibilidad derivada, trazabilidad por usuario y cuatro reportes operativos. La solución usa Flask, PostgreSQL en Neon y Render, con código versionado en GitHub.

El trabajo se organizó en nueve semanas incrementales. Las funciones fueron probadas por módulo, integradas en producción y sometidas a QA. El cierre técnico registró suite acumulada de 38/38 pruebas, 11/11 pruebas de integridad, verificación Neon 7/7 y smoke HTTPS de producción 32/32. La validación móvil se realizó; la prueba presencial con bibliotecaria no se ejecutó y no se afirma lo contrario.

## Problema identificado

La biblioteca necesitaba una forma sencilla de conocer los títulos y copias disponibles, reducir la dependencia de registros manuales, identificar cada ejemplar físico y conservar un historial confiable de préstamos y devoluciones. También era necesario controlar automáticamente mora y límite de préstamos, permitir operación desde teléfono y mantener la solución con tecnologías accesibles para un proyecto académico.

## Objetivo general

Desarrollar un sistema web accesible desde computadora y teléfono que permita administrar libros y ejemplares, consultar disponibilidad, registrar préstamos y devoluciones mediante QR o código manual, controlar morosidad y generar reportes operativos básicos.

## Objetivos específicos

- Digitalizar catálogo e inventario físico.
- Asignar un QR único y estable a cada ejemplar.
- Ofrecer consulta pública por título, autor, materia y nivel.
- Registrar lectores dentro del flujo operativo, sin carga anual masiva.
- Aplicar límite de dos préstamos activos y bloqueo por mora.
- Administrar materias, libros y ejemplares con conservación del historial.
- Generar etiquetas QR y reportes operativos.
- Desplegar la aplicación por HTTPS y documentar su uso y mantenimiento.

## Alcance de la versión 1.0

La versión incluye catálogo público; autenticación con roles `admin` y `asistente`; gestión de materias, libros y ejemplares; activación lógica; generación y reimpresión QR; PDF A4; terminal de cámara e ingreso manual; búsqueda o creación de lectores; préstamos con plazos de 7, 14 o fecha personalizada; devolución; mora; límite de dos; semáforo; trazabilidad; reportes RPT-01 a RPT-04; despliegue Render/Neon y documentación final.

## Fuera de alcance

No incluye multas, pagos, reservas, notificaciones, cuentas de alumnos, aplicación móvil nativa, trabajo offline, integración académica, múltiples sedes ni analítica avanzada. Estas posibilidades se reservan para versiones posteriores.

## Metodología de trabajo

Se utilizó una metodología incremental por semanas, guiada por el Documento Maestro v1.0. Cada módulo se cerró con:

1. revisión de requisitos y estado;
2. implementación limitada al alcance semanal;
3. pruebas del camino principal, restricciones y casos límite;
4. limpieza de datos temporales;
5. evidencia real;
6. commit y publicación controlada;
7. actualización del estado del proyecto.

Git permitió conservar trazabilidad. Neon funcionó como base de datos compartida y Render como entorno de producción temprana, lo que permitió validar HTTPS y uso móvil desde las primeras fases.

## Cronograma resumido de nueve semanas

| Semana | Objetivo | Resultado principal |
|---|---|---|
| 1 | Análisis y diseño | Reglas RN-01 a RN-18, casos CU-01 a CU-10, criterios CA-01 a CA-14, permisos, DER y wireframes. |
| 2 | Base de datos | Seis tablas, restricciones, índices, triggers, seeders y conexión real a Neon. |
| 3 | Flask, autenticación y despliegue temprano | Sesiones, roles, hashes, CSRF, rutas protegidas y primera versión HTTPS en Render. |
| 4 | Catálogo e inventario | Materias, libros, ejemplares, códigos automáticos, búsqueda y filtros. |
| 5 | QR y PDF | QR estable, reimpresión, etiquetas A4, terminal html5-qrcode e ingreso manual. |
| 6 | Operación bibliotecaria | Lectores, préstamos, mora, límite de dos, devolución, semáforo y reportes. |
| 7 | Producción y seguridad | Configuración Render/Neon, cookies, variables privadas, persistencia y cold start. |
| 8 | QA integral | 167 casos clasificados, 38/38 pruebas, dos incidencias corregidas y validación móvil. |
| 9 | Documentación y cierre | Manuales, memoria, guía institucional, checklist, acta y smoke final. |

## Tecnologías empleadas

El backend fue desarrollado en Python con Flask. PostgreSQL en Neon conserva la información y Psycopg 3 ejecuta SQL parametrizado. El frontend usa HTML5, CSS, Bootstrap 5 y JavaScript. html5-qrcode accede a la cámara, qrcode genera PNG y ReportLab crea etiquetas A4. Gunicorn sirve Flask en Render. Git y GitHub mantienen historial y respaldan el flujo de despliegue.

## Análisis

La fase de análisis definió actores público, administrador y asistente; reglas de disponibilidad, mora, trazabilidad e historial; casos de uso; permisos; criterios de aceptación y excepciones del QR. Se decidió no almacenar estados derivados como Prestado o Vencido para evitar inconsistencias.

También se estableció que el lector conserva nombres y apellidos, mientras que nivel y grado/sección pertenecen a cada préstamo. Esto evita una carga anual obligatoria de estudiantes.

## Diseño

El diseño priorizó simplicidad, pocas dependencias y separación entre navegador, aplicación y base de datos. El modelo lógico contiene usuarios, materias, libros, ejemplares, lectores y préstamos. Las interfaces se diseñaron para PC y móvil con un catálogo público, panel administrativo y terminal operativo.

La seguridad consideró sesiones, roles en backend, CSRF, SQL parametrizado, variables privadas, contraseñas con hash y HTTPS.

## Implementación

La aplicación se concentra en `app.py` y módulos pequeños de `utils`. Las plantillas Jinja2 representan catálogo, login, administración, inventario, terminal, préstamos y reportes. La lógica de negocio crítica se ejecuta en el servidor y se refuerza con restricciones de PostgreSQL.

Los registros con historial se desactivan en lugar de eliminarse. La generación de archivos QR y PDF se realiza en memoria, evitando temporales del servidor.

## Base de datos

PostgreSQL conserva las seis entidades del DER. Las claves foráneas restringen borrados, las restricciones `CHECK` delimitan roles y estados, y los índices apoyan catálogo, préstamos activos, mora e historial.

Dos triggers protegen reglas esenciales: uso de materias activas y validación de préstamos. Un índice único parcial garantiza que un ejemplar no tenga dos préstamos activos incluso ante solicitudes simultáneas.

## Autenticación y permisos

Las contraseñas se almacenan como hashes Werkzeug. Flask crea una sesión después de validar una cuenta activa y un rol permitido. Las solicitudes POST requieren CSRF. El rol `admin` accede a gestión y reportes; `asistente` se limita al terminal y operaciones de préstamo/devolución; el público solo consulta catálogo y login.

La provisión de cuentas institucionales definitivas se mantiene como tarea técnica de entrega. La versión actual no incorpora una pantalla de autogestión de usuarios; por seguridad, la sustitución de cuentas de prueba debe realizarla una persona autorizada mediante una operación parametrizada y con hash.

## Catálogo

El catálogo permite buscar título o autor y combinar filtros de materia y nivel. La disponibilidad se calcula por ejemplar considerando activación, condición física y préstamo sin devolución. No expone datos de lectores ni historial interno.

## Códigos QR

Cada ejemplar recibe un código único con formato `LIB-XXX-EJYY`. El QR contiene solamente ese código. La reimpresión conserva el identificador. El administrador puede descargar QR individual y etiquetas PDF A4; el terminal puede usar cámara o ingreso manual equivalente.

## Préstamos y devoluciones

El préstamo busca o crea al lector dentro del flujo, registra nivel y grado/sección, calcula o valida fecha límite y aplica reglas de elegibilidad. Se permiten 7 días, 14 días o fecha personalizada.

La devolución registra fecha, hora y usuario responsable. El semáforo muestra amarillo para activos dentro de plazo, rojo para vencidos y verde para devueltos. La zona horaria de negocio es `America/Lima`.

## Reportes

La versión 1.0 incorpora inventario, préstamos activos, préstamos vencidos e historial por rango. Los reportes son tabulares y orientados a operación diaria. Los paneles analíticos y exportaciones adicionales quedan fuera de alcance.

## Despliegue

El código de `main` se publica en GitHub. Render instala `requirements.txt` y ejecuta `gunicorn app:app`. Las variables privadas se configuran en el servicio y conectan con Neon. La URL pública usa HTTPS.

Auto-Deploy permaneció configurado en `On Commit`, pero no reaccionó de forma consistente durante varias semanas. `Deploy latest commit` fue probado como contingencia. Esta observación no afectó la disponibilidad final, pero debe revisarse en una mejora futura.

## Aseguramiento de calidad

La estrategia combinó pruebas estáticas, pruebas Flask con Neon, integridad SQL, concurrencia, smoke HTTPS, revisión móvil y evidencia visual.

Resultados consolidados antes del cierre:

- matriz de QA: 167/167 casos con estado final;
- 160 aprobados, 4 corregidos y 3 no aplicables;
- suite acumulada: 38/38;
- integridad y concurrencia: 11/11;
- verificación Neon: 7/7;
- smoke Render: 32/32;
- validación móvil: aprobada con cinco capturas;
- datos temporales: eliminados.

El smoke final de Semana 9 revalidó producción por HTTPS, login de ambos roles, catálogo, terminal, reportes, permisos, CSRF, cookies y logout. Se ejecutaron además dos pruebas QR y dos pruebas de préstamo/devolución/reportes, todas correctas.

## Incidencias encontradas y corregidas

### INC-08-001 Alta de ejemplares en libro inactivo

Durante QA se comprobó que una URL directa permitía agregar ejemplares a un libro desactivado. Se añadió validación de backend, se ocultó el formulario y se corrigió la disponibilidad administrativa. La prueba puntual y la suite final aprobaron.

### INC-08-002 Limpieza sensible a mayúsculas

El auxiliar de datos temporales no reconocía un lector creado en mayúsculas. Se normalizó la comparación manteniendo el alcance seguro de borrado. Neon terminó sin residuos.

No quedaron incidencias funcionales pendientes de las Semanas 1 a 8. La falta de una pantalla para administrar cuentas y la intermitencia de Auto-Deploy se documentan como limitaciones operativas que requieren decisión en una versión aprobada, no como funciones añadidas en Semana 9.

## Resultados

El proyecto produjo una aplicación web funcional por HTTPS, con base de datos en la nube, control de acceso, catálogo, inventario, QR, préstamos, devoluciones y reportes. Las reglas críticas se encuentran tanto en la aplicación como en PostgreSQL. El código, scripts, pruebas, evidencias y manuales quedaron organizados para mantenimiento posterior.

La aplicación estaba operativa al cierre técnico. Esto no equivale a entrega formal al colegio; quedan por realizar la presentación, provisión de credenciales institucionales definitivas y, si corresponde, firma del acta.

## Evidencias

Las evidencias se encuentran en `docs/evidencias/semana_01/` a `docs/evidencias/semana_09/`. Incluyen matrices, resultados de pruebas, SQL, capturas, video móvil, PDF de etiquetas, incidencias, comprobaciones de producción y checklist de entrega.

El Documento Maestro v1.0 y el modelo lógico están en `docs/`. Los manuales finales se encuentran en `docs/final/`.

## Conclusiones

1. La arquitectura seleccionada fue suficiente para el volumen y objetivos de la biblioteca escolar.
2. La disponibilidad y mora derivadas reducen el riesgo de estados contradictorios.
3. Las restricciones y transacciones de PostgreSQL son necesarias para proteger reglas críticas y concurrencia.
4. El terminal móvil con alternativa manual mantiene la operación cuando la cámara no está disponible.
5. Las pruebas incrementales y el despliegue temprano facilitaron detectar defectos antes del cierre.
6. La documentación y evidencia permiten transferir conocimiento, siempre que la institución complete la custodia de cuentas y credenciales.

## Recomendaciones

- Crear o sustituir cuentas institucionales y desactivar cuentas de prueba antes de la entrega.
- Nombrar un custodio institucional para GitHub, Render, Neon y credenciales.
- Cambiar contraseñas cuando cambie el personal autorizado.
- Definir un calendario de respaldo y prueba de restauración.
- Registrar incidencias con fecha, captura segura y pasos reproducibles.
- Mantener el código en `main` limpio y probar antes de desplegar.
- Revisar la causa de Auto-Deploy sin exponer hooks ni tokens.
- Realizar una capacitación breve y obtener acta o constancia si la institución la exige.

## Trabajos futuros

Las siguientes mejoras pueden evaluarse como versión 1.1 o 2.0, sin implementarlas en la versión 1.0:

- notificaciones de vencimiento;
- reservas;
- integración con el sistema académico;
- funcionamiento offline y sincronización;
- múltiples sedes;
- analítica avanzada;
- aplicación móvil nativa;
- autogestión administrativa de cuentas internas;
- mejoras y monitoreo de Auto-Deploy;
- exportaciones adicionales de reportes.

## Pendientes administrativos para la versión final académica

- Responsable: **[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]**
- Docente o supervisor: **[PENDIENTE DE COMPLETAR]**
- Responsable receptor y cargo: **[PENDIENTE DE COMPLETAR]**
- Fecha de entrega institucional: **[PENDIENTE DE COMPLETAR]**
- Resultado de capacitación: **[PENDIENTE DE COMPLETAR]**
- Acta o constancia firmada: **[PENDIENTE DE FIRMA, SI CORRESPONDE]**
