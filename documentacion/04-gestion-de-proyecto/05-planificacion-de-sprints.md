# 04.5 — Planificación de Releases y Sprints

> Parte de **04 — Gestión de Proyecto** (PMI/Scrum). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Tabla de sprints (a.md 18.5)
| PMV | Sprint | Duración | Enfoque | Entregable |
|---|---|---|---|---|
| 1 | S1 | Sem 1-3 | TUPA + SLM base | Dataset + SLM local |
| 1 | S2 | Sem 4-7 | UI consulta + enlaces | Demo 5 trámites |
| 2 | S3 | Sem 8-9 | Pipeline RAG | BD vectorial |
| 2 | S4 | Sem 10-11 | 20 trámites + evaluador | SLM ampliado |
| 2 | S5 | Sem 12 | Pruebas piloto | Demo PMV2 |
| 3 | S6 | Sem 13 | Cuantización/latencia | Modelo rápido |
| 3 | S7 | Sem 14 | Seguridad + responsive | Sistema seguro |
| 3 | S8 | Sem 15 | Estrés + SUS + empaquetado | Demo PMV3 |

## Estado real por entregable
| Entregable | Estado |
|---|---|
| Dataset + SLM local | ⚠️ SLM ✅ (Ollama Qwen 2.5 3B); dataset ❌ (G-21) |
| Demo consulta | ✅ Chat funcional |
| BD vectorial | ✅ pgvector HNSW |
| SLM ampliado (20+) | ✅ 252 procedimientos TUPA |
| Evaluador de respuestas | ⚠️ Confianza alta/media/baja |
| Pruebas piloto / SUS | ❌ G-05/G-18 |
| Cuantización | ⚠️ Modelo GGUF managado por Ollama (sin verificación) |
| Seguridad y guardrails | ❌ G-01/G-20 |
| Estrés/empaquetado | ❌ G-17/G-26 |

## Nota
- Los sprints son **documentales**; el repositorio no tiene evidencia de burndown ni velocity.