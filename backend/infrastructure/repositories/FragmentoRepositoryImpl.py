"""Adaptador: repositorio de fragmentos de documento."""

from uuid import UUID

from domain.entities.FragmentoDocumento import FragmentoDocumento
from domain.ports.FragmentoRepository import FragmentoRepository
from infrastructure.repositories.Connection import Connection
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository


QUERY_ELIMINAR = 'DELETE FROM fragmentos_documento WHERE documento_id = $1'
QUERY_INSERT = """
    INSERT INTO fragmentos_documento (id, documento_id, orden, contenido, embedding, creado_en)
    VALUES ($1, $2, $3, $4, $5, NOW())
"""
QUERY_LISTAR = """
    SELECT id, documento_id, orden, contenido, creado_en
    FROM fragmentos_documento
    WHERE documento_id = $1
    ORDER BY orden
"""


def _formatear_vector(embedding: list[float] | None, es_pgvector: bool) -> str | None:
    if embedding is None:
        return None
    valores = ','.join(str(v) for v in embedding)
    return f'[{valores}]' if es_pgvector else f'{{{valores}}}'


class FragmentoRepositoryImpl(PostgreSQLRepository, FragmentoRepository):
    def __init__(self, connection: Connection) -> None:
        super().__init__(connection)

    async def guardar_lote(self, fragmentos: list[FragmentoDocumento]) -> int:
        if not fragmentos:
            return 0
        es_pgvector = await self._connection.es_pgvector()
        async with self._connection.pool.acquire() as conexion:
            for fragmento in fragmentos:
                vector = (
                    _formatear_vector(fragmento.embedding, True)
                    if es_pgvector
                    else fragmento.embedding
                )
                await conexion.execute(
                    QUERY_INSERT,
                    fragmento.id,
                    fragmento.documento_id,
                    fragmento.orden,
                    fragmento.contenido,
                    vector,
                )
        return len(fragmentos)

    async def listar_por_documento(self, documento_id: UUID) -> list[FragmentoDocumento]:
        filas = await self.obtener_muchos(QUERY_LISTAR, documento_id)
        return [
            FragmentoDocumento(
                id=fila['id'],
                documento_id=fila['documento_id'],
                orden=fila['orden'],
                contenido=fila['contenido'],
                creado_en=fila['creado_en'],
            )
            for fila in filas
        ]

    async def eliminar_por_documento(self, documento_id: UUID) -> None:
        await self.ejecutar(QUERY_ELIMINAR, documento_id)