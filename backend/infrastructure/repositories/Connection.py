"""Gestión de la conexión a PostgreSQL (pool de conexiones asyncpg)."""

import os

import asyncpg


class Connection:
    """Encapsula el pool de conexiones a PostgreSQL con extensión pgvector."""

    def __init__(self, dsn: str | None = None) -> None:
        self._dsn = dsn or self._construir_dsn_desde_entorno()
        self._pool: asyncpg.Pool | None = None

    @staticmethod
    def _construir_dsn_desde_entorno() -> str:
        return (
            f"postgresql://{os.getenv('POSTGRES_USER', 'tramites')}:"
            f"{os.getenv('POSTGRES_PASSWORD', 'tramites')}@"
            f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
            f"{os.getenv('POSTGRES_PORT', '5432')}/"
            f"{os.getenv('POSTGRES_DB', 'tramites_municipales')}"
        )

    async def conectar(self, min_size: int = 1, max_size: int = 10) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                dsn=self._dsn, min_size=min_size, max_size=max_size
            )

    async def desconectar(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    @property
    def pool(self) -> asyncpg.Pool:
        if self._pool is None:
            raise RuntimeError(
                'El pool de conexiones no está inicializado. '
                'Ejecuta await Connection.conectar() primero.'
            )
        return self._pool