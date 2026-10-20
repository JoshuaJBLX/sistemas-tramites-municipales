"""Caso de uso: IdentificarTramiteProbable."""

import re
from unicodedata import normalize

from domain.entities.Documento import Documento
from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.TramiteProbable import TramiteProbable

# El trámite elegido debe superar al segundo colocado por este factor.
MARGEN_MINIMO = 1.15
# Y sus documentos deben sumar al menos este puntaje de similitud.
PUNTAJE_MINIMO = 0.45
# Si el nombre del segundo contiene (casi) todos los tokens del primero, se
# trata como variante del mismo trámite (p. ej. "Licencia de Funcionamiento"
# vs "Licencia de Funcionamiento Temporal") y no cuenta como rival para el
# margen de desempate.
SOLO_VARIANTE = 0.5
# Solo los documentos con al menos esta similitud votan por su trámite: evita
# que documentos genéricos (catálogo, TUPA) acumulen puntos flojos y ganen
# frente al trámite específico que el ciudadano pregunta.
VOTO_MINIMO_DOC = 0.45

_STOPWORDS = frozenset(
    'al algo algun alguna ante bajo cada con contra de del desde donde dos el ella '
    'ellas el les en entre era eran es esa ese eso esta estaba estan estar este esta '
    'esto fue han hasta hay la las le les lo los mas me mi muy no nos o otra otro para '
    'pero por porque que quien quienes se ser si sin sobre su sus tambien tan tanto te '
    'tiene traer un una uno y ya'.split()
)


def _tokens(texto: str) -> set[str]:
    plano = (
        normalize('NFKD', texto or '')
        .encode('ascii', 'ignore')
        .decode('ascii')
        .lower()
    )
    return {
        token
        for token in re.findall(r'[a-z0-9]+', plano)
        if len(token) > 2 and token not in _STOPWORDS
    }


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
        equivocado (HU-05, HU-07). Las variantes del mismo trámite (p. ej.
        "Licencia de Funcionamiento" y su versión temporal) no cuentan como
        rivales para el margen.
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

        # Empate técnico: dos trámites distintos suman prácticamente lo mismo.
        tokens_mejor = _tokens(mejor.nombre)
        for rival, puntaje_rival in puntajes[1:]:
            if puntaje_rival <= 0:
                continue
            tokens_rival = _tokens(rival.nombre)
            menor = min(len(tokens_mejor), len(tokens_rival))
            if menor and len(tokens_mejor & tokens_rival) / menor >= SOLO_VARIANTE:
                continue
            if puntaje_primer < self._margen_minimo * puntaje_rival:
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
            if tramite is not None and documento.puntuacion_similitud >= VOTO_MINIMO_DOC:
                acumulado[tramite.id] += documento.puntuacion_similitud

        return sorted(
            ((tramite, acumulado[tramite.id]) for tramite in candidatos),
            key=lambda par: (-par[1], par[0].nombre),
        )