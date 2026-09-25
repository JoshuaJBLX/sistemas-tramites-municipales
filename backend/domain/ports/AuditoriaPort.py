"""Puerto: AuditoriaPort."""

from abc import ABC, abstractmethod

from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta


class AuditoriaPort(ABC):
    @abstractmethod
    async def registrar(self, consulta: Consulta, respuesta: Respuesta) -> None:
        """Registra la interacción consulta-respuesta con fines de trazabilidad."""
        ...
