"""Controlador REST de gestión de documentos oficiales."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

from domain.entities.Documento import Documento
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/documentos', tags=['documentos'])


class DocumentoRequest(BaseModel):
    tramite_id: UUID
    titulo: str = Field(..., min_length=3)
    contenido: str = Field(..., min_length=10)
    url_origen: str
    estado: EstadoDocumento = EstadoDocumento.VIGENTE


class DocumentoResponse(BaseModel):
    id: UUID
    tramite_id: UUID
    titulo: str
    url_origen: str
    estado: EstadoDocumento
    indexado: bool


def _a_response(documento: Documento) -> DocumentoResponse:
    return DocumentoResponse(
        id=documento.id,
        tramite_id=documento.tramite_id,
        titulo=documento.titulo,
        url_origen=documento.url_origen,
        estado=documento.estado,
        indexado=documento.embedding is not None,
    )


@router.post('', response_model=DocumentoResponse, status_code=201)
async def registrar_documento(
    payload: DocumentoRequest,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    """Registra un documento oficial y lo indexa en el buscador vectorial."""
    try:
        documento = Documento(
            id=uuid4(),
            tramite_id=payload.tramite_id,
            titulo=payload.titulo,
            contenido=payload.contenido,
            url_origen=payload.url_origen,
            estado=payload.estado,
            actualizado_en=datetime.now(timezone.utc),
        )
        guardado = await container.gestionar_documentos.registrar(documento)
        return _a_response(guardado)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post('/upload', status_code=201)
async def subir_archivo(
    tramite_id: UUID,
    container: Container = Depends(obtener_container),
    archivo: UploadFile = File(...),
) -> dict[str, str]:
    """Guarda el archivo original en el almacenamiento de documentos."""
    contenido = await archivo.read()
    ruta = container.almacenamiento.guardar(archivo.filename or 'documento.bin', contenido)
    return {'archivo': ruta.name, 'mensaje': 'Archivo almacenado correctamente.'}


@router.put('/{documento_id}/estado', response_model=DocumentoResponse)
async def actualizar_estado(
    documento_id: UUID,
    estado: EstadoDocumento,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    """Actualiza el estado de vigencia de un documento."""
    documento = await container.gestionar_documentos.actualizar_estado(
        documento_id, estado
    )
    if documento is None:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    return _a_response(documento)


@router.get('/{documento_id}', response_model=DocumentoResponse)
async def obtener_documento(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    documento = await container.documento_repository.obtener_por_id(documento_id)
    if documento is None:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    return _a_response(documento)


@router.delete('/{documento_id}', status_code=204)
async def eliminar_documento(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
) -> None:
    await container.gestionar_documentos.eliminar(documento_id)