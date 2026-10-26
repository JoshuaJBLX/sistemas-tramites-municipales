"""Controlador REST de autenticación (HU-13 / G-01).

POST /api/auth/login → valida credenciales, registra el evento de seguridad
(correspondiente) y devuelve un token JWT con el rol del usuario.
GET  /api/auth/me    → perfil del usuario autenticado.
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field

from infrastructure.adapters.auth.JWTAdapter import JWTAdapter
from infrastructure.adapters.auth.PasswordHasher import verify_password
from infrastructure.container import Container, obtener_container
from infrastructure.controllers.dependencias import (
    obtener_usuario_actual,
    registrar_evento_seguridad,
)

router = APIRouter(prefix='/api/auth', tags=['autenticacion'])

_JWT = JWTAdapter()

QUERY_CREDENCIALES = """
    SELECT id, nombre, correo, rol, password_hash, activo
    FROM usuarios
    WHERE correo = $1
"""

QUERY_ULTIMO_ACCESO = """
    UPDATE usuarios SET ultimo_acceso_en = NOW() WHERE id = $1
"""


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str = Field(..., min_length=1)


class SesionResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    usuario: dict


class UsuarioSesion(BaseModel):
    id: UUID
    nombre: str
    correo: str
    rol: str
    creado_en: datetime | None = None
    ultimo_acceso_en: datetime | None = None


@router.post('/login', response_model=SesionResponse)
async def iniciar_sesion(
    payload: LoginRequest,
    request: Request,
    container: Container = Depends(obtener_container),
) -> SesionResponse:
    """Valida las credenciales y emite un token JWT (HU-13, escenario 1)."""
    ip = request.client.host if request.client else None

    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(QUERY_CREDENCIALES, payload.correo)

    credenciales_validas = (
        fila is not None
        and fila['activo']
        and verify_password(payload.password, fila['password_hash'])
    )
    if not credenciales_validas:
        # HU-13, escenario 2: el intento fallido queda registrado.
        await registrar_evento_seguridad(
            container,
            'login_fallido',
            usuario_id=fila['id'] if fila is not None else None,
            correo=payload.correo,
            detalle=(
                'Usuario inactivo'
                if fila is not None and not fila['activo']
                else 'Credenciales incorrectas'
            ),
            ip=ip,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales incorrectas.',
        )

    token = _JWT.crear_token(fila['id'], fila['rol'], fila['nombre'])
    async with container.connection.pool.acquire() as conexion:
        await conexion.execute(QUERY_ULTIMO_ACCESO, fila['id'])
    await registrar_evento_seguridad(
        container,
        'login_exitoso',
        usuario_id=fila['id'],
        correo=fila['correo'],
        ip=ip,
    )
    return SesionResponse(
        access_token=token,
        usuario={
            'id': str(fila['id']),
            'nombre': fila['nombre'],
            'correo': fila['correo'],
            'rol': fila['rol'],
        },
    )


@router.get('/me', response_model=UsuarioSesion)
async def perfil(
    usuario: dict = Depends(obtener_usuario_actual),
) -> UsuarioSesion:
    """Devuelve el perfil del usuario autenticado."""
    return UsuarioSesion(**usuario)
