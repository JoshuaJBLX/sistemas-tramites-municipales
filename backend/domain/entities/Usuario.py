"""Entidad de dominio: Usuario."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Usuario:
    id: UUID
    nombre: str
    correo: str
    rol: str  # 'ciudadano' | 'administrador'
    creado_en: datetime

    def es_administrador(self) -> bool:
        return self.rol == 'administrador'
