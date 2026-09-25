# 05.5 — Herramientas de Datos e IA

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Modelos y frameworks de IA
| Herramienta | Rol | Estado real |
|---|---|---|
| Qwen 2.5 3B (SLM, Ollama) | Generación de respuestas | ✅ (`OllamaAdapter.py`, `ServicioSLM.py`) |
| BGE-M3 (sentence-transformers) | Embeddings multilingüe | ✅ (`BGE_M3Adapter.py`, 1024 dims) |
| Ollama | Gestión de modelos GGUF | ✅ (`docker-compose.yml`) |
| pgvector | Búsqueda semántica | ✅ (HNSW, `vector_cosine_ops`) |
| Fine-tuning QLoRA | Ajuste del SLM al dominio | ❌ (G-15) |
| Dataset de entrenamiento | Domínio municipal | ❌ (G-21) |
| OCR (pdfplumber/doctr) | Extracción de PDFs | ⚠️ Endpoint upload existe; sin OCR/chunking real (G-12/G-13) |

## Flujo de datos implementado
TUPA/PDF ($formato_url) → embeddings BGE-M3 → tabla `documentos.embedding` (vector(1024)) →
consulta → `vector <=> $1` HNSW top_k=5, umbral 0.3 → contexto → SLM → respuesta + fuentes.