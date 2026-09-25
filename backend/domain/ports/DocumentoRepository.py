"""Puerto: DocumentoRepository."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.Documento import Documento


class DocumentoRepository(ABC):
    @abstractmethod
    async def guardar(self, documento: Documento) -> Documento:
        ...

    @abstractmethod
    async def obtener_por_id(self, documento_id: UUID) -> Documento | None:
        ...

    @abstractmethod
    async def listar_por_tramite(self, tramite_id: UUID) -> list[Documento]:
        ...

    @abstractmethod
    async def eliminar(self, documento_id: UUID) -> None:
        ...
