"""Controlador público del directorio de oficinas municipales (HU-17)."""

from fastapi import APIRouter, Depends, Query
from uuid import UUID

from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/oficinas', tags=['oficinas'])


@router.get('')
async def listar_oficinas(
    solo_activas: bool = Query(default=True),
    container: Container = Depends(obtener_container),
) -> list[dict]:
    """Directorio de oficinas para derivación (HU-17).

    Público: cualquier ciudadano puede consultar dónde dirigirse.
    """
    filtro = 'WHERE activa' if solo_activas else ''
    filas = await container.connection.pool.fetch(
        f'SELECT * FROM oficinas {filtro} ORDER BY nombre'
    )
    return [dict(fila) for fila in filas]


@router.get('/{oficina_id}')
async def obtener_oficina(
    oficina_id: UUID,
    container: Container = Depends(obtener_container),
) -> dict:
    fila = await container.connection.pool.fetchrow(
        'SELECT * FROM oficinas WHERE id = $1', oficina_id
    )
    if fila is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail='Oficina no encontrada')
    return dict(fila)