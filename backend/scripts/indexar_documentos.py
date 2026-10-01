"""Indexa los documentos vigentes sin embedding en la base documental.

Genera los embeddings con BGE-M3 (vía el adaptador del backend) y los guarda
en la columna `embedding` de `documentos`. Funciona tanto con pgvector
(columnas `vector`) como en servidores sin la extensión (`double precision[]`).

Uso (desde la raíz del proyecto, con el entorno activo):
    python -m backend.scripts.indexar_documentos
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.repositories.Connection import Connection

QUERY_PENDIENTES = """
    SELECT id, titulo, contenido
    FROM documentos
    WHERE estado = 'vigente' AND embedding IS NULL
"""

QUERY_UPDATE = 'UPDATE documentos SET embedding = $2, actualizado_en = NOW() WHERE id = $1'


async def indexar() -> None:
    connection = Connection()
    await connection.conectar()

    try:
        pendientes = await connection.pool.fetch(QUERY_PENDIENTES)
        if not pendientes:
            print('[indexar] No hay documentos vigentes sin embedding.')
            return

        es_pgvector = await connection.es_pgvector()
        generador = BGE_M3Adapter()
        if es_pgvector:
            print(f"[indexar] Indexando {len(pendientes)} documentos (columna: 'vector').")
        else:
            print(f'[indexar] Indexando {len(pendientes)} documentos (columna: double precision[]).')

        for documento in pendientes:
            texto = f"{documento['titulo']} - {documento['contenido']}"
            vector = await generador.generar_embedding(texto)
            if es_pgvector:
                literal = '[' + ','.join(str(valor) for valor in vector) + ']'
            else:
                literal = vector  # asyncpg codifica la lista como double precision[]
            await connection.pool.execute(
                QUERY_UPDATE, documento['id'], literal
            )
            print(f"  [ok] {documento['titulo'][:60]}")

        print('[indexar] Indexación completada.')
    finally:
        await connection.desconectar()


if __name__ == '__main__':
    asyncio.run(indexar())