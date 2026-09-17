# Guía de entrega institucional del Sistema Web de Gestión Bibliotecaria con Control QR

## Finalidad

Esta guía organiza la entrega de la versión 1.0 al Colegio Privado José Abelardo Quiñones. La entrega se considera pendiente hasta que el estudiante proporcione los materiales, comunique las credenciales por un canal privado y, si corresponde, se firme la constancia.

## Componentes de la entrega

1. Sistema publicado en Render.
2. Base de datos alojada en Neon.
3. Código fuente almacenado en GitHub.
4. Manual de usuario entregado.
5. Manual técnico entregado.
6. URL de producción entregada.
7. Credenciales institucionales entregadas por canal privado.
8. Responsable institucional informado sobre el uso básico.
9. Constancia o acta de conformidad pendiente de firma si corresponde.

## Accesos principales

- Sistema: <https://biblioteca-quinones.onrender.com/>
- Repositorio: <https://github.com/angelsicchadavila-ops/biblioteca-quinones>
- Manuales: carpeta `docs/final/` del repositorio.
- Evidencias: carpeta `docs/evidencias/` del repositorio.

## Roles

| Rol | Uso recomendado |
|---|---|
| Administrador | Responsable de catálogo, inventario, QR, préstamos, reportes y configuración disponible. |
| Asistente | Personal que registra préstamos y devoluciones desde el terminal. |
| Público | Personas que consultan el catálogo sin cuenta. |

La institución debe conservar al menos una cuenta administrativa definitiva. Las cuentas de prueba existentes deben cambiarse, sustituirse o desactivarse antes de la entrega formal.

## Información que debe entregarse por canal privado

Nunca coloque estos datos en el repositorio, manuales, capturas, correo público ni acta visible:

- usuario y contraseña de la cuenta administrativa institucional;
- credenciales de asistentes, si se crean;
- acceso administrativo a Render;
- acceso administrativo a Neon;
- acceso o invitación privada al repositorio, si el repositorio no es público;
- `DATABASE_URL`;
- `SECRET_KEY`;
- tokens, Deploy Hook, claves de recuperación o respaldos con datos personales.

Use una reunión presencial, un gestor de contraseñas con uso compartido seguro o el canal privado aprobado por la institución. Entregue la URL pública por separado de las credenciales.

## Cuenta que debe conservar la institución

La institución debe conservar una cuenta con rol `admin` bajo custodia de una persona responsable. No use como cuenta definitiva un usuario personal del estudiante ni una contraseña de prueba.

Procedimiento recomendado:

1. Acordar un nombre de usuario institucional y un responsable custodio.
2. Crear o actualizar la cuenta mediante mantenimiento técnico autorizado.
3. Generar la contraseña sin incluirla en archivos versionados.
4. Verificar login y permisos.
5. Entregar la contraseña por canal privado.
6. Desactivar las cuentas de prueba cuando la cuenta definitiva esté comprobada.

La aplicación actual no ofrece pantalla para administrar cuentas; este paso debe coordinarse con el responsable técnico antes de la entrega.

## Recomendaciones sobre contraseñas

- Utilizar una contraseña larga, única y no reutilizada.
- No compartir una misma cuenta si se requiere trazabilidad individual.
- No guardarla en notas públicas, fotografías o documentos del repositorio.
- Cambiarla cuando una persona deje de estar autorizada.
- Conservar un mecanismo institucional de recuperación o custodia.

## Acceso desde computadora

1. Abrir Chrome, Edge, Firefox u otro navegador actualizado.
2. Ingresar la URL HTTPS.
3. Para consulta pública, usar directamente el catálogo.
4. Para operación interna, pulsar **Iniciar sesión**.
5. Cerrar sesión al terminar, especialmente en equipos compartidos.

No se instala un programa en la computadora del colegio.

## Acceso desde móvil

1. Abrir la URL HTTPS en un navegador actualizado.
2. Iniciar sesión con una cuenta autorizada.
3. Abrir **Escaneo**.
4. Pulsar **Iniciar cámara** y conceder permiso solo para este sitio cuando corresponda.
5. Usar ingreso manual si la cámara no está disponible.

La cámara requiere HTTPS y conexión a Internet. No se debe añadir la contraseña a capturas ni grabaciones.

## Conexión a Internet y cold start

El sistema necesita Internet para consultar y guardar información. Render y Neon son servicios en la nube.

En el plan gratuito de Render, el servicio puede suspenderse por inactividad. La primera solicitud puede demorar hasta aproximadamente 90 segundos. Espere y recargue una sola vez. Si después de dos intentos no abre, continúe con el procedimiento de incidente.

## Qué hacer ante un error

1. Anotar fecha y hora.
2. Identificar la página y acción realizadas.
3. Copiar únicamente el mensaje visible, sin credenciales.
4. Tomar una captura que no muestre contraseñas, datos personales, tokens ni paneles privados.
5. No repetir préstamos o devoluciones hasta verificar el estado del ejemplar.
6. Contactar al responsable técnico.

Datos de contacto:

- Responsable técnico: **[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]**
- Canal de soporte: **[PENDIENTE DE COMPLETAR]**
- Responsable institucional: **[PENDIENTE DE COMPLETAR]**

## Materiales que deben entregarse

- `docs/final/MANUAL_USUARIO.md`
- `docs/final/MANUAL_TECNICO.md`
- `docs/final/MEMORIA_FINAL_PROYECTO.md`
- `docs/final/GUIA_ENTREGA_INSTITUCIONAL.md`
- `docs/final/CHECKLIST_CIERRE.md`
- `docs/final/PLANTILLA_ACTA_CONFORMIDAD.md`
- URL pública de producción.
- Enlace al repositorio.
- Credenciales institucionales, por canal privado.
- Copia o referencia de la evidencia académica requerida.

Si la institución exige PDF, exporte los Markdown finales a PDF sin alterar su contenido y revise que no aparezcan secretos.

## Custodia de servicios y credenciales

La institución debe designar quién conservará:

- cuenta administrativa del sistema;
- acceso a GitHub;
- acceso a Render;
- acceso a Neon;
- respaldos;
- registro de cambios y solicitudes de mantenimiento.

Complete antes de entregar:

- Custodio institucional: **[PENDIENTE DE COMPLETAR]**
- Cargo: **[PENDIENTE DE COMPLETAR]**
- Canal privado acordado: **[PENDIENTE DE COMPLETAR]**

## Información que no debe publicarse

- Contraseñas actuales o anteriores.
- `DATABASE_URL` o dirección con usuario/clave de Neon.
- `SECRET_KEY`.
- Tokens de GitHub, Render o cualquier proveedor.
- Deploy Hook de Render.
- Archivos `.env`.
- Respaldos de la base de datos.
- Nombres o historial de lectores en capturas públicas.
- Códigos de recuperación o sesiones del navegador.

## Sesión breve de transferencia

La explicación al responsable institucional debe cubrir:

1. URL y catálogo público.
2. Inicio y cierre de sesión.
3. Diferencia entre admin y asistente.
4. Alta de materia, libro y ejemplar.
5. Impresión y reimpresión QR.
6. Préstamo y devolución por QR o código manual.
7. Límite de dos y bloqueo por mora.
8. Semáforo y reportes.
9. Procedimiento ante error y cold start.
10. Custodia de credenciales y solicitud de soporte.

No use datos reales de alumnos durante la demostración salvo autorización institucional.

## Checklist de entrega presencial o remota

- [ ] Responsable del proyecto identificado.
- [ ] Responsable receptor y cargo identificados.
- [ ] Fecha y modalidad de entrega acordadas.
- [ ] URL pública abierta desde PC.
- [ ] URL pública abierta desde móvil.
- [ ] Cuenta administrativa institucional comprobada.
- [ ] Cuentas de prueba cambiadas, sustituidas o desactivadas.
- [ ] Credenciales entregadas por canal privado.
- [ ] Manual de usuario entregado.
- [ ] Manual técnico entregado.
- [ ] Repositorio y custodia explicados.
- [ ] Flujo básico demostrado.
- [ ] Preguntas y observaciones registradas.
- [ ] Acta o constancia firmada, si corresponde.

## Estado actual de la entrega

La versión 1.0 está preparada técnicamente para la transferencia documental. A la fecha de este documento no se declara realizada la entrega formal, no se declara creada la cuenta institucional definitiva y no se declara firmada el acta.
