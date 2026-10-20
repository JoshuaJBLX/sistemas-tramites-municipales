"""Puerto: GeneracionRespuestaPort."""

from abc import ABC, abstractmethod

from domain.entities.Documento import Documento


class GeneracionRespuestaPort(ABC):
    @abstractmethod
    async def generar(
        self,
        pregunta: str,
        contexto: list[Documento],
        instrucciones: str | None = None,
    ) -> str:
        """Genera una respuesta en lenguaje natural (SLM) a partir del contexto RAG.

        `instrucciones` permite pedir un formato de salida concreto (p. ej. la
        estructura de apartados del HU-09) sin acoplar el formato al adaptador.
        """
        ...
