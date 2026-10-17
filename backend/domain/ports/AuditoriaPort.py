"""Puerto: AuditoriaPort."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.entities.Trazabilidad import Trazabilidad


class AuditoriaPort(ABC):
    @abstractmethod
    async def registrar(self, consulta: Consulta, respuesta: Respuesta) -> None:
        """Registra la interacción consulta-respuesta con fines de trazabilidad."""
        ...

    @abstractmethod
    async def obtener_trazabilidad(self, consulta_id: UUID) -> Trazabilidad | None:
        """HU-10 (D-9): consulta + respuesta auditada completa (si existe)."""
        ...

    @abstractmethod
    async def listar_trazabilidad(self, limite: int = 20) -> list[Trazabilidad]:
        """HU-10/HU-14: últimas consultas con su respuesta auditada."""
        ...
