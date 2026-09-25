# 02.4 — Requerimientos Funcionales (RF-01 a RF-10)

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

| RF | Requerimiento | Estado real |
|---|---|---|
| RF-01 | Registrar consulta ciudadana | ✅ `POST /api/consultas` |
| RF-02 | Identificar intención | ⚠️ Regex 6 intenciones (`ServicioNLP.py`); sin ML (G-02) |
| RF-03 | Identificar trámite probable + confianza | ❌ Solo intención; sin trámite/confianza |
| RF-04 | Solicitar aclaración ante ambigüedad | ❌ Sin abstención/aclaración (G-04) |
| RF-05 | Recuperar fuentes oficiales vigentes | ✅ pgvector HNSW, k=5, `estado='vigente'` |
| RF-06 | Filtrar documentos no vigentes | ✅ Búsqueda limitada a `vigente` |
| RF-07 | Orientación de requisitos | ⚠️ Desde contexto recuperado; sin garantía formal |
| RF-08 | Orientación de costos (con abstención) | ⚠️ Campo `costo`; sin abstención (G-04) |
| RF-09 | Orientación de plazos (con abstención) | ⚠️ Campo `duracion_estimada_dias`; sin abstención |
| RF-10 | Mostrar pasos del trámite | ❌ No estructurado (solo texto libre) |

## Evidencia en código
- 🔗 `backend/infrastructure/controllers/consulta_controller.py`
- 🔗 `backend/application/services/ServicioNLP.py`, `ServicioRAG.py`
- 🔗 `backend/infrastructure/adapters/rag/BusquedaVectorialAdapter.py`

## Vacíos
- ❌ G-02 (clasificación ML) · ❌ G-04 (abstención) · ❌ G-10 (pasos estructurados).