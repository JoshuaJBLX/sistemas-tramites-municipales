"""Punto de entrada de la API REST del Sistema de Trámites Municipales.

Ejecución (desde la carpeta backend/):
    uvicorn main:app --reload --port 8000
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Carga variables de entorno desde el .env del proyecto (sube hasta la raíz).
load_dotenv()

from infrastructure.adapters.cache.RedisAdapter import RedisAdapter
from infrastructure.container import Container, crear_container
from infrastructure.controllers.auth_controller import router as auth_router
from infrastructure.controllers.consulta_controller import router as consulta_router
from infrastructure.controllers.dependencias import requiere_administrador
from infrastructure.controllers.documento_controller import router as documento_router
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

# Configuración de CORS - permite localhost y dominio de Vercel
allowed_origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Agregar dominio de Vercel si está configurado
vercel_url = os.getenv('VERCEL_FRONTEND_URL')
if vercel_url:
    allowed_origins.append(vercel_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

from infrastructure.controllers.documento_admin_controller import (
    router as documento_admin_router,
)
from infrastructure.controllers.metrica_controller import (
    router_evaluaciones as evaluaciones_router,
    router_metricas as metricas_router,
    router_reportes as reportes_router,
)
from infrastructure.controllers.oficina_controller import router as oficina_router
from infrastructure.controllers.tramite_admin_controller import (
    router as tramite_admin_router,
)
from infrastructure.controllers.tramite_controller import router as tramite_router

# El router admin se registra antes que el público: `/api/tramites/admin`
# debe resolverse en su ruta y no en `/api/tramites/{tramite_id}` (D-21).
# Los routers de administración exigen rol administrador (HU-13 / G-01).
app.include_router(
    tramite_admin_router, dependencies=[Depends(requiere_administrador)]
)
app.include_router(consulta_router)
app.include_router(tramite_router)
app.include_router(
    documento_admin_router, dependencies=[Depends(requiere_administrador)]
)
app.include_router(documento_router)
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(oficina_router)  # HU-17: directorio público de oficinas
# HU-15/HU-16/HU-18: cada endpoint de estos routers exige rol administrador
# (o es público, en el caso de las evaluaciones del ciudadano).
app.include_router(metricas_router)
app.include_router(evaluaciones_router)
app.include_router(reportes_router)


@app.get('/health', tags=['operacion'])
async def health() -> dict[str, str]:
    """Verificación de estado del servicio."""
    return {'status': 'ok'}
