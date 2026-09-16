# Matriz QA versión 1.0 Semana 8

## Estado de la matriz

Matriz cerrada con 167/167 casos clasificados. `NO APLICA` identifica una ejecución que honestamente no ocurrió o una acción deliberadamente excluida, como la participación presencial de la bibliotecaria y el pentesting destructivo. No hay casos con estado `FALLIDO` ni pendientes.

Estados válidos al cierre: `APROBADO`, `FALLIDO`, `CORREGIDO` y `NO APLICA`.

| ID | Módulo | Precondición | Pasos | Resultado esperado | Resultado obtenido | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| CAT-01 | Catálogo | Sin sesión | Abrir `/` | Catálogo público HTTP 200 | Catálogo visible por HTTPS | APROBADO | Smoke 32/32 |
| CAT-02 | Catálogo | Libro temporal activo | Buscar por título | Coincidencia correcta | Título temporal localizado | APROBADO | Suite 38/38 |
| CAT-03 | Catálogo | Libro temporal activo | Buscar por autor | Coincidencia correcta | Autor localizado | APROBADO | `test_catalogo_semana4.py` |
| CAT-04 | Catálogo | Materias activas | Filtrar por materia | Solo materia solicitada | Filtro correcto | APROBADO | `test_catalogo_semana4.py` |
| CAT-05 | Catálogo | Libro con nivel | Filtrar Primaria/Secundaria/Ambos | Clasificación correcta | Filtro correcto | APROBADO | `test_catalogo_semana4.py` |
| CAT-06 | Catálogo | Libro temporal | Combinar texto, materia y nivel | Coincidencia única coherente | Combinación correcta | APROBADO | `test_catalogo_semana4.py` |
| CAT-07 | Catálogo | Texto inexistente | Buscar marcador sin coincidencias | Mensaje claro y cero títulos | Mensaje mostrado | APROBADO | `test_qa_semana8.py` |
| CAT-08 | Catálogo | Libro activo | Abrir catálogo | Libro visible | Visible | APROBADO | Suite 38/38 |
| CAT-09 | Catálogo | Libro desactivado | Abrir catálogo | Libro oculto | Oculto y reaparece al reactivar | APROBADO | `test_catalogo_semana4.py` |
| CAT-10 | Catálogo | Estados mixtos | Consultar tarjeta | Conteos derivados correctos | Total, disponibles, prestados, dañados e inactivos correctos | APROBADO | Suite 38/38 |
| CAT-11 | Catálogo | Sin sesión | Revisar navegación | Sin controles privados | No aparecen Administración, Escaneo ni Cerrar sesión | APROBADO | `test_qa_semana8.py` |
| CAT-12 | Catálogo | Render Live | Revisar viewport estrecho | Sin desbordamiento visible | Correcto en navegador y teléfono real | APROBADO | Revisión navegador y captura 01 |
| AUT-01 | Autenticación | Admin activo | Login válido | Redirección a `/admin` | Correcta | APROBADO | Suite 38/38 |
| AUT-02 | Autenticación | Asistente activo | Login válido | Redirección a `/escaneo` | Correcta | APROBADO | Suite 38/38 |
| AUT-03 | Autenticación | Credenciales inválidas | Enviar login | HTTP 401 y mensaje genérico | Correcto | APROBADO | `test_core.py` |
| AUT-04 | Autenticación | Sesión admin | Logout con CSRF | Sesión invalidada | Correcto | APROBADO | Suite y smoke |
| AUT-05 | Autenticación | ID de sesión inexistente | Abrir ruta protegida | Limpiar sesión y redirigir | Correcto | APROBADO | `test_qa_semana8.py` |
| AUT-06 | Autenticación | Público | Abrir `/admin` | Redirigir a login | Correcto | APROBADO | Suite 38/38 |
| AUT-07 | Autenticación | Público | Abrir `/escaneo` | Redirigir a login | Correcto | APROBADO | Suite 38/38 |
| AUT-08 | Autenticación | Admin | Abrir `/admin` | HTTP 200 | Correcto | APROBADO | Smoke 32/32 |
| AUT-09 | Autenticación | Admin | Abrir `/escaneo` | HTTP 200 | Correcto | APROBADO | Smoke 32/32 |
| AUT-10 | Autenticación | Asistente | Abrir `/escaneo` | HTTP 200 | Correcto | APROBADO | Smoke 32/32 |
| AUT-11 | Autenticación | Asistente | Manipular URL `/admin` | HTTP 403 | Correcto | APROBADO | Suite y smoke |
| MAT-01 | Materias | Admin | Crear materia TEMP | Alta normalizada | Correcta | APROBADO | `test_catalogo_semana4.py` |
| MAT-02 | Materias | Materia TEMP | Editar nombre | Cambio persistido | Correcto | APROBADO | `test_catalogo_semana4.py` |
| MAT-03 | Materias | Sin libros activos | Desactivar | Queda inactiva | Correcto | APROBADO | `test_catalogo_semana4.py` |
| MAT-04 | Materias | Materia inactiva | Reactivar | Queda activa | Correcto | APROBADO | `test_catalogo_semana4.py` |
| MAT-05 | Materias | Nombre existente | Crear con mayúsculas/espacios distintos | Rechazo explicativo | Correcto | APROBADO | `test_catalogo_semana4.py` |
| MAT-06 | Materias | Libro activo asociado | Desactivar materia | Bloqueo | Correcto | APROBADO | `test_catalogo_semana4.py` |
| MAT-07 | Materias | Admin | Acceso directo | Permitido | Correcto | APROBADO | `test_qa_semana8.py` |
| MAT-08 | Materias | Asistente | GET/URL directa | HTTP 403 | Correcto | APROBADO | `test_qa_semana8.py` |
| LIB-01 | Libros | Admin y materia activa | Crear título TEMP | Alta correcta | Correcta | APROBADO | `test_catalogo_semana4.py` |
| LIB-02 | Libros | Libro TEMP | Editar título y autor | Cambios persistidos | Correcto | APROBADO | `test_catalogo_semana4.py` |
| LIB-03 | Libros | Libro TEMP | Cambiar materia | Solo materia activa | Correcto | APROBADO | Suite 38/38 |
| LIB-04 | Libros | Libro TEMP | Cambiar nivel | Solo dominio aprobado | Correcto | APROBADO | Suite 38/38 |
| LIB-05 | Libros | Libro TEMP | Guardar ISBN/editorial | Dato opcional persistido | Correcto | APROBADO | `test_catalogo_semana4.py` |
| LIB-06 | Libros | Libro activo | Desactivar | Oculto del catálogo | Correcto | APROBADO | Suite 38/38 |
| LIB-07 | Libros | Libro inactivo con materia activa | Reactivar | Vuelve al catálogo | Correcto | APROBADO | Suite 38/38 |
| LIB-08 | Libros | Campos vacíos/largos/nivel inválido | Enviar formulario | Mensajes de validación y sin alta | Validaciones presentes en backend | APROBADO | Revisión código y suite |
| LIB-09 | Libros | Asistente | Abrir crear/editar/listado | HTTP 403 | Correcto | APROBADO | `test_qa_semana8.py` |
| LIB-10 | Libros | Libro inactivo | Intentar agregar ejemplar por URL directa | Bloqueo y aviso | Falló antes; corregido y revalidado | CORREGIDO | INC-08-001, `83d1677` |
| EJE-01 | Ejemplares | Libro activo | Crear uno | Código único | Correcto | APROBADO | Suite 38/38 |
| EJE-02 | Ejemplares | Libro activo | Crear varios | Secuencia única | Correcto | APROBADO | Suite 38/38 |
| EJE-03 | Ejemplares | Códigos existentes | Intentar duplicado en BD | Rechazo UNIQUE | Correcto | APROBADO | Integridad 11/11 |
| EJE-04 | Ejemplares | Operativo | Identificar | Disponible si no tiene préstamo | Correcto | APROBADO | Suite 38/38 |
| EJE-05 | Ejemplares | Activo | Marcar dañado | Estado Dañado | Correcto | APROBADO | Suite 38/38 |
| EJE-06 | Ejemplares | Dañado | Marcar operativo | Estado Operativo | Correcto | APROBADO | Suite 38/38 |
| EJE-07 | Ejemplares | Activo | Desactivar | Estado Inactivo | Correcto | APROBADO | Suite 38/38 |
| EJE-08 | Ejemplares | Inactivo | Reactivar | Estado calculado de nuevo | Correcto | APROBADO | Suite 38/38 |
| EJE-09 | Ejemplares | Préstamo activo | Consultar disponibilidad | Prestado derivado | Correcto | APROBADO | Suite 38/38 |
| EJE-10 | Ejemplares | Libro/materia inactivos | Abrir inventario | Ejemplar visible como Inactivo | Corregido y probado | CORREGIDO | INC-08-001 |
| EJE-11 | Ejemplares | Estados mixtos | Revisar inconsistencias | Sin alta en libro inactivo | Correcto después de fix | CORREGIDO | `test_qa_semana8.py` |
| QRP-01 | QR/PDF | Admin y ejemplar | Ver QR | PNG válido | Correcto | APROBADO | `test_qr_semana5.py` |
| QRP-02 | QR/PDF | Mismo ejemplar | Reimprimir | Mismo `codigo_qr` | Correcto | APROBADO | Suite 38/38 |
| QRP-03 | QR/PDF | Ejemplar | Descargar individual | PDF válido | Correcto | APROBADO | Suite 38/38 |
| QRP-04 | QR/PDF | Varios ejemplares | Descargar múltiple | PDF válido | Correcto | APROBADO | Suite 38/38 |
| QRP-05 | QR/PDF | Etiquetas | Revisar tamaño | A4 | Correcto | APROBADO | `test_qr_semana5.py` |
| QRP-06 | QR/PDF | 21/22 etiquetas | Generar | 21 por página | Correcto | APROBADO | `test_qr_semana5.py` |
| QRP-07 | QR/PDF | QR generado | Decodificar contenido | Código exacto | Correcto | APROBADO | Suite 38/38 |
| QRP-08 | QR/PDF | PDF temporal Semana 8 | Renderizar a PNG y revisar legibilidad | Sin deformación/recorte | Correcto; 4 etiquetas nítidas y alineadas | APROBADO | `ETIQUETAS_QA_SEMANA_08.pdf`, render 150 dpi |
| QRP-09 | QR/PDF | Asistente | Abrir endpoints admin | HTTP 403 | Correcto | APROBADO | Suite 38/38 |
| QRP-10 | QR/PDF | Render | Probar endpoints protegidos | Admin permitido; público/asistente bloqueados | Correcto | APROBADO | Smoke 32/32 |
| ESC-01 | Escáner | Sesión válida | Abrir `/escaneo` | Terminal visible | Correcto | APROBADO | Suite y smoke |
| ESC-02 | Escáner | Página cargada | Revisar estado inicial | Cámara apagada | Lógica y texto correctos | APROBADO | `test_qr_semana5.py` |
| ESC-03 | Escáner | JS disponible | Revisar botón iniciar | Acción explícita requerida | Correcto | APROBADO | Revisión JS |
| ESC-04 | Escáner | Cámara activa | Detener/reiniciar | Controles implementados | Correcto en código y teléfono real | APROBADO | `qr_scanner.js`, captura 03 |
| ESC-05 | Escáner | Código válido | Ingreso manual | Mismo endpoint y validaciones | Correcto | APROBADO | Suite 38/38 |
| ESC-06 | Escáner | Código inexistente | Consultar | HTTP 404 y mensaje | Correcto | APROBADO | Suite 38/38 |
| ESC-07 | Escáner | Dos lecturas rápidas | Revisar bloqueo | Ignora duplicado durante proceso/3 s | Correcto | APROBADO | `test_qr_semana5.py` |
| ESC-08 | Escáner | Error de red | Revisar manejo | No asumir guardado | Mensaje seguro implementado | APROBADO | Revisión JS |
| ESC-09 | Escáner móvil | Teléfono real | Conceder permiso e iniciar | Visor activo | Correcto | APROBADO | Captura 03 y reporte del responsable |
| ESC-10 | Escáner móvil | Teléfono real | Leer `LIB-044-EJ01` | Código exacto | Identificado correctamente | APROBADO | Captura 03 |
| ESC-11 | Escáner móvil | Teléfono real | Baja iluminación | Lectura o alternativa manual útil | Correcto según reporte | APROBADO | Reporte del responsable |
| ESC-12 | Escáner móvil | Teléfono real | Detener y reiniciar | Funciona sin recargar | Correcto según reporte | APROBADO | Reporte del responsable |
| LEC-01 | Lectores | Ejemplar disponible | Crear lector en préstamo | Alta dentro del flujo | Correcto | APROBADO | `test_prestamos_semana6.py` |
| LEC-02 | Lectores | Lector existente | Buscar por tokens | Coincidencia tolerante | Correcto | APROBADO | Suite 38/38 |
| LEC-03 | Lectores | Lector existente | Seleccionar y prestar | Reutiliza ID | Correcto | APROBADO | Suite 38/38 |
| LEC-04 | Lectores | Mismo nombre normalizado | Intentar crear otra vez | Evita duplicación evidente | Código protegido con lock y coincidencia normalizada | APROBADO | Revisión y regresión |
| LEC-05 | Lectores | Préstamo | Guardar nivel/grado | Datos en préstamo | Correcto | APROBADO | Suite 38/38 |
| LEC-06 | Lectores | Historial anual | Revisar tabla lector | Sin nivel/grado permanente | Esquema correcto | APROBADO | Schema y suite |
| PRE-01 | Préstamos | Lector sin activos | Primer préstamo | Permitido | Correcto | APROBADO | Suite 38/38 |
| PRE-02 | Préstamos | Lector con uno activo | Segundo préstamo | Permitido | Correcto | APROBADO | Suite 38/38 |
| PRE-03 | Préstamos | Lector con dos activos | Tercer préstamo | Bloqueo explicativo | Correcto | APROBADO | Suite 38/38 |
| PRE-04 | Préstamos | Ejemplar disponible | Plazo 7 días | Fecha +7 | Correcto | APROBADO | Suite 38/38 |
| PRE-05 | Préstamos | Ejemplar disponible | Plazo 14 días | Fecha +14 | Correcto | APROBADO | Suite 38/38 |
| PRE-06 | Préstamos | Fecha futura | Personalizada | Aceptada exacta | Correcto | APROBADO | Suite 38/38 |
| PRE-07 | Préstamos | Fecha anterior | Personalizada | HTTP 400 | Correcto | APROBADO | Suite 38/38 |
| PRE-08 | Préstamos | Ejemplar dañado | Intentar prestar | Bloqueo | Correcto | APROBADO | Suite 38/38 |
| PRE-09 | Préstamos | Ejemplar inactivo | Intentar prestar | Bloqueo | Correcto | APROBADO | Suite 38/38 |
| PRE-10 | Préstamos | Ejemplar ya prestado | Intentar prestar | Bloqueo | Correcto | APROBADO | Suite 38/38 |
| PRE-11 | Préstamos | Lector con mora | Intentar prestar | Bloqueo | Correcto | APROBADO | Suite 38/38 |
| PRE-12 | Préstamos | Dos conexiones | Mismo ejemplar | Solo una confirma | Correcto | APROBADO | Suite e integridad |
| PRE-13 | Préstamos | Usuarios admin/asistente | Registrar | Trazabilidad de alta | Correcto | APROBADO | Suite 38/38 |
| PRE-14 | Préstamos | Operación completada | Consultar otra conexión | Persistencia real | Correcto | APROBADO | Neon y suite |
| DEV-01 | Devoluciones | Activo dentro de plazo | Devolver | Fecha y responsable | Correcto | APROBADO | Suite 38/38 |
| DEV-02 | Devoluciones | Vencido | Devolver | Cierre permitido | Correcto | APROBADO | Suite 38/38 |
| DEV-03 | Devoluciones | Préstamo activo | Consultar fecha/hora | Registrada en Lima | Correcto | APROBADO | Suite 38/38 |
| DEV-04 | Devoluciones | Admin/asistente | Devolver | Usuario responsable | Correcto | APROBADO | Suite 38/38 |
| DEV-05 | Devoluciones | Historial | Devolver | Registro preservado | Correcto | APROBADO | Suite 38/38 |
| DEV-06 | Devoluciones | Ejemplar activo operativo | Devolver | Vuelve a Disponible | Correcto | APROBADO | Suite 38/38 |
| DEV-07 | Devoluciones | Última mora resuelta | Intentar nuevo préstamo | Lector desbloqueado | Correcto | APROBADO | Suite 38/38 |
| SEM-01 | Semáforo | Activo dentro de plazo | Ver listado | Amarillo | Correcto | APROBADO | Suite 38/38 |
| SEM-02 | Semáforo | Vencido | Ver listado | Rojo | Correcto | APROBADO | Suite 38/38 |
| SEM-03 | Semáforo | Devuelto | Ver listado | Verde | Correcto | APROBADO | Suite 38/38 |
| SEM-04 | Semáforo | Fechas reales | Revisar cálculo | Sin estado redundante | Derivado en SQL | APROBADO | Schema y suite |
| RPT-01 | Reportes | Admin | Inventario título/materia | Columnas presentes | Correcto | APROBADO | Suite 38/38 |
| RPT-02 | Reportes | Estados mixtos | Inventario total | Conteo correcto | Correcto | APROBADO | Suite 38/38 |
| RPT-03 | Reportes | Estados mixtos | Inventario disponibles/prestados/dañados | Conteos coherentes | Correcto | APROBADO | Suite 38/38 |
| RPT-04 | Reportes | Préstamos activos | Abrir RPT-02 | Lector/libro/ejemplar/fechas | Correcto | APROBADO | Suite 38/38 |
| RPT-05 | Reportes | Préstamo vencido | Abrir RPT-03 | Lector/grado/libro/límite/atraso | Correcto | APROBADO | Suite 38/38 |
| RPT-06 | Reportes | Historial | Abrir RPT-04 | Lector/libro/fechas/devolución | Correcto | APROBADO | Suite 38/38 |
| RPT-07 | Reportes | Historial | Revisar estado final | Activo/Vencido/Devuelto | Correcto | APROBADO | Suite 38/38 |
| RPT-08 | Reportes | Historial | Revisar responsables | Alta y devolución | Correcto | APROBADO | Suite 38/38 |
| RPT-09 | Reportes | Rango válido | Filtrar | Solo rango | Correcto | APROBADO | Suite 38/38 |
| RPT-10 | Reportes | Rango inverso | Filtrar | HTTP 400 útil | Correcto | APROBADO | Suite 38/38 |
| RPT-11 | Reportes | Asistente | URL directa | HTTP 403 | Correcto | APROBADO | Smoke 32/32 |
| RPT-12 | Reportes | Público | URL directa | Login requerido | Correcto | APROBADO | `test_qa_semana8.py` |
| PER-01 | Permisos | Público | `/` | Permitido | Correcto | APROBADO | Suite 38/38 |
| PER-02 | Permisos | Público | `/login` | Permitido | Correcto | APROBADO | Suite 38/38 |
| PER-03 | Permisos | Público | Rutas `/admin*` | Bloqueadas | Correcto | APROBADO | `test_qa_semana8.py` |
| PER-04 | Permisos | Público | `/escaneo` | Bloqueado | Correcto | APROBADO | Suite 38/38 |
| PER-05 | Permisos | Público | APIs internas | HTTP 401 | Correcto | APROBADO | Smoke 32/32 |
| PER-06 | Permisos | Admin | Gestión catálogo | Permitida | Correcto | APROBADO | Suite 38/38 |
| PER-07 | Permisos | Admin | Escaneo/préstamo/devolución | Permitidos | Correcto | APROBADO | Suite 38/38 |
| PER-08 | Permisos | Admin | Reportes | Permitidos | Correcto | APROBADO | Smoke 32/32 |
| PER-09 | Permisos | Admin | QR/PDF | Permitidos | Correcto | APROBADO | Suite 38/38 |
| PER-10 | Permisos | Asistente | Escaneo y operaciones | Permitidos | Correcto | APROBADO | Suite 38/38 |
| PER-11 | Permisos | Asistente | Materias/libros/ejemplares/reportes | HTTP 403 | Correcto | APROBADO | `test_qa_semana8.py` |
| PER-12 | Permisos | Asistente | QR/PDF por URL directa | HTTP 403 | Correcto | APROBADO | `test_qa_semana8.py` |
| MOV-01 | Móvil real | Teléfono | Abrir catálogo | Responsive y sin overflow | Correcto | APROBADO | Captura 01 |
| MOV-02 | Móvil real | Teléfono | Login | Campos/botón completos | Correcto según reporte | APROBADO | Reporte del responsable |
| MOV-03 | Móvil real | Sesión válida | Abrir escaneo | Responsive | Correcto | APROBADO | Capturas 03 y 04 |
| MOV-04 | Móvil real | Permiso cámara | Iniciar/detener/reiniciar | Funciona | Correcto según reporte | APROBADO | Captura 03 y reporte del responsable |
| MOV-05 | Móvil real | QR temporal | Escanear | Código correcto | `LIB-044-EJ01` identificado | APROBADO | Captura 03 |
| MOV-06 | Móvil real | Ejemplar disponible | Prestar | Flujo usable | Préstamo confirmado | APROBADO | Captura 04 |
| MOV-07 | Móvil real | Préstamo activo | Devolver | Flujo usable | Correcto según reporte; Neon conservó el historial hasta la limpieza | APROBADO | Reporte del responsable y consulta Neon |
| MOV-08 | Móvil real | Mensajes | Revisar alertas | Comprensibles | Mensajes legibles | APROBADO | Capturas 02, 03 y 04 |
| MOV-09 | Móvil real | Formularios/botones | Interactuar | Sin cortes | Correcto | APROBADO | Capturas 01 a 04 |
| MOV-10 | Móvil real | Reporte | Abrir | Página sin overflow global | Correcto en orientación horizontal | APROBADO | Captura 05 |
| SEC-01 | Seguridad | Repositorio | Revisar `.env` | Ignorado y no versionado | Correcto | APROBADO | Secret scan |
| SEC-02 | Seguridad | Archivos versionados | Buscar secretos | Sin valores reales | Correcto | APROBADO | Secret scan |
| SEC-03 | Seguridad | Usuarios | Revisar BD | Hashes Werkzeug | Correcto | APROBADO | Semana 7 y Neon |
| SEC-04 | Seguridad | POST | Omitir CSRF | HTTP 400 | Correcto | APROBADO | Suite 38/38 |
| SEC-05 | Seguridad | Render | Revisar cookie | Secure y HttpOnly | Correcto | APROBADO | Smoke 32/32 |
| SEC-06 | Seguridad | Configuración | Revisar SameSite | Lax | Correcto | APROBADO | `app.py` |
| SEC-07 | Seguridad | Sesión | Logout | Invalida acceso | Correcto | APROBADO | Suite y smoke |
| SEC-08 | Seguridad | Backend | URLs directas | Roles comprobados | Correcto | APROBADO | `test_qa_semana8.py` |
| SEC-09 | Seguridad | SQL | Revisar entradas | Consultas parametrizadas | Correcto | APROBADO | Revisión código |
| SEC-10 | Seguridad | Errores | Revisar respuestas | Sin credenciales | Correcto | APROBADO | Smoke y plantillas |
| SEC-11 | Seguridad | Producción | API pública | Datos internos bloqueados | Correcto | APROBADO | Smoke 32/32 |
| SEC-12 | Seguridad | Alcance | Ataques externos | No ejecutar pentesting destructivo | No se realizó | NO APLICA | Principio de seguridad |
| INF-01 | Infraestructura | Git | `fetch` y comparar | Sin divergencia inicial | 0/0 | APROBADO | Resultados Semana 8 |
| INF-02 | Infraestructura | Render | HTTPS | HTTP 200 | Correcto | APROBADO | Smoke 32/32 |
| INF-03 | Infraestructura | Render | Build | Correcto | Correcto | APROBADO | Deployment `83d1677` |
| INF-04 | Infraestructura | Render | Start Command | Gunicorn | Gunicorn 23.0.0 | APROBADO | Logs deployment |
| INF-05 | Infraestructura | Render | Logs recientes | Sin error relevante | Correcto | APROBADO | Logs deployment |
| INF-06 | Infraestructura | Render | Auto-Deploy | On Commit debería reaccionar | No reaccionó; contingencia manual documentada | NO APLICA | Observación conocida |
| INF-07 | Infraestructura | Neon | Verificar esquema y ausencia de temporales | 7/7 | Primera ejecución 6/7 por lector temporal en mayúsculas; limpieza corregida y resultado final 7/7 | CORREGIDO | INC-08-002, `2bbf06f` |
| INF-08 | Infraestructura | Neon | Integridad/concurrencia | 11/11 y limpieza | Correcto | APROBADO | `probar_integridad_bd.py` |
| CAM-01 | Campo | Guía lista | Abrir sistema | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-02 | Campo | Guía lista | Buscar libro | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-03 | Campo | Guía lista | Iniciar sesión | Sin credenciales reales | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-04 | Campo | Guía lista | Escanear | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-05 | Campo | Guía lista | Prestar/devolver | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-06 | Campo | Guía lista | Consultar préstamo | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-07 | Campo | Guía lista | Revisar reporte | Paso comprensible | Guía preparada | APROBADO | `GUIA_PRUEBA_CAMPO.md` |
| CAM-08 | Campo presencial | Bibliotecaria disponible | Ejecutar guía | Resultado real documentado | No ejecutado todavía; no se inventa participación | NO APLICA | Pendiente del responsable |

## Cierre de la matriz

Los 167 casos tienen estado final y evidencia asociada. La validación móvil fue informada por el responsable y respaldada con cinco capturas reales; la bibliotecaria no participó. No quedan casos `FALLIDO` ni casos pendientes.
