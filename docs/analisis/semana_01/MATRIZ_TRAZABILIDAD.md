# Matriz de trazabilidad de requisitos

| Regla | Casos de uso relacionados | Criterios relacionados | Verificación prevista |
|---|---|---|---|
| RN-01 Clasificación cruzada | CU-01, CU-03, CU-04 | CA-01 | Registro y filtros por nivel/materia |
| RN-02 Identificación por ejemplar | CU-03, CU-06 | CA-02 | Múltiples ejemplares y QR único |
| RN-03 Registro simplificado de lectores | CU-07 | CA-03 | Buscar/crear sin salir del préstamo |
| RN-04 Datos académicos por préstamo | CU-07 | CA-03 | Persistencia en préstamo, no lector |
| RN-05 Límite de préstamos | CU-07 | CA-04 | Permitir 0/1 activos y rechazar tercero |
| RN-06 Bloqueo por mora | CU-07 | CA-05 | Rechazo con préstamo vencido |
| RN-07 Desbloqueo automático | CU-08 | CA-05 | Recalcular tras última devolución vencida |
| RN-08 Plazos flexibles | CU-07 | CA-06 | 7 días, 14 días y fecha válida |
| RN-09 Disponibilidad derivada | CU-01, CU-07, CU-08, CU-09 | CA-07, CA-08 | Derivar desde préstamo activo |
| RN-10 Condición física | CU-03, CU-07, CU-08 | CA-07 | Bloquear dañado o inactivo |
| RN-11 Activación lógica | CU-03, CU-04, CU-05 | CA-11 | Desactivar/reactivar sin borrar historial |
| RN-12 Trazabilidad | CU-05, CU-07, CU-08, CU-09 | CA-12 | Usuarios responsables y fecha/hora |
| RN-13 QR único y estable | CU-03, CU-06 | CA-02 | Reimpresión conserva código |
| RN-14 Ingreso manual equivalente | CU-07, CU-08 | CA-10 | Mismas validaciones que cámara |
| RN-15 Concurrencia | CU-07 | CA-13 | Dos solicitudes, solo una confirmada |
| RN-16 Catálogo público | CU-01 | CA-09 | Sin datos personales ni internos |
| RN-17 Reportes mínimos | CU-10 | CA-14 | RPT-01 a RPT-04 disponibles |
| RN-18 Zona horaria | CU-07, CU-08, CU-09, CU-10 | CA-05, CA-06, CA-14 | Fechas de negocio en `America/Lima` |

## Cobertura

- Las 18 reglas de negocio tienen al menos un caso de uso y una verificación asociada.
- Los 10 casos de uso tienen actor, precondición, flujo, alternativas, postcondición y trazabilidad.
- Los 14 criterios de aceptación quedan vinculados a las reglas y flujos que deberán probarse en sus semanas de implementación.
- Esta matriz valida cobertura documental; no sustituye las pruebas funcionales futuras.
