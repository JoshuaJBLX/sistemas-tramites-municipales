"""Caso de uso: AuditarConsulta."""

from uuid import UUID

from application.services.ServicioAuditoria import ServicioAuditoria
from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta


class AuditarConsulta:
    """Registra la trazabilidad de una consulta y su respuesta."""

    def __init__(self, servicio_auditoria: ServicioAuditoria) -> None:
        self._servicio_auditoria = servicio_auditoria

    async def ejecutar(self, consulta: Consulta, respuesta: Respuesta) -> None:
        await self._servicio_auditoria.registrar_interaccion(consulta, respuesta)

    async def consultar_trazabilidad(self, consulta_id: UUID) -> Consulta | None:
        return await self._servicio_auditoria.obtener_consulta(consulta_id)