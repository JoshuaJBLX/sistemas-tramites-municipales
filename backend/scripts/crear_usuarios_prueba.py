"""Crea o actualiza los usuarios de prueba (administrador, revisor, ciudadano).

Las contraseñas NO se escriben en el código: se leen de variables de entorno
para no filtrar credenciales al repositorio (Ley N.° 29733 y buenas prácticas).

Uso (PowerShell):
    $env:POSTGRES_HOST='...'; $env:POSTGRES_PORT='5432'
    $env:POSTGRES_DB='...';   $env:POSTGRES_USER='...'; $env:POSTGRES_PASSWORD='...'
    $env:SEED_ADMIN_PASSWORD='...'
    $env:SEED_REVISOR_PASSWORD='...'
    $env:SEED_CIUDADANO_PASSWORD='...'
    .venv\\Scripts\\python.exe backend\\scripts\\crear_usuarios_prueba.py

Nunca se imprime la contraseña; solo el correo y el rol.
"""
import asyncio
import os
import sys
from uuid import uuid4

sys.path.insert(0, "backend")
import asyncpg
from infrastructure.adapters.auth.PasswordHasher import hash_password

# (correo, rol, nombre, variable de entorno con la contraseña)
USUARIOS = [
    ("admin@munihuancayo.gob.pe", "administrador", "Administrador", "SEED_ADMIN_PASSWORD"),
    ("revisor@munihuancayo.gob.pe", "revisor", "Revisor Municipal", "SEED_REVISOR_PASSWORD"),
    ("ciudadano@correo.com", "ciudadano", "Juan Ciudadano", "SEED_CIUDADANO_PASSWORD"),
]


def _conexion() -> dict:
    return dict(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


async def main() -> None:
    faltantes = [var for *_, var in USUARIOS if not os.environ.get(var)]
    if faltantes:
        raise SystemExit(
            "Faltan variables de entorno con las contraseñas: " + ", ".join(faltantes)
        )

    conn = await asyncpg.connect(**_conexion())
    try:
        for correo, rol, nombre, var_password in USUARIOS:
            p_hash = hash_password(os.environ[var_password])
            await conn.execute(
                """
                INSERT INTO usuarios (id, nombre, correo, rol, password_hash, activo)
                VALUES ($1, $2, $3, $4, $5, TRUE)
                ON CONFLICT (correo) DO UPDATE
                SET rol = EXCLUDED.rol,
                    password_hash = EXCLUDED.password_hash,
                    nombre = EXCLUDED.nombre,
                    activo = TRUE
                """,
                uuid4(),
                nombre,
                correo,
                rol,
                p_hash,
            )
            print(f"Usuario {rol} creado/actualizado: {correo}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
