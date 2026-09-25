# 06.5 — Selección de Modelos

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Modelos evaluados (a.md)
| Tipo | Opciones | Selección | Estado real |
|---|---|---|---|
| Gemelo de texto | Qwen 2.5 (Instruct) 0.5B, 1.5B, 3B, 7B | 3B | ✅ Qwen 2.5 3B vía Ollama |
| Embeddings | bge-m3, bge-large, nomic-embed | bge-m3 | ✅ BGE-M3 (1024 dims) |
| Reranker | bge-reranker | A considera | ❌ No implementado |
| Index | BM25 + HNSW | HNSW | ✅ HNSW (pgvector) |

## Justificación del SLM
- 3B: balance precisión × latencia en hardware académico; cuantizable (GGUF).
- Modelo configurable en el código (`OllamaAdapter.Model`) → permite experimentar H5.

## Estado
- ✅ Modelos núcleo implementados (Qwen 2.5 3B + BGE-M3).
- ❌ Reranker no implementado; la selección como "experimento comparado" no está registrada
  (G-21).