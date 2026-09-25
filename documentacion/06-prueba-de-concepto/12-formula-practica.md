# 06.12 — Fórmula Práctica de Implementación

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Recreación paso a paso (a.md 19.11)
1. **Descarga y despliegue del SLM** → ✅ equivalente: `docker compose up -d ollama` + pull de
   Qwen (README/EJECUCION).
2. **Generación del dataset sintético (Sterling)** → ❌ script no versionado (G-21).
3. **Extracción y limpieza docTXT/PDFs** → ⚠️ `POST /api/documentos/upload` existe, sin
   OCR/pipeline completo (G-12).
4. **Chunking y embeddings** → ⚠️ Embeddings ✅; chunking manual/G-13.
5. **RAG (ingesta y consulta)** → ✅ pgvector HNSW + búsquedas top_k=5, umbral 0.3.
6. **SLM + grounding feedback** → ✅ `EvaluadorGroundedness.py` + template de prompt.
7. **Evaluación de la PoC** → ❌ Sin ejecución formal registrada (G-16/G-21).

## Nota
- Pasos 1, 5 y 6 son **plenamente reproducibles** desde el repo; los pasos 2, 3 y 7 requieren
  artefactos pendientes (G-12/G-13/G-21).