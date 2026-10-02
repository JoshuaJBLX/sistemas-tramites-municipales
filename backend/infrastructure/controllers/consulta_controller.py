"""Controlador REST del flujo de consultas al asistente."""

from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ValidationError

from domain.value_objects.IntencionConsulta import IntencionConsulta
from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/consultas', tags=['consultas'])


class ConsultaRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, description='Consulta en lenguaje natural')
    usuario_id: UUID | None = None


class FuenteResponse(BaseModel):
    """Fuente citada. Incluye el título para que el front pueda mostrarla."""

    url: str
    fragmento: str
    titulo: str = ''


class TramiteProbableResponse(BaseModel):
    """Trámite del catálogo que mejor explica la consulta (HU-05, HU-07)."""

    id: UUID
    nombre: str
    requisitos: list[str] = Field(default_factory=list)
    costo: float = 0.0
    duracion_estimada_dias: int = 0
    fuente_url: str | None = None


class RespuestaResponse(BaseModel):
    consulta_id: UUID
    intencion: IntencionConsulta
    texto: str
    confianza: str
    groundedness: float = 0.0
    confianza_intencion: float = 0.0
    pide_aclaracion: bool = False
    tramite_probable: TramiteProbableResponse | None = None
    fuentes: list[FuenteResponse] = Field(default_factory=list)


class ConsultaResponse(BaseModel):
    id: UUID
    usuario_id: UUID | None = None
    pregunta: str
    intencion: IntencionConsulta | None = None
    creada_en: datetime


def _cuerpo_respuesta(respuesta) -> dict:
    """Serializa la respuesta en el formato que consume el front-end."""
    cuerpo = {
        'texto': respuesta.texto,
        'confianza': respuesta.confianza.value,
        'groundedness': respuesta.groundedness,
        'confianza_intencion': respuesta.confianza_intencion,
        'pide_aclaracion': respuesta.pide_aclaracion,
        'fuentes': [
            {
                'url': fuente.url,
                'fragmento': fuente.fragmento,
                'titulo': fuente.titulo,
            }
            for fuente in respuesta.fuentes
        ],
    }

    tramite = respuesta.tramite_probable
    cuerpo['tramite_probable'] = (
        {
            'id': str(tramite.id),
            'nombre': tramite.nombre,
            'requisitos': tramite.requisitos,
            'costo': tramite.costo,
            'duracion_estimada_dias': tramite.duracion_estimada_dias,
            'fuente_url': tramite.fuente_url,
        }
        if tramite is not None
        else None
    )
    return cuerpo


@router.post('', response_model=RespuestaResponse)
async def crear_consulta(
    payload: ConsultaRequest,
    container: Container = Depends(obtener_container),
) -> RespuestaResponse:
    """Registra la consulta, clasifica su intención y genera la orientación."""
    try:
        # 1. Clasificación de intención con confianza y detección de ambigüedad.
        clasificacion = await container.clasificar_intencion.ejecutar_detallado(
            payload.pregunta
        )
        intencion = clasificacion.intencion

        # 2. Registro de la consulta.
        consulta = await container.registrar_consulta.ejecutar(
            pregunta=payload.pregunta,
            usuario_id=payload.usuario_id,
            intencion=intencion,
        )

        # 3. Caché de respuestas frecuentes.
        en_cache = await container.servicio_cache.obtener_respuesta(payload.pregunta)
        if en_cache is not None:
            cuerpo_cache = _cuerpo_valido(en_cache)
            if cuerpo_cache is None:
                # Entrada corrupta o de formato antiguo: se descarta y se recalcula
                # en vez de devolver un error al ciudadano.
                await container.servicio_cache.invalidar(payload.pregunta)
            else:
                # 4. Auditoría también en cache-hit para mantener trazabilidad completa.
                await container.auditar_consulta.ejecutar(
                    consulta,
                    _respuesta_desde_cuerpo(cuerpo_cache, consulta.id),
                )
                return RespuestaResponse(
                    consulta_id=consulta.id, intencion=intencion, **cuerpo_cache
                )

        # 5. Generación de la orientación con RAG.
        try:
            respuesta = await container.generar_orientacion.ejecutar(
                consulta_id=consulta.id,
                pregunta=payload.pregunta,
                clasificacion=clasificacion,
            )
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as error:
            # El SLM local no está disponible: se informa con claridad en lugar de
            # devolver un 500 con traza técnica.
            raise HTTPException(
                status_code=503,
                detail=(
                    'El asistente no está disponible en este momento: no se pudo '
                    'conectar con el modelo de lenguaje local. Intenta en unos '
                    'minutos.'
                ),
            ) from error

        # 6. Auditoría de la interacción.
        await container.auditar_consulta.ejecutar(consulta, respuesta)

        cuerpo = _cuerpo_respuesta(respuesta)
        await container.servicio_cache.guardar_respuesta(payload.pregunta, cuerpo)

        return RespuestaResponse(
            consulta_id=consulta.id, intencion=intencion, **cuerpo
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


def _cuerpo_valido(cuerpo: object) -> dict | None:
    """Devuelve el cuerpo de caché si tiene el formato esperado; si no, None.

    Una entrada corrupta (por ejemplo escrita por una versión anterior del
    esquema) se descarta en lugar de provocar un error 500.
    """
    if not isinstance(cuerpo, dict):
        return None
    try:
        RespuestaResponse.model_validate(cuerpo)
    except ValidationError:
        return None
    return cuerpo


def _respuesta_desde_cuerpo(cuerpo: dict, consulta_id: UUID):
    """Reconstruye una respuesta mínima para poder auditar un acierto de caché."""
    from domain.entities.Fuente import Fuente
    from domain.entities.Respuesta import Respuesta
    from domain.value_objects.FuenteOficial import FuenteOficial
    from domain.value_objects.NivelConfianza import NivelConfianza
    from domain.value_objects.TramiteProbable import TramiteProbable

    tramite = cuerpo.get('tramite_probable')
    tramite_probable = (
        TramiteProbable(
            id=UUID(str(tramite['id'])),
            nombre=tramite['nombre'],
            requisitos=tramite.get('requisitos', []),
            costo=tramite.get('costo', 0.0),
            duracion_estimada_dias=tramite.get('duracion_estimada_dias', 0),
            fuente_url=tramite.get('fuente_url'),
        )
        if tramite
        else None
    )

    return Respuesta(
        id=uuid4(),
        consulta_id=consulta_id,
        texto=cuerpo['texto'],
        confianza=NivelConfianza(cuerpo['confianza']),
        fuentes=[
            Fuente(
                id=uuid4(),
                documento_id=uuid4(),
                tipo=FuenteOficial.PORTAL_MUNICIPAL,
                url=fuente['url'],
                fragmento=fuente['fragmento'],
                titulo=fuente.get('titulo', ''),
            )
            for fuente in cuerpo.get('fuentes', [])
        ],
        groundedness=cuerpo.get('groundedness', 0.0),
        confianza_intencion=cuerpo.get('confianza_intencion', 0.0),
        pide_aclaracion=cuerpo.get('pide_aclaracion', False),
        tramite_probable=tramite_probable,
    )


@router.get('/{consulta_id}', response_model=ConsultaResponse)
async def obtener_consulta(
    consulta_id: UUID,
    container: Container = Depends(obtener_container),
) -> ConsultaResponse:
    """Recupera una consulta registrada por su identificador."""
    consulta = await container.auditar_consulta.consultar_trazabilidad(consulta_id)
    if consulta is None:
        raise HTTPException(status_code=404, detail='Consulta no encontrada')

    return ConsultaResponse(
        id=consulta.id,
        usuario_id=consulta.usuario_id,
        pregunta=consulta.pregunta,
        intencion=consulta.intencion,
        creada_en=consulta.creada_en,
    )