"""Controlador REST de usuarios."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from infrastructure.container import Container, obtener_container

router = APIRouter(prefix='/api/usuarios', tags=['usuarios'])

QUERY_INSERT_USUARIO = """
    INSERT INTO usuarios (id, nombre, correo, rol, creado_en)
    VALUES ($1, $2, $3, $4, $5)
    RETURNING id, nombre, correo, rol, creado_en
"""

QUERY_SELECT_USUARIO = """
    SELECT id, nombre, correo, rol, creado_en
    FROM usuarios
    WHERE id = $1
"""

QUERY_CONSULTAS_USUARIO = """
    SELECT id, pregunta, intencion, creada_en
    FROM consultas
    WHERE usuario_id = $1
    ORDER BY creada_en DESC
    LIMIT 50
"""


class UsuarioRequest(BaseModel):
    nombre: str = Field(..., min_length=3)
    correo: EmailStr
    rol: str = Field(default='ciudadano', pattern='^(ciudadano|administrador)$')


class UsuarioResponse(BaseModel):
    id: UUID
    nombre: str
    correo: str
    rol: str
    creado_en: datetime


@router.post('', response_model=UsuarioResponse, status_code=201)
async def registrar_usuario(
    payload: UsuarioRequest,
    container: Container = Depends(obtener_container),
) -> UsuarioResponse:
    """Registra un nuevo usuario del sistema."""
    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(
            QUERY_INSERT_USUARIO,
            uuid4(),
            payload.nombre,
            payload.correo,
            payload.rol,
            datetime.now(timezone.utc),
        )
    return UsuarioResponse(**dict(fila))


@router.get('/{usuario_id}', response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: UUID,
    container: Container = Depends(obtener_container),
) -> UsuarioResponse:
    fila = await container.connection.pool.fetchrow(QUERY_SELECT_USUARIO, usuario_id)
    if fila is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return UsuarioResponse(**dict(fila))


@router.get('/{usuario_id}/consultas')
async def historial_consultas(
    usuario_id: UUID,
    container: Container = Depends(obtener_container),
) -> list[dict]:
    """Devuelve el historial de consultas del usuario."""
    filas = await container.connection.pool.fetch(QUERY_CONSULTAS_USUARIO, usuario_id)
    return [dict(fila) for fila in filas]