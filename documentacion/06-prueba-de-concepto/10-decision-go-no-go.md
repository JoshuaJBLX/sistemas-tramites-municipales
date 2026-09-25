# 06.10 — Decisión Go / No-Go

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Criterios y resultados de la decisión
| Criterio | Umbral | Resultado esperado (a.md) | Estado real |
|---|---|---|---|
| Recuperación (bge-m3) | precisión > 90% | Supera | ✅ Pipeline ok; ⚠️ sin medición formal |
| Precisión de respuestas | > 85% | Supera | ⚠️ Sin benchmark |
| Groundedness | ≥ 0.8 | Supera | ⚠️ Cualitativo |
| Tiempo de respuesta | < 3 s | Supera con 3B cuantizado | ⚠️ Sin medición |

## Decisión
- **GO ✅** (a.md): la PoC demuestra la viabilidad del enfoque SLM + RAG.
- **Justificación**: síntesis, coherencia, exhaustividad y robustez del RAG en el dominio municipal.

## Nota de transparencia
- La decisión GO se sustenta en el documento académico; en el repositorio faltan los artefactos
  que la evidencian numéricamente (G-16/G-21). El sistema funcional ya está construido.