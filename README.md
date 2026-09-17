# Sistema Web de Gestión Bibliotecaria con Control QR

Aplicación académica desarrollada para el Colegio Privado José Abelardo Quiñones en el marco de Prácticas Pre-Profesionales II. La versión 1.0 integra catálogo, inventario, QR, préstamos, devoluciones, mora, reportes y despliegue web. La Semana 9 corresponde al cierre documental y preparación de la entrega institucional.

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
- Registro simplificado de lectores dentro del flujo operativo.
- Préstamos con plazos de 7, 14 días o fecha personalizada.
- Límite de dos préstamos activos y bloqueo por mora.
- Devolución con trazabilidad de usuario y fecha/hora.
- Semáforo de préstamos y reportes RPT-01 a RPT-04.
- Activación y desactivación lógica para conservar el historial.
- Autenticación y permisos diferenciados para `admin` y `asistente`.

## Producción

- Aplicación: https://biblioteca-quinones.onrender.com
- Repositorio: https://github.com/angelsicchadavila-ops/biblioteca-quinones
- Base de datos: PostgreSQL en Neon.

La entrega formal al colegio, las credenciales institucionales definitivas y la firma de conformidad no se consideran realizadas hasta que el estudiante complete esas acciones.

## Documentación final

Los documentos de cierre están indexados en [`docs/final/README.md`](docs/final/README.md):

- manual de usuario;
- manual técnico;
- memoria final;
- guía de entrega institucional;
- checklist de cierre;
- plantilla de acta.

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

Las pruebas funcionales usan las cuentas ya creadas en Neon y leen sus contraseñas desde variables locales. Los datos temporales reciben identificadores aislados y se eliminan al finalizar. No se muestran ni guardan credenciales.

Smoke de producción:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_produccion.py
```

Verificación de Neon:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_bd.py
```

## Despliegue en Render

El archivo `render.yaml` define el servicio web, la instalación desde `requirements.txt` y el inicio con `gunicorn app:app`. Render solicita `DATABASE_URL` como valor privado y genera `SECRET_KEY` automáticamente.

No se debe copiar `.env` a GitHub ni subir valores secretos al repositorio. Las variables privadas se configuran directamente en Render y en el entorno local autorizado.
