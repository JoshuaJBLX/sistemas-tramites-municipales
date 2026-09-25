"""Adaptador de búsqueda semántica sobre PostgreSQL + pgvector."""

from domain.entities.Documento import Documento
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.repositories.Connection import Connection

QUERY_BUSQUEDA_VECTORIAL = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           1 - (embedding <=> $1::vector) AS similitud
    FROM documentos
    WHERE embedding IS NOT NULL
      AND estado = 'vigente'
    ORDER BY embedding <=> $1::vector
    LIMIT $2
"""


def _formatear_vector(embedding: list[float]) -> str:
    return '[' + ','.join(str(valor) for valor in embedding) + ']'


class BusquedaVectorialAdapter(BusquedaSemanticaPort):
    """Recupera documentos por similitud de coseno usando pgvector."""

    def __init__(
        self,
        connection: Connection,
        generador_embeddings: BGE_M3Adapter,
        umbral_similitud: float = 0.3,
    ) -> None:
        self._connection = connection
        self._generador_embeddings = generador_embeddings
        self._umbral_similitud = umbral_similitud

    async def buscar(self, consulta: str, top_k: int = 5) -> list[Documento]:
        embedding = await self.generar_embedding(consulta)

        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(
                QUERY_BUSQUEDA_VECTORIAL, _formatear_vector(embedding), top_k
            )

        return [
            Documento(
                id=fila['id'],
                tramite_id=fila['tramite_id'],
                titulo=fila['titulo'],
                contenido=fila['contenido'],
                url_origen=fila['url_origen'],
                estado=EstadoDocumento(fila['estado']),
                actualizado_en=fila['actualizado_en'],
            )
            for fila in filas
            if float(fila['similitud']) >= self._umbral_similitud
        ]

    async def generar_embedding(self, texto: str) -> list[float]:
        return await self._generador_embeddings.generar_embedding(texto)