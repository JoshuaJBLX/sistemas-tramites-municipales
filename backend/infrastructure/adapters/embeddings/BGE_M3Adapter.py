"""Adaptador de embeddings basado en el modelo BGE-M3."""

import asyncio
import os

from sentence_transformers import SentenceTransformer


class BGE_M3Adapter:
    """Genera embeddings de texto usando el modelo multilingüe BGE-M3."""

    def __init__(
        self,
        nombre_modelo: str | None = None,
        dispositivo: str | None = None,
    ) -> None:
        self._nombre_modelo = nombre_modelo or os.getenv(
            'EMBEDDING_MODEL', 'BAAI/bge-m3'
        )
        self._dispositivo = dispositivo or os.getenv('EMBEDDING_DEVICE', 'cpu')
        self._modelo: SentenceTransformer | None = None

    @property
    def dimension(self) -> int:
        return 1024  # BGE-M3 produce vectores de 1024 dimensiones.

    def _cargar_modelo(self) -> SentenceTransformer:
        if self._modelo is None:
            self._modelo = SentenceTransformer(
                self._nombre_modelo, device=self._dispositivo
            )
        return self._modelo

    async def generar_embedding(self, texto: str) -> list[float]:
        """Genera el embedding de un texto en un hilo aparte (evita bloquear el loop)."""
        return await asyncio.to_thread(self._generar_sincrono, texto)

    def _generar_sincrono(self, texto: str) -> list[float]:
        modelo = self._cargar_modelo()
        vector = modelo.encode(texto, normalize_embeddings=True)
        return [float(valor) for valor in vector]