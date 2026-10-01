"""Servicio de aplicación: ServicioOrientacion."""

from uuid import UUID, uuid4

from application.services.EvaluadorGroundedness import EvaluadorGroundedness
from application.services.ServicioRAG import ServicioRAG
from application.use_cases.IdentificarTramiteProbable import IdentificarTramiteProbable
from domain.entities.Documento import Documento
from domain.entities.Respuesta import Respuesta
from domain.value_objects.ClasificacionIntencion import ClasificacionIntencion
from domain.value_objects.NivelConfianza import NivelConfianza

# Mensaje de aclaración cuando la pregunta no permite identificar la intención.
ACLARACION_AMBIGUA = (
    'Para orientarte mejor necesito que precises tu consulta. Puedes indicarme, '
    'por ejemplo: qué requisitos necesitas, cuánto cuesta, en qué lugar se '
    'tramita o cómo se sigue el estado de tu expediente.'
)


class ServicioOrientacion:
    """Compone la orientación final entregada al ciudadano."""

    def __init__(
        self,
        servicio_rag: ServicioRAG,
        evaluador_groundedness: EvaluadorGroundedness,
        identificar_tramite: IdentificarTramiteProbable | None = None,
    ) -> None:
        self._servicio_rag = servicio_rag
        self._evaluador_groundedness = evaluador_groundedness
        self._identificar_tramite = identificar_tramite

    async def orientar(
        self,
        consulta_id: UUID,
        pregunta: str,
        clasificacion: ClasificacionIntencion | None = None,
    ) -> Respuesta:
        # Si la pregunta es ambigua se pide aclaración en vez de inventar.
        if clasificacion is not None and clasificacion.requiere_aclaracion:
            return self._respuesta_de_aclaracion(consulta_id, clasificacion)

        documentos: list[Documento] = await self._servicio_rag.recuperar(pregunta)
        texto, fuentes = await self._servicio_rag.responder(pregunta, documentos)
        puntuacion = self._evaluador_groundedness.calcular_puntuacion(texto, documentos)
        confianza = self._evaluador_groundedness.evaluar(texto, documentos)

        if confianza == NivelConfianza.BAJA and fuentes:
            texto = (
                f'{texto}\n\nNota: la información recuperada no sustenta '
                'completamente esta respuesta. Verifica los requisitos en las '
                'fuentes oficiales citadas.'
            )

        tramite_probable = None
        if self._identificar_tramite is not None and documentos:
            tramite_probable = await self._identificar_tramite.ejecutar(documentos)

        respuesta = Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=texto,
            confianza=confianza,
            fuentes=fuentes,
            groundedness=round(puntuacion, 3),
            confianza_intencion=clasificacion.confianza if clasificacion else 0.0,
            tramite_probable=tramite_probable,
        )

        # Los datos estructurados del catálogo se anexan al texto del modelo.
        return self._con_datos_estructurados(respuesta)

    @staticmethod
    def _respuesta_de_aclaracion(
        consulta_id: UUID, clasificacion: ClasificacionIntencion
    ) -> Respuesta:
        return Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=ACLARACION_AMBIGUA,
            confianza=NivelConfianza.MEDIA,
            fuentes=[],
            groundedness=0.0,
            confianza_intencion=clasificacion.confianza,
            pide_aclaracion=True,
            tramite_probable=None,
        )

    @staticmethod
    def _con_datos_estructurados(respuesta: Respuesta) -> Respuesta:
        """Reemplaza el texto por la versión con los datos verificados del catálogo."""
        respuesta.texto = respuesta.con_datos_estructurados()
        return respuesta