"""Entidad de dominio: Documento."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.value_objects.EstadoDocumento import EstadoDocumento


@dataclass
class Documento:
    id: UUID
    tramite_id: UUID
    titulo: str
    contenido: str
    url_origen: str
    estado: EstadoDocumento
    embedding: list[float] | None = None
    actualizado_en: datetime | None = None

    def esta_vigente(self) -> bool:
        return self.estado == EstadoDocumento.VIGENTE
