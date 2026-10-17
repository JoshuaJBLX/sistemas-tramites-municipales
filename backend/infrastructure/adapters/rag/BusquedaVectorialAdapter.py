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
           version, fecha_publicacion,
           1 - (embedding <=> $1::vector) AS similitud
    FROM documentos
    WHERE embedding IS NOT NULL
      AND estado = 'vigente'
    ORDER BY embedding <=> $1::vector
    LIMIT $2
"""

QUERY_BUSQUEDA_IN_MEMORIA = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           version, fecha_publicacion,
           embedding
    FROM documentos
    WHERE embedding IS NOT NULL
      AND estado = 'vigente'
"""

# Recuperación por fragmento (HU-04 / P2-14): el ranking se decide a nivel de
# chunk y después se reagrupa en el documento padre.
QUERY_FRAGMENTOS_PGVECTOR = """
    SELECT d.id, d.tramite_id, d.titulo, d.contenido, d.url_origen, d.estado,
           d.actualizado_en, d.version, d.fecha_publicacion,
           f.contenido AS fragmento,
           1 - (f.embedding <=> $1::vector) AS similitud
    FROM fragmentos_documento f
    JOIN documentos d ON d.id = f.documento_id
    WHERE f.embedding IS NOT NULL
      AND d.estado = 'vigente'
      AND d.eliminado_en IS NULL
    ORDER BY f.embedding <=> $1::vector
    LIMIT $2
"""

QUERY_FRAGMENTOS_IN_MEMORIA = """
    SELECT d.id, d.tramite_id, d.titulo, d.contenido, d.url_origen, d.estado,
           d.actualizado_en, d.version, d.fecha_publicacion,
           f.contenido AS fragmento, f.embedding
    FROM fragmentos_documento f
    JOIN documentos d ON d.id = f.documento_id
    WHERE f.embedding IS NOT NULL
      AND d.estado = 'vigente'
      AND d.eliminado_en IS NULL
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


def _mapear_documento(fila, similitud: float = 0.0, fragmento: str | None = None) -> Documento:
    return Documento(
        id=fila['id'],
        tramite_id=fila['tramite_id'],
        titulo=fila['titulo'],
        contenido=fila['contenido'],
        url_origen=fila['url_origen'],
        estado=EstadoDocumento(fila['estado']),
        actualizado_en=fila['actualizado_en'],
        version=fila['version'] or '1.0',
        fecha_publicacion=fila['fecha_publicacion'],
        puntuacion_similitud=similitud,
        fragmento_destacado=fragmento,
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

        # 1) Recuperación por fragmento (HU-04): ranking a nivel de chunk.
        documentos = await self._buscar_por_fragmento(embedding, top_k)
        if documentos:
            return documentos

        # 2) Sin fragmentos indexados (primer arranque): búsqueda a nivel de
        #    documento, con el mismo umbral.
        if await self._connection.es_pgvector():
            return await self._buscar_pgvector(embedding, top_k)
        return await self._buscar_en_memoria(embedding, top_k)

    async def _buscar_por_fragmento(
        self, embedding: list[float], top_k: int
    ) -> list[Documento]:
        """Reordena los documentos según su mejor fragmento y conserva ese chunk.

        Devuelve una lista vacía cuando la tabla `fragmentos_documento` está
        vacía o todavía no existe, para degradar a la búsqueda por documento.
        """
        try:
            if await self._connection.es_pgvector():
                async with self._connection.pool.acquire() as conexion:
                    filas = await conexion.fetch(
                        QUERY_FRAGMENTOS_PGVECTOR,
                        _formatear_vector(embedding),
                        max(top_k * 4, 20),
                    )
            else:
                async with self._connection.pool.acquire() as conexion:
                    filas = await conexion.fetch(QUERY_FRAGMENTOS_IN_MEMORIA)
        except Exception:  # noqa: BLE001 - tabla ausente o BD no migrada aún
            return []

        if not filas:
            return []

        puntuados: list[tuple[Documento, float]] = []
        for fila in filas:
            if 'similitud' in fila.keys():
                similitud = float(fila['similitud'] or 0.0)
            else:
                similitud = _coseno(embedding, fila['embedding'])
            if similitud < self._umbral_similitud:
                continue
            puntuados.append((_mapear_documento(fila, similitud, fila['fragmento']), similitud))

        # Un documento puede aparecer por varios fragmentos: se queda con el
        # de mayor similitud y se ordena el conjunto por esa puntuación.
        mejor_por_documento: dict = {}
        for documento, similitud in puntuados:
            previo = mejor_por_documento.get(documento.id)
            if previo is None or similitud > previo[1]:
                mejor_por_documento[documento.id] = (documento, similitud)

        ordenados = sorted(
            mejor_por_documento.values(), key=lambda par: -par[1]
        )
        return [documento for documento, _ in ordenados[:top_k]]

    async def _buscar_pgvector(self, embedding: list[float], top_k: int) -> list[Documento]:
        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(
                QUERY_BUSQUEDA_VECTORIAL_PGVECTOR, _formatear_vector(embedding), top_k
            )

        return [
            _mapear_documento(fila, float(fila['similitud']))
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
            _mapear_documento(fila, similitud)
            for similitud, fila in candidatos
            if similitud >= self._umbral_similitud
        ][:top_k]

    async def generar_embedding(self, texto: str) -> list[float]:
        return await self._generador_embeddings.generar_embedding(texto)