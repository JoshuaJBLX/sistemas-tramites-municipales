"""Servicio de aplicación: ServicioAuditoria."""

from uuid import UUID

from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.ports.AuditoriaPort import AuditoriaPort
from domain.ports.ConsultaRepository import ConsultaRepository


class ServicioAuditoria:
    """Centraliza el registro y la consulta de la trazabilidad."""

    def __init__(
        self,
        auditoria: AuditoriaPort,
        consulta_repository: ConsultaRepository,
    ) -> None:
        self._auditoria = auditoria
        self._consulta_repository = consulta_repository

    async def registrar_interaccion(
        self, consulta: Consulta, respuesta: Respuesta
    ) -> None:
        await self._auditoria.registrar(consulta, respuesta)

    async def obtener_consulta(self, consulta_id: UUID) -> Consulta | None:
        return await self._consulta_repository.obtener_por_id(consulta_id)