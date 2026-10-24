"""Adaptador de embeddings usando OpenAI API."""

import asyncio
import os

from openai import OpenAI


class OpenAIEmbeddingsAdapter:
    """Genera embeddings usando OpenAI API (text-embedding-3-small)."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self._api_key:
            raise ValueError('OPENAI_API_KEY es requerido para OpenAIEmbeddingsAdapter')

        self._model = model or os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
        self._client = OpenAI(api_key=self._api_key)

    @property
    def dimension(self) -> int:
        # text-embedding-3-small produce vectores de 1536 dimensiones
        return 1536

    async def generar_embedding(self, texto: str) -> list[float]:
        """Genera embedding para un texto usando OpenAI (async wrapper)."""
        return await asyncio.to_thread(self._generar_sincrono, texto)

    def _generar_sincrono(self, texto: str) -> list[float]:
        """Genera embedding de forma síncrona."""
        response = self._client.embeddings.create(
            model=self._model,
            input=texto
        )
        return response.data[0].embedding

    def generar_embeddings_batch(self, textos: list[str]) -> list[list[float]]:
        """Genera embeddings para múltiples textos (batch)."""
        response = self._client.embeddings.create(
            model=self._model,
            input=textos
        )
        return [item.embedding for item in response.data]
