# Validación de requisitos de la Semana 1

## Propósito

Este documento deja constancia de la revisión de consistencia realizada sobre el Documento Maestro v1.0 antes de iniciar la implementación. La validación conserva sin cambios el alcance, las reglas de negocio, la arquitectura, los roles, el modelo de datos y los criterios de aceptación aprobados.

## Línea base revisada

| Elemento | Cantidad | Identificadores | Resultado |
|---|---:|---|---|
| Reglas de negocio | 18 | RN-01 a RN-18 | Completas y sin contradicciones detectadas |
| Casos de uso | 10 | CU-01 a CU-10 | Actores y resultados definidos |
| Criterios de aceptación | 14 | CA-01 a CA-14 | Condiciones verificables definidas |
| Actores y roles | 3 | Público, `admin`, `asistente` | Permisos delimitados |
| Reportes mínimos | 4 | RPT-01 a RPT-04 | Contenido mínimo definido |
| Casos excepcionales QR | 10 | Sin código propio | Respuesta obligatoria definida |
| Entidades principales | 6 | usuarios, materias, libros, ejemplares, lectores, prestamos | Relaciones y campos definidos |

## Decisiones de negocio validadas

| Tema | Decisión vigente | Reglas relacionadas | Estado |
|---|---|---|---|
| Clasificación | Todo libro requiere nivel y materia activa. | RN-01 | Conforme |
| Ejemplar físico | Cada copia tiene registro y QR único estable. | RN-02, RN-13 | Conforme |
| Lectores | Se buscan o crean dentro del préstamo; no existe carga anual obligatoria. | RN-03 | Conforme |
| Datos académicos | Nivel y grado/sección pertenecen al préstamo, no al lector. | RN-04 | Conforme |
| Límite | Un lector puede tener como máximo dos préstamos activos. | RN-05 | Conforme |
| Mora | La mora bloquea nuevos préstamos y se recalcula al devolver. | RN-06, RN-07 | Conforme |
| Plazo | Se permiten 7 días, 14 días o fecha personalizada válida. | RN-08 | Conforme |
| Disponibilidad | Se deriva del préstamo activo y de la condición del ejemplar. | RN-09, RN-10 | Conforme |
| Historial | Los registros con historial se desactivan en vez de eliminarse desde la interfaz. | RN-11 | Conforme |
| Trazabilidad | Préstamo y devolución registran al usuario responsable. | RN-12 | Conforme |
| Escaneo | El ingreso manual aplica exactamente las mismas validaciones. | RN-14 | Conforme |
| Concurrencia | Solo puede existir un préstamo activo por ejemplar. | RN-15 | Conforme |
| Privacidad | El catálogo público no expone lectores ni datos internos. | RN-16 | Conforme |
| Reportes | Se mantienen los cuatro reportes operativos mínimos. | RN-17 | Conforme |
| Fechas | La lógica usa `America/Lima`; el día límite aún está dentro del plazo. | RN-18 | Conforme |

## Validaciones de consistencia

- Las reglas RN-03 y RN-04 son coherentes con el modelo de datos: `lectores` conserva la identidad y `prestamos` conserva el nivel y grado/sección de cada operación.
- RN-09 evita un estado duplicado en `ejemplares`; la disponibilidad se obtiene desde el préstamo activo, `activo` y `estado_fisico`.
- RN-05 y RN-15 son restricciones diferentes: la primera limita préstamos por lector y la segunda protege un ejemplar ante concurrencia.
- RN-06, RN-07 y RN-18 comparten una definición única de vencimiento basada en fechas de `America/Lima`.
- Los permisos de los casos de uso coinciden con las rutas y con CA-09.
- Los reportes RPT-01 a RPT-04 coinciden con RN-17 y CA-14.
- Los casos excepcionales del QR son compatibles con RN-10, RN-13, RN-14 y RN-15.
- No se detectaron decisiones estructurales abiertas ni contradicciones que requieran modificar la especificación v1.0.

## Alcance congelado para desarrollo

La versión 1.0 mantiene Flask, PostgreSQL en Neon, Psycopg 3, HTML5, CSS, Bootstrap 5, JavaScript, html5-qrcode, qrcode, ReportLab, Gunicorn, Render y GitHub. Se mantienen los roles `admin` y `asistente`, las seis entidades del modelo, los criterios CA-01 a CA-14 y el alcance/fuera de alcance del Documento Maestro.

Durante la Semana 1 no se crean el proyecto Flask, el esquema SQL, cuentas de prueba ni servicios Neon/Render; corresponden a semanas posteriores.

## Resultado

La especificación se considera cerrada para iniciar la implementación una vez que el usuario revise y apruebe los entregables de esta semana. No fue necesario registrar cambios en `docs/REGISTRO_CAMBIOS.md`.
