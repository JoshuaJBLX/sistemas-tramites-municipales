"""Entidad de dominio: Respuesta."""

from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.Fuente import Fuente
from domain.value_objects.NivelConfianza import NivelConfianza


@dataclass
class Respuesta:
    id: UUID
    consulta_id: UUID
    texto: str
    confianza: NivelConfianza
    fuentes: list[Fuente] = field(default_factory=list)

    def es_confiable(self) -> bool:
        return self.confianza in (NivelConfianza.ALTA, NivelConfianza.MEDIA)
