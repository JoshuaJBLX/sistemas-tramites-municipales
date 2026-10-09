"""Caso de uso: GestionarDocumentos.

Administra el ciclo de vida de los documentos oficiales: registro con indexado
automático, consulta con filtros (G-12), actualización de metadatos, cambio de
estado —incluida la derogación (HU-03)— y baja lógica para auditoría.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from domain.entities.Documento import Documento
from domain.errors import DocumentoInvalidoError
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.value_objects.EstadoDocumento import EstadoDocumento


class GestionarDocumentos:
    """Reglas de negocio del módulo documental (HU-01..HU-04)."""

    def __init__(
        self,
        documento_repository: DocumentoRepository,
        busqueda_semantica: BusquedaSemanticaPort,
    ) -> None:
        self._documento_repository = documento_repository
        self._busqueda_semantica = busqueda_semantica

    async def registrar(self, documento: Documento) -> Documento:
        """Publica (si es vigente) y genera el embedding antes de persistir."""
        if documento.estado == EstadoDocumento.VIGENTE:
            faltantes = documento.requiere_metadatos()
            if faltantes:
                raise DocumentoInvalidoError(
                    f'No se puede publicar el documento: faltan metadatos '
                    f'obligatorios ({faltantes}).'
                )
        documento.embedding = await self._busqueda_semantica.generar_embedding(
            f'{documento.titulo}\n{documento.contenido}'
        )
        return await self._documento_repository.guardar(documento)

    async def listar(
        self,
        tramite_id: UUID | None = None,
        estado: EstadoDocumento | None = None,
        incluir_eliminados: bool = False,
        limite: int = 100,
        desde: int = 0,
    ) -> list[Documento]:
        return await self._documento_repository.listar(
            tramite_id=tramite_id,
            estado=estado,
            incluir_eliminados=incluir_eliminados,
            limite=limite,
            desde=desde,
        )

    async def listar_por_tramite(self, tramite_id: UUID) -> list[Documento]:
        return await self._documento_repository.listar_por_tramite(tramite_id)

    async def obtener(self, documento_id: UUID) -> Documento | None:
        return await self._documento_repository.obtener_por_id(documento_id)

    async def actualizar(
        self,
        documento_id: UUID,
        *,
        titulo: str | None = None,
        contenido: str | None = None,
        url_origen: str | None = None,
        version: str | None = None,
        fecha_publicacion: object | None = None,
        estado: EstadoDocumento | None = None,
    ) -> Documento | None:
        """Actualiza metadatos y reconcifica el embedding si cambió el texto."""
        documento = await self._documento_repository.obtener_por_id(documento_id)
        if documento is None:
            return None

        if titulo is not None:
            documento.titulo = titulo
        if url_origen is not None:
            documento.url_origen = url_origen
        if version is not None:
            documento.version = version
        if fecha_publicacion is not None:
            documento.fecha_publicacion = fecha_publicacion
        if estado is not None:
            documento.estado = estado

        cambio_texto = contenido is not None and contenido != documento.contenido
        if cambio_texto:
            documento.contenido = contenido

        if documento.estado == EstadoDocumento.VIGENTE:
            faltantes = documento.requiere_metadatos()
            if faltantes:
                raise DocumentoInvalidoError(
                    f'No se puede publicar el documento: faltan metadatos '
                    f'obligatorios ({faltantes}).'
                )

        if cambio_texto or documento.indexado is False:
            documento.embedding = await self._busqueda_semantica.generar_embedding(
                f'{documento.titulo}\n{documento.contenido}'
            )

        return await self._documento_repository.guardar(documento)

    async def actualizar_estado(
        self, documento_id: UUID, estado: EstadoDocumento
    ) -> Documento | None:
        return await self.actualizar(documento_id, estado=estado)

    async def eliminar(self, documento_id: UUID) -> None:
        """Baja lógica: conserva el documento para auditoría (HU-03)."""
        documento = await self._documento_repository.obtener_por_id(documento_id)
        if documento is not None and not documento.esta_eliminado():
            await self._documento_repository.marcar_eliminado(
                documento_id, datetime.now(timezone.utc)
            )

    async def eliminar_fisico(self, documento_id: UUID) -> None:
        """Eliminación definitiva (solo limpieza administrativa explícita)."""
        await self._documento_repository.eliminar_fisico(documento_id)