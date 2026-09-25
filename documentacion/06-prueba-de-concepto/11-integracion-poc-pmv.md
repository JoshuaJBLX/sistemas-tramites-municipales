# 06.11 — Integración de la PoC con los PMV

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Mapeo PoC → PMV
| Hallazgo de la PoC | PMV que habilita | Estado real |
|---|---|---|
| BGE-M3 supera a BM25 en recuperación | PMV2: RAG sobre 20+ trámites | ✅ pgvector HNSW |
| Modelos pequeños + contexto RAG ≥ 85% | PMV2: SLM ampliado | ✅ Qwen 2.5 3B + RAG |
| Reranker bge-reranker mejora groundedness | PMV2 (optimización) | ❌ No implementado |
| Prompt rigor + k → groundedness | PMV3: validación | ⚠️ Configurable; sin registro |
| 3B cuantizado < 3 s | PMV3: latencia | ⚠️ Ollama cuantiza; sin medición |

## Impacto de los hallazgos (a.md)
- ⚠️ Incorporados en el diseño funcional del repo (RAG por defecto), pero el pipeline de
  experimentos no quedó integrado (G-16/G-21).

## Riesgo
- ❌ Si no se instrumentan métricas, PMV2/PMV3 pierden la evidencia para sustentar la decisión
  GO (G-16).