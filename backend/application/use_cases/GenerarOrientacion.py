"""Caso de uso: GenerarOrientacion."""

from uuid import UUID

from application.services.ServicioOrientacion import ServicioOrientacion
from domain.entities.Respuesta import Respuesta


class GenerarOrientacion:
    """Genera la orientación al ciudadano a partir de fuentes oficiales."""

    def __init__(self, servicio_orientacion: ServicioOrientacion) -> None:
        self._servicio_orientacion = servicio_orientacion

    async def ejecutar(self, consulta_id: UUID, pregunta: str) -> Respuesta:
        if not pregunta or not pregunta.strip():
            raise ValueError('La pregunta no puede estar vacía.')

        return await self._servicio_orientacion.orientar(
            consulta_id=consulta_id,
            pregunta=pregunta.strip(),
        )