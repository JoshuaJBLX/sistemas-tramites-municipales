"""Puerto: AuditoriaPort."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.entities.Trazabilidad import Trazabilidad


class AuditoriaPort(ABC):
    @abstractmethod
    async def registrar(
        self,
        consulta: Consulta,
        respuesta: Respuesta,
        duracion_ms: int | None = None,
    ) -> None:
        """Registra la interacción consulta-respuesta con fines de trazabilidad.

        `duracion_ms` (HU-16) es el tiempo que tardó la generación de la
        respuesta; `tramite_probable` se toma de la propia respuesta.
        """
        ...

    @abstractmethod
    async def obtener_trazabilidad(self, consulta_id: UUID) -> Trazabilidad | None:
        """HU-10 (D-9): consulta + respuesta auditada completa (si existe)."""
        ...

    @abstractmethod
    async def listar_trazabilidad(self, limite: int = 20) -> list[Trazabilidad]:
        """HU-10/HU-14: últimas consultas con su respuesta auditada."""
        ...
