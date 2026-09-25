"""Implementación concreta de ConsultaRepository sobre PostgreSQL."""

from uuid import UUID

from domain.entities.Consulta import Consulta
from domain.ports.ConsultaRepository import ConsultaRepository
from domain.value_objects.IntencionConsulta import IntencionConsulta
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository

QUERY_INSERT = """
    INSERT INTO consultas (id, usuario_id, pregunta, intencion, creada_en)
    VALUES ($1, $2, $3, $4, $5)
    ON CONFLICT (id) DO UPDATE SET
        intencion = EXCLUDED.intencion
    RETURNING id, usuario_id, pregunta, intencion, creada_en
"""

QUERY_SELECT_ID = """
    SELECT id, usuario_id, pregunta, intencion, creada_en
    FROM consultas
    WHERE id = $1
"""

QUERY_SELECT_USUARIO = """
    SELECT id, usuario_id, pregunta, intencion, creada_en
    FROM consultas
    WHERE usuario_id = $1
    ORDER BY creada_en DESC
"""


def _mapear_consulta(fila) -> Consulta:
    return Consulta(
        id=fila['id'],
        usuario_id=fila['usuario_id'],
        pregunta=fila['pregunta'],
        intencion=IntencionConsulta(fila['intencion']) if fila['intencion'] else None,
        creada_en=fila['creada_en'],
    )


class ConsultaRepositoryImpl(PostgreSQLRepository, ConsultaRepository):
    """Persistencia de las consultas realizadas por los ciudadanos."""

    async def guardar(self, consulta: Consulta) -> Consulta:
        fila = await self.obtener_uno(
            QUERY_INSERT,
            consulta.id,
            consulta.usuario_id,
            consulta.pregunta,
            consulta.intencion.value if consulta.intencion else None,
            consulta.creada_en,
        )
        return _mapear_consulta(fila)

    async def obtener_por_id(self, consulta_id: UUID) -> Consulta | None:
        fila = await self.obtener_uno(QUERY_SELECT_ID, consulta_id)
        return _mapear_consulta(fila) if fila else None

    async def listar_por_usuario(self, usuario_id: UUID) -> list[Consulta]:
        filas = await self.obtener_muchos(QUERY_SELECT_USUARIO, usuario_id)
        return [_mapear_consulta(fila) for fila in filas]