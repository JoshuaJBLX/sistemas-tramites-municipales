# EJECUCIÓN DEL PROYECTO

> Guía única de **puesta en marcha**, dividida en dos partes:
>
> - **Parte 1 · Instalación** → se hace **una sola vez** (prepara máquina, dependencias y datos).
> - **Parte 2 · Ejecución** → se hace **cada vez** que se levanta el proyecto.
>
> Verificado localmente en Windows 11 sin Docker (octubre 2026).

---

# PARTE 1 · INSTALACIÓN (una sola vez)

## 1.1 Requisitos previos

| Componente | Versión | Para qué |
|---|---|---|
| Python | 3.11+ (probado en 3.13) | Back-end FastAPI |
| Node.js | 18+ | Front-end Next.js |
| PostgreSQL | 13+ | Base de datos (`pgvector` es **opcional**) |
| Redis | 5+ | Caché de respuestas |
| Ollama | Actual | SLM local |
| Docker Desktop | Opcional | Atajo para levantar PostgreSQL + Redis + Ollama |

## 1.2 Configuración del entorno

```powershell
Copy-Item .env.example .env        # Windows
# cp .env.example .env             # Linux/macOS
```

Valores por defecto (los usa `Connection`, `RedisAdapter`, `OllamaAdapter` y `BGE_M3Adapter`):

```
POSTGRES_HOST=localhost   POSTGRES_PORT=5432
POSTGRES_USER=tramites    POSTGRES_PASSWORD=tramites
POSTGRES_DB=tramites_municipales
REDIS_URL=redis://localhost:6379/0      CACHE_TTL_SEGUNDOS=3600
OLLAMA_URL=http://localhost:11434      OLLAMA_MODEL=qwen2.5:3b
EMBEDDING_MODEL=BAAI/bge-m3            EMBEDDING_DEVICE=cpu
RAG_TOP_K=5                            NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 1.3 Infraestructura — Opción A: Docker (recomendada)

```bash
docker compose up -d
docker exec -it tramites-ollama ollama pull qwen2.5:3b
docker compose ps          # esperar a que los 3 servicios estén 'healthy'
```

Levanta PostgreSQL 16 **con pgvector** (5432), Redis 7 (6379) y Ollama (11434). En el primer
arranque ejecuta solo las migraciones de `database/migrations/` (esquema, sin datos).

## 1.4 Infraestructura — Opción B: sin Docker (servicios nativos)

Requiere PostgreSQL, Redis y Ollama instalados en el sistema.

**a) Rol y base de datos**

```powershell
psql -U postgres -c "CREATE ROLE tramites LOGIN PASSWORD 'tramites' CREATEDB;"
psql -U postgres -c "CREATE DATABASE tramites_municipales OWNER tramites;"
```

**b) Redis y Ollama**

```powershell
redis-server --port 6379            # o como servicio del sistema
ollama serve                        # si no está en segundo plano
ollama pull qwen2.5:3b              # ~1.9 GB, solo la primera vez
```

**c) Modelo del SLM**: `qwen2.5:3b` (3B, CPU, español). Modelos alternativos que funcionan:
`gemma4`, `dolphin-llama3` (cambiar `OLLAMA_MODEL` en `.env`).

> **pgvector es opcional.** La migración `002` crea la extensión `vector` solo si el servidor la
> tiene; si no, `documentos.embedding` queda como `double precision[]` y
> `BusquedaVectorialAdapter` calcula la similitud de coseno en Python. El flujo RAG es el mismo
> en ambos casos; con Docker se usa el operador `<=>` con índice HNSW (recomendado en producción).

## 1.5 Migraciones y datos de ejemplo

```powershell
# Desde la raíz del proyecto
psql -h localhost -U tramites -d tramites_municipales -f database/migrations/002_create_tables.sql
psql -h localhost -U tramites -d tramites_municipales -f database/migrations/003_create_vectors.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/municipios.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/tramites.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/documentos.sql
```

Resultado: **1 municipalidad, 22 trámites y 20 documentos** oficiales del TUPA 2023.
Las migraciones usan `IF NOT EXISTS`, así que repetirlas no rompe nada.

## 1.6 Dependencias del back-end

```powershell
python -m venv .venv                              # entorno en la raíz del proyecto
.\.venv\Scripts\Activate.ps1                      # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Notas:
- Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
- `asyncpg` 0.30 y `pydantic` 2.10 son las versiones con wheels para Python 3.13.
- Descarga `torch` y `sentence-transformers` (BGE-M3), por eso el primer `pip install` es lento.

## 1.7 Indexación de documentos (BGE-M3) — obligatorio para el RAG

Los seeds insertan los documentos con `embedding` en `NULL`. Este paso genera los vectores:

```powershell
python -m backend.scripts.indexar_documentos     # ejecutar desde la raíz del proyecto
```

- Lee `.env`, carga BGE-M3 (la primera vez descarga ~2.3 GB) y guarda el vector de cada documento
  vigente sin indexar.
- Funciona con y sin pgvector (`vector` o `double precision[]`).
- Repetirlo solo procesa los documentos pendientes (`embedding IS NULL`).

## 1.8 Dependencias del front-end

```powershell
cd frontend-tramites
npm install
cd ..
```

---

# PARTE 2 · EJECUCIÓN (cada vez)

## 2.1 Levantar la infraestructura

```bash
# Opción A (Docker)
docker compose up -d

# Opción B (nativo) — solo si no están como servicio
redis-server --port 6379
ollama serve
```

Verifica los puertos: `5432` (PostgreSQL) · `6379` (Redis) · `11434` (Ollama).

## 2.2 Levantar el back-end (puerto 8000)

```powershell
.\.venv\Scripts\Activate.ps1
cd backend
uvicorn main:app --reload --port 8000
```

- API → <http://localhost:8000> · Documentación Swagger → <http://localhost:8000/docs>
- Al arrancar abre el pool de PostgreSQL; si la BD no existe, el proceso falla (ver 2.5).
- Con `.env` en la raíz, `load_dotenv()` lo encuentra desde `backend/`.

## 2.3 Levantar el front-end (puerto 3000)

```powershell
cd frontend-tramites
npm run dev
```

App → <http://localhost:3000> (consume `NEXT_PUBLIC_API_URL` del `.env`).

## 2.4 Verificación rápida del back-end

```powershell
curl http://localhost:8000/health                 # {"status":"ok"}
curl http://localhost:8000/api/tramites           # 22 trámites
curl -X POST http://localhost:8000/api/consultas `
  -H "Content-Type: application/json" `
  -d '{"pregunta":"¿Qué requisitos necesito para inscribir un nacimiento?"}'
```

Tiempos observados con `qwen2.5:3b` en CPU:

| Operación | Tiempo |
|---|---|
| Consulta RAG completa (BGE-M3 + generación) | 5–9 s |
| Misma consulta servida desde la caché de Redis | ~30 ms |
| `/health`, `/api/tramites` | < 100 ms |

## 2.5 Apagar

```bash
docker compose down          # Opción A
docker compose down -v       # borra además el volumen de la BD (empezar de cero)
```

Opción B: detener `uvicorn` con `Ctrl+C`, y cerrar `ollama serve` y `redis-server`
(Ctrl+C o `Stop-Process`). El servicio de PostgreSQL queda instalado como servicio de Windows.

---

# PARTE 3 · SOLUCIÓN DE PROBLEMAS

| Síntoma | Causa | Solución |
|---|---|---|
| `422 field required: request` | Ya corregido en `59562e8` (FastAPI pedía un query param) | Actualiza el código |
| `404 ... /api/generate` desde el back-end | El modelo no está descargado en Ollama | `ollama pull qwen2.5:3b` y verifica con `ollama list` |
| `relation "tramites_municipales" does not exist` | Migraciones no aplicadas | Repetir 1.5 |
| `la extensión «vector» no está disponible` | Normal sin pgvector: el sistema usa el fallback | Ninguna acción; revisar 1.4 |
| Respuestas sin fuentes / sin contexto | Embeddings no generados | Ejecutar 1.7 |
| `address already in use` (puerto 8000) | Otra instancia de uvicorn | `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000 -State Listen).OwningProcess -Force` |
| `spawnSync ENOENT` (Windows) | Ruta de ejecutables larga | Mover el proyecto a una ruta sin espacios |
| Error al activar el venv | Política de PowerShell | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `500` en `/api/consultas` | Fallo en Redis/Ollama/BD | Ver la traza completa en la consola de uvicorn |

---

## Referencias

- Guía general del proyecto: `../../README.md`.
- Qué está implementado y qué falta: `04-implementado-y-por-implementar.md`.
- Avance por PMV1/PMV2/PMV3: `05-trazabilidad-por-pmv.md`.
- Comandos disponibles en la API: <http://localhost:8000/docs>.