"""Aplicación Flask de la Biblioteca Quiñones."""

from __future__ import annotations

import os
import secrets
from datetime import date
from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

import psycopg
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from utils.catalogo import (
    ESTADOS_FISICOS,
    NIVELES_LIBRO,
    consultar_catalogo,
    consultar_ejemplares,
    consultar_libros_admin,
    crear_ejemplares,
    normalizar_texto,
)
from utils.db import iniciar_bd, obtener_bd
from utils.escaneo import (
    codigo_valido,
    consultar_ejemplar_por_codigo,
    normalizar_codigo,
)
from utils.pdf_exporter import generar_pdf_etiquetas
from utils.prestamos import (
    ReglaOperacionError,
    buscar_lectores,
    consultar_prestamos,
    contexto_prestamo_activo,
    registrar_devolucion,
    registrar_prestamo,
    reporte_historial,
    reporte_inventario,
    reporte_prestamos_activos,
    reporte_prestamos_vencidos,
)
from utils.qr_generator import generar_qr_png


RAIZ_PROYECTO = Path(__file__).resolve().parent
P = ParamSpec("P")
R = TypeVar("R")


def crear_app(configuracion_pruebas: dict | None = None) -> Flask:
    """Crea y configura la aplicación para desarrollo, pruebas o producción."""
    load_dotenv(RAIZ_PROYECTO / ".env", override=False)

    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv("DATABASE_URL", "").strip(),
        SECRET_KEY=os.getenv("SECRET_KEY", "").strip(),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "").lower()
        in {"1", "true", "yes"}
        or bool(os.getenv("RENDER")),
    )

    if configuracion_pruebas:
        app.config.update(configuracion_pruebas)

    if not app.config["DATABASE_URL"]:
        raise RuntimeError("Falta DATABASE_URL en las variables de entorno.")
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("Falta SECRET_KEY en las variables de entorno.")

    iniciar_bd(app)

    @app.before_request
    def cargar_usuario_actual() -> None:
        g.usuario = None
        usuario_id = session.get("usuario_id")
        if usuario_id is None:
            return

        usuario = obtener_bd().execute(
            """
            SELECT id, username, nombre_completo, rol, activo
              FROM usuarios
             WHERE id = %s
            """,
            (usuario_id,),
        ).fetchone()

        if not usuario or not usuario["activo"] or usuario["rol"] not in {
            "admin",
            "asistente",
        }:
            session.clear()
            return
        g.usuario = usuario

    def login_requerido(vista: Callable[P, R]) -> Callable[P, R]:
        """Redirige al login cuando no existe una sesión válida."""

        @wraps(vista)
        def protegida(*args: P.args, **kwargs: P.kwargs):
            if g.usuario is None:
                flash("Inicia sesión para acceder a esta página.", "warning")
                return redirect(url_for("login"))
            return vista(*args, **kwargs)

        return protegida

    def rol_requerido(rol: str):
        """Restringe una vista a un rol concreto en el backend."""

        def decorador(vista: Callable[P, R]) -> Callable[P, R]:
            @wraps(vista)
            @login_requerido
            def protegida(*args: P.args, **kwargs: P.kwargs):
                if g.usuario["rol"] != rol:
                    abort(403)
                return vista(*args, **kwargs)

            return protegida

        return decorador

    def api_login_requerido(vista: Callable[P, R]) -> Callable[P, R]:
        """Responde JSON 401 cuando una API interna no tiene sesión válida."""

        @wraps(vista)
        def protegida(*args: P.args, **kwargs: P.kwargs):
            if g.usuario is None:
                return jsonify(
                    ok=False,
                    error={
                        "codigo": "autenticacion_requerida",
                        "mensaje": "Inicia sesión para usar el terminal de escaneo.",
                    },
                ), 401
            return vista(*args, **kwargs)

        return protegida

    def generar_token_csrf() -> str:
        token = session.get("csrf_token")
        if token is None:
            token = secrets.token_urlsafe(32)
            session["csrf_token"] = token
        return token

    app.jinja_env.globals["csrf_token"] = generar_token_csrf

    @app.before_request
    def validar_csrf() -> None:
        if request.method != "POST":
            return
        token_sesion = session.get("csrf_token", "")
        token_formulario = request.form.get("csrf_token", "")
        if not token_sesion or not secrets.compare_digest(
            token_sesion, token_formulario
        ):
            abort(400)

    @app.get("/")
    def inicio():
        texto = normalizar_texto(request.args.get("q", ""))[:200]
        nivel = request.args.get("nivel", "").strip()
        if nivel not in NIVELES_LIBRO:
            nivel = ""

        materia_id = None
        materia_solicitada = request.args.get("materia", "").strip()
        if materia_solicitada.isdigit():
            materia_id = int(materia_solicitada)

        conexion = obtener_bd()
        materias = conexion.execute(
            """
            SELECT id, nombre
              FROM materias
             WHERE activo
             ORDER BY lower(nombre)
            """
        ).fetchall()
        libros = consultar_catalogo(conexion, texto, materia_id, nivel)
        return render_template(
            "index.html",
            libros=libros,
            materias=materias,
            filtros={"q": texto, "materia": materia_id, "nivel": nivel},
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.usuario is not None:
            destino = "admin" if g.usuario["rol"] == "admin" else "escaneo"
            return redirect(url_for(destino))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            usuario = obtener_bd().execute(
                """
                SELECT id, username, password_hash, nombre_completo, rol, activo
                  FROM usuarios
                 WHERE username = %s
                """,
                (username,),
            ).fetchone()

            credenciales_validas = (
                usuario is not None
                and usuario["activo"]
                and usuario["rol"] in {"admin", "asistente"}
                and check_password_hash(usuario["password_hash"], password)
            )
            if not credenciales_validas:
                flash("Usuario o contraseña incorrectos.", "danger")
                return render_template("login.html", username=username), 401

            session.clear()
            session["usuario_id"] = usuario["id"]
            session["csrf_token"] = secrets.token_urlsafe(32)
            flash(f"Bienvenido, {usuario['nombre_completo']}.", "success")
            destino = "admin" if usuario["rol"] == "admin" else "escaneo"
            return redirect(url_for(destino))

        return render_template("login.html")

    @app.post("/logout")
    @login_requerido
    def logout():
        session.clear()
        flash("La sesión se cerró correctamente.", "success")
        return redirect(url_for("login"))

    @app.get("/admin")
    @rol_requerido("admin")
    def admin():
        conexion = obtener_bd()
        resumen = conexion.execute(
            """
            SELECT
                (SELECT count(*) FROM materias WHERE activo) AS materias_activas,
                (SELECT count(*) FROM libros WHERE activo) AS libros_activos,
                (SELECT count(*) FROM ejemplares WHERE activo) AS ejemplares_activos,
                (SELECT count(*) FROM prestamos
                  WHERE fecha_devolucion IS NULL) AS prestamos_pendientes,
                (SELECT count(*) FROM prestamos
                  WHERE fecha_devolucion IS NULL
                    AND fecha_limite <
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                ) AS prestamos_vencidos
            """
        ).fetchone()
        return render_template("admin_dashboard.html", resumen=resumen)

    @app.route("/admin/materias", methods=["GET", "POST"])
    @rol_requerido("admin")
    def materias_admin():
        conexion = obtener_bd()
        if request.method == "POST":
            nombre = normalizar_texto(request.form.get("nombre", ""))
            if not nombre:
                flash("El nombre de la materia es obligatorio.", "danger")
            elif len(nombre) > 100:
                flash("El nombre no puede superar 100 caracteres.", "danger")
            elif conexion.execute(
                "SELECT 1 FROM materias WHERE lower(nombre) = lower(%s)", (nombre,)
            ).fetchone():
                flash("Ya existe una materia con ese nombre.", "danger")
            else:
                conexion.execute("INSERT INTO materias (nombre) VALUES (%s)", (nombre,))
                flash("Materia creada correctamente.", "success")
                return redirect(url_for("materias_admin"))

        materias = conexion.execute(
            """
            SELECT m.id, m.nombre, m.activo,
                   count(l.id) AS total_libros,
                   count(l.id) FILTER (WHERE l.activo) AS libros_activos
              FROM materias m
              LEFT JOIN libros l ON l.materia_id = m.id
             GROUP BY m.id
             ORDER BY m.activo DESC, lower(m.nombre)
            """
        ).fetchall()
        return render_template("materias.html", materias=materias)

    @app.route("/admin/materias/<int:materia_id>/editar", methods=["GET", "POST"])
    @rol_requerido("admin")
    def editar_materia(materia_id: int):
        conexion = obtener_bd()
        materia = conexion.execute(
            "SELECT id, nombre, activo FROM materias WHERE id = %s", (materia_id,)
        ).fetchone()
        if materia is None:
            abort(404)

        if request.method == "POST":
            nombre = normalizar_texto(request.form.get("nombre", ""))
            repetida = conexion.execute(
                """
                SELECT 1
                  FROM materias
                 WHERE lower(nombre) = lower(%s) AND id <> %s
                """,
                (nombre, materia_id),
            ).fetchone()
            if not nombre:
                flash("El nombre de la materia es obligatorio.", "danger")
            elif len(nombre) > 100:
                flash("El nombre no puede superar 100 caracteres.", "danger")
            elif repetida:
                flash("Ya existe una materia con ese nombre.", "danger")
            else:
                conexion.execute(
                    "UPDATE materias SET nombre = %s WHERE id = %s",
                    (nombre, materia_id),
                )
                flash("Materia actualizada correctamente.", "success")
                return redirect(url_for("materias_admin"))
            materia = {**materia, "nombre": nombre}

        return render_template("materia_form.html", materia=materia)

    @app.post("/admin/materias/<int:materia_id>/estado")
    @rol_requerido("admin")
    def cambiar_estado_materia(materia_id: int):
        conexion = obtener_bd()
        materia = conexion.execute(
            "SELECT id, nombre, activo FROM materias WHERE id = %s", (materia_id,)
        ).fetchone()
        if materia is None:
            abort(404)

        if materia["activo"]:
            tiene_libros_activos = conexion.execute(
                "SELECT 1 FROM libros WHERE materia_id = %s AND activo LIMIT 1",
                (materia_id,),
            ).fetchone()
            if tiene_libros_activos:
                flash(
                    "No se puede desactivar la materia mientras tenga libros activos.",
                    "danger",
                )
                return redirect(url_for("materias_admin"))

        nuevo_estado = not materia["activo"]
        conexion.execute(
            "UPDATE materias SET activo = %s WHERE id = %s",
            (nuevo_estado, materia_id),
        )
        accion = "reactivada" if nuevo_estado else "desactivada"
        flash(f"Materia {accion} correctamente.", "success")
        return redirect(url_for("materias_admin"))

    @app.get("/admin/libros")
    @rol_requerido("admin")
    def libros_admin():
        return render_template(
            "libros.html", libros=consultar_libros_admin(obtener_bd())
        )

    def obtener_materias_activas():
        return obtener_bd().execute(
            "SELECT id, nombre FROM materias WHERE activo ORDER BY lower(nombre)"
        ).fetchall()

    def validar_libro_formulario() -> tuple[dict, list[str]]:
        datos = {
            "titulo": normalizar_texto(request.form.get("titulo", "")),
            "autor": normalizar_texto(request.form.get("autor", "")),
            "nivel": request.form.get("nivel", "").strip(),
            "isbn_editorial": normalizar_texto(
                request.form.get("isbn_editorial", "")
            ),
            "materia_id": request.form.get("materia_id", "").strip(),
        }
        errores: list[str] = []
        if not datos["titulo"]:
            errores.append("El título es obligatorio.")
        elif len(datos["titulo"]) > 200:
            errores.append("El título no puede superar 200 caracteres.")
        if not datos["autor"]:
            errores.append("El autor es obligatorio.")
        elif len(datos["autor"]) > 150:
            errores.append("El autor no puede superar 150 caracteres.")
        if datos["nivel"] not in NIVELES_LIBRO:
            errores.append("Selecciona un nivel académico válido.")
        if len(datos["isbn_editorial"]) > 100:
            errores.append("ISBN/editorial no puede superar 100 caracteres.")
        if not datos["materia_id"].isdigit():
            errores.append("Selecciona una materia válida.")
        elif not obtener_bd().execute(
            "SELECT 1 FROM materias WHERE id = %s AND activo",
            (int(datos["materia_id"]),),
        ).fetchone():
            errores.append("La materia seleccionada no existe o está inactiva.")
        return datos, errores

    @app.route("/admin/libros/nuevo", methods=["GET", "POST"])
    @rol_requerido("admin")
    def crear_libro():
        datos = {}
        if request.method == "POST":
            datos, errores = validar_libro_formulario()
            if not errores:
                fila = obtener_bd().execute(
                    """
                    INSERT INTO libros
                        (titulo, autor, materia_id, nivel, isbn_editorial)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        datos["titulo"],
                        datos["autor"],
                        int(datos["materia_id"]),
                        datos["nivel"],
                        datos["isbn_editorial"] or None,
                    ),
                ).fetchone()
                flash("Libro creado correctamente. Ya puedes agregar ejemplares.", "success")
                return redirect(url_for("ejemplares_admin", libro_id=fila["id"]))
            for error in errores:
                flash(error, "danger")
        return render_template(
            "libro_form.html",
            libro=datos,
            materias=obtener_materias_activas(),
            niveles=NIVELES_LIBRO,
            es_nuevo=True,
        )

    @app.route("/admin/libros/<int:libro_id>/editar", methods=["GET", "POST"])
    @rol_requerido("admin")
    def editar_libro(libro_id: int):
        conexion = obtener_bd()
        libro = conexion.execute(
            """
            SELECT id, titulo, autor, materia_id, nivel, isbn_editorial, activo
              FROM libros
             WHERE id = %s
            """,
            (libro_id,),
        ).fetchone()
        if libro is None:
            abort(404)

        if request.method == "POST":
            datos, errores = validar_libro_formulario()
            if not errores:
                conexion.execute(
                    """
                    UPDATE libros
                       SET titulo = %s, autor = %s, materia_id = %s,
                           nivel = %s, isbn_editorial = %s
                     WHERE id = %s
                    """,
                    (
                        datos["titulo"],
                        datos["autor"],
                        int(datos["materia_id"]),
                        datos["nivel"],
                        datos["isbn_editorial"] or None,
                        libro_id,
                    ),
                )
                flash("Libro actualizado correctamente.", "success")
                return redirect(url_for("libros_admin"))
            for error in errores:
                flash(error, "danger")
            libro = {**libro, **datos}

        return render_template(
            "libro_form.html",
            libro=libro,
            materias=obtener_materias_activas(),
            niveles=NIVELES_LIBRO,
            es_nuevo=False,
        )

    @app.post("/admin/libros/<int:libro_id>/estado")
    @rol_requerido("admin")
    def cambiar_estado_libro(libro_id: int):
        conexion = obtener_bd()
        libro = conexion.execute(
            """
            SELECT l.id, l.activo, m.activo AS materia_activa
              FROM libros l
              JOIN materias m ON m.id = l.materia_id
             WHERE l.id = %s
            """,
            (libro_id,),
        ).fetchone()
        if libro is None:
            abort(404)
        nuevo_estado = not libro["activo"]
        if nuevo_estado and not libro["materia_activa"]:
            flash("Reactiva primero la materia asociada al libro.", "danger")
            return redirect(url_for("libros_admin"))
        conexion.execute(
            "UPDATE libros SET activo = %s WHERE id = %s",
            (nuevo_estado, libro_id),
        )
        accion = "reactivado" if nuevo_estado else "desactivado"
        flash(f"Libro {accion} correctamente.", "success")
        return redirect(url_for("libros_admin"))

    @app.route("/admin/libros/<int:libro_id>/ejemplares", methods=["GET", "POST"])
    @rol_requerido("admin")
    def ejemplares_admin(libro_id: int):
        conexion = obtener_bd()
        libro = conexion.execute(
            """
            SELECT l.id, l.titulo, l.autor, l.activo, m.nombre AS materia
              FROM libros l
              JOIN materias m ON m.id = l.materia_id
             WHERE l.id = %s
            """,
            (libro_id,),
        ).fetchone()
        if libro is None:
            abort(404)

        if request.method == "POST":
            valor = request.form.get("cantidad", "").strip()
            if not libro["activo"]:
                flash(
                    "El libro está inactivo. Reactívalo antes de agregar ejemplares.",
                    "danger",
                )
            elif not valor.isdigit() or not 1 <= int(valor) <= 100:
                flash("La cantidad debe ser un número entre 1 y 100.", "danger")
            else:
                codigos = crear_ejemplares(conexion, libro_id, int(valor))
                flash(
                    f"Se crearon {len(codigos)} ejemplar(es): "
                    f"{codigos[0]} a {codigos[-1]}.",
                    "success",
                )
                return redirect(url_for("ejemplares_admin", libro_id=libro_id))

        return render_template(
            "ejemplares.html",
            libro=libro,
            ejemplares=consultar_ejemplares(conexion, libro_id),
            estados=ESTADOS_FISICOS,
        )

    @app.post("/admin/ejemplares/<int:ejemplar_id>/estado-fisico")
    @rol_requerido("admin")
    def cambiar_estado_fisico_ejemplar(ejemplar_id: int):
        estado = request.form.get("estado_fisico", "").strip()
        if estado not in ESTADOS_FISICOS:
            abort(400)
        fila = obtener_bd().execute(
            """
            UPDATE ejemplares
               SET estado_fisico = %s
             WHERE id = %s
             RETURNING libro_id
            """,
            (estado, ejemplar_id),
        ).fetchone()
        if fila is None:
            abort(404)
        flash(f"Estado físico actualizado a {estado}.", "success")
        return redirect(url_for("ejemplares_admin", libro_id=fila["libro_id"]))

    @app.post("/admin/ejemplares/<int:ejemplar_id>/estado")
    @rol_requerido("admin")
    def cambiar_estado_ejemplar(ejemplar_id: int):
        fila = obtener_bd().execute(
            """
            UPDATE ejemplares
               SET activo = NOT activo
             WHERE id = %s
             RETURNING libro_id, activo
            """,
            (ejemplar_id,),
        ).fetchone()
        if fila is None:
            abort(404)
        accion = "reactivado" if fila["activo"] else "desactivado"
        flash(f"Ejemplar {accion} correctamente.", "success")
        return redirect(url_for("ejemplares_admin", libro_id=fila["libro_id"]))

    def obtener_etiquetas(ids: list[int]) -> list[dict]:
        filas = obtener_bd().execute(
            """
            SELECT e.id, e.codigo_qr, l.titulo
              FROM ejemplares e
              JOIN libros l ON l.id = e.libro_id
             WHERE e.id = ANY(%s)
            """,
            (ids,),
        ).fetchall()
        por_id = {fila["id"]: fila for fila in filas}
        return [por_id[ejemplar_id] for ejemplar_id in ids if ejemplar_id in por_id]

    @app.get("/admin/ejemplares/<int:ejemplar_id>/qr.png")
    @rol_requerido("admin")
    def qr_ejemplar(ejemplar_id: int):
        etiquetas = obtener_etiquetas([ejemplar_id])
        if not etiquetas:
            abort(404)
        ejemplar = etiquetas[0]
        return send_file(
            generar_qr_png(ejemplar["codigo_qr"]),
            mimetype="image/png",
            download_name=f"qr-{ejemplar['codigo_qr']}.png",
            max_age=0,
        )

    @app.get("/admin/ejemplares/<int:ejemplar_id>/etiqueta.pdf")
    @rol_requerido("admin")
    def etiqueta_ejemplar_pdf(ejemplar_id: int):
        etiquetas = obtener_etiquetas([ejemplar_id])
        if not etiquetas:
            abort(404)
        ejemplar = etiquetas[0]
        return send_file(
            generar_pdf_etiquetas(etiquetas),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"etiqueta-{ejemplar['codigo_qr']}.pdf",
        )

    @app.post("/admin/etiquetas-qr.pdf")
    @rol_requerido("admin")
    def etiquetas_qr_pdf():
        valores = request.form.getlist("ejemplar_id")
        libro_id = request.form.get("libro_id", "").strip()
        ids = list(dict.fromkeys(int(valor) for valor in valores if valor.isdigit()))
        if not ids:
            flash("Selecciona al menos un ejemplar para generar el PDF.", "warning")
            if libro_id.isdigit():
                return redirect(url_for("ejemplares_admin", libro_id=int(libro_id)))
            return redirect(url_for("libros_admin"))
        etiquetas = obtener_etiquetas(ids)
        if len(etiquetas) != len(ids):
            abort(404)
        return send_file(
            generar_pdf_etiquetas(etiquetas),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="etiquetas-qr.pdf",
        )

    @app.get("/escaneo")
    @login_requerido
    def escaneo():
        return render_template("scanner.html")

    @app.get("/api/ejemplar/<path:codigo_qr>")
    @api_login_requerido
    def api_ejemplar(codigo_qr: str):
        codigo = normalizar_codigo(codigo_qr)
        if not codigo_valido(codigo):
            return jsonify(
                ok=False,
                error={
                    "codigo": "codigo_invalido",
                    "mensaje": "El código del ejemplar no tiene un formato válido.",
                },
            ), 400

        ejemplar = consultar_ejemplar_por_codigo(obtener_bd(), codigo)
        if ejemplar is None:
            return jsonify(
                ok=False,
                error={
                    "codigo": "codigo_no_registrado",
                    "mensaje": "Código no registrado.",
                },
            ), 404

        prestamo_activo = contexto_prestamo_activo(ejemplar)
        if prestamo_activo is not None:
            operacion = "devolucion"
        elif ejemplar["disponibilidad"] == "Disponible":
            operacion = "prestamo"
        else:
            operacion = "bloqueado"

        return jsonify(
            ok=True,
            operacion=operacion,
            ejemplar={
                "codigo_qr": ejemplar["codigo_qr"],
                "titulo": ejemplar["titulo"],
                "autor": ejemplar["autor"],
                "materia": ejemplar["materia"],
                "nivel": ejemplar["nivel"],
                "estado_fisico": ejemplar["estado_fisico"],
                "activo": ejemplar["activo"],
                "libro_activo": ejemplar["libro_activo"],
                "disponibilidad": ejemplar["disponibilidad"],
            },
            prestamo_activo=prestamo_activo,
        )

    def error_operacion(error: ReglaOperacionError):
        return jsonify(
            ok=False,
            error={"codigo": error.codigo, "mensaje": error.mensaje},
        ), error.estado_http

    @app.get("/api/lectores")
    @api_login_requerido
    def api_lectores():
        texto = request.args.get("q", "")
        return jsonify(ok=True, lectores=buscar_lectores(obtener_bd(), texto))

    @app.post("/api/prestamos")
    @api_login_requerido
    def api_registrar_prestamo():
        codigo = normalizar_codigo(request.form.get("codigo_qr", ""))
        if not codigo_valido(codigo):
            return error_operacion(
                ReglaOperacionError(
                    "codigo_invalido",
                    "El código del ejemplar no tiene un formato válido.",
                    400,
                )
            )

        lector_id_texto = request.form.get("lector_id", "").strip()
        if lector_id_texto and not lector_id_texto.isdigit():
            return error_operacion(
                ReglaOperacionError(
                    "lector_invalido", "Selecciona un lector válido.", 400
                )
            )
        try:
            prestamo = registrar_prestamo(
                obtener_bd(),
                codigo_qr=codigo,
                usuario_id=g.usuario["id"],
                lector_id=int(lector_id_texto) if lector_id_texto else None,
                lector_nombres=request.form.get("lector_nombres", ""),
                lector_apellidos=request.form.get("lector_apellidos", ""),
                nivel_alumno=request.form.get("nivel_alumno", "").strip(),
                grado_seccion_alumno=request.form.get(
                    "grado_seccion_alumno", ""
                ),
                tipo_plazo=request.form.get("tipo_plazo", "").strip(),
                fecha_personalizada=request.form.get(
                    "fecha_personalizada", ""
                ).strip(),
            )
        except ReglaOperacionError as error:
            return error_operacion(error)
        return jsonify(
            ok=True,
            mensaje="Préstamo registrado correctamente.",
            prestamo=prestamo,
        ), 201

    @app.post("/api/devoluciones")
    @api_login_requerido
    def api_registrar_devolucion():
        codigo = normalizar_codigo(request.form.get("codigo_qr", ""))
        if not codigo_valido(codigo):
            return error_operacion(
                ReglaOperacionError(
                    "codigo_invalido",
                    "El código del ejemplar no tiene un formato válido.",
                    400,
                )
            )
        try:
            devolucion = registrar_devolucion(
                obtener_bd(), codigo_qr=codigo, usuario_id=g.usuario["id"]
            )
        except ReglaOperacionError as error:
            return error_operacion(error)
        return jsonify(
            ok=True,
            mensaje="Devolución registrada correctamente.",
            devolucion=devolucion,
        )

    @app.get("/admin/prestamos")
    @rol_requerido("admin")
    def prestamos_admin():
        filtro = request.args.get("estado", "todos").strip().lower()
        if filtro not in {"todos", "activos", "vencidos", "devueltos"}:
            filtro = "todos"
        return render_template(
            "prestamos.html",
            prestamos=consultar_prestamos(obtener_bd(), filtro),
            filtro=filtro,
        )

    @app.get("/admin/reportes")
    @rol_requerido("admin")
    def reportes_admin():
        reporte = request.args.get("reporte", "inventario").strip().lower()
        if reporte not in {"inventario", "activos", "vencidos", "historial"}:
            reporte = "inventario"

        fecha_desde_texto = request.args.get("desde", "").strip()
        fecha_hasta_texto = request.args.get("hasta", "").strip()
        fecha_desde = None
        fecha_hasta = None
        error_rango = ""
        if reporte == "historial":
            try:
                fecha_desde = (
                    date.fromisoformat(fecha_desde_texto)
                    if fecha_desde_texto
                    else None
                )
                fecha_hasta = (
                    date.fromisoformat(fecha_hasta_texto)
                    if fecha_hasta_texto
                    else None
                )
            except ValueError:
                error_rango = "El rango contiene una fecha inválida."
            if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
                error_rango = "La fecha inicial no puede ser posterior a la fecha final."

        conexion = obtener_bd()
        consultas = {
            "inventario": reporte_inventario,
            "activos": reporte_prestamos_activos,
            "vencidos": reporte_prestamos_vencidos,
        }
        if error_rango:
            filas = []
        elif reporte == "historial":
            filas = reporte_historial(conexion, fecha_desde, fecha_hasta)
        else:
            filas = consultas[reporte](conexion)

        respuesta = render_template(
            "reportes.html",
            reporte=reporte,
            filas=filas,
            desde=fecha_desde_texto,
            hasta=fecha_hasta_texto,
            error_rango=error_rango,
        )
        return (respuesta, 400) if error_rango else respuesta

    @app.errorhandler(403)
    def acceso_denegado(_error):
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def pagina_no_encontrada(_error):
        return render_template("404.html"), 404

    @app.errorhandler(psycopg.Error)
    def error_base_datos(_error):
        return render_template("error_bd.html"), 503

    return app


app = crear_app()


if __name__ == "__main__":
    app.run()
