"""Servicio de aplicación: EvaluadorGroundedness."""

from domain.entities.Documento import Documento
from domain.value_objects.NivelConfianza import NivelConfianza

UMBRAL_CONFIANZA_ALTA = 0.75
UMBRAL_CONFIANZA_MEDIA = 0.40


class EvaluadorGroundedness:
    """Evalúa qué tan sustentada está una respuesta en el contexto recuperado.

    Se calcula la proporción de términos de la respuesta presentes en los
    documentos fuente (cobertura léxica), lo que permite descartar respuestas
    con posible alucinación.
    """

    def evaluar(self, respuesta: str, contexto: list[Documento]) -> NivelConfianza:
        puntuacion = self.calcular_puntuacion(respuesta, contexto)

        if puntuacion >= UMBRAL_CONFIANZA_ALTA:
            return NivelConfianza.ALTA
        if puntuacion >= UMBRAL_CONFIANZA_MEDIA:
            return NivelConfianza.MEDIA
        return NivelConfianza.BAJA

    def calcular_puntuacion(self, respuesta: str, contexto: list[Documento]) -> float:
        if not contexto:
            return 0.0

        terminos_respuesta = self._tokenizar(respuesta)
        if not terminos_respuesta:
            return 0.0

        vocabulario_contexto: set[str] = set()
        for documento in contexto:
            vocabulario_contexto.update(self._tokenizar(documento.contenido))
            vocabulario_contexto.update(self._tokenizar(documento.titulo))

        coincidencias = terminos_respuesta & vocabulario_contexto

        return len(coincidencias) / len(terminos_respuesta)

    def esta_grounded(self, respuesta: str, contexto: list[Documento]) -> bool:
        return self.calcular_puntuacion(respuesta, contexto) >= UMBRAL_CONFIANZA_MEDIA

    @staticmethod
    def _tokenizar(texto: str) -> set[str]:
        return {palabra for palabra in texto.lower().split() if len(palabra) > 3}