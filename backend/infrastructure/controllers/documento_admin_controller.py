"""API admin de documentos: listado/filtros, registro, carga, reprocesado y baja (HU-01..HU-04, G-12)."""

from datetime import date
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from domain.entities.Documento import Documento
from domain.errors import DocumentoIlegibleError, FormatoNoSoportadoError
from domain.value_objects.EstadoDocumento import EstadoDocumento
from infrastructure.container import Container, obtener_container
from infrastructure.schemas.documento_admin import (
    DocumentoAdminRequest,
    DocumentoAdminResponse,
)

router = APIRouter(prefix='/api/admin/documentos', tags=['admin-documentos'])


def _map(doc: Documento) -> DocumentoAdminResponse:
    return DocumentoAdminResponse(
        id=str(doc.id),
        tramite_id=str(doc.tramite_id),
        titulo=doc.titulo,
        url_origen=doc.url_origen,
        estado=doc.estado.value,
        indexado=doc.indexado or doc.embedding is not None,
        version=doc.version,
        fecha_publicacion=doc.fecha_publicacion,
        fragmentado=doc.fragmentado,
        archivo_nombre=doc.archivo_nombre,
        mime_type=doc.mime_type,
        hash_contenido=doc.hash_contenido,
        actualizado_en=doc.actualizado_en,
        eliminado_en=doc.eliminado_en,
    )


@router.get('', response_model=list[DocumentoAdminResponse])
async def listar(
    tramite_id: UUID | None = Query(default=None),
    estado: str | None = Query(default=None),
    incluir_eliminados: bool = Query(default=False),
    limite: int = Query(default=50, ge=1, le=500),
    desde: int = Query(default=0, ge=0),
    container: Container = Depends(obtener_container),
):
    estado_vo = EstadoDocumento(estado) if estado else None
    docs = await container.gestionar_documentos.listar(
        tramite_id=tramite_id,
        estado=estado_vo,
        incluir_eliminados=incluir_eliminados,
        limite=limite,
        desde=desde,
    )
    return [_map(d) for d in docs]


@router.post('', response_model=DocumentoAdminResponse, status_code=201)
async def crear(
    payload: DocumentoAdminRequest,
    container: Container = Depends(obtener_container),
):
    try:
        doc = Documento(
            id=uuid4(),
            tramite_id=UUID(payload.tramite_id),
            titulo=payload.titulo,
            contenido=payload.contenido,
            url_origen=payload.url_origen,
            estado=EstadoDocumento(payload.estado),
            version=payload.version,
            fecha_publicacion=payload.fecha_publicacion,
        )
        guardado = await container.gestionar_documentos.registrar(doc)
        try:
            await container.procesar_documento.ejecutar(guardado.id)
        except Exception:
            pass
        final = await container.gestionar_documentos.obtener(guardado.id)
        return _map(final or guardado)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post('/upload', response_model=DocumentoAdminResponse, status_code=201)
async def upload(
    tramite_id: UUID = Form(...),
    titulo: str = Form(...),
    url_origen: str = Form(...),
    version: str = Form('1.0'),
    fecha_publicacion: date | None = Form(None),
    estado: str = Form('vigente'),
    archivo: UploadFile = File(...),
    container: Container = Depends(obtener_container),
):
    contenido = await archivo.read()
    try:
        guardado = await container.cargar_documento.ejecutar(
            tramite_id=tramite_id,
            titulo=titulo,
            url_origen=url_origen,
            version=version,
            fecha_publicacion=fecha_publicacion,
            estado=EstadoDocumento(estado),
            nombre_archivo=archivo.filename or 'documento.bin',
            contenido=contenido,
        )
        final = await container.gestionar_documentos.obtener(guardado.id)
        return _map(final or guardado)
    except (FormatoNoSoportadoError, DocumentoIlegibleError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post('/{documento_id}/procesar', response_model=DocumentoAdminResponse)
async def procesar(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
):
    doc = await container.procesar_documento.ejecutar(documento_id)
    if doc is None:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    final = await container.gestionar_documentos.obtener(doc.id)
    return _map(final or doc)


@router.delete('/{documento_id}', status_code=204)
async def baja_logica(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
):
    await container.gestionar_documentos.eliminar(documento_id)


@router.delete('/{documento_id}/fisico', status_code=204)
async def baja_fisica(
    documento_id: UUID,
    container: Container = Depends(obtener_container),
):
    await container.gestionar_documentos.eliminar_fisico(documento_id)