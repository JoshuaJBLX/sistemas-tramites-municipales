# EJECUCIÓN RESUMIDA

> 0) Una sola vez: `Copy-Item .env.example .env` (Win) o `cp .env.example .env`
> 1) Infraestructura: `docker compose up -d` y `docker exec -it tramites-ollama ollama pull qwen2.5:3b`
> 2) Esperar `docker compose ps` (todo `healthy`), luego ejecutar los apartados.

---

## BACKEND (FastAPI · puerto 8000)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

Docs → <http://localhost:8000/docs> · Health → <http://localhost:8000/health>

---

## FRONTEND (Next.js · puerto 3000)

```powershell
cd frontend-tramites
npm install
npm run dev
```

App → <http://localhost:3000>

---

## Datos de ejemplo (opcional, una vez)

```powershell
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/municipios.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/tramites.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/documentos.sql
```

## Apagar

```bash
docker compose down   # -v para borrar BD y reiniciar desde cero
```