"""Adaptador: JWTAdapter (emisión y validación de tokens JWT).

Cumple HU-13 (acceso autorizado): el login devuelve un token firmado (HS256)
con el usuario y su rol; los endpoints protegidos lo exigen en la cabecera
Authorization. El secreto se toma de JWT_SECRET; si no está definido se deriva
de la API key existente para no requerir una variable nueva en el despliegue
(Render CLI no permite añadir env vars sin recrear el servicio).
"""

import hashlib
import os
import time
from uuid import UUID

import jwt

# Duración del token: 8 horas de sesión administrativa.
DURACION_SEGUNDOS = 8 * 60 * 60
_ALGORITMO = 'HS256'


def _secreto() -> str:
    secreto = os.getenv('JWT_SECRET')
    if secreto:
        return secreto
    base = (
        os.getenv('OPENAI_API_KEY')
        or os.getenv('OPENROUTER_API_KEY')
        or os.getenv('POSTGRES_PASSWORD')
        or ''
    )
    # Derivación determinista: el token sigue siendo válido entre reinicios.
    return hashlib.sha256(('tramites-jwt:' + base).encode('utf-8')).hexdigest()


class JWTAdapter:
    """Emite y valida tokens JWT firmados con HS256."""

    def crear_token(self, usuario_id: UUID, rol: str, nombre: str) -> str:
        ahora = int(time.time())
        payload = {
            'sub': str(usuario_id),
            'rol': rol,
            'nombre': nombre,
            'iat': ahora,
            'exp': ahora + DURACION_SEGUNDOS,
        }
        return jwt.encode(payload, _secreto(), algorithm=_ALGORITMO)

    def decodificar_token(self, token: str) -> dict | None:
        """Devuelve el payload del token o None si es inválido o expiró."""
        try:
            return jwt.decode(token, _secreto(), algorithms=[_ALGORITMO])
        except jwt.PyJWTError:
            return None
