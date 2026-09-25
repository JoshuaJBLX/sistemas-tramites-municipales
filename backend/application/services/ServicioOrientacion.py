"""Servicio de aplicación: ServicioOrientacion."""

from uuid import UUID, uuid4

from application.services.EvaluadorGroundedness import EvaluadorGroundedness
from application.services.ServicioRAG import ServicioRAG
from domain.entities.Documento import Documento
from domain.entities.Respuesta import Respuesta
from domain.value_objects.NivelConfianza import NivelConfianza


class ServicioOrientacion:
    """Compone la orientación final entregada al ciudadano."""

    def __init__(
        self,
        servicio_rag: ServicioRAG,
        evaluador_groundedness: EvaluadorGroundedness,
    ) -> None:
        self._servicio_rag = servicio_rag
        self._evaluador_groundedness = evaluador_groundedness

    async def orientar(self, consulta_id: UUID, pregunta: str) -> Respuesta:
        documentos: list[Documento] = await self._servicio_rag.recuperar(pregunta)
        texto, fuentes = await self._servicio_rag.responder(pregunta, documentos)
        confianza = self._evaluador_groundedness.evaluar(texto, documentos)

        if confianza == NivelConfianza.BAJA and fuentes:
            texto = (
                f'{texto}\n\nNota: la información recuperada no sustenta '
                'completamente esta respuesta. Verifica los requisitos en las '
                'fuentes oficiales citadas.'
            )

        return Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=texto,
            confianza=confianza,
            fuentes=fuentes,
        )