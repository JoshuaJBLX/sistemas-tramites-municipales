"""Caso de uso: ClasificarIntencion."""

from application.services.ServicioNLP import ServicioNLP
from domain.value_objects.IntencionConsulta import IntencionConsulta


class ClasificarIntencion:
    """Determina la intención de la consulta del ciudadano."""

    def __init__(self, servicio_nlp: ServicioNLP) -> None:
        self._servicio_nlp = servicio_nlp

    async def ejecutar(self, pregunta: str) -> IntencionConsulta:
        if not pregunta or not pregunta.strip():
            raise ValueError('La pregunta no puede estar vacía.')

        return await self._servicio_nlp.clasificar_intencion(pregunta)