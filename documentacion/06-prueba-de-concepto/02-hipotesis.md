# 06.2 — Hipótesis de la Prueba de Concepto

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Hipótesis formuladas (a.md 19.1)
| Hipótesis | Formulación |
|---|---|
| H1 | El contexto (RAG) mejora la precisión de respuestas del SLM vs. SLM sin contexto |
| H2 | Modelos BERT/BGE-M3 recuperan documentos más rápidos y precisos que TF-IDF/BM25 |
| H3 | Query rewriting mejora el rendimiento del RAG para consultas coloquiales |
| H4 | La relevancia de top-k influye en la calidad de las respuestas (k=5) |
| H5 | Según la dificultad de la pregunta, variar el modelo (2B/3B/7B) altera precisión y latencia |

## Estado en el repositorio
- ✅ H1/H2/H4 verificables en el pipeline actual (pgvector HNSW top_k=5, RAG por defecto).
- ⚠️ H3 (query rewriting) no documentado como atributo explícito.
- ⚠️ H5 viable técnicamente (Ollama admite Model en el adapter), pero sin ejecución registrada.

## Nota
- Los experimentos formales no están ejecutados ni versionados (❌ G-21).