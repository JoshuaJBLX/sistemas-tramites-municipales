# 05.11 — Limitaciones y Decisiones de Herramientas

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Limitaciones documentadas
| Limitación | Impacto | Mitigación adoptada |
|---|---|---|
| Modelos pequeños: menor contextualización | Respuestas menos ricas | Arquitectura RAG con documentos oficiales |
| Alucinaciones | Información errónea | Evaluador de groundedness + citas (⚠️ sin abstención G-04) |
| Latencia en GPUs de academia | Respuesta lenta | SLM cuantizado (Ollama GGUF) + caché Redis |
| GPU limitada | QLoRA no viable | Modelo base + fine-tuning solo si necesario (G-15) |
| Contexto limitado (norma larga) | Pérdida de información | Chunking y RAG por fragmentos (⚠️ G-13) |

## Decisiones técnicas tomadas
1. BGE-M3 sobre BERT para embeddings multilingües modernos (✅).
2. pgvector sobre FAISS/milvus: integración nativa con PostgreSQL (✅).
3. FastAPI sobre Flask/Django: async + OAS automática (✅).
4. Next.js para el frontend: SSR/ISR para SEO y rendimiento (✅).
5. Docker Compose para distribución sin dependencias innecesarias del host (✅).

## Nota de transparencia
- Las limitaciones de a.md (OCR, dataset reducido) no tienen implementación en el repo (G-12/G-13/G-21).