# Resultados de pruebas de la base de datos

## Entorno verificado

- PostgreSQL alojado en Neon.
- Rama: `production`.
- Base: `neondb`.
- Cliente: Psycopg 3.3.5.
- Zona horaria aplicada por los scripts: `America/Lima`.
- Conexión: variable local `DATABASE_URL`, ignorada por Git.

## Verificación del esquema

Resultado final: 7 de 7 verificaciones correctas.

1. Las seis tablas del DER están creadas.
2. Las restricciones esenciales están presentes.
3. Los índices funcionales y de búsqueda están presentes.
4. Los triggers de materia activa y préstamos están presentes.
5. Las cinco materias iniciales están cargadas.
6. Las dos cuentas de prueba tienen los roles aprobados.
7. No quedaron libros, ejemplares, lectores ni préstamos temporales después de las pruebas.

## Pruebas reales de integridad

Resultado final: 11 de 11 pruebas correctas.

| Caso | Resultado |
|---|---|
| Primer préstamo válido | Aceptado |
| Segundo préstamo activo del lector | Aceptado |
| Tercer préstamo activo del lector | Rechazado |
| Segundo préstamo activo del mismo ejemplar | Rechazado |
| Nuevo préstamo para lector moroso | Rechazado |
| Préstamo de ejemplar dañado | Rechazado |
| Código QR duplicado | Rechazado |
| Rol fuera del dominio aprobado | Rechazado |
| Libro asociado a materia inactiva | Rechazado |
| Devolución sin usuario responsable | Rechazado |
| Dos conexiones simultáneas para el mismo ejemplar | Solo una fue confirmada |

Los primeros diez casos se ejecutaron dentro de una transacción revertida. La prueba concurrente utilizó dos conexiones reales y eliminó después todos sus registros identificados. Una verificación posterior confirmó que no quedaron datos temporales.

## Pruebas locales complementarias

- `unittest`: 8 de 8 pruebas estáticas correctas.
- `compileall`: scripts sin errores de sintaxis.
- `pip check`: dependencias compatibles.
- `git diff --check`: sin errores de espacios ni marcadores de conflicto.
