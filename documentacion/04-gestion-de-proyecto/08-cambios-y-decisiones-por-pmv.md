# 04.8 — Cambios y Decisiones por PMV

> Parte de **04 — Gestión de Proyecto** (PMI/Scrum). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Registro de decisiones (a.md 18.10)
| PMV | Hallazgo | Decisión | Estado real |
|---|---|---|---|
| PMV1 | El ciudadano no comprende la interfaz inicial de navegación | Rediseñar UX priorizando el chat conversacional directo | ✅ Chat como foco del diseño (`app/chat`, `ChatBox`) |
| PMV2 | Bajo recall en trámites complejos del TUPA | Incorporar arquitectura RAG con búsqueda vectorial | ✅ RAG implementado (pgvector HNSW) |
| PMV3 | Latencia alta con normativas extensas | Cuantización + caché + optimizar endpoints | ⚠️ Caché Redis ✅; cuantización/vLLM ❌ (G-15/G-17) |

## Nota de coherencia a.md vs código
- El orden causa→decisión del a.md parece invertido respecto a lo implementado (en el repo el RAG
  ya está hecho y el OCR/chunking no); se documenta la decisión y su estado real.

## Decisiones de diseño del repositorio
- Arquitectura hexagonal con inyección de dependencias (`container.py`).
- Estilo cálido/orgánico (rediseño UI).
- Demo/fallback en el frontend cuando el backend no responde (`lib/api.ts`).