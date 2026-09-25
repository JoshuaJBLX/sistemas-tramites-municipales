# 05.2 — Selección y Justificación de Herramientas (AG-I11)

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Evaluación por categoría (a.md 17.3) y estado de implementación
| Categoría | Evaluada | Seleccionada | Implementada |
|---|---|---|---|
| ML/AI | ✅ | BERT/BGE-M3 | ✅ BGE-M3 (`BGE_M3Adapter.py`) |
| MLOps y LLMOps | ✅ | Docker | ✅ (`docker-compose.yml`) |
| DevOps | ✅ | GitHub Actions | ❌ (G-17) |
| DB vectorial | ✅ | pgvector | ✅ (PostgreSQL 16, HNSW) |
| Frontend | ✅ | React/Next.js | ✅ (Next.js 14 + Tailwind) |
| Backend | ✅ | Python/FastAPI | ✅ (Python 3.11 + FastAPI) |
| Despliegue | ✅ | Docker + balancer | ⚠️ Docker ✅; balancer ❌ (G-17) |
| Colaboración | ✅ | GitHub | ✅ (repo) |
| Casos de uso | ✅ | 7 casos (Trello, VS Code, Docker, gitea, GitHub CI, Redis, Proxmox) | ⚠️ parcial |
| Contenedores | ✅ | Docker + Proxmox | ✅ Docker; ❌ Proxmox |
| Caché | ✅ | Redis | ✅ (`RedisAdapter.py`) |

## Justificación resumida
- Modelo multimodal ligero, contexto limitado (RAG), código abierto, GPU no exigida, integración
  en ecosistema Python, despliegue por contenedores.