# Checklist de cierre de la versión 1.0

Fecha de revisión técnica: 17 de septiembre de 2026.

Este checklist distingue el cierre técnico/documental de la entrega formal a la institución. Una casilla pendiente no debe presentarse como ejecutada.

## Documentación final

- [x] Manual de usuario terminado.
- [x] Manual técnico terminado.
- [x] Memoria final base terminada.
- [x] Guía de entrega institucional terminada.
- [x] Plantilla de acta creada.
- [x] Responsable no inventado; se usa `[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]`.
- [x] Credenciales y secretos excluidos de los documentos.
- [x] Mejoras futuras separadas de la versión 1.0.

## Operación final

- [x] URL pública respondió por HTTPS.
- [x] Catálogo público operativo.
- [x] Login administrador comprobado sin registrar la contraseña.
- [x] Login asistente comprobado sin registrar la contraseña.
- [x] Terminal QR accesible para ambos roles autorizados.
- [x] Generación/reimpresión QR comprobada mediante prueba controlada.
- [x] Préstamo y devolución comprobados mediante prueba controlada.
- [x] Límite de dos y mora respaldados por pruebas acumuladas y QA de Semana 8.
- [x] Semáforo y reportes comprobados mediante prueba controlada y smoke HTTPS.
- [x] Cierre de sesión comprobado.
- [x] Ausencia de errores críticos observados en el smoke final.

## Render y Neon

- [x] Render operativo por HTTPS; smoke de producción 32/32.
- [x] Cold start contemplado y documentado.
- [x] Gunicorn y comandos de deployment documentados.
- [x] Neon accesible.
- [x] Neon 7/7: tablas, restricciones, índices, triggers, seed y estado base.
- [x] Sin datos temporales operativos de pruebas.
- [x] Scripts SQL y de mantenimiento versionados.
- [x] Contingencia de Auto-Deploy documentada.

## Seguridad

- [x] `.env` ignorado y no versionado.
- [x] `.env.example` sin valores reales.
- [x] Variables privadas solo en entorno local/Render.
- [x] Contraseñas almacenadas como hashes Werkzeug.
- [x] SQL parametrizado en las operaciones de aplicación.
- [x] CSRF en solicitudes POST.
- [x] Cookie `Secure` y `HttpOnly` observada en producción.
- [x] Roles verificados en backend.
- [x] Documentación sin contraseñas, tokens, `DATABASE_URL` o `SECRET_KEY` reales.
- [x] Archivos con nombre TEMP de Semana 8 identificados como evidencia histórica; datos Neon asociados eliminados.

## Git y revisión documental

- [x] Rama de trabajo `main`.
- [x] Estado inicial limpio antes de Semana 9.
- [x] `main` y `origin/main` iniciaron con divergencia 0/0 en `0f581cb`.
- [x] Documento Maestro, estado y cierres de Semanas 1 a 8 revisados.
- [x] Semana 8 aprobada por la orden expresa de iniciar Semana 9.
- [x] Revisión de rutas, esquema, scripts, plantillas y dependencias.
- [ ] Commit documental final registrado en este checklist.
- [ ] Push final confirmado y repositorio limpio/sincronizado.

Las dos últimas casillas se completan después de crear y publicar el commit que contiene estos documentos.

## Evidencias de Semana 9

- [x] `SEMANA_09_EVIDENCIA.md` creado.
- [x] `RESULTADOS_CIERRE.md` creado.
- [x] `CHECKLIST_ENTREGA.md` creado.
- [x] Instrucciones para capturas finales mínimas creadas.
- [ ] Capturas finales manuales incorporadas y revisadas.

Las capturas son una acción manual del estudiante porque incluyen sesiones y paneles privados. No bloquean la validez de los resultados automatizados, pero deben incorporarse si la institución o evaluación académica exige evidencia visual de cierre.

## Limitaciones y decisiones pendientes

- [x] No se añadieron funcionalidades nuevas en Semana 9.
- [x] La aplicación real y los manuales distinguen `admin`, `asistente` y público.
- [x] Se documentó que la versión actual no tiene pantalla de autogestión de cuentas.
- [ ] Cuenta administrativa institucional definitiva creada o actualizada.
- [ ] Cuentas de prueba cambiadas, sustituidas o desactivadas.
- [ ] Custodio institucional de GitHub, Render, Neon y credenciales designado.
- [ ] Responsable del Documento Maestro completado por el estudiante.

## Entrega institucional

- [ ] Fecha y modalidad de entrega acordadas.
- [ ] Manuales entregados al colegio.
- [ ] URL de producción entregada.
- [ ] Credenciales entregadas por canal privado.
- [ ] Responsable institucional capacitado.
- [ ] Observaciones de recepción registradas.
- [ ] Acta o constancia firmada, si corresponde.

## Resultado

El sistema y la documentación están preparados para cierre técnico de la versión 1.0. La entrega institucional, las credenciales definitivas, las capturas manuales y las firmas continúan pendientes hasta que el estudiante las realice y registre.

