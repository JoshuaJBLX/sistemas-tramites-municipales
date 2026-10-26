"""Puerto: TramiteCatalogoPort."""

from abc import ABC, abstractmethod
from uuid import UUID

from domain.value_objects.TramiteProbable import TramiteProbable


class TramiteCatalogoPort(ABC):
    @abstractmethod
    async def buscar_por_documentos(
        self, documento_ids: list[UUID]
    ) -> list[TramiteProbable]:
        """Devuelve los trámites del catálogo vinculados a los documentos dados.

        Se usa para convertir los documentos recuperados por el RAG en datos
        estructurados del trámite (requisitos, arancel y plazo) verificados en la
        base de datos, en lugar de dejarlos al redactado del modelo (HU-05, HU-07).
        """
        ...

    @abstractmethod
    async def buscar_por_texto(self, texto: str) -> TramiteProbable | None:
        """Busca en el catálogo el trámite cuyo nombre coincida con el texto.

        La mayoría de los trámites del TUPA no tienen documentos indexados
        (el RAG no puede responder sobre ellos); este método permite orientar
        al ciudadano con los datos estructurados del propio catálogo
        (requisitos, arancel, plazo y área responsable).
        """
        ...

    @abstractmethod
    async def relacionados(
        self, tramite_id: UUID, limite: int = 4
    ) -> list[TramiteProbable]:
        """Trámites más parecidos al indicado, por similitud de sus embeddings.

        Base del motor de recomendación de trámites complementarios (HU-12).
        """
        ...