"""Value Object: TramiteProbable.

Trámite del catálogo que mejor explica la consulta del ciudadano, junto con los
datos estructurados que el RAG no puede ofrecer por sí solo (requisitos, arancel
y plazo). Permite que la respuesta sea verificable contra la base de datos en
lugar de depender solo del texto generado (HU-05, HU-07).
"""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class TramiteProbable:
    id: UUID
    nombre: str
    requisitos: list[str] = field(default_factory=list)
    costo: float = 0.0
    duracion_estimada_dias: int = 0
    fuente_url: str | None = None
    documentos_coincidentes: int = 0
    puntaje_relevancia: float = 0.0

    def resumen_requisitos(self, limite: int | None = None) -> list[str]:
        """Devuelve la lista de requisitos, opcionalmente recortada."""
        return self.requisitos if limite is None else self.requisitos[:limite]