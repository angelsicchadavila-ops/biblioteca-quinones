"use strict";

(() => {
  const mensaje = document.getElementById("mensaje-escaneo");
  const botonIniciar = document.getElementById("iniciar-camara");
  const botonDetener = document.getElementById("detener-camara");
  const formularioManual = document.getElementById("form-codigo-manual");
  const entradaManual = document.getElementById("codigo-manual");
  const ficha = document.getElementById("ficha-ejemplar");
  const bloqueo = document.getElementById("bloqueo-operacion");
  const flujoPrestamo = document.getElementById("flujo-prestamo");
  const flujoDevolucion = document.getElementById("flujo-devolucion");
  const formularioPrestamo = document.getElementById("form-prestamo");
  const formularioDevolucion = document.getElementById("form-devolucion");
  const entradaBuscarLector = document.getElementById("buscar-lector");
  const botonBuscarLector = document.getElementById("boton-buscar-lector");
  const resultadosLectores = document.getElementById("resultados-lectores");
  const botonNuevoLector = document.getElementById("boton-nuevo-lector");
  const lectorSeleccionado = document.getElementById("lector-seleccionado");
  const camposNuevoLector = document.getElementById("campos-nuevo-lector");
  const tipoPlazo = document.getElementById("tipo-plazo");
  const campoFechaPersonalizada = document.getElementById("campo-fecha-personalizada");
  const fechaPersonalizada = document.getElementById("fecha-personalizada");

  if (!mensaje || !botonIniciar || !botonDetener || !formularioManual || !entradaManual || !ficha) {
    return;
  }

  const BLOQUEO_LECTURA_MS = 3000;
  let lector = null;
  let camaraActiva = false;
  let procesando = false;
  let ultimoCodigo = "";
  let ultimaLectura = 0;

  function mostrarMensaje(texto, tipo = "info") {
    mensaje.className = `alert alert-${tipo}`;
    mensaje.textContent = texto;
  }

  function ocultarFicha() {
    ficha.classList.add("d-none");
  }

  function reiniciarFlujos() {
    bloqueo.classList.add("d-none");
    bloqueo.textContent = "";
    flujoPrestamo.classList.add("d-none");
    flujoDevolucion.classList.add("d-none");
    resultadosLectores.replaceChildren();
    resultadosLectores.className = "lista-lectores mb-3";
    lectorSeleccionado.classList.add("d-none");
    lectorSeleccionado.textContent = "";
    camposNuevoLector.classList.add("d-none");
    formularioPrestamo.reset();
    document.getElementById("prestamo-lector-id").value = "";
    campoFechaPersonalizada.classList.add("d-none");
    fechaPersonalizada.required = false;
  }

  function mostrarFicha(ejemplar) {
    const clases = {
      Disponible: "text-bg-success",
      Prestado: "text-bg-warning",
      "Dañado": "text-bg-danger",
      Inactivo: "text-bg-secondary",
    };
    document.getElementById("ficha-titulo").textContent = ejemplar.titulo;
    document.getElementById("ficha-estado").textContent = ejemplar.disponibilidad;
    document.getElementById("ficha-estado").className = `badge fs-6 ${clases[ejemplar.disponibilidad] || "text-bg-secondary"}`;
    document.getElementById("ficha-codigo").textContent = ejemplar.codigo_qr;
    document.getElementById("ficha-autor").textContent = ejemplar.autor;
    document.getElementById("ficha-materia").textContent = ejemplar.materia;
    document.getElementById("ficha-nivel").textContent = ejemplar.nivel;
    document.getElementById("ficha-condicion").textContent = ejemplar.estado_fisico;
    ficha.classList.remove("d-none");
  }

  function formatearFecha(valor) {
    if (!valor) return "—";
    const [anio, mes, dia] = valor.slice(0, 10).split("-");
    return `${dia}/${mes}/${anio}`;
  }

  function formatearFechaHora(valor) {
    if (!valor) return "—";
    const fecha = new Date(valor);
    return Number.isNaN(fecha.getTime())
      ? valor
      : fecha.toLocaleString("es-PE", { dateStyle: "short", timeStyle: "short" });
  }

  function mostrarFlujo(datos) {
    reiniciarFlujos();
    mostrarFicha(datos.ejemplar);
    if (datos.operacion === "prestamo") {
      document.getElementById("prestamo-codigo").value = datos.ejemplar.codigo_qr;
      flujoPrestamo.classList.remove("d-none");
      entradaBuscarLector.focus();
      return;
    }
    if (datos.operacion === "devolucion" && datos.prestamo_activo) {
      const prestamo = datos.prestamo_activo;
      document.getElementById("devolucion-codigo").value = datos.ejemplar.codigo_qr;
      document.getElementById("devolucion-lector").textContent = prestamo.lector;
      document.getElementById("devolucion-grado").textContent = `${prestamo.nivel_alumno} · ${prestamo.grado_seccion_alumno}`;
      document.getElementById("devolucion-fecha-prestamo").textContent = formatearFechaHora(prestamo.fecha_prestamo);
      document.getElementById("devolucion-fecha-limite").textContent = formatearFecha(prestamo.fecha_limite);
      const estado = document.getElementById("devolucion-estado");
      estado.textContent = prestamo.estado === "Vencido" ? `Vencido · ${prestamo.dias_atraso} día(s)` : "Activo dentro del plazo";
      estado.className = `badge ${prestamo.estado === "Vencido" ? "text-bg-danger" : "text-bg-warning"}`;
      flujoDevolucion.classList.remove("d-none");
      return;
    }
    const razones = {
      "Dañado": "El ejemplar está dañado y no puede prestarse.",
      Inactivo: "El ejemplar está inactivo y no puede prestarse.",
    };
    bloqueo.textContent = razones[datos.ejemplar.disponibilidad] || "El ejemplar no está disponible para préstamo.";
    bloqueo.classList.remove("d-none");
  }

  async function procesarCodigo(valor, origen, forzar = false) {
    const codigo = valor.trim().toUpperCase();
    const ahora = Date.now();
    if (!codigo) {
      ocultarFicha();
      mostrarMensaje("Escribe el código alfanumérico impreso en la etiqueta.", "warning");
      entradaManual.focus();
      return;
    }
    if (procesando || (!forzar && codigo === ultimoCodigo && ahora - ultimaLectura < BLOQUEO_LECTURA_MS)) {
      return;
    }

    procesando = true;
    ultimoCodigo = codigo;
    ultimaLectura = ahora;
    mostrarMensaje(`${origen}: buscando ${codigo}…`, "info");

    try {
      const respuesta = await fetch(`/api/ejemplar/${encodeURIComponent(codigo)}`, {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const datos = await respuesta.json();
      if (!respuesta.ok) {
        ocultarFicha();
        mostrarMensaje(datos.error?.mensaje || "No fue posible consultar el código.", respuesta.status === 404 ? "warning" : "danger");
        return;
      }
      mostrarFlujo(datos);
      mostrarMensaje(`Ejemplar ${datos.ejemplar.codigo_qr} identificado correctamente.`, "success");
    } catch (_error) {
      ocultarFicha();
      mostrarMensaje("No se pudo consultar el servidor. Verifica la conexión y vuelve a intentar.", "danger");
    } finally {
      procesando = false;
    }
  }

  function seleccionarLector(lectorEncontrado) {
    document.getElementById("prestamo-lector-id").value = lectorEncontrado.id;
    document.getElementById("lector-nombres").value = "";
    document.getElementById("lector-apellidos").value = "";
    camposNuevoLector.classList.add("d-none");
    lectorSeleccionado.textContent = `Lector seleccionado: ${lectorEncontrado.nombres} ${lectorEncontrado.apellidos}`;
    lectorSeleccionado.classList.remove("d-none");
  }

  function dibujarLectores(lectores) {
    resultadosLectores.replaceChildren();
    if (!lectores.length) {
      const aviso = document.createElement("p");
      aviso.className = "small text-secondary mb-0";
      aviso.textContent = "No se encontraron coincidencias. Puedes crear un lector nuevo.";
      resultadosLectores.append(aviso);
      return;
    }
    lectores.forEach((lectorEncontrado) => {
      const boton = document.createElement("button");
      boton.type = "button";
      boton.className = "list-group-item list-group-item-action";
      boton.disabled = !lectorEncontrado.activo;
      const referencia = lectorEncontrado.ultimo_grado_seccion
        ? `Último registro: ${lectorEncontrado.ultimo_nivel} · ${lectorEncontrado.ultimo_grado_seccion}`
        : "Sin préstamos anteriores";
      const estado = lectorEncontrado.prestamos_vencidos
        ? `${lectorEncontrado.prestamos_vencidos} vencido(s)`
        : `${lectorEncontrado.prestamos_activos} activo(s)`;
      boton.textContent = `${lectorEncontrado.nombres} ${lectorEncontrado.apellidos} — ${referencia} — ${estado}${lectorEncontrado.activo ? "" : " — Inactivo"}`;
      boton.addEventListener("click", () => seleccionarLector(lectorEncontrado));
      resultadosLectores.append(boton);
    });
    resultadosLectores.className = "lista-lectores list-group mb-3";
  }

  async function buscarLector() {
    const texto = entradaBuscarLector.value.trim();
    if (!texto) {
      mostrarMensaje("Escribe nombres o apellidos para buscar un lector.", "warning");
      entradaBuscarLector.focus();
      return;
    }
    botonBuscarLector.disabled = true;
    try {
      const respuesta = await fetch(`/api/lectores?q=${encodeURIComponent(texto)}`, {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const datos = await respuesta.json();
      if (!respuesta.ok) throw new Error();
      dibujarLectores(datos.lectores);
      mostrarMensaje(`${datos.lectores.length} coincidencia(s) encontrada(s).`, "info");
    } catch (_error) {
      mostrarMensaje("No fue posible buscar lectores. Vuelve a intentar.", "danger");
    } finally {
      botonBuscarLector.disabled = false;
    }
  }

  function prepararNuevoLector() {
    document.getElementById("prestamo-lector-id").value = "";
    lectorSeleccionado.classList.add("d-none");
    camposNuevoLector.classList.remove("d-none");
    document.getElementById("lector-nombres").focus();
  }

  async function enviarOperacion(ruta, formulario, codigo) {
    procesando = true;
    mostrarMensaje("Guardando la operación…", "info");
    try {
      const respuesta = await fetch(ruta, {
        method: "POST",
        body: new FormData(formulario),
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const datos = await respuesta.json();
      if (!respuesta.ok) {
        mostrarMensaje(datos.error?.mensaje || "La operación fue rechazada.", "danger");
        return;
      }
      mostrarMensaje(datos.mensaje, "success");
      procesando = false;
      await procesarCodigo(codigo, "Estado actualizado", true);
      mostrarMensaje(datos.mensaje, "success");
    } catch (_error) {
      mostrarMensaje("No se confirmó la operación. Verifica el estado antes de reintentar.", "danger");
    } finally {
      procesando = false;
    }
  }

  function explicarErrorCamara(error) {
    const detalle = String(error?.name || error || "");
    if (/NotAllowed|PermissionDenied/i.test(detalle)) {
      return "No se concedió permiso para usar la cámara. Puedes habilitarlo en el navegador o ingresar el código manualmente.";
    }
    if (/NotFound|DevicesNotFound/i.test(detalle)) {
      return "No se encontró una cámara disponible. Utiliza el ingreso manual.";
    }
    if (/NotReadable|TrackStart/i.test(detalle)) {
      return "La cámara no pudo iniciarse; puede estar siendo usada por otra aplicación. Utiliza el ingreso manual o vuelve a intentar.";
    }
    return "No fue posible iniciar la cámara. Utiliza el ingreso manual o revisa los permisos del navegador.";
  }

  async function iniciarCamara() {
    if (camaraActiva) return;
    if (typeof Html5Qrcode === "undefined") {
      mostrarMensaje("El lector QR no pudo cargarse. Mantén la conexión disponible o utiliza el ingreso manual.", "danger");
      return;
    }

    botonIniciar.disabled = true;
    mostrarMensaje("Solicitando acceso a la cámara…", "info");
    try {
      lector ||= new Html5Qrcode("qr-reader");
      await lector.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 }, aspectRatio: 1 },
        (textoDecodificado) => procesarCodigo(textoDecodificado, "QR leído"),
        () => {}
      );
      camaraActiva = true;
      botonDetener.disabled = false;
      mostrarMensaje("Cámara activa. Coloca una etiqueta QR dentro del recuadro.", "success");
    } catch (error) {
      camaraActiva = false;
      botonIniciar.disabled = false;
      botonDetener.disabled = true;
      mostrarMensaje(explicarErrorCamara(error), "warning");
    }
  }

  async function detenerCamara() {
    if (!lector || !camaraActiva) return;
    botonDetener.disabled = true;
    try {
      await lector.stop();
      camaraActiva = false;
      botonIniciar.disabled = false;
      mostrarMensaje("Cámara detenida. Puedes reiniciarla o utilizar el ingreso manual.", "info");
    } catch (_error) {
      botonDetener.disabled = false;
      mostrarMensaje("No se pudo detener la cámara correctamente. Recarga la página si continúa activa.", "danger");
    }
  }

  botonIniciar.addEventListener("click", iniciarCamara);
  botonDetener.addEventListener("click", detenerCamara);
  formularioManual.addEventListener("submit", (evento) => {
    evento.preventDefault();
    procesarCodigo(entradaManual.value, "Ingreso manual");
  });
  botonBuscarLector.addEventListener("click", buscarLector);
  entradaBuscarLector.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
      evento.preventDefault();
      buscarLector();
    }
  });
  botonNuevoLector.addEventListener("click", prepararNuevoLector);
  tipoPlazo.addEventListener("change", () => {
    const personalizada = tipoPlazo.value === "personalizada";
    campoFechaPersonalizada.classList.toggle("d-none", !personalizada);
    fechaPersonalizada.required = personalizada;
  });
  formularioPrestamo.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const lectorId = document.getElementById("prestamo-lector-id").value;
    const nombres = document.getElementById("lector-nombres").value.trim();
    const apellidos = document.getElementById("lector-apellidos").value.trim();
    if (!lectorId && (!nombres || !apellidos)) {
      mostrarMensaje("Selecciona un lector existente o completa nombres y apellidos para crear uno.", "warning");
      return;
    }
    if (!formularioPrestamo.reportValidity()) return;
    enviarOperacion("/api/prestamos", formularioPrestamo, document.getElementById("prestamo-codigo").value);
  });
  formularioDevolucion.addEventListener("submit", (evento) => {
    evento.preventDefault();
    enviarOperacion("/api/devoluciones", formularioDevolucion, document.getElementById("devolucion-codigo").value);
  });
  window.addEventListener("pagehide", () => {
    if (lector && camaraActiva) lector.stop().catch(() => {});
  });
})();
