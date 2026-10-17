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
    titulo: str = ''
    puntuacion_relevancia: float = 0.0
    # --- Metadatos de trazabilidad (HU-10 / P3-08): lo disponible del
    # documento (número de resolución, fecha de publicación, versión). ---
    numero: str = ''
    fecha: str = ''
    version: str = ''
