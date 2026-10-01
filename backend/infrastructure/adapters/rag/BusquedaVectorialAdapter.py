"""Adaptador de búsqueda semántica sobre PostgreSQL.

- Si la extensión pgvector está disponible: búsqueda nativa con `<=>` (HNSW).
- En servidores sin pgvector (p. ej. desarrollo local sin Docker): los
  embeddings se guardan en `double precision[]` y la similitud de coseno se
  calcula en Python (suficiente para catálogos pequeños).
"""

import numpy as np

from domain.entities.Documento import Documento
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.repositories.Connection import Connection

QUERY_BUSQUEDA_VECTORIAL_PGVECTOR = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           1 - (embedding <=> $1::vector) AS similitud
    FROM documentos
    WHERE embedding IS NOT NULL
      AND estado = 'vigente'
    ORDER BY embedding <=> $1::vector
    LIMIT $2
"""

QUERY_BUSQUEDA_IN_MEMORIA = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           embedding
    FROM documentos
    WHERE embedding IS NOT NULL
      AND estado = 'vigente'
"""


def _formatear_vector(embedding: list[float]) -> str:
    return '[' + ','.join(str(valor) for valor in embedding) + ']'


def _coseno(a: list[float] | None, b: list[float] | None) -> float:
    if not a or not b:
        return 0.0
    va = np.asarray(a, dtype=np.float32)
    vb = np.asarray(b, dtype=np.float32)
    minimo = min(va.size, vb.size)
    if minimo == 0:
        return 0.0
    va, vb = va[:minimo], vb[:minimo]
    norma = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if norma == 0.0:
        return 0.0
    return float(np.dot(va, vb) / norma)


def _mapear_documento(fila) -> Documento:
    return Documento(
        id=fila['id'],
        tramite_id=fila['tramite_id'],
        titulo=fila['titulo'],
        contenido=fila['contenido'],
        url_origen=fila['url_origen'],
        estado=EstadoDocumento(fila['estado']),
        actualizado_en=fila['actualizado_en'],
    )


class BusquedaVectorialAdapter(BusquedaSemanticaPort):
    """Recupera documentos por similitud de coseno (pgvector o en memoria)."""

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

        if await self._connection.es_pgvector():
            return await self._buscar_pgvector(embedding, top_k)
        return await self._buscar_en_memoria(embedding, top_k)

    async def _buscar_pgvector(self, embedding: list[float], top_k: int) -> list[Documento]:
        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(
                QUERY_BUSQUEDA_VECTORIAL_PGVECTOR, _formatear_vector(embedding), top_k
            )

        return [
            _mapear_documento(fila)
            for fila in filas
            if float(fila['similitud']) >= self._umbral_similitud
        ]

    async def _buscar_en_memoria(self, embedding: list[float], top_k: int) -> list[Documento]:
        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(QUERY_BUSQUEDA_IN_MEMORIA)

        candidatos = [
            (_coseno(embedding, fila['embedding']), fila)
            for fila in filas
        ]
        candidatos.sort(key=lambda par: par[0], reverse=True)

        return [
            _mapear_documento(fila)
            for similitud, fila in candidatos
            if similitud >= self._umbral_similitud
        ][:top_k]

    async def generar_embedding(self, texto: str) -> list[float]:
        return await self._generador_embeddings.generar_embedding(texto)