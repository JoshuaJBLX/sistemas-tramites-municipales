# 02.9 — Aplicación de Conocimientos al Diseño (Trazabilidad)

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Matriz de trazabilidad AG-I07 / AG-107
| Conocimiento | Aplicación concreta | Evidencia | Estado |
|---|---|---|---|
| Arquitectura hexagonal | Capas domain/application/infrastructure | `backend/` | ✅ |
| Bases de datos vectoriales | Búsqueda semántica RAG (pgvector HNSW) | `003_create_vectors.sql` | ✅ |
| NLP | Clasificación de intención | `ServicioNLP.py` | ✅ (básico) |
| IA generativa (SLM) | Respuestas del asistente | `OllamaAdapter.py`, `ServicioSLM.py` | ✅ |
| Evaluación (groundedness) | Confianza alta/media/baja | `EvaluadorGroundedness.py` | ⚠️ |
| Ingeniería de requisitos | RF-01..10, HU-01..18 | `00/01-historias-de-usuario.md`, 02.4 | ⚠️ |
| Redes/API REST | FastAPI routers | `infrastructure/controllers/` | ✅ |
| Seguridad | Validación + SQL parametrizado | controllers | ⚠️ (sin auth G-01) |

## Cómo se conectan los conocimientos
Problema → requisitos (HU/RF) → diseño hexagonal → selección de stack → RAG+SLM+groundedness →
validación (pendiente métrica: G-16).

## Conclusión
- Los conocimientos AG-107 se aplican de forma end-to-end en el sistema ✅.
- La validación cuantitativa (métricas, pruebas) queda pendiente ❌ (G-16/G-18).