# 06.1 — Identificación de la Prueba de Concepto (PoC)

> Parte de **06 — Prueba de Concepto** (a.md "6.Prueba de Concepto.docx").
> Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Identificación
- **Nombre**: "Evaluación de un sistema RAG con SLM local para orientación de trámites
  municipales (MPJ — TUPA 2023)".
- **Problema que resuelve**: verificar que un SLM pequeño (Qwen 2.5 3B) combinado con RAG
  (BGE-M3 + pgvector) produce respuestas fundamentadas, precisas y de baja latencia para
  consultas ciudadanas, sin depender de la nube.
- **Tipo de PoC**: técnica/funcional (prueba de viabilidad del enfoque SLM + RAG).

## Documento formulario (a.md vs repo)
| Campo | a.md | En el repositorio |
|---|---|---|
| Nombre de la PoC | (formulario) | ✅ 06.1-06.13 |
| Plan de exp. | Sí | ⚠️ Documento (G-21) |
| Guía de ejecución | Sí | ⚠️ `00/03-ejecucion.md` navega el sistema |

## Alcance
- ✅ Viabilidad técnica del pipeline RAG (embedding → búsqueda → SLM → groundedness).
- ❌ No se ejecutaron experimentos formales con datos registrados (G-21).