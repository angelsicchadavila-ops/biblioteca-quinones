# Resultados de pruebas de catálogo e inventario

## Entorno

- Aplicación Flask 3.1.3.
- PostgreSQL en Neon mediante Psycopg 3.
- Zona horaria de conexión: `America/Lima`.
- Datos temporales identificados con sufijos aleatorios y eliminados en un bloque `finally`.
- Credenciales leídas desde variables locales ignoradas por Git.

## Suite automatizada

Comando ejecutado:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado final: 20 de 20 pruebas correctas en 111,707 segundos.

La suite reúne:

- 1 prueba integral de Semana 4 con múltiples verificaciones internas.
- 11 pruebas funcionales de autenticación y permisos de Semana 3.
- 8 pruebas estáticas del esquema y seguridad de Semana 2.

## Comprobaciones de Semana 4

| N.º | Caso | Resultado real |
|---:|---|---|
| 1 | Crear materia | Correcto; espacios normalizados |
| 2 | Editar materia | Correcto |
| 3 | Desactivar materia | Correcto |
| 4 | Reactivar materia | Correcto |
| 5 | Crear libro | Correcto |
| 6 | Editar libro | Correcto |
| 7 | Asociar materia y nivel | Correcto; solo materia activa y nivel aprobado |
| 8 | Crear un ejemplar | Correcto |
| 9 | Crear varios ejemplares | Correcto; cuatro códigos únicos y consecutivos |
| 10 | Marcar ejemplar como dañado | Correcto |
| 11 | Volver ejemplar a operativo | Correcto |
| 12 | Desactivar y reactivar ejemplar | Correcto |
| 13 | Buscar por título | Correcto |
| 14 | Buscar por autor | Correcto |
| 15 | Filtrar por materia | Correcto |
| 16 | Filtrar por nivel | Correcto |
| 17 | Combinar texto, materia y nivel | Correcto |
| 18 | Calcular disponibilidad | Correcto: 1 disponible, 1 prestado, 1 dañado y 1 inactivo |
| 19 | Bloquear al asistente | Correcto; HTTP 403 en GET y POST administrativos |
| 20 | Consultar sin sesión | Correcto; HTTP 200 y sin controles administrativos |

Validaciones adicionales:

- Se rechazó un nombre de materia repetido con distinta capitalización.
- Se impidió desactivar una materia con un libro activo.
- Se ocultó un libro desactivado del catálogo y reapareció al reactivarlo.
- Se comprobó el patrón exacto `LIB-<libro>-EJ<secuencia>`.

## Verificación posterior de Neon

Resultado: 7 de 7 controles correctos.

1. Las seis tablas del DER continúan creadas.
2. Las restricciones esenciales continúan presentes.
3. Los índices funcionales y de búsqueda continúan presentes.
4. Los triggers de materia activa y préstamos continúan presentes.
5. Las cinco materias iniciales continúan cargadas.
6. Las dos cuentas de prueba conservan roles válidos.
7. No quedaron datos temporales de catálogo, lectores o préstamos.

## Deployment

| Verificación | Resultado |
|---|---|
| Push a `origin/main` | Correcto |
| Commit de implementación en GitHub | `a190a88` |
| Build de Render | Correcto |
| Estado final | `Deploy succeeded | Live` |
| Comando de inicio | `gunicorn app:app` |
| Health check | HTTP 200 |
| Página pública nueva | HTTP 200; `Catálogo · Biblioteca Quiñones` |
| HTTPS | Correcto |

El Auto-Deploy estaba configurado como `On Commit`, pero el webhook no inició el build. Se ejecutó `Deploy latest commit` desde el panel y el resultado fue correcto.

## Controles complementarios

- Compilación de Python: correcta.
- Dependencias: `pip check` sin incompatibilidades.
- Espacios y conflictos: `git diff --check` correcto.
- Secretos: no se encontraron URLs PostgreSQL, claves privadas ni valores de `DATABASE_URL` o `SECRET_KEY` en archivos versionados.
