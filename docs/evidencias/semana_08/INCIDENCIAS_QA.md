# Incidencias QA Semana 8

## INC-08-001 Alta de ejemplares en un libro inactivo

- Descripción: la ruta administrativa permitía crear ejemplares físicos nuevos para un libro desactivado. Después de crearlos, el catálogo público ocultaba el libro y el terminal consideraba inactivo el ejemplar, mientras la pantalla administrativa lo mostraba como Disponible.
- Severidad: media.
- Estado: CORREGIDO.
- Módulo: libros y ejemplares.
- Pasos para reproducir:
  1. Crear un libro temporal activo.
  2. Desactivar el libro.
  3. Abrir directamente `/admin/libros/<id>/ejemplares`.
  4. Enviar el formulario para crear un ejemplar.
- Resultado anterior: el sistema insertaba el ejemplar y mostraba `Se crearon 1 ejemplar(es)`; la tabla administrativa lo presentaba como Disponible pese a que el libro estaba inactivo.
- Resultado esperado: un libro inactivo conserva su inventario histórico, pero no admite nuevas altas; sus ejemplares deben mostrarse como Inactivo mientras el libro o la materia estén inactivos.
- Corrección:
  - validación de backend antes de crear ejemplares;
  - aviso visible que indica reactivar primero el libro;
  - ocultamiento del formulario de alta cuando el libro está inactivo;
  - disponibilidad administrativa derivada también de la activación del libro y la materia.
- Verificación antes/después:
  - antes: `test_04_no_se_crean_ejemplares_en_libro_inactivo` falló y demostró que se había creado un ejemplar;
  - después: la prueba puntual pasó, las cuatro pruebas nuevas pasaron y la suite completa terminó 38/38.
- Datos utilizados: registros aislados con marcador `TEMP-SEMANA-08`, eliminados por la propia prueba.
- Commit relacionado: `83d1677` (`fix: corregir inventario inactivo en QA semana 8`).
- Deployment relacionado: `83d1677`, despliegue manual `Deploy latest commit`, estado `Deploy succeeded | Live`.

## INC-08-002 Limpieza sensible a mayúsculas del lector temporal

- Descripción: el auxiliar de cierre localizaba al lector `Lector TEMP / SEMANA 08` mediante comparación exacta. La prueba móvil creó `LECTOR TEMP / SEMANA 08`; por ello la primera limpieza eliminó materia, libro, ejemplares y préstamo, pero dejó ese lector sin préstamos.
- Severidad: baja.
- Estado: CORREGIDO.
- Módulo: herramienta auxiliar de QA; no afecta el comportamiento funcional de la aplicación publicada.
- Pasos para reproducir:
  1. Preparar el conjunto `TEMP-SEMANA-08`.
  2. Crear el lector temporal usando mayúsculas.
  3. Ejecutar `scripts/datos_qa_semana8.py limpiar`.
  4. Ejecutar `scripts/verificar_bd.py`.
- Resultado anterior: la verificación final devolvía 6/7 porque quedaba un lector temporal sin préstamos.
- Resultado esperado: reconocer el marcador temporal con normalización de mayúsculas y espacios y limpiar exclusivamente ese lector, siempre que no tenga préstamos ajenos.
- Corrección:
  - comparación mediante `lower(btrim(...))` para nombres y apellidos;
  - posibilidad segura de completar la limpieza cuando solo queda el lector marcado;
  - conservación de la comprobación que cancela la limpieza si el lector tiene préstamos ajenos.
- Verificación antes/después:
  - antes: `verificar_bd.py` informó 6/7;
  - después: estado temporal 0/0/0/0/0 y `verificar_bd.py` terminó 7/7.
- Commit relacionado: `2bbf06f` (`fix: normalizar limpieza temporal semana 8`).

## Incidencias pendientes

No hay incidencias pendientes. Las dos incidencias reales detectadas quedaron corregidas y verificadas. La validación móvil no reveló nuevos defectos funcionales. La prueba presencial con bibliotecaria no se realizó y no se presenta como ejecutada.
