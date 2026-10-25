"""Adaptador del SLM servido por OpenRouter."""

import os

import httpx

from domain.entities.Documento import Documento
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort

PROMPT_SISTEMA = (
    'Eres un asistente experto en trámites municipales. Responde en español, '
    'de forma muy breve y concreta (máximo 4 pasos numerados y luego apartados '
    'cortos), usando exclusivamente el contexto entregado. '
    'Si el contexto no responde la pregunta, dilo explícitamente.'
)


class OpenRouterAdapter(GeneracionRespuestaPort):
    """Genera respuestas usando OpenRouter API (compatible con OpenAI)."""

    def __init__(
        self,
        api_key: str | None = None,
        modelo: str | None = None,
        timeout_segundos: float = 120.0,
    ) -> None:
        self._api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self._api_key:
            raise ValueError(
                'OPENROUTER_API_KEY es requerido para OpenRouterAdapter'
            )

        self._modelo = modelo or os.getenv(
            'OPENROUTER_MODEL',
            # Verificado empíricamente contra OpenRouter (2026-10-25): el
            # modelo anterior 'meta-llama/llama-3-8b-instruct' ya no existe (404).
            'meta-llama/llama-3.3-70b-instruct'
        )
        self._timeout_segundos = timeout_segundos
        self._url_base = 'https://openrouter.ai/api/v1'

    async def generar(
        self,
        pregunta: str,
        contexto: list[Documento],
        instrucciones: str | None = None,
    ) -> str:
        prompt = self.construir_prompt(pregunta, contexto)
        sistema = (
            f'{PROMPT_SISTEMA}\n\n{instrucciones}' if instrucciones else PROMPT_SISTEMA
        )

        payload = {
            'model': self._modelo,
            'messages': [
                {'role': 'system', 'content': sistema},
                {'role': 'user', 'content': prompt},
            ],
            'temperature': 0.2,
            'max_tokens': 320,
        }

        headers = {
            'Authorization': f'Bearer {self._api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://tramites-municipales.app',  # Tu dominio o localhost
            'X-Title': 'Sistema de Tramites Municipales',  # sin acentos: httpx codifica headers en ASCII
        }

        async with httpx.AsyncClient(timeout=self._timeout_segundos) as cliente:
            respuesta = await cliente.post(
                f'{self._url_base}/chat/completions',
                json=payload,
                headers=headers
            )
            respuesta.raise_for_status()
            datos = respuesta.json()

        try:
            return datos['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError) as e:
            raise RuntimeError(f'Error al procesar respuesta de OpenRouter: {e}')

    @staticmethod
    def construir_prompt(pregunta: str, contexto: list[Documento]) -> str:
        if not contexto:
            return f'Pregunta: {pregunta}\n\nNo se recuperó contexto documental.'

        fragmentos = '\n\n'.join(
            f'--- Fuente: {documento.titulo} ({documento.url_origen}) ---\n{documento.contenido}'
            for documento in contexto
        )
        return f'Contexto:\n{fragmentos}\n\nPregunta: {pregunta}'
