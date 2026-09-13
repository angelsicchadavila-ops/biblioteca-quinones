# Sistema Web de Gestión Bibliotecaria con Control QR

Aplicación académica de la Biblioteca Quiñones. La Semana 5 está completa y pendiente de aprobación del usuario; incorpora identificación QR, etiquetas PDF A4 y un terminal móvil de escaneo, además del catálogo y la administración construidos en semanas anteriores. La Semana 6 no ha comenzado.

## Funciones disponibles

- Catálogo público en `/`, sin autenticación, con búsqueda por título o autor.
- Filtros combinables por materia y nivel académico.
- Conteos derivados de ejemplares disponibles, prestados, dañados e inactivos.
- Gestión administrativa de materias en `/admin/materias`.
- Gestión administrativa de libros y ejemplares en `/admin/libros`.
- Generación automática de códigos de ejemplar con el formato `LIB-XXX-EJYY`.
- Generación y reimpresión administrativa de QR estables sin archivos temporales.
- PDF A4 con una cuadrícula de 21 etiquetas por página mediante ReportLab.
- Terminal autenticado en `/escaneo`, con cámara trasera preferida e ingreso manual equivalente.
- API interna `GET /api/ejemplar/<codigo_qr>` para identificar ejemplares sin modificar inventario ni historial.
- Activación y desactivación lógica para conservar el historial.
- Autenticación y permisos diferenciados para `admin` y `asistente`.

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

Las pruebas funcionales usan las cuentas ya creadas en Neon y leen sus contraseñas desde variables locales. Los datos temporales del catálogo reciben identificadores aleatorios y se eliminan al finalizar, incluso si una prueba falla. No se muestran ni guardan credenciales.

## Despliegue en Render

El archivo `render.yaml` define el servicio web, la instalación desde `requirements.txt` y el inicio con `gunicorn app:app`. Render solicita `DATABASE_URL` como valor privado y genera `SECRET_KEY` automáticamente.

Instancia pública: https://biblioteca-quinones.onrender.com

No se debe copiar `.env` a GitHub ni a Render.
