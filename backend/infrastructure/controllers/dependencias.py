"""Dependencias de autenticación y control de acceso (HU-13 / G-01).

- `obtener_usuario_actual`: exige un JWT válido en Authorization Bearer y
  devuelve el usuario vigente de la base de datos.
- `requiere_administrador`: exige el rol administrador (403 + evento de
  seguridad si se deniega el acceso).
- `registrar_evento_seguridad`: persiste los eventos en `eventos_seguridad`
  (login fallido, token inválido, acceso denegado, …) sin tumbar la petición
  si el registro falla.
"""

from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from infrastructure.adapters.auth.JWTAdapter import JWTAdapter
from infrastructure.container import Container, obtener_container

_BEARER = HTTPBearer(auto_error=False)
_JWT = JWTAdapter()

QUERY_USUARIO_POR_ID = """
    SELECT id, nombre, correo, rol, activo
    FROM usuarios
    WHERE id = $1
"""

QUERY_EVENTO_SEGURIDAD = """
    INSERT INTO eventos_seguridad (usuario_id, correo, evento, detalle, ip)
    VALUES ($1, $2, $3, $4, $5)
"""


async def registrar_evento_seguridad(
    container: Container,
    evento: str,
    usuario_id: UUID | None = None,
    correo: str | None = None,
    detalle: str | None = None,
    ip: str | None = None,
) -> None:
    """Registra un evento de seguridad; los fallos de registro no rompen la petición."""
    try:
        async with container.connection.pool.acquire() as conexion:
            await conexion.execute(
                QUERY_EVENTO_SEGURIDAD, usuario_id, correo, evento, detalle, ip
            )
    except Exception:  # noqa: BLE001 - la auditoría no debe bloquear el flujo
        pass


def _cliente_ip(request: Request) -> str:
    return request.client.host if request.client else None


async def _usuario_desde_token(
    request: Request,
    credenciales: HTTPAuthorizationCredentials,
    container: Container,
) -> dict:
    """Valida el token y carga el usuario vigente (401 si no es válido)."""
    token_invalido = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Autenticación requerida: envía un token válido en Authorization.',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = _JWT.decodificar_token(credenciales.credentials)
    if payload is None:
        await registrar_evento_seguridad(
            container,
            'token_invalido',
            detalle='Token JWT inválido o expirado',
            ip=_cliente_ip(request),
        )
        raise token_invalido

    try:
        usuario_id = UUID(payload.get('sub', ''))
    except ValueError:
        raise token_invalido from None

    async with container.connection.pool.acquire() as conexion:
        fila = await conexion.fetchrow(QUERY_USUARIO_POR_ID, usuario_id)
    if fila is None or not fila['activo']:
        await registrar_evento_seguridad(
            container,
            'token_invalido',
            usuario_id=usuario_id,
            detalle='Usuario inexistente o inactivo',
            ip=_cliente_ip(request),
        )
        raise token_invalido

    return {
        'id': fila['id'],
        'nombre': fila['nombre'],
        'correo': fila['correo'],
        'rol': fila['rol'],
    }


async def obtener_usuario_actual(
    request: Request,
    credenciales: HTTPAuthorizationCredentials | None = Depends(_BEARER),
    container: Container = Depends(obtener_container),
) -> dict:
    """Devuelve el usuario autenticado; 401 si no hay token válido."""
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Autenticación requerida: envía un token válido en Authorization.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return await _usuario_desde_token(request, credenciales, container)


async def obtener_usuario_opcional(
    request: Request,
    credenciales: HTTPAuthorizationCredentials | None = Depends(_BEARER),
    container: Container = Depends(obtener_container),
) -> dict | None:
    """Como `obtener_usuario_actual`, pero sin token devuelve None (no 401).

    Se usa en el arranque del sistema: mientras no exista ningún
    administrador se permite crear el primero sin autenticación.
    """
    if credenciales is None or credenciales.scheme.lower() != 'bearer':
        return None
    return await _usuario_desde_token(request, credenciales, container)


async def requiere_administrador(
    request: Request,
    usuario: dict = Depends(obtener_usuario_actual),
    container: Container = Depends(obtener_container),
) -> dict:
    """Exige el rol administrador; registra el acceso denegado (HU-13 esc. 2)."""
    if usuario['rol'] != 'administrador':
        await registrar_evento_seguridad(
            container,
            'acceso_denegado',
            usuario_id=usuario['id'],
            correo=usuario['correo'],
            detalle=f'Rol "{usuario["rol"]}" sin permiso para {request.url.path}',
            ip=_cliente_ip(request),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No tienes permisos de administrador para esta operación.',
        )
    return usuario


async def requiere_revisor(
    request: Request,
    usuario: dict = Depends(obtener_usuario_actual),
    container: Container = Depends(obtener_container),
) -> dict:
    """HU-03: exige rol revisor o administrador (flujo de aprobación y
    derogación de documentos); registra el acceso denegado como evento."""
    if usuario['rol'] not in ('revisor', 'administrador'):
        await registrar_evento_seguridad(
            container,
            'acceso_denegado',
            usuario_id=usuario['id'],
            correo=usuario['correo'],
            detalle=f'Rol "{usuario["rol"]}" sin permiso para {request.url.path}',
            ip=_cliente_ip(request),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Se requiere el rol revisor o administrador para esta operación.',
        )
    return usuario
