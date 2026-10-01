"""Servicio de aplicación: ServicioSLM (Small Language Model)."""

from domain.entities.Documento import Documento
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort

PLANTILLA_SISTEMA = (
    'Eres un asistente municipal. Responde únicamente con la información '
    'contenida en el contexto proporcionado. Si el contexto no contiene la '
    'respuesta, indícalo explícitamente y sugiere acudir a la municipalidad.'
)

# Estructura de salida para que la respuesta sea clara y ordenable (HU-09).
INSTRUCCION_ESTRUCTURA = (
    'Organiza la respuesta en estos apartados, solo si el contexto los respalda: '
    'REQUISITOS, PASOS, COSTO, PLAZO y OBSERVACIONES. Si el contexto no aporta '
    'un dato, escribe "No especificado en la base documental" en ese apartado. '
    'No inventes montos, plazos ni documentos que no aparezcan en el contexto.'
)


class ServicioSLM:
    """Construye el prompt y delega la generación al modelo de lenguaje."""

    def __init__(self, generacion_respuesta: GeneracionRespuestaPort) -> None:
        self._generacion_respuesta = generacion_respuesta

    async def generar(self, pregunta: str, contexto: list[Documento]) -> str:
        if not contexto:
            return (
                'No encontré información oficial en la base documental para '
                'responder tu consulta. Te recomiendo acudir a la oficina de '
                'trámites de tu municipalidad.'
            )

        return await self._generacion_respuesta.generar(pregunta, contexto)

    def construir_prompt(self, pregunta: str, contexto: list[Documento]) -> str:
        fragmentos = '\n\n'.join(
            f'[Documento: {documento.titulo}]\n{documento.contenido}'
            for documento in contexto
        )
        return (
            f'{PLANTILLA_SISTEMA}\n\n{INSTRUCCION_ESTRUCTURA}'
            f'\n\nContexto:\n{fragmentos}\n\nPregunta: {pregunta}'
        )