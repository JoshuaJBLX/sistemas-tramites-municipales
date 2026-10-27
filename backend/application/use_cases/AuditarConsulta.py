"""Caso de uso: AuditarConsulta."""

from datetime import datetime
from uuid import UUID

from application.services.ServicioAuditoria import ServicioAuditoria
from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.entities.Trazabilidad import Trazabilidad


class AuditarConsulta:
    """Registra la trazabilidad de una consulta y su respuesta."""

    def __init__(self, servicio_auditoria: ServicioAuditoria) -> None:
        self._servicio_auditoria = servicio_auditoria

    async def ejecutar(
        self,
        consulta: Consulta,
        respuesta: Respuesta,
        duracion_ms: int | None = None,
    ) -> None:
        await self._servicio_auditoria.registrar_interaccion(
            consulta, respuesta, duracion_ms
        )

    async def consultar_trazabilidad(self, consulta_id: UUID) -> Trazabilidad | None:
        """HU-10 (D-9): la consulta con su respuesta auditada completa."""
        return await self._servicio_auditoria.obtener_trazabilidad(consulta_id)

    async def listar_trazabilidad(self, limite: int = 20) -> list[Trazabilidad]:
        return await self._servicio_auditoria.listar_trazabilidad(limite)

    # HU-14
    async def listar_trazabilidad_filtrada(
        self,
        limite: int = 20,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        texto: str | None = None,
        usuario_id: UUID | None = None,
    ) -> list[Trazabilidad]:
        return await self._servicio_auditoria.listar_trazabilidad_filtrada(
            limite, desde, hasta, texto, usuario_id
        )

    async def marcar_inconsistente(
        self,
        consulta_id: UUID,
        marcado: bool,
        nota: str | None,
        marcado_por: str,
    ) -> None:
        await self._servicio_auditoria.marcar_inconsistente(
            consulta_id, marcado, nota, marcado_por
        )