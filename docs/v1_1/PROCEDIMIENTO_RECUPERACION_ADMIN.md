# Recuperación técnica de contraseña del administrador

Este procedimiento es exclusivamente de mantenimiento autorizado. No crea administradores, no cambia roles y no reactiva cuentas.

## Requisitos

- Entorno virtual instalado.
- `DATABASE_URL` disponible como variable de entorno o en el archivo local `.env` ignorado por Git.
- Username exacto de una cuenta cuyo rol ya sea `admin`.

## Ejecución

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe scripts\restablecer_password_admin.py
```

El script solicita el username y luego pide dos veces la nueva contraseña mediante `getpass`, por lo que no se muestra en pantalla. La contraseña debe tener al menos 12 caracteres. No debe pasarse como argumento de consola ni guardarse en documentación.

El script confirma el rol, genera un hash Werkzeug y actualiza solo `password_hash` mediante una consulta parametrizada dentro de una transacción. El mensaje final no incluye datos sensibles.

## Verificación posterior

1. Iniciar sesión con el username administrativo y la nueva contraseña.
2. Confirmar acceso al panel de administración.
3. Confirmar que la cuenta conserva su rol y estado previos.
4. No registrar la contraseña ni el hash en capturas, Git, logs o evidencias.
