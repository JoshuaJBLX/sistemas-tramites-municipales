"""Implementación concreta de DocumentoRepository con baja lógica (HU-03)."""

from datetime import datetime
from uuid import UUID

from domain.entities.Documento import Documento
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository

QUERY_UPSERT = """
    INSERT INTO documentos (id, tramite_id, titulo, contenido, url_origen, estado,
                            version, fecha_publicacion, archivo_nombre, mime_type,
                            hash_contenido, fragmentado, eliminado_en, embedding, actualizado_en)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, NOW())
    ON CONFLICT (id) DO UPDATE SET
        titulo = EXCLUDED.titulo,
        contenido = EXCLUDED.contenido,
        url_origen = EXCLUDED.url_origen,
        estado = EXCLUDED.estado,
        version = EXCLUDED.version,
        fecha_publicacion = EXCLUDED.fecha_publicacion,
        archivo_nombre = COALESCE(EXCLUDED.archivo_nombre, documentos.archivo_nombre),
        mime_type = COALESCE(EXCLUDED.mime_type, documentos.mime_type),
        hash_contenido = COALESCE(EXCLUDED.hash_contenido, documentos.hash_contenido),
        fragmentado = EXCLUDED.fragmentado,
        eliminado_en = EXCLUDED.eliminado_en,
        embedding = COALESCE(EXCLUDED.embedding, documentos.embedding),
        actualizado_en = NOW()
    RETURNING id, tramite_id, titulo, contenido, url_origen, estado,
              version, fecha_publicacion, archivo_nombre, mime_type,
              hash_contenido, fragmentado, eliminado_en, actualizado_en,
              (embedding IS NOT NULL) AS indexado
"""

QUERY_SELECT_ID = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado,
           version, fecha_publicacion, archivo_nombre, mime_type,
           hash_contenido, fragmentado, eliminado_en, actualizado_en,
           (embedding IS NOT NULL) AS indexado
    FROM documentos
    WHERE id = $1
"""

QUERY_SELECT_TRAMITE = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado,
           version, fecha_publicacion, archivo_nombre, mime_type,
           hash_contenido, fragmentado, eliminado_en, actualizado_en,
           (embedding IS NOT NULL) AS indexado
    FROM documentos
    WHERE tramite_id = $1 AND eliminado_en IS NULL
    ORDER BY actualizado_en DESC
"""

QUERY_LISTAR = """
    SELECT id, tramite_id, titulo, contenido, url_origen, estado,
           version, fecha_publicacion, archivo_nombre, mime_type,
           hash_contenido, fragmentado, eliminado_en, actualizado_en,
           (embedding IS NOT NULL) AS indexado
    FROM documentos
    WHERE ($1::uuid IS NULL OR tramite_id = $1)
      AND ($2::text IS NULL OR estado = $2)
      AND ($3::boolean OR eliminado_en IS NULL)
    ORDER BY actualizado_en DESC
    LIMIT $4 OFFSET $5
"""

QUERY_DELETE_FISICO = 'DELETE FROM documentos WHERE id = $1'
QUERY_DELETE_FRAGMENTOS = 'DELETE FROM fragmentos_documento WHERE documento_id = $1'
QUERY_MARCAR_ELIMINADO = 'UPDATE documentos SET eliminado_en = $2, actualizado_en = NOW() WHERE id = $1'


def _formatear_vector(embedding: list[float] | None, es_pgvector: bool) -> str | None:
    if embedding is None:
        return None
    valores = ','.join(str(v) for v in embedding)
    return f'[{valores}]' if es_pgvector else f'{{{valores}}}'


def _mapear_documento(fila) -> Documento:
    fecha = fila['fecha_publicacion']
    return Documento(
        id=fila['id'],
        tramite_id=fila['tramite_id'],
        titulo=fila['titulo'],
        contenido=fila['contenido'],
        url_origen=fila['url_origen'],
        estado=EstadoDocumento(fila['estado']),
        version=str(fila['version']) if fila['version'] else '1.0',
        fecha_publicacion=fecha,
        archivo_nombre=fila['archivo_nombre'],
        mime_type=fila['mime_type'],
        hash_contenido=fila['hash_contenido'],
        fragmentado=bool(fila['fragmentado']),
        eliminado_en=fila['eliminado_en'],
        actualizado_en=fila['actualizado_en'],
        indexado=bool(fila['indexado']) if 'indexado' in fila.keys() else False,
    )


class DocumentoRepositoryImpl(PostgreSQLRepository, DocumentoRepository):
    async def guardar(self, documento: Documento) -> Documento:
        es_pgvector = await self._connection.es_pgvector()
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
            documento.version,
            documento.fecha_publicacion,
            documento.archivo_nombre,
            documento.mime_type,
            documento.hash_contenido,
            1 if documento.fragmentado else 0,
            documento.eliminado_en,
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

    async def listar(
        self,
        tramite_id: UUID | None = None,
        estado: EstadoDocumento | None = None,
        incluir_eliminados: bool = False,
        limite: int = 100,
        desde: int = 0,
    ) -> list[Documento]:
        filas = await self.obtener_muchos(
            QUERY_LISTAR,
            tramite_id,
            estado.value if estado else None,
            incluir_eliminados,
            limite,
            desde,
        )
        return [_mapear_documento(fila) for fila in filas]

    async def marcar_eliminado(self, documento_id: UUID, eliminado_en: datetime) -> None:
        await self.ejecutar(QUERY_MARCAR_ELIMINADO, documento_id, eliminado_en)

    async def eliminar_fisico(self, documento_id: UUID) -> None:
        await self.ejecutar(QUERY_DELETE_FRAGMENTOS, documento_id)
        await self.ejecutar(QUERY_DELETE_FISICO, documento_id)