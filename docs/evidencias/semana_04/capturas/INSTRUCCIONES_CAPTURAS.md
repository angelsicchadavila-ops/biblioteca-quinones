# Instrucciones para capturas de la Semana 4

Guarda todas las imágenes en esta misma carpeta:

`docs/evidencias/semana_04/capturas/`

Antes de capturar, verifica que ningún campo contenga usuario, contraseña, cadena de conexión, token o secreto.

## 01 Catálogo público en PC

- Abre `https://biblioteca-quinones.onrender.com/` en una ventana de escritorio.
- Deben verse el encabezado `Catálogo bibliográfico`, el campo `Título o autor`, los filtros `Materia` y `Nivel`, el botón `Buscar` y el área de resultados.
- Nombre: `01_catalogo_publico_pc.png`.

## 02 Materias administrativas

- Inicia sesión como administrador y abre `https://biblioteca-quinones.onrender.com/admin/materias`.
- Limpia cualquier credencial escrita antes de capturar.
- Deben verse el formulario `Nueva materia`, las cinco materias iniciales, sus estados y las acciones administrativas.
- Nombre: `02_materias_admin.png`.

## 03 Formulario de libro

- Abre `https://biblioteca-quinones.onrender.com/admin/libros/nuevo`.
- No completes el formulario.
- Deben verse título, autor, nivel académico, materia e ISBN/editorial.
- Nombre: `03_nuevo_libro_admin.png`.

## 04 Catálogo público en móvil

- Abre `https://biblioteca-quinones.onrender.com/` desde un teléfono o desde el modo responsive del navegador con un ancho aproximado de 390 píxeles.
- Deben verse el encabezado, los tres filtros apilados, el botón `Buscar` y el área de resultados sin desbordamiento horizontal.
- Nombre: `04_catalogo_publico_movil.png`.

## 05 Deployment de Render

- En Render, abre el deployment del commit `a190a88`.
- Deben verse `feat: implementar catalogo y ejemplares`, `Deploy succeeded | Live` y el origen `a190a88`.
- No abras ni muestres la sección Environment ni el Deploy Hook.
- Nombre: `05_render_deploy_semana04.png`.

## 06 Bloqueo del asistente

- Cierra la sesión de administrador.
- Inicia sesión como asistente y abre `https://biblioteca-quinones.onrender.com/admin/libros`.
- Debe verse `Acceso denegado`; la barra de direcciones debe mostrar la ruta administrativa.
- No debe verse la contraseña.
- Nombre: `06_bloqueo_asistente_catalogo.png`.

## Captura opcional después de cargar datos reales

Cuando exista al menos un libro real con ejemplares, abre su listado de ejemplares y captura los códigos y estados visibles. No crees datos ficticios permanentes solo para esta imagen.

- Nombre sugerido: `07_ejemplares_admin.png`.
