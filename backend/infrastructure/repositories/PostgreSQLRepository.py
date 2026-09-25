"""Repositorio base para PostgreSQL."""

from typing import Any, Sequence

from infrastructure.repositories.Connection import Connection


class PostgreSQLRepository:
    """Provee utilidades de acceso a datos compartidas por los repositorios."""

    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    @property
    def connection(self) -> Connection:
        return self._connection

    async def ejecutar(self, query: str, *args: Any) -> str:
        async with self._connection.pool.acquire() as conexion:
            return await conexion.execute(query, *args)

    async def obtener_uno(self, query: str, *args: Any) -> Any:
        async with self._connection.pool.acquire() as conexion:
            return await conexion.fetchrow(query, *args)

    async def obtener_muchos(self, query: str, *args: Any) -> Sequence[Any]:
        async with self._connection.pool.acquire() as conexion:
            return await conexion.fetch(query, *args)