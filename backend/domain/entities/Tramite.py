"""Entidad de dominio: Tramite."""

from dataclasses import dataclass, field
from uuid import UUID

from domain.value_objects.TipoTramite import TipoTramite


@dataclass
class Tramite:
    id: UUID
    municipalidad_id: UUID
    nombre: str
    descripcion: str
    tipo: TipoTramite
    requisitos: list[str] = field(default_factory=list)
    costo: float = 0.0
    duracion_estimada_dias: int = 0

    def agregar_requisito(self, requisito: str) -> None:
        self.requisitos.append(requisito)
