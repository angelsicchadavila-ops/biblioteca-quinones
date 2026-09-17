# Manual de usuario del Sistema Web de Gestión Bibliotecaria con Control QR

## Propósito y público

Este manual explica cómo utilizar la versión 1.0 del sistema de la Biblioteca Quiñones. Está dirigido al personal de la institución y no requiere conocimientos de programación, base de datos ni administración de servidores.

El sistema permite consultar el catálogo, organizar materias, libros y ejemplares, imprimir etiquetas QR, registrar préstamos y devoluciones, y consultar reportes operativos. La información se guarda en línea y se actualiza al confirmar cada operación.

## Objetivo del sistema

Facilitar la gestión del catálogo e inventario físico de la biblioteca, identificar cada ejemplar con un QR, registrar préstamos y devoluciones, controlar el límite y la mora, y ofrecer información operativa confiable desde computadora o teléfono.

## Dirección de acceso

URL pública de producción: <https://biblioteca-quinones.onrender.com/>

Puede abrirse desde una computadora, tableta o teléfono con navegador moderno y conexión a Internet. El acceso por HTTPS protege la comunicación y permite usar la cámara del teléfono para leer códigos QR.

Si el sistema tarda en responder después de un periodo sin uso, espere hasta 90 segundos y vuelva a intentarlo una vez. El servicio gratuito de Render puede necesitar ese tiempo para reactivarse; esto se conoce como *cold start*.

## Roles disponibles

| Rol | Qué puede hacer |
|---|---|
| Público | Consultar el catálogo, buscar por título o autor y filtrar por materia o nivel. No ve lectores ni préstamos. |
| Administrador (`admin`) | Acceder a materias, libros, ejemplares, QR, préstamos, terminal de escaneo y reportes. |
| Asistente (`asistente`) | Usar el terminal de escaneo y registrar préstamos o devoluciones. No accede a configuración ni reportes administrativos. |

Cada persona debe usar únicamente la cuenta que le asigne la institución. No comparta contraseñas ni las escriba en capturas, manuales o mensajes públicos.

## Inicio de sesión

1. Abra la URL pública.
2. Pulse **Iniciar sesión** en la parte superior.
3. Escriba el usuario institucional asignado.
4. Escriba la contraseña.
5. Pulse **Ingresar**.

Después del acceso:

- el administrador llega al panel **Administración**;
- el asistente llega al **Terminal de préstamos y devoluciones**.

Si aparece “Usuario o contraseña incorrectos”, revise mayúsculas, espacios y el usuario recibido. No intente adivinar credenciales repetidamente; contacte a la persona responsable.

## Catálogo público

El catálogo está disponible sin iniciar sesión.

1. En **Título o autor**, escriba una palabra o parte del nombre.
2. Si lo necesita, elija una **Materia**.
3. Si lo necesita, elija **Primaria**, **Secundaria** o **Ambos**.
4. Pulse **Buscar**.

Los filtros pueden combinarse. Cada resultado muestra el inventario calculado en ese momento. Un ejemplar operativo, activo y sin préstamo pendiente aparece como disponible. Si no hay coincidencias, limpie o cambie los filtros.

El catálogo nunca debe mostrar nombres de lectores, historial interno ni contraseñas.

## Panel de administración

Solo el rol administrador puede abrir **Administración**. El panel resume:

- materias activas;
- libros activos;
- ejemplares activos;
- préstamos sin devolver y vencidos;
- acceso a los cuatro reportes de la versión 1.0.

Use los botones del panel o la barra superior para desplazarse entre módulos.

## Gestión de materias

### Crear una materia

1. Abra **Administración** y luego **Materias activas**.
2. Escriba un nombre claro, por ejemplo `Arte y Cultura`.
3. Pulse el botón para crear la materia.

No se permiten nombres vacíos ni repetidos.

### Editar una materia

1. En el listado, localice la materia.
2. Pulse **Editar**.
3. Corrija el nombre y guarde.

### Desactivar o reactivar

- Desactive una materia cuando ya no deba usarse para nuevas altas.
- Una materia con libros activos no puede desactivarse; primero desactive esos libros.
- La desactivación conserva el historial. No elimina físicamente el registro.

## Gestión de libros

### Registrar un libro

1. Abra **Administración** y luego **Libros activos**.
2. Pulse **Nuevo libro**.
3. Complete título, autor, materia y nivel académico.
4. Complete ISBN/editorial solo si corresponde; es opcional.
5. Guarde.

Todo libro debe pertenecer a una materia activa y tener nivel **Primaria**, **Secundaria** o **Ambos**.

### Editar, desactivar o reactivar

Desde el listado puede corregir los datos o cambiar el estado del libro. Desactivar conserva sus ejemplares y su historial, pero lo oculta del catálogo y bloquea nuevas altas de ejemplares. Para reactivarlo, la materia asociada también debe estar activa.

## Gestión de ejemplares

Un libro es el título bibliográfico; cada copia física es un ejemplar independiente.

1. En **Libros**, abra **Ejemplares** o **Inventario** del título.
2. Indique cuántas copias agregará, entre 1 y 100.
3. Confirme la creación.

El sistema asigna códigos estables con formato similar a `LIB-001-EJ01`. No cambie el código impreso ni lo reutilice en otra copia.

En el inventario puede:

- marcar un ejemplar como **Operativo** o **Dañado**;
- desactivarlo o reactivarlo;
- consultar su estado calculado: Disponible, Prestado, Dañado o Inactivo.

Un ejemplar dañado o inactivo no puede prestarse. La condición Prestado se calcula a partir de un préstamo sin devolución; no se cambia manualmente.

## Generación y reimpresión de QR

Solo el administrador puede generar o reimprimir etiquetas.

### Etiqueta individual

1. Abra los ejemplares de un libro.
2. Localice el ejemplar.
3. Use la opción de QR o etiqueta PDF.
4. Descargue e imprima el archivo en tamaño real.

### Varias etiquetas

1. Seleccione uno o más ejemplares.
2. Pulse la opción para generar el PDF de etiquetas.
3. Imprima el PDF en papel A4, sin ajustar ni deformar la página.

La reimpresión conserva el mismo código QR. No crea un ejemplar nuevo ni altera el historial.

Recomendación: coloque la etiqueta en una zona plana, limpia y visible. El código alfanumérico debe quedar legible para poder ingresarlo manualmente si el QR se deteriora.

## Terminal de escaneo

El administrador y el asistente pueden abrir **Escaneo**.

### Uso de la cámara

1. Pulse **Iniciar cámara**.
2. Autorice la cámara si el navegador lo solicita.
3. Coloque la etiqueta QR dentro del recuadro.
4. Espere a que aparezca la ficha del ejemplar.
5. Pulse **Detener cámara** cuando termine o cuando necesite detener temporalmente la lectura.

La cámara no se enciende sola. El sistema prefiere la cámara trasera del teléfono. Mientras procesa una lectura, ignora escaneos repetidos para evitar operaciones dobles.

### Ingreso manual del código

1. Escriba el código impreso, por ejemplo `LIB-001-EJ01`.
2. Pulse **Buscar ejemplar**.

El ingreso manual y la cámara ejecutan las mismas validaciones. Úselo cuando no haya cámara, el permiso esté bloqueado, la iluminación sea insuficiente o el QR esté deteriorado.

## Registro y selección de lectores

El lector se identifica durante el préstamo; no se realiza una carga anual masiva.

1. Después de identificar un ejemplar disponible, escriba nombres o apellidos en **Buscar lector**.
2. Revise las coincidencias y seleccione a la persona correcta.
3. Si no existe, pulse **Crear lector nuevo** y complete nombres y apellidos.

Antes de crear un lector, busque con distintas partes del nombre para evitar duplicados. El nivel y el grado/sección se registran en cada préstamo, porque pueden cambiar con el tiempo.

## Registrar un préstamo

1. Identifique un ejemplar disponible mediante QR o código manual.
2. Busque y seleccione al lector, o cree uno nuevo.
3. Elija **Primaria** o **Secundaria**.
4. Escriba grado y sección, por ejemplo `2 A`.
5. Elija 7 días, 14 días o una fecha personalizada válida.
6. Revise los datos.
7. Pulse **Confirmar préstamo** una sola vez.
8. Espere el mensaje de confirmación antes de retirar el libro.

El servidor vuelve a validar todos los datos al confirmar. Si aparece un error de red, no asuma que el préstamo se guardó: identifique otra vez el ejemplar para comprobar su estado antes de repetir.

## Límite de dos préstamos y bloqueo por mora

Un lector puede tener como máximo dos préstamos sin devolver:

- con cero activos, puede recibir el primero;
- con uno activo, puede recibir el segundo;
- con dos activos, el tercero se rechaza con un mensaje explicativo.

También se bloquea un nuevo préstamo cuando el lector tiene al menos uno vencido. Un préstamo se considera vencido si sigue sin devolver y su fecha límite es anterior a la fecha actual. Si la fecha límite es hoy, todavía está dentro del plazo.

Al devolver todos los préstamos vencidos, el sistema recalcula el permiso automáticamente. El lector podrá recibir otro ejemplar si además tiene menos de dos préstamos activos.

## Registrar una devolución

1. Identifique el ejemplar prestado mediante QR o código manual.
2. Revise el lector, nivel, grado, fecha de préstamo, fecha límite y estado.
3. Pulse **Confirmar devolución**.
4. Espere el mensaje de éxito.

La devolución registra fecha, hora y usuario responsable. Si el ejemplar sigue activo y operativo, vuelve a mostrarse como Disponible.

## Semáforo de préstamos

En el listado administrativo:

- **amarillo**: préstamo activo dentro del plazo;
- **rojo**: préstamo vencido;
- **verde**: préstamo devuelto.

El color ayuda a leer el estado, pero siempre revise también el texto y las fechas.

## Reportes

Solo el administrador puede abrir **Reportes**.

| Reporte | Contenido principal |
|---|---|
| RPT-01 Inventario | Título, materia, total, disponibles, prestados y dañados. |
| RPT-02 Préstamos activos | Lector, libro, ejemplar, préstamo, límite y estado. |
| RPT-03 Préstamos vencidos | Lector, nivel, grado/sección, libro, límite y días de atraso. |
| RPT-04 Historial | Préstamo, devolución, estado y responsables; permite filtrar por rango de fechas. |

Para el historial, seleccione **Desde** y **Hasta** y pulse **Aplicar rango**. La fecha inicial no puede ser posterior a la final.

## Cierre de sesión

Pulse **Cerrar sesión** en la barra superior cuando termine, especialmente en equipos compartidos. No basta con cerrar la pestaña si otra persona utilizará inmediatamente el mismo dispositivo.

## Recomendaciones básicas

- Use una conexión estable durante préstamos y devoluciones.
- No comparta cuentas entre personas si la institución necesita trazabilidad individual.
- Mantenga los QR limpios y el código impreso visible.
- No desactive un registro por error; confirme primero que corresponde.
- Verifique el estado del ejemplar después de un error de red.
- Cambie o sustituya las cuentas de prueba antes de la entrega institucional.
- Conserve la contraseña institucional en un gestor seguro o en custodia formal, nunca en este repositorio.

## Solución de problemas comunes

| Situación | Qué hacer |
|---|---|
| La página tarda en abrir | Espere hasta 90 segundos por el *cold start* de Render y recargue una vez. |
| Usuario o contraseña incorrectos | Revise el usuario asignado y la escritura; contacte al responsable si continúa. |
| La cámara no inicia | Revise el permiso del navegador, cierre otras aplicaciones que usen la cámara o utilice ingreso manual. |
| No hay cámara | Use el código alfanumérico impreso. |
| “Código no registrado” | Revise caracteres y guiones; confirme que la etiqueta pertenece a este sistema. |
| El ejemplar aparece Dañado o Inactivo | El préstamo está bloqueado; el administrador debe revisar el inventario. |
| El lector está bloqueado por mora | Devuelva los préstamos vencidos; el permiso se recalcula automáticamente. |
| Se rechaza un tercer préstamo | El lector ya tiene dos activos; debe devolver uno antes. |
| Error de red al confirmar | No repita inmediatamente. Vuelva a consultar el ejemplar para saber si la operación se guardó. |
| El asistente recibe “Acceso denegado” | La página es exclusiva del administrador; use el terminal de escaneo. |
| El reporte no muestra datos | Revise el tipo de reporte y, en historial, el rango de fechas. |
| El problema persiste | Anote fecha, hora, página, acción y mensaje; tome una captura sin credenciales y comuníquelo al responsable técnico. |

## Soporte y datos pendientes

- Responsable técnico: **[PENDIENTE DE COMPLETAR POR EL ESTUDIANTE]**
- Responsable institucional: **[PENDIENTE DE COMPLETAR]**
- Canal de soporte: **[PENDIENTE DE COMPLETAR]**

No incluya contraseñas, tokens, `DATABASE_URL` ni `SECRET_KEY` al solicitar ayuda.
