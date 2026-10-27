"""Controlador REST de usuarios (HU-13 / G-01).

El registro exige contraseña (almacenada con PBKDF2) y controla quién puede
crear usuarios: un administrador autenticado, o en su ausencia el primer
administrador (arranque del sistema). Las lecturas son del propio usuario o
de un administrador.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field

from infrastructure.adapters.auth.PasswordHasher import hash_password
from infrastructure.container import Container, obtener_container
from infrastructure.controllers.dependencias import (
    obtener_usuario_actual,
    obtener_usuario_opcional,
    registrar_evento_seguridad,
    requiere_administrador,
)

router = APIRouter(prefix='/api/usuarios', tags=['usuarios'])

QUERY_INSERT_USUARIO = """
    INSERT INTO usuarios (id, nombre, correo, rol, password_hash, creado_en)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id, nombre, correo, rol, creado_en
"""

QUERY_SELECT_USUARIO = """
    SELECT id, nombre, correo, rol, creado_en, ultimo_acceso_en
    FROM usuarios
    WHERE id = $1
"""

QUERY_LISTAR_USUARIOS = """
    SELECT id, nombre, correo, rol, activo, creado_en, ultimo_acceso_en
    FROM usuarios
    ORDER BY creado_en DESC
    LIMIT 200
"""

QUERY_EXISTE_ADMIN = """
    SELECT 1 FROM usuarios WHERE rol = 'administrador' LIMIT 1
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
    rol: str = Field(default='ciudadano', pattern='^(ciudadano|revisor|administrador)$')
    password: str = Field(..., min_length=8)


class UsuarioResponse(BaseModel):
    id: UUID
    nombre: str
    correo: str
    rol: str
    creado_en: datetime
    ultimo_acceso_en: datetime | None = None


def _mismo_usuario(usuario: dict, usuario_id: UUID) -> bool:
    return str(usuario['id']) == str(usuario_id)


@router.post('', response_model=UsuarioResponse, status_code=201)
async def registrar_usuario(
    payload: UsuarioRequest,
    request: Request,
    container: Container = Depends(obtener_container),
    usuario: dict | None = Depends(obtener_usuario_opcional),
) -> UsuarioResponse:
    """Registra un usuario con contraseña (HU-13).

    Solo un administrador autenticado puede registrar usuarios; como excepción
    de arranque, si todavía no existe ningún administrador se permite crear el
    primero sin autenticación.
    """
    if usuario is None:
        async with container.connection.pool.acquire() as conexion:
            existe_admin = await conexion.fetchval(QUERY_EXISTE_ADMIN)
        if existe_admin or payload.rol != 'administrador':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Solo un administrador puede registrar usuarios.',
            )

    ip = request.client.host if request.client else None
    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(
            QUERY_INSERT_USUARIO,
            uuid4(),
            payload.nombre,
            payload.correo,
            payload.rol,
            hash_password(payload.password),
            datetime.now(timezone.utc),
        )
    await registrar_evento_seguridad(
        container,
        'usuario_registrado',
        usuario_id=fila['id'],
        correo=fila['correo'],
        detalle=f'Rol: {payload.rol}',
        ip=ip,
    )
    return UsuarioResponse(**dict(fila))


@router.get('', response_model=list[UsuarioResponse])
async def listar_usuarios(
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> list[UsuarioResponse]:
    """Lista los usuarios del sistema (solo administradores)."""
    async with container.connection.pool.acquire() as conexion:
        filas = await conexion.fetch(QUERY_LISTAR_USUARIOS)
    return [UsuarioResponse(**dict(fila)) for fila in filas]


@router.get('/{usuario_id}', response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: UUID,
    container: Container = Depends(obtener_container),
    usuario: dict = Depends(obtener_usuario_actual),
) -> UsuarioResponse:
    """Perfil de un usuario: el propio o el de cualquiera si eres admin."""
    if not _mismo_usuario(usuario, usuario_id) and usuario['rol'] != 'administrador':
        raise HTTPException(status_code=403, detail='Sin permisos sobre este usuario.')
    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(QUERY_SELECT_USUARIO, usuario_id)
    if fila is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return UsuarioResponse(**dict(fila))


@router.get('/{usuario_id}/consultas')
async def historial_consultas(
    usuario_id: UUID,
    container: Container = Depends(obtener_container),
    usuario: dict = Depends(obtener_usuario_actual),
) -> list[dict]:
    """Historial de consultas del usuario: el propio o el de cualquiera si eres admin."""
    if not _mismo_usuario(usuario, usuario_id) and usuario['rol'] != 'administrador':
        raise HTTPException(status_code=403, detail='Sin permisos sobre este historial.')
    async with container.connection.pool.acquire() as conexion:
        filas = await conexion.fetch(QUERY_CONSULTAS_USUARIO, usuario_id)
    return [dict(fila) for fila in filas]
