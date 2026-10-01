"""Caso de uso: IdentificarTramiteProbable."""

from domain.entities.Documento import Documento
from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.TramiteProbable import TramiteProbable

# El trámite elegido debe superar al segundo colocado por este factor.
MARGEN_MINIMO = 1.15
# Y sus documentos deben sumar al menos este puntaje de similitud.
PUNTAJE_MINIMO = 0.45


class IdentificarTramiteProbable:
    """Deduce el trámite del catálogo que corresponde a los documentos recuperados."""

    def __init__(
        self,
        catalogo: TramiteCatalogoPort,
        margen_minimo: float = MARGEN_MINIMO,
        puntaje_minimo: float = PUNTAJE_MINIMO,
    ) -> None:
        self._catalogo = catalogo
        self._margen_minimo = margen_minimo
        self._puntaje_minimo = puntaje_minimo

    async def ejecutar(self, documentos: list[Documento]) -> TramiteProbable | None:
        """Devuelve el trámite más respaldado por los documentos recuperados.

        Los votos se ponderan por la similitud semántica del RAG. Si ningún
        trámite domina claramente al resto, no se propone ninguno: es preferible
        no afirmar de qué trámite se trata antes que señalar el trámite
        equivocado (HU-05, HU-07).
        """
        if not documentos:
            return None

        candidatos = await self._catalogo.buscar_por_documentos(
            [documento.id for documento in documentos]
        )
        if not candidatos:
            return None

        puntajes = self._puntuar(documentos, candidatos)
        mejor, puntaje_primer = puntajes[0]
        if puntaje_primer < self._puntaje_minimo:
            return None

        # Empate técnico: dos trámites suman prácticamente lo mismo.
        if len(puntajes) > 1 and puntajes[1][1] > 0:
            if puntaje_primer < self._margen_minimo * puntajes[1][1]:
                return None

        mejor.puntaje_relevancia = round(puntaje_primer, 3)
        return mejor

    @staticmethod
    def _puntuar(
        documentos: list[Documento], candidatos: list[TramiteProbable]
    ) -> list[tuple[TramiteProbable, float]]:
        """Suma la similitud de los documentos de cada trámite candidato."""
        indice = {tramite.id: tramite for tramite in candidatos}
        acumulado: dict[object, float] = {tramite.id: 0.0 for tramite in candidatos}

        for documento in documentos:
            tramite = indice.get(documento.tramite_id)
            if tramite is not None:
                acumulado[tramite.id] += documento.puntuacion_similitud

        return sorted(
            ((tramite, acumulado[tramite.id]) for tramite in candidatos),
            key=lambda par: (-par[1], par[0].nombre),
        )