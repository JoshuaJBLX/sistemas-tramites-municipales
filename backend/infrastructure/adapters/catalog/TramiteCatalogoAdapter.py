"""Adaptador: TramiteCatalogoAdapter (consulta de trámites en PostgreSQL)."""

from uuid import UUID

from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.TramiteProbable import TramiteProbable
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository

QUERY_TRAMITES_POR_DOCUMENTOS = """
    SELECT t.id, t.nombre, t.requisitos, t.costo, t.duracion_estimada_dias,
           MIN(d.url_origen) AS url_origen,
           COUNT(d.id) AS documentos_coincidentes
    FROM tramites t
    JOIN documentos d ON d.tramite_id = t.id
    WHERE d.id = ANY($1::uuid[])
    GROUP BY t.id, t.nombre, t.requisitos, t.costo, t.duracion_estimada_dias
    ORDER BY documentos_coincidentes DESC, t.nombre
"""


class TramiteCatalogoAdapter(TramiteCatalogoPort):
    """Resuelve los trámites del catálogo a partir de los documentos recuperados."""

    def __init__(self, repository: PostgreSQLRepository) -> None:
        self._repository = repository

    async def buscar_por_documentos(
        self, documento_ids: list[UUID]
    ) -> list[TramiteProbable]:
        if not documento_ids:
            return []

        filas = await self._repository.obtener_muchos(
            QUERY_TRAMITES_POR_DOCUMENTOS, list(documento_ids)
        )

        return [
            TramiteProbable(
                id=fila['id'],
                nombre=fila['nombre'],
                requisitos=list(fila['requisitos'] or []),
                costo=float(fila['costo'] or 0.0),
                duracion_estimada_dias=int(fila['duracion_estimada_dias'] or 0),
                fuente_url=fila['url_origen'],
                documentos_coincidentes=int(fila['documentos_coincidentes']),
            )
            for fila in filas
        ]