# 05.12 — Matriz de Trazabilidad de Herramientas (AG-I11)

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Matriz AG-I11 → herramientas → evidencia
| Atributo ICACIT | Herramienta(s) | Evidencia en el repo | Estado |
|---|---|---|---|
| AG-I11-1: Herramientas modernas | VS Code, Git, GitHub, Ollama, pgvector, Docker, Redis, FastAPI, Next.js | `backend/`, `frontend-tramites/`, `docker-compose.yml`, `requirements.txt` | ✅ |
| AG-I11-2: Uso justificado | Documentos 05.1-05.11 | Matrices de selección con criterios | ✅ |
| AG-I11-3: Datos modernos | TUPA 2023, seeds | `database/seeds/` | ✅ |
| AG-I11-4: Diseño/ingeniería | Arquitectura hexagonal | `backend/domain | application | infrastructure` | ✅ |
| AG-I11-5: Generación | SLM + RAG (Qwen 2.5 3B + BGE-M3) | `adapters/rag`, `adapters/llm` | ✅ |
| AG-I11-6: Validación | Evaluador de groundedness | `EvaluadorGroundedness.py` | ⚠️ (el resto sin métricas G-16) |
| AG-I11-7: Entrega | Docker Compose, ejecutables | `docker-compose.yml`, `00/03-ejecucion.md` | ⚠️ (sin CI G-17) |

## Síntesis
- **AG-I11 cubierto en gran parte** con evidencia real en el repositorio.
- Pendientes que debilitan la trazabilidad: CI/CD (G-17), sistema de pruebas (G-18),
  auditoría de calidad/seguridad (G-26) y métricas del desempeño (G-16).