"""Entidad de dominio: Trazabilidad (HU-10).

Una consulta registrada junto con su respuesta auditada completa: texto,
confianza, groundedness, fuentes con metadatos y banderas de bloqueo o de
consulta fuera de dominio.
"""

from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.Consulta import Consulta
from domain.entities.Fuente import Fuente


@dataclass
class Trazabilidad:
    consulta: Consulta
    respuesta: str | None = None
    confianza: str | None = None
    groundedness: float = 0.0
    fuentes: list[Fuente] = field(default_factory=list)
    fuera_dominio: bool = False
    afirmaciones_bloqueadas: bool = False
    entidad_sugerida: str = ''
    # HU-16: tiempo de generación (ms) y trámite probable de la respuesta.
    duracion_ms: int | None = None
    tramite_probable: str | None = None
    registrado_en: datetime | None = None
