"""Adaptador de embeddings usando OpenAI API (o cualquier compatible).

Compatible con OpenAI y con endpoints OpenAI-compatible (p. ej. OpenRouter)
mediante las variables de entorno:

- OPENAI_API_KEY: clave del proveedor.
- OPENAI_BASE_URL: URL base alternativa (p. ej. https://openrouter.ai/api/v1).
- OPENAI_EMBEDDING_MODEL: modelo a usar (por defecto text-embedding-3-small).
- OPENAI_EMBEDDING_DIMENSIONS: dimensiones del vector (por defecto 1536,
  que es la dimensión nativa de text-embedding-3-small; con OpenRouter
  se usa 1024 para calzar con las columnas vector(1024) del esquema).
"""

import asyncio
import os

from openai import OpenAI


class OpenAIEmbeddingsAdapter:
    """Genera embeddings usando la API de embeddings (OpenAI u compatible)."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self._api_key:
            raise ValueError('OPENAI_API_KEY es requerido para OpenAIEmbeddingsAdapter')

        self._model = model or os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')

        base_url = os.getenv('OPENAI_BASE_URL')
        self._client = OpenAI(api_key=self._api_key, base_url=base_url) if base_url else OpenAI(api_key=self._api_key)

        dimension_env = os.getenv('OPENAI_EMBEDDING_DIMENSIONS')
        self._dimensions = int(dimension_env) if dimension_env else 1536

    @property
    def dimension(self) -> int:
        return self._dimensions

    def _crear_embedding(self, texto: str) -> list[float]:
        """Llama al endpoint /embeddings con `dimensions` (si el modelo lo soporta)."""
        kwargs: dict = {'model': self._model, 'input': texto}
        # text-embedding-3-* permite reducir dimensiones; modelos sin soportarlo
        # ignoran el parámetro o fallan, por eso solo se envía si está configurado.
        if self._dimensions:
            kwargs['dimensions'] = self._dimensions
        response = self._client.embeddings.create(**kwargs)
        return response.data[0].embedding

    async def generar_embedding(self, texto: str) -> list[float]:
        """Genera embedding para un texto (async wrapper)."""
        return await asyncio.to_thread(self._crear_embedding, texto)

    def generar_embeddings_batch(self, textos: list[str]) -> list[list[float]]:
        """Genera embeddings para múltiples textos (batch)."""
        kwargs: dict = {'model': self._model, 'input': textos}
        if self._dimensions:
            kwargs['dimensions'] = self._dimensions
        response = self._client.embeddings.create(**kwargs)
        return [item.embedding for item in response.data]
