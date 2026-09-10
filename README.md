# Sistema Web de Gestión Bibliotecaria con Control QR

Aplicación académica de la Biblioteca Quiñones. La versión actual corresponde a la Semana 3 y valida la base Flask, la conexión con PostgreSQL en Neon, la autenticación del personal y los permisos de los roles `admin` y `asistente`.

## Requisitos

- Python 3.
- Variables privadas en `.env`: `DATABASE_URL` y `SECRET_KEY`.
- Las contraseñas de las cuentas de prueba solo son necesarias para ejecutar la suite funcional local.

## Ejecución local en Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

La aplicación queda disponible en `http://127.0.0.1:5000`.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas funcionales usan las cuentas ya creadas en Neon y leen sus contraseñas desde variables locales. No muestran ni guardan esas credenciales.

## Despliegue en Render

El archivo `render.yaml` define el servicio web, la instalación desde `requirements.txt` y el inicio con `gunicorn app:app`. Render solicita `DATABASE_URL` como valor privado y genera `SECRET_KEY` automáticamente.

Instancia técnica de la Semana 3: https://biblioteca-quinones.onrender.com

No se debe copiar `.env` a GitHub ni a Render.
