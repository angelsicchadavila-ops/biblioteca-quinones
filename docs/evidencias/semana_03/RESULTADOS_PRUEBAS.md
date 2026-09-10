# Resultados de pruebas de Flask y autenticación

## Entorno verificado

- Aplicación: Flask 3.1.3.
- Base de datos: PostgreSQL en Neon mediante Psycopg 3.
- Contraseñas: verificación de hashes con Werkzeug.
- Zona horaria de las conexiones: `America/Lima`.
- Variables privadas: archivo local `.env`, ignorado por Git.

## Verificación previa de Neon

Resultado: 7 de 7 comprobaciones correctas. Se confirmaron las seis tablas del DER, restricciones, índices, triggers, cinco materias, las cuentas `admin` y `asistente`, y la ausencia de datos temporales de las pruebas de Semana 2.

## Suite automatizada

Comando ejecutado:

```text
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Resultado final: 19 de 19 pruebas correctas en 21.628 segundos. La suite reúne 11 pruebas funcionales de Semana 3 y las 8 pruebas estáticas de Semana 2.

| Caso de Semana 3 | Resultado |
|---|---|
| Aplicación creada y consulta `SELECT 1` en Neon | Correcto |
| Rutas públicas `/` y `/login` | Correcto |
| Bloqueo de `/admin` y `/escaneo` sin sesión | Correcto |
| Login inválido | Correcto, HTTP 401 y sin sesión |
| Login válido de `admin` | Correcto, redirige a `/admin` |
| `admin` accede a `/admin` | Correcto |
| `admin` accede a `/escaneo` | Correcto |
| Login válido de `asistente` | Correcto, redirige a `/escaneo` |
| `asistente` accede a `/escaneo` | Correcto |
| `asistente` intenta acceder a `/admin` | Correcto, HTTP 403 |
| Logout e invalidación de sesión | Correcto |
| Solicitud POST sin token CSRF | Correcto, HTTP 400 |

## Pruebas locales complementarias

- Inicio del servidor Flask local: correcto.
- Respuesta de `http://127.0.0.1:5000/`: HTTP 200.
- Revisión visual del login en navegador de escritorio: correcta.
- Revisión responsive del login con viewport de 390 × 844: correcta, sin desbordes ni controles cortados.
- Login inválido desde navegador: correcto, mensaje genérico sin revelar qué campo falló.
- `compileall`: correcto.
- `pip check`: sin dependencias incompatibles.
- `git diff --check`: sin errores.

Gunicorn se incluye y se configura para Render. Su ejecución directa no se considera una prueba local válida en Windows porque depende del módulo POSIX `fcntl`; la prueba efectiva del comando `gunicorn app:app` debe realizarse durante el deployment Linux en Render.

## Pruebas pendientes del deployment

- Respuesta HTTPS en Render.
- Login y navegación desde navegador de escritorio sobre la URL pública.
- Acceso desde un dispositivo móvil real.
