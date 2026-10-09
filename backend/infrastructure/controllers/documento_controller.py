"""Controlador de documentos ampliado: carga conectada (G-12), filtros (HU-03) y reprocesado (HU-04)."""

from datetime import date, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from domain.entities.Documento import Documento
from domain.errors import DocumentoIlegibleError, FormatoNoSoportadoError
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/documentos', tags=['documentos'])


class DocumentoRequest(BaseModel):
    tramite_id: UUID
    titulo: str = Field(..., min_length=3)
    contenido: str = Field(..., min_length=10)
    url_origen: str
    estado: EstadoDocumento = EstadoDocumento.VIGENTE
    version: str = Field(default='1.0')
    fecha_publicacion: date | None = None


class DocumentoResponse(BaseModel):
    id: UUID
    tramite_id: UUID
    titulo: str
    url_origen: str
    estado: EstadoDocumento
    indexado: bool
    version: str | None = None
    fecha_publicacion: date | None = None
    fragmentado: bool = False
    archivo_nombre: str | None = None


def _a_response(documento: Documento) -> DocumentoResponse:
    return DocumentoResponse(
        id=documento.id,
        tramite_id=documento.tramite_id,
        titulo=documento.titulo,
        url_origen=documento.url_origen,
        estado=documento.estado,
        indexado=documento.indexado or documento.embedding is not None,
        version=documento.version,
        fecha_publicacion=documento.fecha_publicacion,
        fragmentado=documento.fragmentado,
        archivo_nombre=documento.archivo_nombre,
    )


@router.post('', response_model=DocumentoResponse, status_code=201)
async def registrar_documento(
    payload: DocumentoRequest,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    try:
        documento = Documento(
            id=uuid4(),
            tramite_id=payload.tramite_id,
            titulo=payload.titulo,
            contenido=payload.contenido,
            url_origen=payload.url_origen,
            estado=payload.estado,
            version=payload.version,
            fecha_publicacion=payload.fecha_publicacion,
            actualizado_en=datetime.utcnow(),
        )
        guardado = await container.gestionar_documentos.registrar(documento)
        # Procesar fragmentos de ser posible
        try:
            await container.procesar_documento.ejecutar(guardado.id)
        except Exception:
            pass
        final = await container.gestionar_documentos.obtener(guardado.id)
        return _a_response(final or guardado)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post('/upload', response_model=DocumentoResponse, status_code=201)
async def subir_archivo(
    tramite_id: UUID = Form(...),
    titulo: str = Form(...),
    url_origen: str = Form(...),
    version: str = Form(default='1.0'),
    fecha_publicacion: date | None = Form(default=None),
    estado: EstadoDocumento = Form(default=EstadoDocumento.VIGENTE),
    archivo: UploadFile = File(...),
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    contenido = await archivo.read()
    try:
        guardado = await container.cargar_documento.ejecutar(
            tramite_id=tramite_id,
            titulo=titulo,
            url_origen=url_origen,
            version=version,
            fecha_publicacion=fecha_publicacion,
            estado=estado,
            nombre_archivo=archivo.filename or 'documento.bin',
            contenido=contenido,
        )
        final = await container.gestionar_documentos.obtener(guardado.id)
        return _a_response(final or guardado)
    except (FormatoNoSoportadoError, DocumentoIlegibleError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get('', response_model=list[DocumentoResponse])
async def listar_documentos(
    tramite_id: UUID | None = None,
    estado: EstadoDocumento | None = None,
    incluir_eliminados: bool = False,
    limite: int = 50,
    desde: int = 0,
    container: Container = Depends(obtener_container),
) -> list[DocumentoResponse]:
    documentos = await container.gestionar_documentos.listar(
        tramite_id=tramite_id,
        estado=estado,
        incluir_eliminados=incluir_eliminados,
        limite=limite,
        desde=desde,
    )
    return [_a_response(d) for d in documentos]


@router.put('/{documento_id}/estado', response_model=DocumentoResponse)
async def actualizar_estado(
    documento_id: UUID,
    estado: EstadoDocumento,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
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
    documento = await container.gestionar_documentos.obtener(documento_id)
    if documento is None:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    return _a_response(documento)


@router.post('/{documento_id}/procesar', response_model=DocumentoResponse)
async def reprocesar_documento(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
) -> DocumentoResponse:
    documento = await container.procesar_documento.ejecutar(documento_id)
    if documento is None:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    final = await container.gestionar_documentos.obtener(documento.id)
    return _a_response(final or documento)


@router.delete('/{documento_id}', status_code=204)
async def eliminar_documento(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
) -> None:
    await container.gestionar_documentos.eliminar(documento_id)


@router.delete('/{documento_id}/fisico', status_code=204)
async def eliminar_fisico(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
) -> None:
    await container.gestionar_documentos.eliminar_fisico(documento_id)