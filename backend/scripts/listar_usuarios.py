import asyncio
import os
import sys

sys.path.insert(0, "backend")
import asyncpg


async def main():
    conn = await asyncpg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    filas = await conn.fetch("SELECT correo, rol, nombre FROM usuarios ORDER BY rol")
    for f in filas:
        print(f"User: {f['correo']} | Role: {f['rol']} | Name: {f['nombre']}")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
