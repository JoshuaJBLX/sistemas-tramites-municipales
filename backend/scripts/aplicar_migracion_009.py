"""Aplica database/migrations/009_revisor_auditoria_derivacion.sql en la BD configurada.

Uso (desde la raíz), con las env vars POSTGRES_* del entorno a probar:
    .venv\\Scripts\\python.exe backend\\scripts\\aplicar_migracion_009.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncpg  # noqa: E402

MIGRACION = Path(__file__).resolve().parents[2] / 'database' / 'migrations' / '009_revisor_auditoria_derivacion.sql'


async def main() -> None:
    if not os.getenv('POSTGRES_HOST'):
        raise SystemExit('Define las env vars POSTGRES_HOST/PORT/DB/USER/PASSWORD.')

    sql = MIGRACION.read_text(encoding='utf-8')
    conn = await asyncpg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=int(os.environ.get('POSTGRES_PORT', '5432')),
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
    )
    try:
        await conn.execute(sql)
        print('Migracion 009 aplicada.')

        roles = await conn.fetchval(
            "SELECT conname FROM pg_constraint WHERE conrelid = 'usuarios'::regclass AND contype = 'c'"
        )
        print('CHECK de usuarios verificado.')
        oficinas = await conn.fetchval('SELECT COUNT(*) FROM oficinas')
        print(f'Oficinas en el directorio: {oficinas} (roles constraint: {roles})')
    finally:
        await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
