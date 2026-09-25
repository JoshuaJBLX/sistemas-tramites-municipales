# 02.5 — Fundamentos Matemáticos y Científicos

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Estadística descriptiva del corpus documental (a.md 4.1)
- Documental: distribución de documentos por tipo, tamaño del TUPA, páginas.
- ⚠️ Sin artefactos versionados (G-21); el corpus real son los seeds de `database/seeds/documentos.sql`.

## Distribución de datos y balance de clases (a.md 4.2)
- Documental: balance por categoría de intención del dataset sintético (200 consultas de a.md).
- ❌ No existe dataset de entrenamiento/validación en el repositorio (G-21).

## Fundamentos matemáticos aplicados en el código
- **Similitud coseno**: pgvector (`embedding <=> $1::vector`) y umbral de similitud 0.3
  (✅ `BusquedaVectorialAdapter.py`).
- **Normalización Unicode / NLP básico**: eliminación de tildes y puntuación
  (✅ `ServicioNLP._normalizar`).
- **Distancias/índices vectoriales**: HNSW (✅ `003_create_vectors.sql`).
- ✅ SLM: atención transformers (Ollama/Qwen), sin entrenamiento local (G-15).

## Vacíos
- ❌ G-21 (datos de estadística/dataset no versionados).
- ❌ G-02 (no aplica F1/precisión/recall de ML clásico).