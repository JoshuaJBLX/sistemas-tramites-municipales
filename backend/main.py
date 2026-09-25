"""Punto de entrada de la API REST del Sistema de Trámites Municipales.

Ejecución (desde la carpeta backend/):
    uvicorn main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Carga variables de entorno desde el .env del proyecto (sube hasta la raíz).
load_dotenv()

from infrastructure.adapters.cache.RedisAdapter import RedisAdapter
from infrastructure.container import Container, crear_container
from infrastructure.controllers.consulta_controller import router as consulta_router
from infrastructure.controllers.documento_controller import router as documento_router
from infrastructure.controllers.tramite_controller import router as tramite_router
from infrastructure.controllers.usuario_controller import router as usuario_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Abre el pool de PostgreSQL al arrancar y libera recursos al apagar."""
    container: Container = crear_container()
    await container.connection.conectar()
    app.state.container = container

    yield

    await container.connection.desconectar()
    if isinstance(container.cache, RedisAdapter):
        await container.cache.cerrar()


app = FastAPI(
    title='Sistema de Trámites Municipales API',
    description='API de orientación de trámites con RAG (pgvector + SLM local)',
    version='0.1.0',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(consulta_router)
app.include_router(tramite_router)
app.include_router(documento_router)
app.include_router(usuario_router)


@app.get('/health', tags=['operacion'])
async def health() -> dict[str, str]:
    """Verificación de estado del servicio."""
    return {'status': 'ok'}
