# 05.9 — Herramientas por PMV

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Matriz herramientas × PMV (a.md 17.3)
| Herramienta | PMV1 | PMV2 | PMV3 | Estado real |
|---|---|---|---|---|
| BERT/BGE-M3 | ✅ | ✅ | ✅ | ✅ BGE-M3 |
| Ollama (SLM) | ✅ | ✅ | ✅ | ✅ Qwen 2.5 3B |
| Docker Compose | ✅ | ✅ | ✅ | ✅ |
| GitHub Actions | — | ✅ | ✅ | ❌ G-17 |
| Proxmox | — | — | ✅ | ❌ |
| Redis | — | — | ✅ | ✅ |
| pgvector + HNSW | — | ✅ | ✅ | ✅ |
| FastAPI | — | — | ✅ | ✅ |
| Next.js/React | — | — | ✅ | ✅ |

## Lectura de avance
- ✅ Las herramientas de PMV1/PMV2 (modelo, embeddings, pgvector) están implementadas.
- ⚠️ De PMV3 solo redes y caché; faltan CI/CD, virtualización de despliegue y monitoreo.