"""Controlador REST del flujo de consultas al asistente."""

import time
from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, ValidationError

from domain.value_objects.IntencionConsulta import IntencionConsulta
from infrastructure.container import Container, obtener_container
from infrastructure.controllers.dependencias import requiere_administrador

router = APIRouter(prefix='/api/consultas', tags=['consultas'])


class ConsultaRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, description='Consulta en lenguaje natural')
    usuario_id: UUID | None = None


class FuenteResponse(BaseModel):
    """Fuente citada. Incluye título y metadatos disponibles (HU-10 / P3-08)."""

    url: str
    fragmento: str
    titulo: str = ''
    numero: str = ''
    fecha: str = ''
    version: str = ''


class TramiteProbableResponse(BaseModel):
    """Trámite del catálogo que mejor explica la consulta (HU-05, HU-07)."""

    id: UUID
    nombre: str
    requisitos: list[str] = Field(default_factory=list)
    costo: float = 0.0
    duracion_estimada_dias: int = 0
    fuente_url: str | None = None
    area: str | None = Field(
        default=None, description='Área u oficina responsable del trámite (HU-07)'
    )


class RespuestaResponse(BaseModel):
    consulta_id: UUID
    intencion: IntencionConsulta
    texto: str
    confianza: str
    groundedness: float = 0.0
    confianza_intencion: float = 0.0
    pide_aclaracion: bool = False
    afirmaciones_bloqueadas: bool = Field(
        default=False, description='HU-10/G-04: la afirmación fue bloqueada por bajo groundedness'
    )
    fuera_dominio: bool = Field(
        default=False, description='HU-11: la consulta corresponde a otra entidad'
    )
    entidad_sugerida: str = Field(
        default='', description='HU-11: entidad externa sugerida (SUNAT, RENIEC…)'
    )
    tramite_probable: TramiteProbableResponse | None = None
    fuentes: list[FuenteResponse] = Field(default_factory=list)


class ConsultaResponse(BaseModel):
    id: UUID
    usuario_id: UUID | None = None
    pregunta: str
    intencion: IntencionConsulta | None = None
    creada_en: datetime


class TrazabilidadResponse(ConsultaResponse):
    """HU-10 (D-9): la consulta con su respuesta auditada completa."""

    respuesta: str | None = None
    confianza: str | None = None
    groundedness: float = 0.0
    afirmaciones_bloqueadas: bool = False
    fuera_dominio: bool = False
    entidad_sugerida: str = ''
    duracion_ms: int | None = None
    tramite_probable: str | None = None
    fuentes: list[FuenteResponse] = Field(default_factory=list)
    registrado_en: datetime | None = None


class EvaluacionRequest(BaseModel):
    """HU-15: calificación del ciudadano sobre la respuesta recibida."""

    valoracion: str = Field(
        ..., pattern='^(util|parcialmente_util|no_util)$'
    )
    comentario: str | None = Field(default=None, max_length=1000)


class EvaluacionResponse(BaseModel):
    id: UUID
    consulta_id: UUID
    valoracion: str
    comentario: str | None = None
    creada_en: datetime
    actualizada_en: datetime | None = None


def _datos_fuente(fuente) -> dict:
    return {
        'url': fuente.url,
        'fragmento': fuente.fragmento,
        'titulo': fuente.titulo,
        'numero': fuente.numero,
        'fecha': fuente.fecha,
        'version': fuente.version,
    }


def _cuerpo_respuesta(respuesta) -> dict:
    """Serializa la respuesta en el formato que consume el front-end."""
    cuerpo = {
        'texto': respuesta.texto,
        'confianza': respuesta.confianza.value,
        'groundedness': respuesta.groundedness,
        'confianza_intencion': respuesta.confianza_intencion,
        'pide_aclaracion': respuesta.pide_aclaracion,
        'afirmaciones_bloqueadas': respuesta.afirmaciones_bloqueadas,
        'fuera_dominio': respuesta.fuera_dominio,
        'entidad_sugerida': respuesta.entidad_sugerida,
        'fuentes': [_datos_fuente(fuente) for fuente in respuesta.fuentes],
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
            'area': tramite.area_responsable,
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
    inicio = time.monotonic()
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
                    duracion_ms=int((time.monotonic() - inicio) * 1000),
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

        # 6. Auditoría de la interacción (con el tiempo real de generación, HU-16).
        await container.auditar_consulta.ejecutar(
            consulta,
            respuesta,
            duracion_ms=int((time.monotonic() - inicio) * 1000),
        )

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
            area_responsable=tramite.get('area'),
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
        afirmaciones_bloqueadas=cuerpo.get('afirmaciones_bloqueadas', False),
        fuera_dominio=cuerpo.get('fuera_dominio', False),
        entidad_sugerida=cuerpo.get('entidad_sugerida', ''),
    )


def _cuerpo_trazabilidad(trazabilidad) -> TrazabilidadResponse:
    """HU-10: serializa una trazabilidad completa para el front-end."""
    return TrazabilidadResponse(
        id=trazabilidad.consulta.id,
        usuario_id=trazabilidad.consulta.usuario_id,
        pregunta=trazabilidad.consulta.pregunta,
        intencion=trazabilidad.consulta.intencion,
        creada_en=trazabilidad.consulta.creada_en,
        respuesta=trazabilidad.respuesta,
        confianza=trazabilidad.confianza,
        groundedness=trazabilidad.groundedness,
        afirmaciones_bloqueadas=trazabilidad.afirmaciones_bloqueadas,
        fuera_dominio=trazabilidad.fuera_dominio,
        entidad_sugerida=trazabilidad.entidad_sugerida,
        duracion_ms=trazabilidad.duracion_ms,
        tramite_probable=trazabilidad.tramite_probable,
        fuentes=[_datos_fuente(fuente) for fuente in trazabilidad.fuentes],
        registrado_en=trazabilidad.registrado_en,
    )


@router.get('', response_model=list[TrazabilidadResponse])
async def listar_consultas(
    limite: int = 20,
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> list[TrazabilidadResponse]:
    """HU-10/HU-14: últimas consultas con su respuesta auditada (solo administradores)."""
    cantidad = max(1, min(limite, 100))
    registros = await container.auditar_consulta.listar_trazabilidad(cantidad)
    return [_cuerpo_trazabilidad(registro) for registro in registros]


@router.get('/{consulta_id}', response_model=TrazabilidadResponse)
async def obtener_consulta(
    consulta_id: UUID,
    container: Container = Depends(obtener_container),
) -> TrazabilidadResponse:
    """HU-10 (D-9): consulta con su respuesta, fuentes y confianza auditadas."""
    trazabilidad = await container.auditar_consulta.consultar_trazabilidad(consulta_id)
    if trazabilidad is None:
        raise HTTPException(status_code=404, detail='Consulta no encontrada')

    return _cuerpo_trazabilidad(trazabilidad)


# ---------- HU-15: retroalimentación ciudadana ----------

QUERY_CONSULTA_EXISTE = """
    SELECT 1 FROM consultas WHERE id = $1
"""

QUERY_UPSERT_EVALUACION = """
    INSERT INTO evaluaciones_calidad (id, consulta_id, valoracion, comentario)
    VALUES ($1, $2, $3, $4)
    ON CONFLICT (consulta_id) DO UPDATE
    SET valoracion = EXCLUDED.valoracion,
        comentario = COALESCE(EXCLUDED.comentario, evaluaciones_calidad.comentario),
        actualizada_en = NOW()
    RETURNING id, consulta_id, valoracion, comentario, creada_en, actualizada_en
"""

QUERY_SELECT_EVALUACION = """
    SELECT id, consulta_id, valoracion, comentario, creada_en, actualizada_en
    FROM evaluaciones_calidad
    WHERE consulta_id = $1
"""


@router.post(
    '/{consulta_id}/evaluacion',
    response_model=EvaluacionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def calificar_respuesta(
    consulta_id: UUID,
    payload: EvaluacionRequest,
    container: Container = Depends(obtener_container),
) -> EvaluacionResponse:
    """HU-15: el ciudadano califica la respuesta (útil / parcialmente útil / no útil).

    Es pública (no requiere cuenta): solo identifica la consulta. Si la consulta
    ya fue calificada, la calificación se actualiza (una vigente por consulta).
    """
    async with container.connection.pool.acquire() as conexion:
        existe = await conexion.fetchval(QUERY_CONSULTA_EXISTE, consulta_id)
        if existe is None:
            raise HTTPException(status_code=404, detail='Consulta no encontrada')
        fila = await conexion.fetchrow(
            QUERY_UPSERT_EVALUACION,
            uuid4(),
            consulta_id,
            payload.valoracion,
            payload.comentario.strip() if payload.comentario else None,
        )
    return EvaluacionResponse(**dict(fila))


@router.get('/{consulta_id}/evaluacion', response_model=EvaluacionResponse)
async def obtener_evaluacion(
    consulta_id: UUID,
    container: Container = Depends(obtener_container),
) -> EvaluacionResponse:
    """HU-15: calificación vigente de una consulta (404 si aún no fue calificada)."""
    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(QUERY_SELECT_EVALUACION, consulta_id)
    if fila is None:
        raise HTTPException(status_code=404, detail='Consulta sin calificación')
    return EvaluacionResponse(**dict(fila))