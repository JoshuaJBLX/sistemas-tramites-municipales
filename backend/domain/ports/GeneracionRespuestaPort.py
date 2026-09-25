"""Puerto: GeneracionRespuestaPort."""

from abc import ABC, abstractmethod

from domain.entities.Documento import Documento


class GeneracionRespuestaPort(ABC):
    @abstractmethod
    async def generar(self, pregunta: str, contexto: list[Documento]) -> str:
        """Genera una respuesta en lenguaje natural (SLM) a partir del contexto RAG."""
        ...
