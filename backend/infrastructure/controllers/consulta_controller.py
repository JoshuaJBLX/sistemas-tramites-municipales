"""Controlador REST del flujo de consultas al asistente."""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from domain.value_objects.IntencionConsulta import IntencionConsulta
from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/consultas', tags=['consultas'])


class ConsultaRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, description='Consulta en lenguaje natural')
    usuario_id: UUID | None = None


class FuenteResponse(BaseModel):
    url: str
    fragmento: str


class RespuestaResponse(BaseModel):
    consulta_id: UUID
    intencion: IntencionConsulta
    texto: str
    confianza: str
    fuentes: list[FuenteResponse]


class ConsultaResponse(BaseModel):
    id: UUID
    usuario_id: UUID | None = None
    pregunta: str
    intencion: IntencionConsulta | None = None
    creada_en: datetime


@router.post('', response_model=RespuestaResponse)
async def crear_consulta(
    payload: ConsultaRequest,
    container: Container = Depends(obtener_container),
) -> RespuestaResponse:
    """Registra la consulta, clasifica su intención y genera la orientación."""
    try:
        # 1. Clasificación de intención.
        intencion = await container.clasificar_intencion.ejecutar(payload.pregunta)

        # 2. Registro de la consulta.
        consulta = await container.registrar_consulta.ejecutar(
            pregunta=payload.pregunta,
            usuario_id=payload.usuario_id,
            intencion=intencion,
        )

        # 3. Caché de respuestas frecuentes.
        en_cache = await container.servicio_cache.obtener_respuesta(payload.pregunta)
        if en_cache is not None:
            return RespuestaResponse(
                consulta_id=consulta.id, intencion=intencion, **en_cache
            )

        # 4. Generación de la orientación con RAG.
        respuesta = await container.generar_orientacion.ejecutar(
            consulta_id=consulta.id, pregunta=payload.pregunta
        )

        # 5. Auditoría de la interacción.
        await container.auditar_consulta.ejecutar(consulta, respuesta)

        cuerpo = {
            'texto': respuesta.texto,
            'confianza': respuesta.confianza.value,
            'fuentes': [
                FuenteResponse(url=fuente.url, fragmento=fuente.fragmento)
                for fuente in respuesta.fuentes
            ],
        }
        await container.servicio_cache.guardar_respuesta(payload.pregunta, cuerpo)

        return RespuestaResponse(
            consulta_id=consulta.id, intencion=intencion, **cuerpo
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


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