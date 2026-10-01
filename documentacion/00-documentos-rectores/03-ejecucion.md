# EJECUCIÓN LOCAL

> Guía verificada en Windows 11 (octubre 2026) con servicios nativos, sin Docker.
> **1. Una vez** (preparación) · **2. Cada vez** (arranque).

## 1. Una vez (instalación)

```powershell
# Configuración
Copy-Item .env.example .env

# Base de datos (rol, BD, migraciones y datos)
psql -U postgres -c "CREATE ROLE tramites LOGIN PASSWORD 'tramites' CREATEDB;"
psql -U postgres -c "CREATE DATABASE tramites_municipales OWNER tramites;"
psql -h localhost -U tramites -d tramites_municipales -f database/migrations/002_create_tables.sql
psql -h localhost -U tramites -d tramites_municipales -f database/migrations/003_create_vectors.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/municipios.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/tramites.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/documentos.sql

# Dependencias
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd frontend-tramites; npm install; cd ..

# Modelo del SLM
ollama pull qwen2.5:3b

# Embeddings de los documentos (imprescindible para el RAG)
python -m backend.scripts.indexar_documentos
```

## 2. Cada vez (ejecución)

```powershell
# Servicios (si no están como servicio del sistema)
redis-server --port 6379
ollama serve

# API
.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000; cd ..

# Front-end (otra terminal)
cd frontend-tramites; npm run dev
```

- API: <http://localhost:8000> · Swagger: <http://localhost:8000/docs> · App: <http://localhost:3000>
- Verificar: `curl http://localhost:8000/health` → `{"status":"ok"}`
- Una consulta RAG tarda ~5-9 s; las repetidas salen de la caché en ~30 ms.

## Notas

- PostgreSQL queda instalado como servicio de Windows (puerto 5432); Redis (6379) y Ollama (11434) se levantan a mano.
- Si PowerShell bloquea el venv: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- Sin pgvector la búsqueda usa coseno en Python; el flujo es el mismo (ver `04-implementado-y-por-implementar.md`).