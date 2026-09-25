"""Controlador REST del catálogo de trámites municipales."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/tramites', tags=['tramites'])

QUERY_LISTAR_TRAMITES = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    WHERE ($1::uuid IS NULL OR t.municipalidad_id = $1)
    ORDER BY t.nombre
"""

QUERY_OBTENER_TRAMITE = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    WHERE t.id = $1
"""


@router.get('')
async def listar_tramites(
    municipalidad_id: str | None = Query(default=None),
    container: Container = Depends(obtener_container),
) -> list[dict[str, Any]]:
    """Lista el catálogo de trámites, opcionalmente filtrado por municipalidad."""
    filas = await container.connection.pool.fetch(
        QUERY_LISTAR_TRAMITES, municipalidad_id
    )
    return [dict(fila) for fila in filas]


@router.get('/{tramite_id}')
async def obtener_tramite(
    tramite_id: str,
    container: Container = Depends(obtener_container),
) -> dict[str, Any]:
    """Devuelve el detalle de un trámite junto con su documentación vigente."""
    fila = await container.connection.pool.fetchrow(QUERY_OBTENER_TRAMITE, tramite_id)
    if fila is None:
        raise HTTPException(status_code=404, detail='Trámite no encontrado')

    tramite = dict(fila)
    documentos = await container.consultar_tramite.ejecutar(tramite_id)
    tramite['documentos'] = [
        {
            'id': str(documento.id),
            'titulo': documento.titulo,
            'url_origen': documento.url_origen,
            'estado': documento.estado.value,
        }
        for documento in documentos
    ]
    return tramite