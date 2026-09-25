# 04.4 — Modelo de Tres PMV

> Parte de **04 — Gestión de Proyecto** (PMI/Scrum). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Comparación de PMV
| Aspecto | PMV1 | PMV2 | PMV3 |
|---|---|---|---|
| Pregunta clave | ¿El SLM procesa la intención y orienta trámites básicos? | ¿La RAG reduce alucinaciones? | ¿Producto seguro, accesible y de baja latencia? |
| Objetivo | Prototipo funcional | Modelo optimizado con RAG y citas | Sistema integrado desplegable |
| Funcionalidades | Chat + SLM + 5 trámites | RAG 20+ trámites + abstención | API completa + seguridad + UX |
| Arquitectura | Capas local | Hexagonal + pgvector | Hexagonal + Docker + Redis |
| Validación | 15 usuarios | 50 ciudadanos | 100+ / SUS / carga |

## Estado real del repositorio
- ✅ Arquitectura hexagonal, PostgreSQL + pgvector, Redis, Docker Compose (3 servicios).
- ✅ Catálogo TUPA 2023 ampliado (**252 procedimientos**) — supera los 5 del PMV1.
- ✅ RAG + SLM funcional (cubre avance de PMV2 en lo funcional).
- ⚠️/❌ Pendientes de PMV2/PMV3: abstención (G-04), filtros de seguridad (G-01/G-20),
  métricas (G-16), pruebas de carga/SUS (G-05/G-18/G-26).

## Ubicación del avance
El código se sitúa **entre PMV1 y PMV2**: núcleo funcional probado en entorno local, con pila
hexagonal; faltan validaciones y refuerzos de PMV2/PMV3.