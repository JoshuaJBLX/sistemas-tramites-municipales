"""Caso de uso: RecomendarTramites (HU-12).

Devuelve los trámites del catálogo más parecidos a uno dado, para mostrarlos
como complementarios junto a la ficha de un trámite. El criterio es la similitud
de los embeddings de sus documentos oficiales, calculada por el adaptador del
catálogo —no por reglas manuales—.
"""

from __future__ import annotations

from uuid import UUID

from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.TramiteProbable import TramiteProbable

LIMITE_POR_DEFECTO = 4


class RecomendarTramites:
    """Motor de recomendación de trámites relacionados."""

    def __init__(
        self, catalogo: TramiteCatalogoPort, limite: int = LIMITE_POR_DEFECTO
    ) -> None:
        self._catalogo = catalogo
        self._limite = limite

    async def ejecutar(
        self, tramite_id: UUID, limite: int | None = None
    ) -> list[TramiteProbable]:
        """Trámites relacionados con `tramite_id`, de mayor a menor similitud."""
        return await self._catalogo.relacionados(
            tramite_id, limite=limite or self._limite
        )
