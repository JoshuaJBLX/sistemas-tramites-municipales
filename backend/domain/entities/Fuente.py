"""Entidad de dominio: Fuente."""

from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.FuenteOficial import FuenteOficial


@dataclass
class Fuente:
    id: UUID
    documento_id: UUID
    tipo: FuenteOficial
    url: str
    fragmento: str
    puntuacion_relevancia: float = 0.0
