# 02.8 — Selección y Justificación de Tecnologías

> Parte de **02 — Conocimientos de Ingeniería** (AG-107; comparativas detalladas en el documento
> 05). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Criterios de evaluación (a.md)
Adecuación técnica, costo/licencia, escalabilidad, seguridad, interoperabilidad,
aprendizaje, soporte/comunidad, eficiencia computacional.

## Selección del lenguaje backend: Python (FastAPI)
- Argumento (a.md 8.2): ecosistema IA (transformers, sentence-transformers), tipado y doc
  automática — ✅ implementado (Python 3.11 + FastAPI 0.111).
- Alternativas evaluadas documentalmente: Java, Node.js.

## Selección real del stack
| Capa | Elección | Evidencia |
|---|---|---|
| Backend | Python 3.11 + FastAPI | `requirements.txt`, `backend/main.py` |
| Frontend | Next.js 14 + React + Tailwind | `frontend-tramites/package.json` |
| SLM | Qwen 2.5 3B vía Ollama | `docker-compose.yml`, `OllamaAdapter.py` |
| Embeddings | BGE-M3 | `BGE_M3Adapter.py`, `requirements.txt` |
| Búsqueda | PostgreSQL 16 + pgvector (HNSW) | migraciones 001-003 |
| Caché | Redis 7 (cache-aside) | `RedisAdapter.py`, compose |
| Contenedores | Docker Compose (3 servicios) | `docker-compose.yml` |

## Vacíos
- ❌ G-17 (vLLM/CI/CD no adoptados) · ❌ G-18 (pytest no instalado).