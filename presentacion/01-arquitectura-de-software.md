# 01 — Arquitectura de Software

> Sistema de Orientación de Trámites Municipales · MPJ (TUPA 2023)

## 1. Estilo arquitectónico: Hexagonal (Puertos y Adaptadores)

El proyecto se organiza en **capas puras** donde el dominio nunca depende de la infraestructura.
La regla de dependencias apunta siempre hacia adentro (del `infrastructure` hacia `domain`).

```
┌────────────────────────────────────────────────────────────────────────────┐
│  PRESENTACIÓN (HTTP)                                                       │
│  FastAPI routers (controllers)             Next.js (frontend, puerto 3000) │
└───────────────┬────────────────────────────────────────────────────────────┘
                │  llama casos de uso (reglas de negocio)
┌───────────────▼────────────────────────────────────────────────────────────┐
│  APPLICATION  (casos de uso + servicios)                                   │
│  RegistrarConsulta · GenerarOrientacion · GestionarDocumentos · ...        │
│  ServicioNLP · ServicioRAG · ServicioSLM · EvaluadorGroundedness · Caché   │
└───────┬─────────────────────────────┬──────────────────────────────────────┘
        │ inyecta implementaciones    │ usa PUERTOS (interfaces abstractas)
┌───────▼─────────────────────────────▼──────────────────────────────────────┐
│  DOMAIN (núcleo, sin dependencias)                                          │
│  Entidades: Tramite, Documento, Consulta, Respuesta, Usuario, ...           │
│  Value Objects: IntencionConsulta, NivelConfianza, EstadoDocumento, ...     │
│  Puertos: BusquedaSemanticaPort, GeneracionRespuestaPort, CachePort, ...    │
└─────────────────────────────────────────────────────────────────────────────┘
        ▲                        ▲                        ▲
┌───────┴─────────┐ ┌────────────┴────────────┐ ┌─────────┴──────────────┐
│ ADAPTADORES SALIDA │ ADAPTADORES SALIDA      │ ADAPTADORES SALIDA       │
│ PostgreSQL repos    │ RAG+Embeddings+SLM      │ Redis + storage local    │
│ DocumentoRepositoryImpl │ BusquedaVectorialAdapter │ RedisAdapter        │
│ ConsultaRepositoryImpl  │ BGE_M3Adapter            │ DocumentStorageAdapter│
│ Connection (asyncpg)    │ OllamaAdapter            │                       │
└──────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

## 2. Capas del backend (rutas reales)

| Capa | Carpeta | Contenido |
|---|---|---|
| Presentación | `backend/infrastructure/controllers/` | 4 routers FastAPI (consulta, tramite, documento, usuario) |
| Composición | `backend/infrastructure/container.py` | `Container` + `crear_container()` — único lugar que cablea adaptadores y casos de uso |
| Aplicación | `backend/application/use_cases/` | 7 casos de uso con una responsabilidad cada uno |
| Aplicación | `backend/application/services/` | Servicios de aplicación (NLP, RAG, SLM, groundedness, caché, auditoría, orientación) |
| Dominio | `backend/domain/entities/` · `domain/value_objects/` | Dataclasses puras + enums |
| Dominio | `backend/domain/ports/` | Interfaces (ABC) que definen qué necesita la aplicación |
| Infraestructura | `backend/infrastructure/adapters/` | Implementaciones concretas (BD → pgvector, embeddings, SLM, caché Redis, storage) |
| Infraestructura | `backend/infrastructure/repositories/` | Acceso a datos con `asyncpg` |

## 3. Inyección de dependencias

- `main.py` crea el contenedor en el *lifespan* (`crear_container()`) y lo guarda en
  `app.state.container` (`backend/main.py:27-29`).
- Los controllers piden el contenedor con `Depends(obtener_container)`.
- `crear_container()` construye todo el grafo: adaptadores → repositorios → servicios → casos de
  uso (`backend/infrastructure/container.py:88-136`).

## 4. Stack tecnológico

| Capa | Tecnología | Versión | Configuración |
|---|---|---|---|
| API REST | FastAPI + Uvicorn | 0.111.0 / 0.30.1 | `requirements.txt`, puerto 8000 |
| BD | PostgreSQL 16 + pgvector | pgvector/pgvector:pg16 | `docker-compose.yml` |
| Caché | Redis 7 | redis:7-alpine | `RedisAdapter.py`, TTL 3600 s |
| SLM | Qwen 2.5 3B (Ollama) | qwen2.5:3b | `docker-compose.yml`, `OllamaAdapter.py` |
| Embeddings | BGE-M3 (sentence-transformers) | BAAI/bge-m3 (1024 dims, CPU) | `BGE_M3Adapter.py` |
| Frontend | Next.js 14 + React 18 + Tailwind | 14.2.5 / ^18.3.1 / ^3.4.4 | `frontend-tramites/package.json` |
| Contenedores | Docker Compose | — | 3 servicios + 3 volúmenes |

## 5. Despliegue (Docker Compose)

Servicios definidos en `docker-compose.yml`:

| Servicio | Imagen | Puerto | Healthcheck |
|---|---|---|---|
| postgres | `pgvector/pgvector:pg16` | 5432 | `pg_isready` |
| redis | `redis:7-alpine` | 6379 | `redis-cli ping` |
| ollama | `ollama/ollama:latest` | 11434 | — (modelo se descarga con `ollama pull qwen2.5:3b`) |

- Las migraciones `database/migrations/` se ejecutan automáticamente al primer arranque
  (montadas en `/docker-entrypoint-initdb.d`).
- Volúmenes persistentes: `pgdata`, `redisdata`, `ollamadata`.
- GPU opcional: bloque comentado `deploy.resources` (NVIDIA) en el servicio ollama.

## 6. Flujo end-to-end de una consulta

```
Ciudadano ──> Next.js /chat ──> enviarConsulta() ──> POST /api/consultas
                                                          │
        (controller) clasifica_intencion ──> ServicioNLP (regex, 6 intenciones)
                          │
                          ├─ registrar_consulta ──> tabla consultas
                          ├─ servicio_cache (¿respuesta en Redis? → HIT)
                          ├─ generar_orientacion ──> ServicioRAG
                          │     ├─ buscar (BGE-M3 embedding → pgvector HNSW top_k=5, ≥0.3)
                          │     ├─ ServicioSLM → OllamaAdapter (qwen2.5:3b, temp 0.2)
                          │     └─ construir_fuentes (url + fragmento 280 chars)
                          ├─ evaluador_groundedness (cobertura léxica: alta ≥0.75, media ≥0.40)
                          ├─ auditar_consulta ──> tabla auditoria_consultas
                          └─ guardar en caché Redis
                          │
                          ▼
                   Respuesta {texto, confianza, fuentes} → chat (badge groundedness)
```

## 7. Decisiones arquitectónicas clave

- **Dominio puro**: entidades y value objects sin imports de FastAPI/BD → fácil de probar y
  reemplazar componentes.
- **RAG configurable**: `RAG_TOP_K` (5) y umbral de similitud 0.3 vía `BusquedaVectorialAdapter`.
- **SLM intercambiable**: `OllamaAdapter` implementa `GeneracionRespuestaPort`; se puede sustituir
  por vLLM u otro proveedor sin tocar el núcleo.
- **Caché transparente**: la capa de aplicación sólo conoce `CachePort`; Redis es un detalle.