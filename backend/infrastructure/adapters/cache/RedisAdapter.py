"""Adaptador de caché sobre Redis.

Redis es una optimización, no un requisito: si no está disponible, la caché
queda deshabilitada y el flujo de consulta sigue funcionando (más lento, pero
sin inventarse respuestas ni devolver errores al ciudadano).
"""

import json
import logging
import os
from typing import Any

import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import RedisError, TimeoutError as RedisTimeoutError

from domain.ports.CachePort import CachePort

logger = logging.getLogger(__name__)

MENSAJE_INDISPONIBLE = 'Redis no disponible; la caché de consultas queda deshabilitada.'


class RedisAdapter(CachePort):
    """Implementación del puerto de caché usando Redis asíncrono.

    Los errores de conexión se capturan y se registra una sola advertencia: la
    caché es un acelerador, por lo que no debe impedir responder al ciudadano.
    """

    def __init__(self, url: str | None = None) -> None:
        self._url = url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self._cliente: redis.Redis | None = None
        self._advertido = False

    @property
    def cliente(self) -> redis.Redis:
        if self._cliente is None:
            self._cliente = redis.from_url(self._url, decode_responses=True)
        return self._cliente

    def _advertir_una_vez(self, error: Exception) -> None:
        if not self._advertido:
            self._advertido = True
            logger.warning('%s Motivo: %s', MENSAJE_INDISPONIBLE, error)

    @staticmethod
    def _es_error_de_conexion(error: Exception) -> bool:
        return isinstance(error, (RedisConnectionError, RedisTimeoutError))

    async def obtener(self, clave: str) -> Any | None:
        try:
            valor = await self.cliente.get(clave)
        except (RedisError, OSError) as error:
            if self._es_error_de_conexion(error):
                self._advertir_una_vez(error)
                return None
            raise

        if valor is None:
            return None

        try:
            return json.loads(valor)
        except (TypeError, json.JSONDecodeError):
            return valor

    async def guardar(self, clave: str, valor: Any, ttl_segundos: int = 3600) -> None:
        try:
            await self.cliente.set(clave, json.dumps(valor, default=str), ex=ttl_segundos)
        except (RedisError, OSError) as error:
            if self._es_error_de_conexion(error):
                self._advertir_una_vez(error)
                return
            raise

    async def eliminar(self, clave: str) -> None:
        try:
            await self.cliente.delete(clave)
        except (RedisError, OSError) as error:
            if self._es_error_de_conexion(error):
                self._advertir_una_vez(error)
                return
            raise

    async def cerrar(self) -> None:
        if self._cliente is not None:
            await self._cliente.aclose()
            self._cliente = None