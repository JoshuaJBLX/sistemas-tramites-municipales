"""Servicio de aplicación: ServicioAuditoria."""

from datetime import datetime
from uuid import UUID

from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.entities.Trazabilidad import Trazabilidad
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
        self,
        consulta: Consulta,
        respuesta: Respuesta,
        duracion_ms: int | None = None,
    ) -> None:
        await self._auditoria.registrar(consulta, respuesta, duracion_ms)

    async def obtener_consulta(self, consulta_id: UUID) -> Consulta | None:
        return await self._consulta_repository.obtener_por_id(consulta_id)

    async def obtener_trazabilidad(self, consulta_id: UUID) -> Trazabilidad | None:
        """HU-10 (D-9): consulta con su respuesta auditada completa."""
        return await self._auditoria.obtener_trazabilidad(consulta_id)

    async def listar_trazabilidad(self, limite: int = 20) -> list[Trazabilidad]:
        """HU-10/HU-14: últimas consultas con su respuesta auditada."""
        return await self._auditoria.listar_trazabilidad(limite)

    # HU-14
    async def listar_trazabilidad_filtrada(
        self,
        limite: int = 20,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        texto: str | None = None,
        usuario_id: UUID | None = None,
    ) -> list[Trazabilidad]:
        return await self._auditoria.listar_trazabilidad_filtrada(
            limite, desde, hasta, texto, usuario_id
        )

    async def marcar_inconsistente(
        self,
        consulta_id: UUID,
        marcado: bool,
        nota: str | None,
        marcado_por: str,
    ) -> None:
        await self._auditoria.marcar_inconsistente(consulta_id, marcado, nota, marcado_por)