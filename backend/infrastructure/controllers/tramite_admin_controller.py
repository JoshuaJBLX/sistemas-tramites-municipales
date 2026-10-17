"""Controlador REST de administración del catálogo de trámites (HU-07, HU-08).

Expone `GET /api/tramites/admin` —el listado que consume el panel de
administración del front-end— y la gestión del área responsable de cada trámite,
que es la columna que permite derivar al ciudadano hacia la oficina competente.
"""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from infrastructure.container import Container, obtener_container

# Prefijo compartido con tramite_controller: este router se registra ANTES que
# él para que `/api/tramites/admin` no caiga en la ruta `/api/tramites/{id}`.
router = APIRouter(prefix='/api/tramites', tags=['admin-tramites'])

QUERY_LISTAR_ADMIN = """
    SELECT t.id, t.municipalidad_id, t.nombre, t.descripcion, t.tipo,
           t.requisitos, t.costo, t.duracion_estimada_dias, t.area_responsable,
           m.nombre AS municipalidad
    FROM tramites t
    JOIN municipalidades m ON m.id = t.municipalidad_id
    ORDER BY t.nombre
"""

QUERY_ACTUALIZAR_AREA = """
    UPDATE tramites SET area_responsable = $2 WHERE id = $1 RETURNING id
"""


class AreaResponsableRequest(BaseModel):
    area_responsable: str = Field(
        ..., min_length=3, max_length=120, description='Oficina o área que tramita'
    )


@router.get('/admin')
async def listar_tramites_admin(
    container: Container = Depends(obtener_container),
) -> list[dict[str, Any]]:
    """Catálogo completo para el panel de administración (incluye área)."""
    filas = await container.connection.pool.fetch(QUERY_LISTAR_ADMIN)
    return [dict(fila) for fila in filas]


@router.put('/{tramite_id}/area')
async def definir_area_responsable(
    tramite_id: UUID,
    payload: AreaResponsableRequest,
    container: Container = Depends(obtener_container),
) -> dict[str, Any]:
    """Asigna (o corrige) el área responsable de un trámite (HU-07)."""
    fila = await container.connection.pool.fetchrow(
        QUERY_ACTUALIZAR_AREA, tramite_id, payload.area_responsable.strip()
    )
    if fila is None:
        raise HTTPException(status_code=404, detail='Trámite no encontrado')
    return {
        'id': str(fila['id']),
        'area_responsable': payload.area_responsable.strip(),
    }
