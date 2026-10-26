"""Adaptador: PasswordHasher (PBKDF2-SHA256 con la stdlib de Python).

Cumple HU-13 (gestión de contraseñas): las contraseñas nunca se almacenan ni
se transmiten en claro; se guardan con PBKDF2-HMAC-SHA256 y salt aleatorio
por usuario. No requiere dependencias externas (Render free: sin bcrypt).
"""

import hashlib
import hmac
import secrets

# Iteraciones recomendadas por OWASP para PBKDF2-SHA256 (2023+).
ITERACIONES = 310_000
_SAL_BYTES = 16
_PREFIJO = 'pbkdf2_sha256'


def hash_password(password: str) -> str:
    """Devuelve el hash almacenable: pbkdf2_sha256$iteraciones$salt$hash."""
    salt = secrets.token_bytes(_SAL_BYTES)
    digesto = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, ITERACIONES
    )
    return f'{_PREFIJO}${ITERACIONES}${salt.hex()}${digesto.hex()}'


def verify_password(password: str, almacenado: str | None) -> bool:
    """Verifica una contraseña contra el hash almacenado (comparación segura)."""
    if not almacenado:
        return False
    try:
        prefijo, iteraciones, salt_hex, digesto_hex = almacenado.split('$')
        if prefijo != _PREFIJO:
            return False
        digesto = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            bytes.fromhex(salt_hex),
            int(iteraciones),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digesto.hex(), digesto_hex)
