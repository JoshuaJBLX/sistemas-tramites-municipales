"""Entidad de dominio: Municipalidad."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Municipalidad:
    id: UUID
    nombre: str
    departamento: str
    provincia: str
    distrito: str
    sitio_web: str | None = None
