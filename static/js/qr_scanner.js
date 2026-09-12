"use strict";

(() => {
  const mensaje = document.getElementById("mensaje-escaneo");
  const botonIniciar = document.getElementById("iniciar-camara");
  const botonDetener = document.getElementById("detener-camara");
  const formularioManual = document.getElementById("form-codigo-manual");
  const entradaManual = document.getElementById("codigo-manual");
  const ficha = document.getElementById("ficha-ejemplar");

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

  async function procesarCodigo(valor, origen) {
    const codigo = valor.trim().toUpperCase();
    const ahora = Date.now();
    if (!codigo) {
      ocultarFicha();
      mostrarMensaje("Escribe el código alfanumérico impreso en la etiqueta.", "warning");
      entradaManual.focus();
      return;
    }
    if (procesando || (codigo === ultimoCodigo && ahora - ultimaLectura < BLOQUEO_LECTURA_MS)) {
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
      mostrarFicha(datos.ejemplar);
      mostrarMensaje(`Ejemplar ${datos.ejemplar.codigo_qr} identificado correctamente.`, "success");
    } catch (_error) {
      ocultarFicha();
      mostrarMensaje("No se pudo consultar el servidor. Verifica la conexión y vuelve a intentar.", "danger");
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
    if (camaraActiva) {
      return;
    }
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
    if (!lector || !camaraActiva) {
      return;
    }
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
  window.addEventListener("pagehide", () => {
    if (lector && camaraActiva) {
      lector.stop().catch(() => {});
    }
  });
})();
