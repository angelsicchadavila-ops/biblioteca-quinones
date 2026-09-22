# Resultados de cierre de la Semana 9

Fecha de ejecución: 17 de septiembre de 2026.
Fecha de revisión de capturas finales: 22 de septiembre de 2026.

## Precondiciones

| Control | Resultado |
|---|---|
| Git antes de cambios | Limpio, rama `main`. |
| Sincronización remota | 0 commits por delante y 0 por detrás; `HEAD` y `origin/main` en `0f581cb`. |
| Semana 8 | Completa técnicamente; aprobada mediante autorización expresa de inicio de Semana 9. |
| Documento Maestro | 242 párrafos, 32 tablas; Semana 9 limitada a documentación y cierre. |
| Registro de cambios | Sin cambios estructurales posteriores a v1.0. |

## Render y HTTPS

Se ejecutó:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_produccion.py
```

Resultado: **32/32 comprobaciones correctas**.

Cobertura de la prueba:

- catálogo público por HTTPS;
- API interna bloqueada al público;
- login público disponible;
- cookie `Secure` y `HttpOnly`;
- formulario con CSRF;
- autenticación admin y asistente;
- panel admin, materias, libros, préstamos y cuatro reportes;
- terminal y búsqueda de lectores;
- endpoints QR/PDF protegidos;
- bloqueo HTTP 403 para asistente en rutas administrativas;
- logout y pérdida de acceso administrativo.

La primera conexión incluyó la demora compatible con *cold start*; la aplicación respondió correctamente. Se inspeccionó además el catálogo en navegador: URL HTTPS, diseño cargado, filtros de materia/nivel y estado sin títulos, sin error visible.

## Neon

Se ejecutó:

```powershell
.\.venv\Scripts\python.exe scripts\verificar_bd.py
```

Resultado: **7/7 verificaciones correctas**.

- seis tablas del DER;
- restricciones esenciales;
- índices funcionales y de búsqueda;
- triggers de materia activa y préstamos;
- cinco materias iniciales;
- dos cuentas de prueba con roles válidos;
- cero libros, ejemplares, lectores o préstamos temporales restantes.

## Pruebas funcionales seleccionadas

### QR

Se ejecutaron dos pruebas:

- contenido exacto y formato PNG del QR;
- generación/reimpresión administrativa sin modificar `codigo_qr`.

Resultado: **2/2 correctas en 9,790 s**.

### Préstamos, devolución, semáforo y reportes

Se ejecutaron dos pruebas integrales seleccionadas:

- búsqueda/creación de lector, plazos, límite, devolución e historial;
- estados, permisos, listado, semáforo y reportes.

Resultado: **2/2 correctas en 57,272 s**.

Estas pruebas usan identificadores temporales y limpieza de clase. La verificación final de Neon se repite después de todo el cierre para confirmar ausencia de residuos.

## Seguridad y repositorio

| Control | Resultado |
|---|---|
| `.env` versionado | No. |
| `.env` ignorado | Sí, regla explícita en `.gitignore`. |
| Valores reales en `.env.example` | No; solo marcadores. |
| Contraseñas en documentación final | No. |
| `DATABASE_URL` o `SECRET_KEY` reales en documentación | No. |
| Hashes de contraseña | Werkzeug, comprobado en cierres previos y Neon. |
| CSRF y permisos backend | Correctos en smoke. |
| Archivos temporales innecesarios | No detectados; los archivos TEMP de Semana 8 son evidencia histórica. |
| Escaneo final de secretos versionados | Correcto: sin tokens ni claves privadas; solo marcador PostgreSQL ficticio en `.env.example`; `.env` no versionado. |

## Revisión documental

Se verificará automáticamente:

- presencia de los archivos obligatorios;
- encabezados y marcadores administrativos;
- URL consistente;
- ausencia de secretos conocidos;
- enlaces Markdown locales;
- `git diff --check`.

Resultado final: **10/10 archivos obligatorios presentes; enlaces locales correctos; `compileall` correcto; `pip check` sin dependencias rotas; `git diff --check` sin errores**. Los avisos LF/CRLF son informativos del entorno Windows.

## Git final

- Commit de contenido: `69f6d0b` (`docs: cerrar semana 9 y preparar entrega v1.0`).
- Push del contenido: correcto, `0f581cb..69f6d0b main -> main`.
- Commit de registro final: el commit que contiene este archivo actualizado; consultar `git log -1`.
- Verificación definitiva de divergencia y árbol: se ejecuta después de publicar el registro final y queda informada en el resumen de cierre.

## Evidencia visual final

Se revisaron las cinco capturas finales: catálogo público por HTTPS, panel administrativo, terminal QR, módulo de reportes y panel de Render. Todas fueron aprobadas y quedaron organizadas en `docs/evidencias/semana_09/capturas/`, sin secretos ni datos personales sensibles visibles.

La captura de Render muestra el servicio `Live` en el snapshot `0f581cb`, que contiene el último cambio funcional `83d1677`. Los commits posteriores ya publicados, `69f6d0b` y `407e6b8`, son documentales; la incorporación de las capturas también es documental. No se forzó un nuevo deployment.

## Resultado general

Smoke de aplicación, producción y Neon aprobados. Evidencias visuales finales aprobadas. No se detectó un error crítico en la operación final. La Semana 9 queda cerrada técnica y documentalmente. Los pendientes son institucionales o administrativos: cuenta definitiva, custodio, datos de responsables, entrega y firma.
