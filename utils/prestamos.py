"""Reglas transaccionales de lectores, préstamos, devoluciones y reportes."""

from __future__ import annotations

from datetime import date

import psycopg

from utils.catalogo import escapar_patron_like, normalizar_texto


NIVELES_ALUMNO = ("Primaria", "Secundaria")
TIPOS_PLAZO = ("7", "14", "personalizada")


class ReglaOperacionError(Exception):
    """Error esperado de una regla de negocio, apto para mostrar al operador."""

    def __init__(self, codigo: str, mensaje: str, estado_http: int = 409) -> None:
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje
        self.estado_http = estado_http


def _texto_fecha(valor) -> str | None:
    return valor.isoformat(timespec="minutes") if valor is not None else None


def _prestamo_serializable(fila: dict) -> dict:
    return {
        "id": fila["prestamo_id"],
        "lector": f"{fila['lector_nombres']} {fila['lector_apellidos']}",
        "nivel_alumno": fila["nivel_alumno"],
        "grado_seccion_alumno": fila["grado_seccion_alumno"],
        "fecha_prestamo": _texto_fecha(fila["fecha_prestamo"]),
        "fecha_limite": fila["fecha_limite"].isoformat(),
        "estado": fila["estado_prestamo"],
        "dias_atraso": fila["dias_atraso"],
    }


def buscar_lectores(conexion: psycopg.Connection, texto: str) -> list[dict]:
    """Busca lectores por tokens, sin distinguir mayúsculas ni espacios repetidos."""
    busqueda = normalizar_texto(texto)[:200]
    if not busqueda:
        return []

    expresion_nombre = (
        "lower(regexp_replace(btrim(le.nombres || ' ' || le.apellidos), "
        "'\\s+', ' ', 'g'))"
    )
    condiciones = []
    parametros: list[str] = []
    for token in busqueda.split():
        condiciones.append(f"{expresion_nombre} LIKE %s ESCAPE '\\'")
        parametros.append(f"%{escapar_patron_like(token.lower())}%")

    filas = conexion.execute(
        f"""
        SELECT le.id, le.nombres, le.apellidos, le.activo,
               ultimo.nivel_alumno AS ultimo_nivel,
               ultimo.grado_seccion_alumno AS ultimo_grado_seccion,
               coalesce(resumen.prestamos_activos, 0) AS prestamos_activos,
               coalesce(resumen.prestamos_vencidos, 0) AS prestamos_vencidos
          FROM lectores le
          LEFT JOIN LATERAL (
                SELECT p.nivel_alumno, p.grado_seccion_alumno
                  FROM prestamos p
                 WHERE p.lector_id = le.id
                 ORDER BY p.fecha_prestamo DESC, p.id DESC
                 LIMIT 1
          ) ultimo ON TRUE
          LEFT JOIN LATERAL (
                SELECT count(*) FILTER (
                           WHERE p.fecha_devolucion IS NULL
                       ) AS prestamos_activos,
                       count(*) FILTER (
                           WHERE p.fecha_devolucion IS NULL
                             AND p.fecha_limite <
                                 (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                       ) AS prestamos_vencidos
                  FROM prestamos p
                 WHERE p.lector_id = le.id
          ) resumen ON TRUE
         WHERE {" AND ".join(condiciones)}
         ORDER BY le.activo DESC, lower(le.apellidos), lower(le.nombres), le.id
         LIMIT 10
        """,
        parametros,
    ).fetchall()
    return [dict(fila) for fila in filas]


def _obtener_o_crear_lector(
    conexion: psycopg.Connection,
    lector_id: int | None,
    nombres: str,
    apellidos: str,
) -> tuple[dict, bool]:
    if lector_id is not None:
        lector = conexion.execute(
            """
            SELECT id, nombres, apellidos, activo
              FROM lectores
             WHERE id = %s
             FOR UPDATE
            """,
            (lector_id,),
        ).fetchone()
        if lector is None:
            raise ReglaOperacionError(
                "lector_no_existe", "El lector seleccionado ya no existe."
            )
        if not lector["activo"]:
            raise ReglaOperacionError(
                "lector_inactivo", "El lector seleccionado está inactivo."
            )
        return lector, False

    nombres = normalizar_texto(nombres)
    apellidos = normalizar_texto(apellidos)
    if not nombres or not apellidos:
        raise ReglaOperacionError(
            "lector_invalido",
            "Para crear el lector, completa nombres y apellidos.",
            400,
        )
    if len(nombres) > 100 or len(apellidos) > 100:
        raise ReglaOperacionError(
            "lector_invalido",
            "Nombres y apellidos no pueden superar 100 caracteres.",
            400,
        )

    clave = f"{nombres.lower()}|{apellidos.lower()}"
    conexion.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (clave,))
    lector = conexion.execute(
        """
        SELECT id, nombres, apellidos, activo
          FROM lectores
         WHERE lower(regexp_replace(btrim(nombres), '\\s+', ' ', 'g')) = lower(%s)
           AND lower(regexp_replace(btrim(apellidos), '\\s+', ' ', 'g')) = lower(%s)
         ORDER BY activo DESC, id
         LIMIT 1
         FOR UPDATE
        """,
        (nombres, apellidos),
    ).fetchone()
    if lector is not None:
        if not lector["activo"]:
            raise ReglaOperacionError(
                "lector_inactivo",
                "Ya existe un lector inactivo con esos nombres y apellidos.",
            )
        return lector, False

    lector = conexion.execute(
        """
        INSERT INTO lectores (nombres, apellidos)
        VALUES (%s, %s)
        RETURNING id, nombres, apellidos, activo
        """,
        (nombres, apellidos),
    ).fetchone()
    return lector, True


def _calcular_fecha_limite(
    tipo_plazo: str, fecha_personalizada: str, fecha_actual: date
) -> date:
    if tipo_plazo in {"7", "14"}:
        return fecha_actual.fromordinal(fecha_actual.toordinal() + int(tipo_plazo))
    if tipo_plazo != "personalizada":
        raise ReglaOperacionError(
            "plazo_invalido", "Selecciona un plazo de 7 días, 14 días o personalizado.", 400
        )
    try:
        fecha_limite = date.fromisoformat(fecha_personalizada)
    except (TypeError, ValueError):
        raise ReglaOperacionError(
            "fecha_invalida", "Selecciona una fecha personalizada válida.", 400
        ) from None
    if fecha_limite < fecha_actual:
        raise ReglaOperacionError(
            "fecha_invalida",
            "La fecha límite no puede ser anterior a la fecha del préstamo.",
            400,
        )
    return fecha_limite


def registrar_prestamo(
    conexion: psycopg.Connection,
    *,
    codigo_qr: str,
    usuario_id: int,
    lector_id: int | None,
    lector_nombres: str,
    lector_apellidos: str,
    nivel_alumno: str,
    grado_seccion_alumno: str,
    tipo_plazo: str,
    fecha_personalizada: str,
) -> dict:
    """Registra un préstamo atómico y vuelve a validar todas las reglas críticas."""
    grado_seccion_alumno = normalizar_texto(grado_seccion_alumno)
    if nivel_alumno not in NIVELES_ALUMNO:
        raise ReglaOperacionError(
            "nivel_invalido", "Selecciona Primaria o Secundaria.", 400
        )
    if not grado_seccion_alumno or len(grado_seccion_alumno) > 50:
        raise ReglaOperacionError(
            "grado_invalido",
            "El grado y sección es obligatorio y no puede superar 50 caracteres.",
            400,
        )

    try:
        with conexion.transaction():
            reloj = conexion.execute(
                """
                SELECT CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima' AS ahora,
                       (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date AS hoy
                """
            ).fetchone()
            fecha_limite = _calcular_fecha_limite(
                tipo_plazo, fecha_personalizada, reloj["hoy"]
            )

            lector, lector_creado = _obtener_o_crear_lector(
                conexion, lector_id, lector_nombres, lector_apellidos
            )

            ejemplar = conexion.execute(
                """
                SELECT e.id, e.codigo_qr, e.activo, e.estado_fisico,
                       l.titulo, l.activo AS libro_activo,
                       m.activo AS materia_activa
                  FROM ejemplares e
                  JOIN libros l ON l.id = e.libro_id
                  JOIN materias m ON m.id = l.materia_id
                 WHERE e.codigo_qr = %s
                 FOR UPDATE OF e
                """,
                (codigo_qr,),
            ).fetchone()
            if ejemplar is None:
                raise ReglaOperacionError(
                    "codigo_no_registrado", "Código no registrado.", 404
                )
            if not ejemplar["activo"] or not ejemplar["libro_activo"] or not ejemplar["materia_activa"]:
                raise ReglaOperacionError(
                    "ejemplar_inactivo", "El ejemplar está inactivo y no puede prestarse."
                )
            if ejemplar["estado_fisico"] != "Operativo":
                raise ReglaOperacionError(
                    "ejemplar_danado", "El ejemplar está dañado y no puede prestarse."
                )
            if conexion.execute(
                """
                SELECT 1 FROM prestamos
                 WHERE ejemplar_id = %s AND fecha_devolucion IS NULL
                 LIMIT 1
                """,
                (ejemplar["id"],),
            ).fetchone():
                raise ReglaOperacionError(
                    "ejemplar_prestado",
                    "El ejemplar ya tiene un préstamo activo. Actualiza la ficha.",
                )

            resumen = conexion.execute(
                """
                SELECT count(*) AS activos,
                       count(*) FILTER (
                           WHERE fecha_limite < %s
                       ) AS vencidos
                  FROM prestamos
                 WHERE lector_id = %s
                   AND fecha_devolucion IS NULL
                """,
                (reloj["hoy"], lector["id"]),
            ).fetchone()
            if resumen["vencidos"]:
                raise ReglaOperacionError(
                    "lector_con_mora",
                    "El lector tiene al menos un préstamo vencido. Debe devolverlo antes de recibir otro.",
                )
            if resumen["activos"] >= 2:
                raise ReglaOperacionError(
                    "limite_prestamos",
                    "El lector ya tiene dos préstamos activos; no puede recibir un tercero.",
                )

            prestamo = conexion.execute(
                """
                INSERT INTO prestamos (
                    lector_id, ejemplar_id, registrado_por_usuario_id,
                    nivel_alumno, grado_seccion_alumno,
                    fecha_prestamo, fecha_limite
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, fecha_prestamo, fecha_limite
                """,
                (
                    lector["id"],
                    ejemplar["id"],
                    usuario_id,
                    nivel_alumno,
                    grado_seccion_alumno,
                    reloj["ahora"],
                    fecha_limite,
                ),
            ).fetchone()
    except psycopg.errors.UniqueViolation as error:
        raise ReglaOperacionError(
            "ejemplar_prestado",
            "Otro operador prestó este ejemplar primero. Actualiza la ficha.",
        ) from error
    except psycopg.errors.CheckViolation as error:
        detalle = error.diag.message_primary or "La base de datos rechazó la operación."
        raise ReglaOperacionError("regla_bd", detalle) from error

    return {
        "id": prestamo["id"],
        "lector_id": lector["id"],
        "lector": f"{lector['nombres']} {lector['apellidos']}",
        "lector_creado": lector_creado,
        "ejemplar": ejemplar["codigo_qr"],
        "libro": ejemplar["titulo"],
        "fecha_prestamo": _texto_fecha(prestamo["fecha_prestamo"]),
        "fecha_limite": prestamo["fecha_limite"].isoformat(),
    }


def registrar_devolucion(
    conexion: psycopg.Connection, *, codigo_qr: str, usuario_id: int
) -> dict:
    """Cierra el préstamo activo sin borrar historial y conserva al responsable."""
    with conexion.transaction():
        ejemplar = conexion.execute(
            """
            SELECT e.id, e.codigo_qr, e.activo, e.estado_fisico, l.titulo
              FROM ejemplares e
              JOIN libros l ON l.id = e.libro_id
             WHERE e.codigo_qr = %s
             FOR UPDATE OF e
            """,
            (codigo_qr,),
        ).fetchone()
        if ejemplar is None:
            raise ReglaOperacionError(
                "codigo_no_registrado", "Código no registrado.", 404
            )

        prestamo = conexion.execute(
            """
            SELECT p.id, p.fecha_limite,
                   le.nombres, le.apellidos
              FROM prestamos p
              JOIN lectores le ON le.id = p.lector_id
             WHERE p.ejemplar_id = %s
               AND p.fecha_devolucion IS NULL
             FOR UPDATE OF p
            """,
            (ejemplar["id"],),
        ).fetchone()
        if prestamo is None:
            raise ReglaOperacionError(
                "sin_prestamo_activo",
                "El ejemplar no tiene un préstamo activo para devolver.",
            )

        devuelto = conexion.execute(
            """
            UPDATE prestamos
               SET fecha_devolucion = CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima',
                   devuelto_por_usuario_id = %s
             WHERE id = %s
               AND fecha_devolucion IS NULL
            RETURNING fecha_devolucion
            """,
            (usuario_id, prestamo["id"]),
        ).fetchone()
        if devuelto is None:
            raise ReglaOperacionError(
                "sin_prestamo_activo",
                "Otro operador ya registró la devolución. Actualiza la ficha.",
            )

    disponibilidad = (
        "Disponible"
        if ejemplar["activo"] and ejemplar["estado_fisico"] == "Operativo"
        else "No disponible"
    )
    return {
        "id": prestamo["id"],
        "lector": f"{prestamo['nombres']} {prestamo['apellidos']}",
        "ejemplar": ejemplar["codigo_qr"],
        "libro": ejemplar["titulo"],
        "fecha_devolucion": _texto_fecha(devuelto["fecha_devolucion"]),
        "disponibilidad": disponibilidad,
    }


def contexto_prestamo_activo(fila: dict) -> dict | None:
    """Convierte los campos unidos por la consulta QR en una ficha privada."""
    if fila.get("prestamo_id") is None:
        return None
    return _prestamo_serializable(fila)


def consultar_prestamos(conexion: psycopg.Connection, filtro: str) -> list[dict]:
    """Listado administrativo con estado calculado en tiempo real."""
    condiciones = {
        "activos": (
            "p.fecha_devolucion IS NULL AND p.fecha_limite >= "
            "(CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date"
        ),
        "vencidos": (
            "p.fecha_devolucion IS NULL AND p.fecha_limite < "
            "(CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date"
        ),
        "devueltos": "p.fecha_devolucion IS NOT NULL",
    }
    condicion = condiciones.get(filtro, "TRUE")
    return conexion.execute(
        f"""
        SELECT p.id, le.nombres || ' ' || le.apellidos AS lector,
               p.nivel_alumno, p.grado_seccion_alumno,
               l.titulo AS libro, e.codigo_qr AS ejemplar,
               p.fecha_prestamo, p.fecha_limite, p.fecha_devolucion,
               ur.nombre_completo AS registrado_por,
               ud.nombre_completo AS devuelto_por,
               CASE
                   WHEN p.fecha_devolucion IS NOT NULL THEN 'Devuelto'
                   WHEN p.fecha_limite <
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                        THEN 'Vencido'
                   ELSE 'Activo'
               END AS estado,
               CASE
                   WHEN p.fecha_devolucion IS NULL AND p.fecha_limite <
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                   THEN (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                        - p.fecha_limite
                   ELSE 0
               END AS dias_atraso
          FROM prestamos p
          JOIN lectores le ON le.id = p.lector_id
          JOIN ejemplares e ON e.id = p.ejemplar_id
          JOIN libros l ON l.id = e.libro_id
          JOIN usuarios ur ON ur.id = p.registrado_por_usuario_id
          LEFT JOIN usuarios ud ON ud.id = p.devuelto_por_usuario_id
         WHERE {condicion}
         ORDER BY
               (p.fecha_devolucion IS NOT NULL),
               p.fecha_limite,
               p.fecha_prestamo DESC,
               p.id DESC
        """
    ).fetchall()


def reporte_inventario(conexion: psycopg.Connection) -> list[dict]:
    return conexion.execute(
        """
        SELECT l.titulo, m.nombre AS materia,
               count(e.id) FILTER (WHERE e.activo) AS total,
               count(e.id) FILTER (
                   WHERE e.activo AND e.estado_fisico = 'Operativo' AND p.id IS NULL
               ) AS disponibles,
               count(e.id) FILTER (
                   WHERE e.activo AND e.estado_fisico = 'Operativo' AND p.id IS NOT NULL
               ) AS prestados,
               count(e.id) FILTER (
                   WHERE e.activo AND e.estado_fisico = 'Dañado'
               ) AS danados
          FROM libros l
          JOIN materias m ON m.id = l.materia_id
          LEFT JOIN ejemplares e ON e.libro_id = l.id
          LEFT JOIN prestamos p
            ON p.ejemplar_id = e.id AND p.fecha_devolucion IS NULL
         GROUP BY l.id, l.titulo, m.id, m.nombre
         ORDER BY lower(l.titulo), l.id
        """
    ).fetchall()


def reporte_prestamos_activos(conexion: psycopg.Connection) -> list[dict]:
    return conexion.execute(
        """
        SELECT le.nombres || ' ' || le.apellidos AS lector,
               l.titulo AS libro, e.codigo_qr AS ejemplar,
               p.fecha_prestamo, p.fecha_limite,
               CASE WHEN p.fecha_limite <
                    (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                    THEN 'Vencido' ELSE 'Activo' END AS estado
          FROM prestamos p
          JOIN lectores le ON le.id = p.lector_id
          JOIN ejemplares e ON e.id = p.ejemplar_id
          JOIN libros l ON l.id = e.libro_id
         WHERE p.fecha_devolucion IS NULL
         ORDER BY p.fecha_limite, p.fecha_prestamo
        """
    ).fetchall()


def reporte_prestamos_vencidos(conexion: psycopg.Connection) -> list[dict]:
    return conexion.execute(
        """
        SELECT le.nombres || ' ' || le.apellidos AS lector,
               p.nivel_alumno,
               p.grado_seccion_alumno,
               l.titulo AS libro,
               p.fecha_limite,
               (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                   - p.fecha_limite AS dias_atraso
          FROM prestamos p
          JOIN lectores le ON le.id = p.lector_id
          JOIN ejemplares e ON e.id = p.ejemplar_id
          JOIN libros l ON l.id = e.libro_id
         WHERE p.fecha_devolucion IS NULL
           AND p.fecha_limite <
               (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
         ORDER BY p.fecha_limite, le.apellidos, le.nombres
        """
    ).fetchall()


def reporte_historial(
    conexion: psycopg.Connection,
    fecha_desde: date | None,
    fecha_hasta: date | None,
) -> list[dict]:
    condiciones = ["TRUE"]
    parametros: list[date] = []
    if fecha_desde is not None:
        condiciones.append("p.fecha_prestamo::date >= %s")
        parametros.append(fecha_desde)
    if fecha_hasta is not None:
        condiciones.append("p.fecha_prestamo::date <= %s")
        parametros.append(fecha_hasta)
    return conexion.execute(
        f"""
        SELECT le.nombres || ' ' || le.apellidos AS lector,
               l.titulo AS libro,
               e.codigo_qr AS ejemplar,
               p.fecha_prestamo, p.fecha_limite, p.fecha_devolucion,
               CASE
                   WHEN p.fecha_devolucion IS NOT NULL THEN 'Devuelto'
                   WHEN p.fecha_limite <
                        (CURRENT_TIMESTAMP AT TIME ZONE 'America/Lima')::date
                        THEN 'Vencido'
                   ELSE 'Activo'
               END AS estado_final,
               ur.nombre_completo AS registrado_por,
               ud.nombre_completo AS devuelto_por
          FROM prestamos p
          JOIN lectores le ON le.id = p.lector_id
          JOIN ejemplares e ON e.id = p.ejemplar_id
          JOIN libros l ON l.id = e.libro_id
          JOIN usuarios ur ON ur.id = p.registrado_por_usuario_id
          LEFT JOIN usuarios ud ON ud.id = p.devuelto_por_usuario_id
         WHERE {" AND ".join(condiciones)}
         ORDER BY p.fecha_prestamo DESC, p.id DESC
        """,
        parametros,
    ).fetchall()
