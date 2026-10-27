import asyncio
import os
import sys

sys.path.insert(0, "backend")
import asyncpg


async def main():
    conn = await asyncpg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    # Test oficinas
    filas = await conn.fetch("SELECT nombre, area FROM oficinas WHERE activa ORDER BY nombre")
    for f in filas:
        print(f"Oficina: {f['nombre']} | Area: {f['area']}")
    # Test filtro auditoria
    filas = await conn.fetch(
        """
        SELECT c.pregunta, a.tramite_probable, a.marcado_inconsistente,
               (a.respuesta IS NOT NULL AND (COALESCE(a.fuentes_detalle, '[]') = '[]' OR NOT EXISTS (SELECT 1 FROM evaluaciones_calidad e WHERE e.consulta_id = c.id))) AS inconsistente
        FROM consultas c
        LEFT JOIN LATERAL (
            SELECT tramite_probable, marcado_inconsistente, respuesta, fuentes_detalle
            FROM auditoria_consultas a
            WHERE a.consulta_id = c.id
            ORDER BY a.registrado_en DESC LIMIT 1
        ) a ON TRUE
        ORDER BY c.creada_en DESC LIMIT 5
        """
    )
    for f in filas:
        print(f"Q: {f['pregunta'][:40]}... | Tramite: {f['tramite_probable']} | Marcado: {f['marcado_inconsistente']} | Inconsistente: {f['inconsistente']}")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())