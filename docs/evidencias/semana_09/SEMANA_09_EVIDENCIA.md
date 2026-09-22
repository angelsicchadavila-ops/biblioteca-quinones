# Evidencia técnica y documental de la Semana 9

## Estado

Semana 9 cerrada técnica y documentalmente como fase final de la versión 1.0. No se añadieron funcionalidades ni se modificaron reglas de negocio, arquitectura, esquema, roles o permisos. Las cinco capturas finales fueron incorporadas y revisadas el 22 de septiembre de 2026. La entrega formal a la institución, la cuenta institucional definitiva, los datos administrativos y la firma de conformidad permanecen pendientes del estudiante.

## Fuente de verdad y continuidad

Antes de modificar el proyecto se revisaron:

- `AGENTS.md` completo;
- Documento Maestro v1.0, con 242 párrafos y 32 tablas;
- `docs/ESTADO_PROYECTO.md`;
- `docs/REGISTRO_CAMBIOS.md`;
- cierres y evidencias de Semanas 1 a 8;
- código, rutas, esquema, plantillas, scripts y pruebas;
- estado e historial Git.

La Semana 8 constaba como completa técnicamente y pendiente de aprobación expresa. La orden del usuario de iniciar oficialmente la Semana 9 constituye esa aprobación y se registra en el estado del proyecto.

## Documentos creados

En `docs/final/`:

- `README.md`;
- `MANUAL_USUARIO.md`;
- `MANUAL_TECNICO.md`;
- `MEMORIA_FINAL_PROYECTO.md`;
- `GUIA_ENTREGA_INSTITUCIONAL.md`;
- `CHECKLIST_CIERRE.md`;
- `PLANTILLA_ACTA_CONFORMIDAD.md`.

En `docs/evidencias/semana_09/`:

- `SEMANA_09_EVIDENCIA.md`;
- `RESULTADOS_CIERRE.md`;
- `CHECKLIST_ENTREGA.md`;
- `capturas/INSTRUCCIONES_CAPTURAS.md`;
- cinco capturas finales verificadas en `capturas/`.

## Smoke final ejecutado

| Verificación | Resultado real |
|---|---|
| Render por HTTPS | Correcto; catálogo y rutas de producción respondieron. |
| Smoke `verificar_produccion.py` | 32/32 comprobaciones correctas. |
| Login admin | Correcto, sin imprimir credencial. |
| Login asistente | Correcto, sin imprimir credencial. |
| Catálogo público | Correcto por HTTPS y revisado visualmente. |
| QR/reimpresión | 2/2 pruebas seleccionadas correctas. |
| Préstamo/devolución/historial | Prueba integral seleccionada correcta. |
| Semáforo y reportes | Prueba integral seleccionada correcta; cuatro reportes accesibles en producción. |
| Neon | 7/7 verificaciones correctas. |
| Logout y sesión | Correctos. |
| Permisos | Público, admin y asistente respondieron según rol. |

No se repitió la matriz exhaustiva de Semana 8. El smoke se limitó a producción de solo lectura y cuatro pruebas funcionales seleccionadas con limpieza controlada.

## Seguridad de cierre

- `.env` permanece ignorado y no versionado.
- `.env.example` contiene marcadores, no secretos.
- Las contraseñas reales no se escribieron en documentos ni evidencias.
- La base conserva hashes Werkzeug.
- Render usa cookies seguras y CSRF.
- Las variables privadas permanecen en entorno local o Render.
- Neon no contiene datos temporales operativos.
- `QR_TEMP_SEMANA_08.png` y el PDF de QA son evidencias históricas versionadas; no representan datos activos en Neon.
- El escaneo final no detectó tokens, claves privadas ni cadenas PostgreSQL reales. La única coincidencia de URL PostgreSQL fue el marcador ficticio de `.env.example`; `.env` no está versionado.

## Observaciones y limitaciones documentadas

- La versión desplegada no contiene una pantalla para autogestionar cuentas internas. La cuenta institucional debe crearse o actualizarse mediante mantenimiento técnico autorizado, con hash, y las cuentas de prueba deben desactivarse cuando se confirme el acceso definitivo.
- Auto-Deploy de Render ha sido intermitente. `Deploy latest commit` continúa documentado como contingencia.
- La prueba de campo con bibliotecaria no se realizó en Semana 8 y no se afirma lo contrario.
- El responsable del Documento Maestro sigue pendiente: `[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]`.
- El render interno del Documento Maestro no pudo repetirse por ausencia de `soffice.exe`; se revisó su contenido completo por extracción estructural y se conserva la evidencia visual de 16 páginas registrada en Semana 1.

## Capturas finales

Las cinco capturas solicitadas fueron incorporadas en `docs/evidencias/semana_09/capturas/` y revisadas visualmente. Todas son archivos PNG válidos; no muestran contraseñas, tokens, cadenas de conexión, claves privadas ni datos personales de lectores.

| Captura | Dimensiones | Verificación | Resultado |
|---|---:|---|---|
| `01_catalogo_publico_live_semana09.png` | 1902 × 962 | URL pública por HTTPS, catálogo y filtros visibles. | Aprobada. |
| `02_panel_admin_semana09.png` | 1912 × 872 | Panel administrativo y rol `admin` visibles, sin credenciales. | Aprobada. |
| `03_terminal_qr_semana09.png` | 1897 × 852 | Terminal QR, control de cámara e ingreso manual visibles. | Aprobada. |
| `04_reporte_semana09.png` | 1912 × 870 | Módulo Reportes v1.0 y reportes RPT-01 a RPT-04 visibles. | Aprobada. |
| `05_render_live_semana09.png` | 1891 × 872 | Servicio `biblioteca-quinones`, rama `main`, HTTPS y estado `Live`; snapshot desplegado `0f581cb`. | Aprobada. |

La captura 05 demuestra que Render continúa `Live` sobre el snapshot `0f581cb`. Ese snapshot contiene el último cambio funcional de la aplicación, `83d1677`; los commits posteriores a `0f581cb` que existían antes de incorporar estas capturas (`69f6d0b` y `407e6b8`) son exclusivamente documentales. El presente cierre solo agrega documentación y evidencias visuales. Por ello no se forzó ni se requiere un deployment adicional.

## Git y publicación

- Estado inicial: limpio en `main`.
- Sincronización inicial: `main...origin/main` = 0/0 en `0f581cb`.
- Commit documental: `69f6d0b` (`docs: cerrar semana 9 y preparar entrega v1.0`).
- Registro documental posterior: `407e6b8` (`docs: registrar cierre final de semana 9`).
- Push del contenido a `origin/main`: correcto.
- El commit que incorpora las capturas y esta validación completa el cierre visual/documental; su hash se consulta con `git log -1` para evitar autorreferencia imposible dentro del propio commit.
- No se solicitó deployment de Render porque no hubo cambios funcionales posteriores al snapshot desplegado `0f581cb`.

## Criterios de cierre

Los cinco documentos finales mínimos, la plantilla de acta y las cinco capturas finales están preparados y revisados. El smoke, Neon, revisión de seguridad y cierre documental están aprobados. La Semana 9 queda cerrada técnica y documentalmente. La entrega institucional, la entrega de credenciales por canal privado y la firma no se declaran realizadas.
