# Guía de capturas de la Semana 7

Las cuatro capturas de PC se guardaron en esta carpeta y fueron revisadas el 15 de septiembre de 2026. La tabla conserva las indicaciones de captura para trazabilidad. Los resultados de la revisión y los límites de cada imagen constan en `../SEMANA_07_EVIDENCIA.md`. No se repitieron capturas de módulos funcionales ya aceptadas en Semanas 4 a 6.

| Archivo exacto | Pantalla a abrir y contenido visible | Excluir del encuadre |
|---|---|---|
| `01_render_live_semana07.png` | Render → servicio `biblioteca-quinones` → Deploys. Mostrar nombre, fuente GitHub, rama `main`, estado `Live` y commit definitivo de Semana 7. | Perfil/cuenta, logs, variables de entorno, Deploy Hook. |
| `02_render_build_semana07.png` | Render → servicio → Settings → Build. Mostrar repositorio, rama `main`, Root Directory vacío, Build Command `pip install -r requirements.txt` y ausencia de filtros de rutas. | Cualquier otra sección que contenga secretos. |
| `03_render_deploy_semana07.png` | Render → servicio → Settings → Deploy. Recortar únicamente el bloque de Start Command `gunicorn app:app` y Auto-Deploy `On Commit`. | **No incluir el bloque Deploy Hook que aparece justo debajo**, aunque se muestre oculto. |
| `04_https_catalogo_semana07.png` | Navegador de PC en `https://biblioteca-quinones.onrender.com/`. Mostrar dominio HTTPS y página pública cargada después del redeploy. | Sesiones internas, credenciales, datos personales reales. |

No capturar `Environment`, `.env`, Neon Connection Details, Shell ni pantallas que contengan `DATABASE_URL`, `SECRET_KEY`, contraseñas, tokens o el Deploy Hook. Las verificaciones de esas áreas quedan respaldadas por las pruebas y la evidencia técnica sin valores sensibles. No se requiere captura móvil: HTTPS y escaneo móvil ya fueron documentados en Semanas 3, 5 y 6.
