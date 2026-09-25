"""Entidad de dominio: Consulta."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.value_objects.IntencionConsulta import IntencionConsulta


@dataclass
class Consulta:
    id: UUID
    usuario_id: UUID | None
    pregunta: str
    intencion: IntencionConsulta | None
    creada_en: datetime

    def clasificada(self) -> bool:
        return self.intencion is not None
