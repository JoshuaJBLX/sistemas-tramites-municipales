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