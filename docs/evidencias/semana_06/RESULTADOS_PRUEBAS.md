# Resultados de pruebas de la Semana 6

Fecha de ejecución: 14 de septiembre de 2026  
Entorno: aplicación local conectada a PostgreSQL Neon, zona horaria `America/Lima`.

## Resumen

- Línea base anterior a los cambios: **30/30 pruebas correctas** en 192,606 segundos.
- Suite específica de Semana 6: **4/4 escenarios integrales correctos** en 96,552 segundos.
- Suite completa de regresión: **34/34 pruebas correctas** en 260,031 segundos.
- Revalidación específica de préstamo por asistente y trazabilidad: **1/1 correcta** en 35,020 segundos.
- Verificación de Neon: **7/7 comprobaciones correctas**.
- Limpieza posterior: 0 materias, 0 libros, 0 lectores y 0 préstamos con los identificadores temporales de la suite.

La primera ejecución aislada no pudo abrir conexiones TCP hacia Neon y devolvió errores de permisos de red. Se repitió con acceso de red autorizado; no se consideró un fallo funcional y la suite real terminó correctamente.

## Cobertura de los casos solicitados

| N.° | Caso | Resultado | Evidencia automática |
|---:|---|---|---|
| 1 | Crear lector desde el préstamo | Correcto | `test_01_lector_plazos_limite_devolucion_e_historial` |
| 2 | Reutilizar lector existente | Correcto | búsqueda tolerante y segundo préstamo por `lector_id` |
| 3 | Registrar primer préstamo | Correcto | respuesta HTTP 201 y persistencia |
| 4 | Registrar segundo préstamo | Correcto | permitido con un préstamo activo |
| 5 | Bloquear tercer préstamo | Correcto | HTTP 409, código `limite_prestamos` |
| 6 | Bloquear lector con mora | Correcto | HTTP 409, código `lector_con_mora` |
| 7 | Permitir préstamo tras resolver mora | Correcto | devolución vencida seguida de préstamo HTTP 201 |
| 8 | Plazo de 7 días | Correcto | fecha actual + 7 |
| 9 | Plazo de 14 días | Correcto | fecha actual + 14 |
| 10 | Fecha personalizada válida | Correcto | fecha persistida sin modificación |
| 11 | Fecha personalizada inválida | Correcto | HTTP 400, código `fecha_invalida` |
| 12 | Identificar préstamo activo por QR/código | Correcto | endpoint devuelve `operacion=devolucion` y ficha privada |
| 13 | Registrar devolución | Correcto | fecha y responsable persistidos |
| 14 | Registrar quién hizo el préstamo | Correcto | admin y asistente verificados por identificador |
| 15 | Registrar quién hizo la devolución | Correcto | asistente verificado por identificador |
| 16 | Detectar vencimiento dinámico | Correcto | `fecha_devolucion IS NULL` y límite anterior a hoy |
| 17 | Calcular días de atraso | Correcto | préstamo de un día de atraso devuelve `1` |
| 18 | Semáforo amarillo | Correcto | clase `fila-prestamo-activo` y badge amarillo |
| 19 | Semáforo rojo | Correcto | clase `fila-prestamo-vencido` y badge rojo |
| 20 | Preservar historial | Correcto | tres préstamos permanecen después de devolución |
| 21 | Bloquear ejemplar dañado | Correcto | operación bloqueada y préstamo rechazado |
| 22 | Bloquear ejemplar inactivo | Correcto | operación bloqueada y préstamo rechazado |
| 23 | Impedir doble préstamo simultáneo | Correcto | dos conexiones: un creado y un rechazado; un activo final |
| 24 | Acceso administrador | Correcto | listado y reportes HTTP 200 |
| 25 | Acceso asistente | Correcto | terminal y operaciones permitidas; admin HTTP 403 |
| 26 | Bloqueo público | Correcto | API HTTP 401 y rutas admin redirigidas |
| 27 | RPT-01 | Correcto | conteos temporales esperados: total 7, disponibles 4, prestados 2, dañados 1 |
| 28 | RPT-02 | Correcto | préstamos sin devolver con estado calculado |
| 29 | RPT-03 | Correcto | lector, grado/sección, límite y atraso |
| 30 | RPT-04 | Correcto | historial y validación de rango; rango inverso HTTP 400 |
| 31 | Aplicación en Render | Pendiente final | la versión de Semana 5 respondió por HTTPS antes de implementar; falta verificar el nuevo commit |
| 32 | Ciclo real desde móvil | Pendiente manual | requiere cámara física, login, préstamo, relectura y devolución |

## Integridad y concurrencia

La aplicación usa transacciones explícitas y bloqueos `FOR UPDATE` sobre lector y ejemplar. Las validaciones se repiten en el backend y permanecen respaldadas por `trg_validar_prestamo_activo` y `uq_prestamos_ejemplar_activo`. La prueba concurrente abrió dos conexiones independientes contra Neon y confirmó un único préstamo activo.

## Pendientes manuales

La Semana 6 no se declara cerrada hasta completar el ciclo móvil real, las capturas indicadas en `capturas/INSTRUCCIONES_CAPTURAS.md` y la verificación del deployment del commit técnico.
