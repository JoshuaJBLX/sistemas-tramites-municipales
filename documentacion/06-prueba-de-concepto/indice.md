# 06 — Prueba de Concepto (PoC)

**Resumen:** validez técnica de la solución SLM + RAG + ML antes del desarrollo (equiv. "6.Prueba
de Concepto.docx" de a.md). Contrastado con el pipeline real y señalando qué artefactos de PoC no
están versionados (G-21), con leyenda: ✅ · ⚠️ · ❌ (G-XX).

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene |
|---|---|
| `01-identificacion-de-la-poc.md` | Identificación y alcance de la PoC. |
| `02-hipotesis.md` | Hipótesis H1-H5. |
| `03-corpus-documental.md` | Corpus documental (TUPA) y su mapeo a la BD real. |
| `04-dataset-de-consultas-sinteticas.md` | Dataset de 200 consultas (método Sterling). |
| `05-seleccion-de-modelos.md` | SLM/embeddings/vectorial evaluados y seleccionados. |
| `06-experimentos-planificados.md` | Plan de experimentos E1-E6. |
| `07-resultados-esperados.md` | Resultados esperados (precisión, groundedness, latencia). |
| `08-validacion-vs-criterios-de-exito.md` | Validación cuantitativa/cualitativa/estadística. |
| `09-limitaciones.md` | Limitaciones de datos, modelo y evaluación. |
| `10-decision-go-no-go.md` | Decisión GO con evidencias y notas de transparencia. |
| `11-integracion-poc-pmv.md` | Impacto de hallazgos en PMV2/PMV3. |
| `12-formula-practica.md` | Implementación paso a paso reproducida desde el repo. |
| `13-conclusiones.md` | Conclusiones y estudios futuros. |

## Relación con el repositorio

- Pipeline real: `backend/application/services/ServicioRAG.py`, `ServicioSLM.py`,
  `EvaluadorGroundedness.py`; `backend/infrastructure/adapters/`.
- No existen datasets ni resultados de PoC versionados: ver G-21.