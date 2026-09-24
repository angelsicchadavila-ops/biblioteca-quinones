# ADENDA v1.1 — CAMBIOS SOLICITADOS POSTERIORES A LA VERSIÓN 1.0

## Sistema Web de Gestión Bibliotecaria con Control QR — Biblioteca Quiñones

**Versión base:** v1.0  
**Nueva versión propuesta:** v1.1  
**Estado de la v1.0:** Terminada, probada y desplegada.  
**Origen de los cambios:** Requerimientos adicionales comunicados por el responsable de la entidad luego de la culminación de la versión 1.0.

---

# 1. Propósito de la adenda

La presente adenda complementa el Documento Maestro de la versión 1.0 y registra formalmente un conjunto reducido de mejoras solicitadas posteriormente.

Estos cambios no modifican los objetivos principales del proyecto ni implican reconstruir el sistema.

La versión 1.1 deberá implementarse sobre la versión 1.0 estable, preservando las funcionalidades previamente desarrolladas, probadas y aprobadas.

---

# 2. Principio de conservación de la versión 1.0

Las funcionalidades existentes de la versión 1.0 deberán continuar funcionando sin cambios funcionales no solicitados.

En particular, no deberán modificarse innecesariamente:

- catálogo público;
- materias;
- ejemplares;
- códigos QR;
- generación de PDF;
- escaneo QR;
- lectores;
- préstamos;
- devoluciones;
- límite de dos préstamos;
- bloqueo por mora;
- semáforo;
- reportes;
- trazabilidad;
- autenticación;
- despliegue Render;
- base de datos Neon;
- arquitectura general.

Cualquier modificación sobre componentes existentes deberá limitarse exclusivamente a lo necesario para integrar los requerimientos de la v1.1.

---

# 3. Requerimiento V1.1-01 — Año del libro

## 3.1 Descripción

Se incorporará un campo específico para registrar el año asociado al libro.

El año no deberá formar parte artificialmente del título del libro.

## 3.2 Características

El campo deberá:

- pertenecer al registro del libro;
- aceptar un año de cuatro dígitos;
- mostrarse como campo de texto o numérico simple;
- no utilizar una lista desplegable;
- permitir que registros anteriores continúen siendo válidos;
- ser opcional para los registros existentes si técnicamente es necesario para mantener compatibilidad.

Ejemplo:

**Año:** 2022

## 3.3 Formularios afectados

El campo Año deberá integrarse en:

- creación de libro;
- edición de libro;
- visualización correspondiente cuando resulte útil.

## 3.4 Filtro por año

El catálogo deberá incorporar un filtro por año.

El usuario podrá combinarlo con los filtros existentes, incluyendo:

- título/autor;
- materia;
- nivel;
- año.

Los filtros deberán poder utilizarse conjuntamente.

## 3.5 Compatibilidad

Los libros creados antes de la v1.1 no deberán perder información ni quedar inválidos por no poseer un año registrado.

---

# 4. Requerimiento V1.1-02 — Ampliación de permisos del asistente

## 4.1 Situación actual

En la versión 1.0 el rol asistente está orientado principalmente a las operaciones de biblioteca relacionadas con escaneo, préstamos y devoluciones.

## 4.2 Nuevo alcance

En la versión 1.1 el asistente también podrá gestionar parcialmente libros.

El asistente podrá:

- consultar el listado administrativo de libros;
- crear libros;
- editar libros existentes.

## 4.3 Campos editables

El asistente podrá modificar cualquier campo permitido del libro, incluyendo:

- título;
- autor;
- materia;
- nivel;
- año;
- ISBN;
- editorial.

## 4.4 Restricciones

El asistente NO podrá:

- eliminar libros;
- desactivar libros;
- reactivar libros;
- administrar materias;
- administrar usuarios;
- modificar funciones administrativas reservadas al administrador.

La seguridad deberá aplicarse en backend y no únicamente ocultando botones.

## 4.5 Ejemplares

La gestión de ejemplares conserva los permisos definidos actualmente en la versión 1.0.

No se amplían los permisos del asistente sobre ejemplares en esta adenda, salvo que posteriormente exista un requerimiento explícito.

---

# 5. Requerimiento V1.1-03 — Gestión de usuarios asistentes

## 5.1 Descripción

Se incorporará dentro del área administrativa un módulo sencillo para gestionar cuentas de asistentes.

El objetivo es evitar que la institución dependa de modificaciones manuales en la base de datos para las operaciones habituales de alta y mantenimiento de asistentes.

## 5.2 Acceso

Solo el rol `admin` podrá acceder al módulo.

El rol `asistente` no podrá acceder, incluso escribiendo directamente la URL.

## 5.3 Funciones permitidas al administrador

El administrador podrá:

- visualizar asistentes existentes;
- crear una cuenta de asistente;
- desactivar una cuenta de asistente;
- reactivar una cuenta de asistente cuando corresponda;
- cambiar o restablecer la contraseña de un asistente.

## 5.4 Creación de cuentas

Al crear un asistente, el sistema deberá solicitar únicamente los datos necesarios contemplados por el modelo actual.

Como mínimo:

- nombre de usuario;
- contraseña inicial.

El rol deberá establecerse automáticamente como:

`asistente`

El administrador no podrá utilizar esta interfaz para crear otro administrador.

## 5.5 Contraseñas

Las contraseñas:

- nunca deberán almacenarse en texto plano;
- deberán convertirse a hash utilizando el mecanismo Werkzeug ya empleado por el sistema;
- no deberán mostrarse posteriormente;
- no deberán incluirse en logs;
- no deberán incorporarse a Git;
- no deberán aparecer en documentación o evidencias.

## 5.6 Cambio de contraseña

El administrador podrá establecer una nueva contraseña para un asistente.

El cambio deberá reemplazar únicamente el hash correspondiente, sin afectar el historial de operaciones del usuario.

---

# 6. Desactivación de usuarios

La desactivación deberá implementarse de manera compatible con la trazabilidad histórica.

Un usuario desactivado:

- no podrá iniciar nuevas sesiones;
- conservará sus registros históricos;
- seguirá figurando como responsable de préstamos o devoluciones realizados anteriormente.

No deberá eliminarse físicamente un usuario cuando su eliminación pueda romper referencias históricas o claves foráneas.

Antes de modificar el esquema, deberá comprobarse si la tabla `usuarios` ya dispone de un mecanismo de estado activo/inactivo.

Si no existe, el cambio deberá diseñarse mediante una migración segura y compatible.

---

# 7. Recuperación de contraseña del administrador

La versión 1.1 NO incorporará recuperación mediante correo electrónico ni la funcionalidad pública “Olvidé mi contraseña”.

Si el administrador pierde su contraseña, la recuperación se realizará mediante mantenimiento técnico controlado.

Se deberá disponer de un procedimiento o script administrativo seguro que permita:

- identificar la cuenta administrativa;
- solicitar una nueva contraseña sin almacenarla en texto plano;
- generar un nuevo hash Werkzeug;
- actualizar únicamente la contraseña de esa cuenta;
- comprobar posteriormente el acceso.

Este procedimiento no deberá permitir visualizar la contraseña anterior.

El script o procedimiento deberá quedar documentado en el manual técnico.

---

# 8. Módulo administrativo de usuarios

La navegación administrativa podrá incorporar una opción similar a:

**Administración → Usuarios**

Dentro del módulo podrán mostrarse únicamente las funciones necesarias para v1.1.

Ejemplo conceptual:

Administración  
→ Materias  
→ Libros  
→ Préstamos  
→ Reportes  
→ Usuarios

Usuarios  
→ Listar asistentes  
→ Crear asistente  
→ Cambiar contraseña  
→ Desactivar / Reactivar

No se requiere un sistema complejo de gestión de permisos dinámicos.

Los roles continuarán siendo:

- `admin`
- `asistente`

---

# 9. Impacto esperado en base de datos

La implementación deberá realizar primero un análisis del esquema existente.

Cambios previsibles:

## Tabla libros

Incorporación de un campo equivalente a:

`anio`

o

`anio_publicacion`

La denominación definitiva deberá respetar las convenciones existentes del proyecto.

El cambio deberá ser compatible con registros existentes.

## Tabla usuarios

Deberá analizarse si ya existe un atributo que permita determinar si una cuenta está activa.

Si existe, deberá reutilizarse.

Si no existe, podrá añadirse un campo equivalente a:

`activo`

con una migración segura.

No se deben reconstruir tablas existentes innecesariamente.

---

# 10. Impacto esperado en permisos

La matriz objetivo de permisos será:

| Función | Admin | Asistente |
|---|---:|---:|
| Catálogo público | Sí | Sí |
| Crear libro | Sí | Sí |
| Editar libro | Sí | Sí |
| Desactivar libro | Sí | No |
| Reactivar libro | Sí | No |
| Gestionar materias | Sí | No |
| Gestionar ejemplares | Sin cambios v1.0 | Sin cambios v1.0 |
| Escaneo | Sí | Sí |
| Préstamos | Sí | Sí |
| Devoluciones | Sí | Sí |
| Reportes | Según v1.0 | Según v1.0 |
| Crear asistentes | Sí | No |
| Cambiar contraseña de asistentes | Sí | No |
| Desactivar asistentes | Sí | No |
| Crear administradores desde web | No | No |

---

# 11. Criterios de aceptación

La versión 1.1 será considerada correcta cuando, como mínimo:

### Año

- sea posible crear un libro indicando año;
- sea posible editar el año;
- los libros anteriores sigan funcionando;
- el catálogo permita filtrar por año;
- el filtro por año pueda combinarse con los filtros existentes;
- un año inválido sea rechazado adecuadamente.

### Asistente

- pueda acceder al listado de libros permitido;
- pueda crear libros;
- pueda editar todos los campos autorizados;
- no pueda desactivar libros;
- no pueda reactivar libros;
- no pueda acceder a materias administrativas;
- no pueda acceder al módulo de usuarios;
- el bloqueo exista también mediante acceso directo por URL.

### Usuarios

- admin pueda listar asistentes;
- admin pueda crear asistente;
- la contraseña se almacene únicamente como hash;
- el nuevo asistente pueda iniciar sesión;
- admin pueda cambiar la contraseña de un asistente;
- la contraseña anterior deje de funcionar después del cambio;
- admin pueda desactivar un asistente;
- el asistente desactivado no pueda iniciar sesión;
- la trazabilidad histórica del asistente desactivado permanezca;
- admin pueda reactivar al asistente si esa función queda implementada.

### Recuperación administrativa

- exista un procedimiento técnico para restablecer la contraseña del administrador;
- el procedimiento no revele ni almacene contraseñas en texto plano;
- no sea necesario modificar manualmente hashes en Neon.

---

# 12. Pruebas de regresión

Después de implementar v1.1 deberán ejecutarse nuevamente las pruebas existentes relevantes de v1.0.

Como mínimo deberán comprobarse:

- autenticación;
- permisos;
- catálogo;
- materias;
- libros;
- ejemplares;
- QR;
- PDF;
- escáner;
- lectores;
- préstamos;
- devoluciones;
- mora;
- máximo de dos préstamos;
- semáforo;
- reportes;
- trazabilidad;
- Neon;
- Render;
- HTTPS.

Una nueva funcionalidad no podrá considerarse correcta si rompe una función previamente aprobada.

---

# 13. Estrategia de implementación segura

La implementación seguirá este orden:

1. Auditoría del estado actual.
2. Análisis de impacto.
3. Verificación de respaldo lógico y estado Git.
4. Diseño de migración no destructiva.
5. Implementación del campo Año.
6. Implementación del filtro Año.
7. Modificación controlada de permisos del asistente.
8. Implementación del módulo de asistentes.
9. Implementación del procedimiento técnico de recuperación del admin.
10. Pruebas específicas v1.1.
11. Regresión de v1.0.
12. Deployment.
13. Evidencias.
14. Cierre v1.1.

---

# 14. Rollback

Antes de cualquier cambio estructural deberá existir capacidad de volver al estado estable de la versión 1.0.

Como mínimo:

- identificar el commit estable previo a v1.1;
- documentar las modificaciones de esquema;
- realizar migraciones no destructivas;
- evitar eliminar columnas o registros;
- no modificar datos reales innecesariamente.

Si una nueva funcionalidad falla de forma crítica, deberá ser posible restaurar el código estable sin perder información existente.

---

# 15. Documentación v1.1

No se repetirá la documentación completa de las nueve semanas.

Se utilizará una documentación compacta:

`docs/v1_1/ADENDA_V1_1_CAMBIOS_SOLICITADOS.md`

`docs/v1_1/RESUMEN_CAMBIOS.md`

`docs/v1_1/RESULTADOS_PRUEBAS.md`

`docs/v1_1/capturas/`

Las capturas deberán ser únicamente representativas de los cambios realizados.

---

# 16. Fuera de alcance de v1.1

No se implementará en esta versión:

- recuperación de contraseña mediante correo;
- creación de administradores desde la interfaz;
- permisos dinámicos;
- roles adicionales;
- notificaciones;
- reservas;
- pagos;
- multas;
- aplicación móvil nativa;
- integración con sistemas externos;
- cambios de arquitectura;
- rediseño integral de interfaz.

---

# 17. Resultado esperado

La versión 1.1 deberá mantener íntegramente las capacidades de la v1.0 e incorporar de forma controlada:

1. Año de libro y filtro por año.
2. Creación y edición de libros por asistentes.
3. Gestión administrativa de cuentas asistentes.
4. Procedimiento técnico seguro para recuperación de contraseña del administrador.

La v1.1 solo será declarada estable después de completar pruebas específicas y regresión de las funcionalidades existentes.
