"""Servicio de aplicación: ServicioOrientacion."""

from uuid import UUID, uuid4

from application.services.EvaluadorGroundedness import (
    UMBRAL_CONFIANZA_MEDIA,
    EvaluadorGroundedness,
)
from application.services.ServicioDominio import EvaluacionDominio, ServicioDominio
from application.services.ServicioRAG import ServicioRAG
from application.use_cases.IdentificarTramiteProbable import IdentificarTramiteProbable
from domain.entities.Documento import Documento
from domain.entities.Respuesta import Respuesta
from domain.value_objects.ClasificacionIntencion import ClasificacionIntencion
from domain.value_objects.IntencionConsulta import IntencionConsulta
from domain.value_objects.NivelConfianza import NivelConfianza

# Mensaje de aclaración cuando la pregunta no permite identificar la intención.
ACLARACION_AMBIGUA = (
    'Para orientarte mejor necesito que precises tu consulta. Puedes indicarme, '
    'por ejemplo: qué requisitos necesitas, cuánto cuesta, en qué lugar se '
    'tramita o cómo se sigue el estado de tu expediente.'
)

# Respuesta a un saludo (HU-05): bienvenida sin consultar el RAG.
RESPUESTA_SALUDO = (
    '¡Hola! Soy el asistente virtual de la Municipalidad Provincial de Huancayo. '
    'Puedo orientarte sobre requisitos, costos, plazos y pasos de trámites como '
    'licencias de funcionamiento, certificados de habitabilidad, partidas de '
    'nacimiento, matrimonio o defunción, carnet de sanidad, ITSE y más. '
    '¿Sobre qué trámite necesitas orientación?'
)

# Respuesta cuando la consulta no tiene sentido (HU-05): no se entendió.
RESPUESTA_SIN_SENTIDO = (
    'No entendí tu consulta. Escríbela con palabras claras y completas, por '
    'ejemplo: "¿Qué necesito para el carnet de sanidad?" o "¿Cuánto cuesta la '
    'licencia de funcionamiento?".'
)

# Derivación al área responsable del trámite cuando la confianza es baja (HU-07).
DERIVACION_AL_AREA = (
    '\n\nDerivación: esta consulta corresponde al área de {area}. Dirígete a '
    'esa oficina para que un funcionario competente resuelva tu trámite.'
)

# Derivación a un funcionario cuando el asistente no resuelve la consulta
# (sin documentos recuperados o con confianza baja y sin área asignada) (HU-09).
DERIVACION_AL_FUNCIONARIO = (
    '\n\nDerivación a funcionario: el asistente no resuelve tu consulta con la '
    'información disponible en la base documental. Un funcionario de la oficina '
    'de trámites (Mesa de Partes o portal oficial https://www.gob.pe/munihuancayo) '
    'puede atender tu caso de forma personalizada.'
)

# Bloqueo de afirmaciones sin respaldo documental (HU-10 Escenario 2,
# HU-08 Escenario 2, G-04): en lugar de confiar en el texto del SLM se
# reemplaza por una abstención explícita que pide verificar con la
# municipalidad (el SLM no debe inventar datos).
BLOQUEO_AFIRMACIONES = (
    'No encontré respaldo en la base documental para afirmarlo, así que no lo '
    'presentaré como un dato oficial. Verifícalo directamente con la '
    'municipalidad antes de continuar.'
)


# Piso de similitud para las consultas sin intención de trámite (horarios,
# teléfonos, catálogo…): el umbral general de 0.30 recupera documentos con
# similitud floja que ensucian la respuesta, así que una consulta general solo
# se responde si existe un documento claramente afín (≥ 0.45); si no, se pide
# aclaración.
UMBRAL_CONSULTA_GENERAL = 0.45


class ServicioOrientacion:
    """Compone la orientación final entregada al ciudadano."""

    def __init__(
        self,
        servicio_rag: ServicioRAG,
        evaluador_groundedness: EvaluadorGroundedness,
        identificar_tramite: IdentificarTramiteProbable | None = None,
        servicio_dominio: ServicioDominio | None = None,
    ) -> None:
        self._servicio_rag = servicio_rag
        self._evaluador_groundedness = evaluador_groundedness
        self._identificar_tramite = identificar_tramite
        self._servicio_dominio = servicio_dominio

    async def orientar(
        self,
        consulta_id: UUID,
        pregunta: str,
        clasificacion: ClasificacionIntencion | None = None,
    ) -> Respuesta:
        # HU-11: una consulta de otra entidad (SUNAT, RENIEC, AFP…) se deriva
        # antes de cualquier otra evaluación, sin llamar al RAG ni al SLM.
        if self._servicio_dominio is not None:
            evaluacion = self._servicio_dominio.evaluar(pregunta)
            if evaluacion.fuera_de_dominio:
                return self._respuesta_fuera_de_dominio(
                    consulta_id, clasificacion, evaluacion
                )

        # Saludo: se responde con una bienvenida, sin consultar el RAG (HU-05).
        if clasificacion is not None and clasificacion.intencion == IntencionConsulta.SALUDO:
            return self._respuesta_saludo(consulta_id, clasificacion)

        # Consulta sin sentido: no se entendió, se pide reformular (HU-05).
        if clasificacion is not None and clasificacion.sin_sentido:
            return self._respuesta_sin_sentido(consulta_id, clasificacion)

        # Si la pregunta es ambigua se pide aclaración en vez de inventar, pero
        # primero se consulta la base documental: si hay información que responde
        # la consulta (p. ej. horarios, teléfonos o catálogo de trámites) se
        # responde con el RAG y sus fuentes; si no hay nada, se pide precisar.
        documentos: list[Documento] = await self._servicio_rag.recuperar(pregunta)
        consulta_general = (
            clasificacion is not None and clasificacion.requiere_aclaracion
        )
        if consulta_general:
            documentos = [
                documento
                for documento in documentos
                if documento.puntuacion_similitud >= UMBRAL_CONSULTA_GENERAL
            ]
        if consulta_general and not documentos:
            return self._respuesta_de_aclaracion(consulta_id, clasificacion)

        texto, fuentes = await self._servicio_rag.responder(
            pregunta, documentos, estructura=not consulta_general
        )
        puntuacion = self._evaluador_groundedness.calcular_puntuacion(texto, documentos)
        confianza = self._evaluador_groundedness.evaluar(texto, documentos)

        # HU-10 (Escenario 2) / HU-08 (Escenario 2) / G-04: si la respuesta del
        # SLM no alcanza el umbral de groundedness se bloquea la afirmación y
        # se pide verificar el dato con la municipalidad (no inventar).
        bloqueada = puntuacion < UMBRAL_CONFIANZA_MEDIA
        if bloqueada:
            # En una consulta general sin respaldo se prefiere pedir aclaración
            # antes que entregar un bloqueo críptico.
            if consulta_general:
                return self._respuesta_de_aclaracion(consulta_id, clasificacion)
            texto = BLOQUEO_AFIRMACIONES

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
            afirmaciones_bloqueadas=bloqueada,
        )

        # Derivación: al área responsable si hay trámite identificado; si no,
        # a un funcionario cuando el asistente no pudo responder (HU-07, HU-09).
        respuesta.texto = self._derivar(respuesta, sin_respuesta=not fuentes)

        # Los datos estructurados del catálogo se anexan al texto del modelo.
        return self._con_datos_estructurados(respuesta)

    @staticmethod
    def _derivar(respuesta: Respuesta, sin_respuesta: bool) -> str:
        """Añade la derivación correspondiente al texto de la respuesta.

        - Confianza baja + trámite con área asignada → derivación al **área**.
        - Sin respuesta (sin fuentes) o confianza baja sin área → derivación al
          **funcionario** de la oficina de trámites.
        """
        texto = respuesta.texto
        tramite = respuesta.tramite_probable
        baja = respuesta.confianza == NivelConfianza.BAJA

        if baja and tramite is not None and tramite.area_responsable:
            return texto + DERIVACION_AL_AREA.format(area=tramite.area_responsable)

        if sin_respuesta or baja:
            return texto + DERIVACION_AL_FUNCIONARIO

        return texto

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
    def _respuesta_saludo(
        consulta_id: UUID, clasificacion: ClasificacionIntencion
    ) -> Respuesta:
        return Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=RESPUESTA_SALUDO,
            confianza=NivelConfianza.ALTA,
            fuentes=[],
            groundedness=0.0,
            confianza_intencion=clasificacion.confianza,
            pide_aclaracion=False,
            tramite_probable=None,
        )

    @staticmethod
    def _respuesta_sin_sentido(
        consulta_id: UUID, clasificacion: ClasificacionIntencion
    ) -> Respuesta:
        return Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=RESPUESTA_SIN_SENTIDO,
            confianza=NivelConfianza.MEDIA,
            fuentes=[],
            groundedness=0.0,
            confianza_intencion=clasificacion.confianza,
            pide_aclaracion=True,
            tramite_probable=None,
        )

    @staticmethod
    def _respuesta_fuera_de_dominio(
        consulta_id: UUID,
        clasificacion: ClasificacionIntencion | None,
        evaluacion: EvaluacionDominio,
    ) -> Respuesta:
        """HU-11: informa que la consulta es de otra entidad y sugiere dónde ir."""
        destino = evaluacion.entidad_sugerida
        url = evaluacion.entidad_url
        texto = (
            'Esta consulta está fuera del alcance de este asistente municipal. '
            f'{evaluacion.motivo} Para este trámite, acude a: {destino}'
            + (f' — {url}' if url else '')
            + '. '
            'Si tu consulta sí es sobre un trámite municipal (requisitos, '
            'costos, plazos o estado), reformúlala y con gusto te oriento.'
        )
        return Respuesta(
            id=uuid4(),
            consulta_id=consulta_id,
            texto=texto,
            confianza=NivelConfianza.BAJA,
            fuentes=[],
            groundedness=0.0,
            confianza_intencion=clasificacion.confianza if clasificacion else 0.0,
            fuera_dominio=True,
            entidad_sugerida=destino,
        )

    @staticmethod
    def _con_datos_estructurados(respuesta: Respuesta) -> Respuesta:
        """Reemplaza el texto por la versión con los datos verificados del catálogo."""
        respuesta.texto = respuesta.con_datos_estructurados()
        return respuesta