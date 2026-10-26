"""Crea (o actualiza) el usuario administrador inicial (HU-13 / G-01).

Uso (desde backend/):
    ADMIN_CORREO=admin@munihuancayo.gob.pe ADMIN_PASSWORD=... \
        python -m scripts.crear_admin

La contraseña se almacena hasheada (PBKDF2-SHA256); nunca se guarda en claro
ni se registra en el repositorio.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from infrastructure.adapters.auth.PasswordHasher import hash_password  # noqa: E402
from infrastructure.repositories.Connection import Connection  # noqa: E402

QUERY_ADMIN_POR_CORREO = """
    SELECT id, rol FROM usuarios WHERE correo = $1
"""

QUERY_INSERT_ADMIN = """
    INSERT INTO usuarios (id, nombre, correo, rol, password_hash, activo, creado_en)
    VALUES ($1, $2, $3, 'administrador', $4, TRUE, $5)
    RETURNING id
"""

QUERY_ACTIVAR_Y_ACTUALIZAR = """
    UPDATE usuarios
    SET rol = 'administrador', password_hash = $2, activo = TRUE
    WHERE id = $1
"""


async def main() -> None:
    correo = os.getenv('ADMIN_CORREO', 'admin@munihuancayo.gob.pe')
    password = os.getenv('ADMIN_PASSWORD')
    nombre = os.getenv('ADMIN_NOMBRE', 'Administrador')

    if not password or len(password) < 8:
        raise SystemExit(
            'Define ADMIN_PASSWORD (mínimo 8 caracteres), p. ej.: '
            'ADMIN_PASSWORD=... python -m scripts.crear_admin'
        )

    connection = Connection()
    await connection.conectar()
    try:
        async with connection.pool.acquire() as conexion:
            existente = await conexion.fetchrow(QUERY_ADMIN_POR_CORREO, correo)
            if existente:
                await conexion.execute(
                    QUERY_ACTIVAR_Y_ACTUALIZAR, existente['id'], hash_password(password)
                )
                print(f'Administrador actualizado: {correo} (id {existente["id"]})')
            else:
                fila = await conexion.fetchrow(
                    QUERY_INSERT_ADMIN,
                    uuid4(),
                    nombre,
                    correo,
                    hash_password(password),
                    datetime.now(timezone.utc),
                )
                print(f'Administrador creado: {correo} (id {fila["id"]})')
    finally:
        await connection.desconectar()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
