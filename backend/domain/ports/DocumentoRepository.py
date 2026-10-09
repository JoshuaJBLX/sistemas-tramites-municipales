"""Puerto: DocumentoRepository."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from domain.entities.Documento import Documento
from domain.value_objects.EstadoDocumento import EstadoDocumento


class DocumentoRepository(ABC):
    @abstractmethod
    async def guardar(self, documento: Documento) -> Documento:
        """Inserta o actualiza (upsert por id) un documento."""
        ...

    @abstractmethod
    async def obtener_por_id(self, documento_id: UUID) -> Documento | None:
        ...

    @abstractmethod
    async def listar_por_tramite(self, tramite_id: UUID) -> list[Documento]:
        ...

    @abstractmethod
    async def listar(
        self,
        tramite_id: UUID | None = None,
        estado: EstadoDocumento | None = None,
        incluir_eliminados: bool = False,
        limite: int = 100,
        desde: int = 0,
    ) -> list[Documento]:
        """Lista documentos con filtros opcionales (G-12: panel real)."""
        ...

    @abstractmethod
    async def marcar_eliminado(self, documento_id: UUID, eliminado_en: datetime) -> None:
        """Baja lógica: conserva el documento para auditoría (HU-03)."""
        ...

    @abstractmethod
    async def eliminar_fisico(self, documento_id: UUID) -> None:
        """Eliminación definitiva (solo para limpieza administrativa)."""
        ...