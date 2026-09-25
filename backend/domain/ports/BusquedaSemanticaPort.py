"""Puerto: BusquedaSemanticaPort."""

from abc import ABC, abstractmethod

from domain.entities.Documento import Documento


class BusquedaSemanticaPort(ABC):
    @abstractmethod
    async def buscar(self, consulta: str, top_k: int = 5) -> list[Documento]:
        """Busca documentos semánticamente relevantes usando embeddings vectoriales."""
        ...

    @abstractmethod
    async def generar_embedding(self, texto: str) -> list[float]:
        """Genera el vector de embedding para un texto dado."""
        ...
