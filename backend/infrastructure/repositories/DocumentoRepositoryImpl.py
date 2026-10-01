"""Implementación concreta de DocumentoRepository sobre PostgreSQL + pgvector."""

from uuid import UUID

from domain.entities.Documento import Documento
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository

QUERY_UPSERT = """
    INSERT INTO documentos (id, tramite_id, titulo, contenido, url_origen, estado, embedding, actualizado_en)
    VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
    ON CONFLICT (id) DO UPDATE SET
        titulo = EXCLUDED.titulo,
        contenido = EXCLUDED.contenido,
        url_origen = EXCLUDED.url_origen,
        estado = EXCLUDED.estado,
        embedding = COALESCE(EXCLUDED.embedding, documentos.embedding),
        actualizado_en = NOW()
    RETURNING id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
              (embedding IS NOT NULL) AS indexado
"""

QUERY_SELECT_ID = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           (embedding IS NOT NULL) AS indexado
    FROM documentos
    WHERE id = $1
"""

QUERY_SELECT_TRAMITE = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
           (embedding IS NOT NULL) AS indexado
    FROM documentos
    WHERE tramite_id = $1
    ORDER BY actualizado_en DESC
"""

QUERY_DELETE = 'DELETE FROM documentos WHERE id = $1'


def _formatear_vector(embedding: list[float] | None, es_pgvector: bool) -> str | None:
    """Convierte una lista de floats a la sintaxis del tipo de columna.

    - pgvector:      `[0.1,0.2,...]` (literal aceptado por el tipo `vector`).
    - double[]:      `{0.1,0.2,...}` (literal de arreglo de PostgreSQL).
    """
    if embedding is None:
        return None
    valores = ','.join(str(valor) for valor in embedding)
    return f'[{valores}]' if es_pgvector else f'{{{valores}}}'


def _mapear_documento(fila) -> Documento:
    return Documento(
        id=fila['id'],
        tramite_id=fila['tramite_id'],
        titulo=fila['titulo'],
        contenido=fila['contenido'],
        url_origen=fila['url_origen'],
        estado=EstadoDocumento(fila['estado']),
        actualizado_en=fila['actualizado_en'],
        indexado=bool(fila['indexado']) if 'indexado' in fila.keys() else False,
    )


class DocumentoRepositoryImpl(PostgreSQLRepository, DocumentoRepository):
    """Persistencia de documentos oficiales y sus embeddings vectoriales."""

    async def guardar(self, documento: Documento) -> Documento:
        es_pgvector = await self._connection.es_pgvector()
        # En servidores sin pgvector asyncpg espera la lista directamente;
        # con pgvector se envía el literal '[..]' que la columna vector acepta.
        embedding = (
            _formatear_vector(documento.embedding, True)
            if es_pgvector
            else documento.embedding
        )
        fila = await self.obtener_uno(
            QUERY_UPSERT,
            documento.id,
            documento.tramite_id,
            documento.titulo,
            documento.contenido,
            documento.url_origen,
            documento.estado.value,
            embedding,
        )
        guardado = _mapear_documento(fila)
        guardado.embedding = documento.embedding
        return guardado

    async def obtener_por_id(self, documento_id: UUID) -> Documento | None:
        fila = await self.obtener_uno(QUERY_SELECT_ID, documento_id)
        return _mapear_documento(fila) if fila else None

    async def listar_por_tramite(self, tramite_id: UUID) -> list[Documento]:
        filas = await self.obtener_muchos(QUERY_SELECT_TRAMITE, tramite_id)
        return [_mapear_documento(fila) for fila in filas]

    async def eliminar(self, documento_id: UUID) -> None:
        await self.ejecutar(QUERY_DELETE, documento_id)