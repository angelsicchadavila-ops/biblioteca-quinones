"""Aplicación Flask base de la Biblioteca Quiñones."""

from __future__ import annotations

import os
import secrets
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
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from utils.db import iniciar_bd, obtener_bd


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
        return render_template("index.html")

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
        return render_template("admin_dashboard.html")

    @app.get("/escaneo")
    @login_requerido
    def escaneo():
        return render_template("scanner.html")

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
