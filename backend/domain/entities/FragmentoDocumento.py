"""Entidad de dominio: FragmentoDocumento.

Cada documento vigente se divide en fragmentos (chunks) con solape (HU-04 /
G-13). Cada fragmento tiene su propio embedding, lo que permite recuperar el
fragmento exacto en lugar de un documento completo.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FragmentoDocumento:
    id: UUID
    documento_id: UUID
    orden: int
    contenido: str
    embedding: list[float] | None = None
    creado_en: datetime | None = None