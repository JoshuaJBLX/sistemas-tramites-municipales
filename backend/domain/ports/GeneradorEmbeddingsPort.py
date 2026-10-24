"""Puerto: GeneradorEmbeddingsPort."""

from abc import ABC, abstractmethod


class GeneradorEmbeddingsPort(ABC):
    """Puerto para generar embeddings de texto."""

    @abstractmethod
    def generar_embedding(self, texto: str) -> list[float]:
        """Genera embedding para un texto."""
        ...

    @abstractmethod
    def generar_embeddings_batch(self, textos: list[str]) -> list[list[float]]:
        """Genera embeddings para múltiples textos."""
        ...
