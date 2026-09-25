"""Servicio de aplicación: ServicioCache."""

import hashlib
import json
from typing import Any

from domain.ports.CachePort import CachePort


class ServicioCache:
    """Abstrae el acceso a la caché de respuestas frecuentes."""

    def __init__(self, cache: CachePort, ttl_segundos: int = 3600) -> None:
        self._cache = cache
        self._ttl_segundos = ttl_segundos

    @staticmethod
    def construir_clave(pregunta: str) -> str:
        huella = hashlib.sha256(pregunta.strip().lower().encode('utf-8')).hexdigest()
        return f'consulta:{huella}'

    async def obtener_respuesta(self, pregunta: str) -> dict[str, Any] | None:
        clave = self.construir_clave(pregunta)
        valor = await self._cache.obtener(clave)

        if isinstance(valor, str):
            return json.loads(valor)
        return valor

    async def guardar_respuesta(self, pregunta: str, respuesta: dict[str, Any]) -> None:
        clave = self.construir_clave(pregunta)
        await self._cache.guardar(clave, respuesta, ttl_segundos=self._ttl_segundos)

    async def invalidar(self, pregunta: str) -> None:
        await self._cache.eliminar(self.construir_clave(pregunta))