"""Puerto: FragmentoRepository (chunks del documento)."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.FragmentoDocumento import FragmentoDocumento


class FragmentoRepository(ABC):
    @abstractmethod
    async def guardar_lote(self, fragmentos: list[FragmentoDocumento]) -> int:
        """Persiste los fragmentos de un documento; devuelve cuántos se guardaron."""
        ...

    @abstractmethod
    async def listar_por_documento(self, documento_id: UUID) -> list[FragmentoDocumento]:
        ...

    @abstractmethod
    async def eliminar_por_documento(self, documento_id: UUID) -> None:
        ...