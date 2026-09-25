"""Puerto: ConsultaRepository."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.Consulta import Consulta


class ConsultaRepository(ABC):
    @abstractmethod
    async def guardar(self, consulta: Consulta) -> Consulta:
        ...

    @abstractmethod
    async def obtener_por_id(self, consulta_id: UUID) -> Consulta | None:
        ...

    @abstractmethod
    async def listar_por_usuario(self, usuario_id: UUID) -> list[Consulta]:
        ...
