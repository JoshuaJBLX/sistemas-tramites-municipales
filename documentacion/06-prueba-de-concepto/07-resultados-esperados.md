# 06.7 — Resultados Esperados

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Resultados esperados (a.md 19.7 → proyectados)
| Indicador | Esperado |
|---|---|
| Precisión de recuperación bibliográfica RAG | > 90% |
| Precisión de respuestas (2B/3B/7B ± contexto) | 84-94% |
| Métricas de groundedness | Mejora con rigor de prompt, bge-reranker y k |
| Latencia (3B cuantizado) | < 3 s (p95) |

## Estado verificable en el repositorio
- ⚠️ El pipeline RAG existe y es evaluable manualmente (`Respuesta.confianza`, `fuentes`).
- ❌ **No se han registrado resultados** (sin scripts de benchmark — G-16/G-21).
- ⚠️ Los umbrales operativos reales: similitud ≥ 0.3, top_k=5 (no declarados como "resultado" en el repo).