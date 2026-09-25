"""Caso de uso: RegistrarConsulta."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.entities.Consulta import Consulta
from domain.ports.ConsultaRepository import ConsultaRepository
from domain.value_objects.IntencionConsulta import IntencionConsulta


class RegistrarConsulta:
    """Registra y persiste una consulta realizada por un ciudadano."""

    def __init__(self, consulta_repository: ConsultaRepository) -> None:
        self._consulta_repository = consulta_repository

    async def ejecutar(
        self,
        pregunta: str,
        usuario_id: UUID | None = None,
        intencion: IntencionConsulta | None = None,
    ) -> Consulta:
        if not pregunta or not pregunta.strip():
            raise ValueError('La pregunta no puede estar vacía.')

        consulta = Consulta(
            id=uuid4(),
            usuario_id=usuario_id,
            pregunta=pregunta.strip(),
            intencion=intencion,
            creada_en=datetime.now(timezone.utc),
        )

        return await self._consulta_repository.guardar(consulta)