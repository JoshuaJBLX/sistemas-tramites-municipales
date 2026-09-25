# 04.6 — Product Backlog (Hu por PMV)

> Parte de **04 — Gestión de Proyecto** (PMI/Scrum). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Backlog priorizado (a.md 5.2)
| Épica | ID | Historia | Prioridad | PMV |
|---|---|---|---|---|
| Consulta | HU-01 | Consultar requisitos de licencias | Alta | PMV1 |
| Consulta | HU-02 | Costos y plazos de un trámite | Alta | PMV1 |
| IA / RAG | HU-03 | Consultar base vectorial de normas | Alta | PMV2 |
| Feedback | HU-04 | Calificar la respuesta del SLM | Media | PMV2 |
| Seguridad | HU-05 | Filtro de entradas | Alta | PMV3 |
| Rendimiento | HU-06 | Respuesta en < 3 segundos | Media | PMV3 |

> Nota: este backlog de a.md renumera historias (HU-01..06) distintas a las 18 HU del documento
> 02. Se reporta como referencia de priorización PMV.

## Backlog completo (18 HU)
- Listado y estado: ver **02.3** y `../00-documentos-rectores/02-implementacion-de-historias.md`.

## Estado real del backlog prioritario
| Historia | Estado |
|---|---|
| Consultar requisitos | ⚠️ Parcial (desde contexto RAG) |
| Costos y plazos | ⚠️ Parcial (campos `costo`/`duracion_estimada_dias`) |
| RAG sobre norma municipal | ✅ Implementado |
| Calificar respuesta | ❌ G-05 |
| Filtro de entradas | ⚠️ Validación Pydantic ✅; guardrails ❌ (G-20) |
| Respuesta < 3 s | ⚠️ Sin medición (G-16) |