# Resultados de pruebas v1.1

## Validaciones ejecutadas

| Verificación | Resultado |
|---|---|
| Validación transaccional de migración y rollback | Correcta; columna y constraint creados dentro de la transacción y ausentes tras revertir |
| Migración Neon | Aplicada; `SMALLINT NULL`, constraint validado, sin índice de año |
| Pruebas específicas v1.1 | 4/4 correctas; casos internos y subpruebas de año, roles, usuarios y recuperación |
| Suite acumulada final pre-deployment | 43/43 correctas en 484,539 s |
| Integridad y concurrencia | 11/11 correctas; datos revertidos o eliminados |
| Verificación Neon | 7/7 correcta; esquema, seed y limpieza |
| Compilación Python | Correcta |
| `pip check` | Sin dependencias incompatibles |

## Cobertura v1.1

- Año: alta, edición, filtro y combinación de filtros, vacío legado, formatos inválidos, rango y registros `NULL`.
- Asistente: listado, alta, edición de todos los datos bibliográficos, libros inactivos visibles y bloqueos GET/POST para estado, materias, ejemplares y usuarios.
- Usuarios: listado exclusivo de asistentes, nombre obligatorio, rol fijado en backend, hash, login, cambio de contraseña, invalidación de contraseña anterior, desactivación, invalidación de sesión, bloqueo de login, reactivación, trazabilidad y protección del ID admin.
- Recuperación admin: entrada con `getpass`, longitud, confirmación, restricción por rol, hash y login posterior.
- Regresión: autenticación, CSRF, sesiones, catálogo, inventario, materias, ejemplares, QR, PDF, escaneo, lectores, préstamos, devoluciones, máximo de dos préstamos, mora, semáforo, reportes, trazabilidad y concurrencia.

## Limpieza

Los datos funcionales temporales incorporaron identificadores UUID y se eliminaron al finalizar cada prueba. La verificación posterior confirmó 0 libros, 0 ejemplares, 0 lectores y 0 préstamos, con las dos cuentas base y cinco materias iniciales intactas.

## Pendiente de cierre

- Smoke actualizado sobre Render después del deployment.

Commit técnico validado: `e0283aaf428933e06ae05e3f830057d216aea970`.
