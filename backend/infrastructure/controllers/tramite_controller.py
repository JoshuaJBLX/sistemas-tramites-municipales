"""Controlador REST del catálogo de trámites municipales."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/tramites', tags=['tramites'])

QUERY_LISTAR_TRAMITES = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias, t.area_responsable,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    WHERE ($1::uuid IS NULL OR t.municipalidad_id = $1)
    ORDER BY t.nombre
"""

# Catálogo destacado de la portada: ordena por número de consultas registradas
# (trámite probable de la auditoría) y usa desempate aleatorio; si nadie ha
# consultado aún, el orden aleatorio deja la selección siempre renovada.
QUERY_TRAMITES_DESTACADOS = """
    WITH conteo AS (
        SELECT LOWER(TRIM(a.tramite_probable)) AS clave, COUNT(*) AS veces
        FROM auditoria_consultas a
        WHERE a.tramite_probable IS NOT NULL
        GROUP BY 1
    )
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias, t.area_responsable,
           m.nombre AS municipalidad,
           COALESCE(c.veces, 0) AS consultas,
           (SELECT COALESCE(SUM(veces), 0) FROM conteo) AS consultas_totales
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    LEFT JOIN conteo c ON c.clave = LOWER(TRIM(t.nombre))
    ORDER BY consultas DESC, RANDOM()
    LIMIT $1
"""

QUERY_OBTENER_TRAMITE = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias, t.area_responsable,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    WHERE t.id = $1
"""

QUERY_LISTAR_POR_IDS = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias, t.area_responsable,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    WHERE t.id = ANY($1::uuid[])
    ORDER BY t.nombre
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


@router.get('/destacados')
async def tramites_destacados(
    limite: int = Query(default=4, ge=1, le=8),
    container: Container = Depends(obtener_container),
) -> dict[str, Any]:
    """Catálogo destacado para la portada: los trámites más consultados y, en
    segundo lugar, un desempate aleatorio para que la vitrina nunca sea estática."""
    filas = await container.connection.pool.fetch(
        QUERY_TRAMITES_DESTACADOS, limite
    )
    tramites = []
    for fila in filas:
        tramite = dict(fila)
        tramites.append({
            **tramite,
            'consultas': int(tramite.pop('consultas', 0) or 0),
        })
    consultas_totales = tramites[0].pop('consultas_totales', 0) if tramites else 0
    return {
        'tramites': tramites,
        'criterio': 'mas_solicitados' if consultas_totales else 'aleatorio',
    }


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


@router.get('/{tramite_id}/relacionados')
async def tramites_relacionados(
    tramite_id: str,
    limite: int = Query(default=4, ge=1, le=10),
    container: Container = Depends(obtener_container),
) -> list[dict[str, Any]]:
    """Trámites complementarios al indicado, por similitud de embeddings (HU-12)."""
    try:
        uuid_tramite = UUID(tramite_id)
    except ValueError as error:
        raise HTTPException(status_code=422, detail='Identificador de trámite no válido') from error

    recomendaciones = await container.recomendar_tramites.ejecutar(
        uuid_tramite, limite=limite
    )
    if not recomendaciones:
        return []

    filas = await container.connection.pool.fetch(
        QUERY_LISTAR_POR_IDS, [recomendacion.id for recomendacion in recomendaciones]
    )
    por_id = {fila['id']: fila for fila in filas}

    # Se respeta el orden de similitud (mayor a menor), no el del `ORDER BY nombre`.
    relacionados = []
    for recomendacion in recomendaciones:
        fila = por_id.get(recomendacion.id)
        if fila is None:
            continue
        tramite = dict(fila)
        tramite['similitud'] = recomendacion.puntaje_relevancia
        relacionados.append(tramite)
    return relacionados