"""Puerto: CachePort."""

from abc import ABC, abstractmethod
from typing import Any


class CachePort(ABC):
    @abstractmethod
    async def obtener(self, clave: str) -> Any | None:
        ...

    @abstractmethod
    async def guardar(self, clave: str, valor: Any, ttl_segundos: int = 3600) -> None:
        ...

    @abstractmethod
    async def eliminar(self, clave: str) -> None:
        ...
