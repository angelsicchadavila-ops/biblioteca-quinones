# Matriz de permisos de la versión 1.0

## Leyenda

- **Sí:** acceso permitido.
- **Operación:** acceso limitado al flujo de escaneo, préstamo y devolución.
- **No:** acceso denegado por el backend.

| Recurso o acción | Público | `asistente` | `admin` |
|---|:---:|:---:|:---:|
| Consultar catálogo, filtros y disponibilidad | Sí | Sí | Sí |
| Abrir `/login` | Sí | Sí | Sí |
| Iniciar/cerrar sesión propia | No | Sí | Sí |
| Usar `/escaneo` y código manual | No | Operación | Sí |
| Consultar `/api/ejemplar/<codigo_qr>` dentro del terminal | No | Operación | Sí |
| Buscar o crear lector dentro de un préstamo | No | Operación | Sí |
| Registrar préstamo | No | Operación | Sí |
| Registrar devolución | No | Operación | Sí |
| Acceder a `/admin` | No | No | Sí |
| Gestionar libros y ejemplares | No | No | Sí |
| Gestionar materias | No | No | Sí |
| Gestionar usuarios internos | No | No | Sí |
| Generar/reimprimir QR y PDF A4 | No | No | Sí |
| Consultar administración de préstamos | No | No | Sí |
| Consultar RPT-01 a RPT-04 | No | No | Sí |
| Consultar datos personales o historial desde el catálogo público | No | No aplica | No aplica |

## Matriz por caso de uso

| Caso de uso | Público | `asistente` | `admin` |
|---|:---:|:---:|:---:|
| CU-01 Consultar catálogo | Sí | Sí | Sí |
| CU-02 Autenticarse | No | Sí | Sí |
| CU-03 Gestionar catálogo | No | No | Sí |
| CU-04 Gestionar materias | No | No | Sí |
| CU-05 Gestionar usuarios | No | No | Sí |
| CU-06 Generar/reimprimir QR | No | No | Sí |
| CU-07 Registrar préstamo | No | Sí | Sí |
| CU-08 Registrar devolución | No | Sí | Sí |
| CU-09 Consultar préstamos | No | No | Sí |
| CU-10 Consultar reportes | No | No | Sí |

## Controles obligatorios

- La autorización se verifica en el backend; ocultar un enlace en la interfaz no sustituye la validación.
- Un `asistente` no puede acceder a rutas de gestión exclusivas de `admin`.
- Las APIs operativas requieren sesión y rol autorizado.
- El catálogo público solo expone libros, clasificación y disponibilidad; no expone lectores ni préstamos internos.
- Una cuenta inactiva no puede iniciar una nueva sesión.
- La trazabilidad conserva el usuario que registró el préstamo y el que confirmó la devolución.

## Trazabilidad

Esta matriz consolida los actores de CU-01 a CU-10, las rutas del capítulo 3.1, RN-12, RN-16 y CA-09 del Documento Maestro v1.0.
