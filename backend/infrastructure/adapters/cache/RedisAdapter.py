"""Adaptador de caché sobre Redis."""

import json
import os
from typing import Any

import redis.asyncio as redis

from domain.ports.CachePort import CachePort


class RedisAdapter(CachePort):
    """Implementación del puerto de caché usando Redis asíncrono."""

    def __init__(self, url: str | None = None) -> None:
        self._url = url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self._cliente: redis.Redis | None = None

    @property
    def cliente(self) -> redis.Redis:
        if self._cliente is None:
            self._cliente = redis.from_url(self._url, decode_responses=True)
        return self._cliente

    async def obtener(self, clave: str) -> Any | None:
        valor = await self.cliente.get(clave)
        if valor is None:
            return None

        try:
            return json.loads(valor)
        except (TypeError, json.JSONDecodeError):
            return valor

    async def guardar(self, clave: str, valor: Any, ttl_segundos: int = 3600) -> None:
        await self.cliente.set(clave, json.dumps(valor, default=str), ex=ttl_segundos)

    async def eliminar(self, clave: str) -> None:
        await self.cliente.delete(clave)

    async def cerrar(self) -> None:
        if self._cliente is not None:
            await self._cliente.aclose()
            self._cliente = None