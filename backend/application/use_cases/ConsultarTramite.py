"""Caso de uso: ConsultarTramite."""

from uuid import UUID

from domain.entities.Documento import Documento
from domain.ports.CachePort import CachePort
from domain.ports.DocumentoRepository import DocumentoRepository


class ConsultarTramite:
    """Obtiene la información documental oficial vigente de un trámite."""

    def __init__(
        self,
        documento_repository: DocumentoRepository,
        cache: CachePort | None = None,
        ttl_segundos: int = 1800,
    ) -> None:
        self._documento_repository = documento_repository
        self._cache = cache
        self._ttl_segundos = ttl_segundos

    async def ejecutar(self, tramite_id: UUID) -> list[Documento]:
        clave = f'tramite:{tramite_id}:documentos'

        if self._cache is not None:
            en_cache = await self._cache.obtener(clave)
            if en_cache is not None:
                return en_cache

        documentos = await self._documento_repository.listar_por_tramite(tramite_id)
        vigentes = [documento for documento in documentos if documento.esta_vigente()]

        if self._cache is not None:
            await self._cache.guardar(clave, vigentes, ttl_segundos=self._ttl_segundos)

        return vigentes