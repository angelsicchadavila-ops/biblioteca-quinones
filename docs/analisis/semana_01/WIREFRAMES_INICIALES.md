# Wireframes iniciales de la versión 1.0

## Alcance

Los wireframes son propuestas de baja fidelidad para validar jerarquía, información y flujo. No representan una implementación HTML ni decisiones visuales finales.

## Pantallas

| Archivo | Vistas incluidas | Casos de uso |
|---|---|---|
| [`01_catalogo_login.svg`](wireframes/01_catalogo_login.svg) | Catálogo público e inicio de sesión | CU-01, CU-02 |
| [`02_panel_gestion.svg`](wireframes/02_panel_gestion.svg) | Panel administrativo y gestión de libros/ejemplares | CU-03, CU-04, CU-05, CU-06 |
| [`03_terminal_prestamo.svg`](wireframes/03_terminal_prestamo.svg) | Terminal QR e ingreso de préstamo | CU-07 |
| [`04_devolucion_reportes.svg`](wireframes/04_devolucion_reportes.svg) | Confirmación de devolución y reportes | CU-08, CU-09, CU-10 |

## Criterios de diseño validados

- El catálogo público muestra búsqueda, filtros y disponibilidad sin datos personales.
- El inicio de sesión separa el acceso del personal del catálogo público.
- La navegación administrativa es exclusiva del rol `admin`.
- El terminal prioriza la cámara, mantiene ingreso manual equivalente y muestra mensajes de estado claros.
- El préstamo permite buscar o crear lector sin abandonar el flujo y registra nivel, grado/sección y plazo.
- La devolución exige confirmación y muestra el préstamo activo.
- Los estados Disponible, Prestado, Dañado/Inactivo, Activo, Vencido y Devuelto se acompañan de texto; no dependen solo del color.
- Los reportes se plantean como tablas y filtros funcionales, sin incorporar analítica avanzada fuera de alcance.
- Las vistas consideran uso en computadora y teléfono.

## Decisiones pendientes de detalle visual

Tipografía final, logotipo institucional, espaciado definitivo y paleta de marca se ajustarán durante la implementación de interfaz sin alterar los flujos ni permisos aprobados.
