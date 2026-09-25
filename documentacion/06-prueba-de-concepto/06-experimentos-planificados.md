# 06.6 — Experimentos Planificados

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Plan de experimentos (a.md 19.6)
| Exp. | Descripción | Variable(s) | Objetivo |
|---|---|---|---|
| E1 | SLM sin contexto vs con RAG | contexto | Precisión de respuestas |
| E2 | TF-IDF/BM25 vs bge-m3 | index | Recall/precisión de recuperación |
| E3 | Query rewriting on/off | reescritura | Rendimiento RAG coloquial |
| E4 | k=5 vs otros k | top-k | Calidad según k |
| E5 | 2B/3B/7B | modelo SLM | Precisión × latencia |
| E6 | rigor de grounding feedback | prompt | Rendimiento del evaluador |

## Estado en el código
- ⚠️ E1: RAG es el flujo por defecto (no hay comparación sin contexto instrumentada).
- ⚠️ E2: pgvector HNSW implementado; no hay contra-prueba BM25 versionada.
- ⚠️ E3/E4: parámetros configurables (top_k=5, template de prompt), sin ejecución registrada.
- ⚠️ E5/E6: opciones del LlmFactory/EvaluadorGroundedness; sin resultados capturados.

## Conclusión
- ❌ Los resultados de experimentos **no se registran** de forma automatizada (G-16/G-21).