"""Adaptador del SLM servido por Ollama."""

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


class OllamaAdapter(GeneracionRespuestaPort):
    """Genera respuestas con un modelo pequeño ejecutado localmente en Ollama."""

    def __init__(
        self,
        url_base: str | None = None,
        modelo: str | None = None,
        timeout_segundos: float = 120.0,
    ) -> None:
        self._url_base = (url_base or os.getenv('OLLAMA_URL', 'http://localhost:11434')).rstrip('/')
        self._modelo = modelo or os.getenv('OLLAMA_MODEL', 'qwen2.5:3b')
        self._timeout_segundos = timeout_segundos

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
            'prompt': prompt,
            'system': sistema,
            'stream': False,
            'options': {'temperature': 0.2, 'num_predict': 320},
        }

        async with httpx.AsyncClient(timeout=self._timeout_segundos) as cliente:
            respuesta = await cliente.post(f'{self._url_base}/api/generate', json=payload)
            respuesta.raise_for_status()
            datos = respuesta.json()

        return datos.get('response', '').strip()

    @staticmethod
    def construir_prompt(pregunta: str, contexto: list[Documento]) -> str:
        if not contexto:
            return f'Pregunta: {pregunta}\n\nNo se recuperó contexto documental.'

        fragmentos = '\n\n'.join(
            f'--- Fuente: {documento.titulo} ({documento.url_origen}) ---\n{documento.contenido}'
            for documento in contexto
        )
        return f'Contexto:\n{fragmentos}\n\nPregunta: {pregunta}'