"""Caso de uso: GestionarDocumentos."""

from uuid import UUID

from domain.entities.Documento import Documento
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.value_objects.EstadoDocumento import EstadoDocumento


class GestionarDocumentos:
    """Administra el ciclo de vida de los documentos oficiales indexados."""

    def __init__(
        self,
        documento_repository: DocumentoRepository,
        busqueda_semantica: BusquedaSemanticaPort,
    ) -> None:
        self._documento_repository = documento_repository
        self._busqueda_semantica = busqueda_semantica

    async def registrar(self, documento: Documento) -> Documento:
        """Indexa el documento generando su embedding antes de persistirlo."""
        documento.embedding = await self._busqueda_semantica.generar_embedding(
            documento.contenido
        )
        return await self._documento_repository.guardar(documento)

    async def listar(self, tramite_id: UUID) -> list[Documento]:
        return await self._documento_repository.listar_por_tramite(tramite_id)

    async def actualizar_estado(
        self, documento_id: UUID, estado: EstadoDocumento
    ) -> Documento | None:
        documento = await self._documento_repository.obtener_por_id(documento_id)
        if documento is None:
            return None

        documento.estado = estado
        return await self._documento_repository.guardar(documento)

    async def eliminar(self, documento_id: UUID) -> None:
        await self._documento_repository.eliminar(documento_id)