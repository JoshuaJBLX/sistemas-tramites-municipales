# 02.1 — Definición del Problema de Ingeniería

> Parte de **02 — Conocimientos de Ingeniería** (equiv. a.md "2.Conocimientos de Ingenieria.docx",
> AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Planteamiento
Diseñar un sistema de orientación de trámites municipales basado en **SLM + RAG** que:
- comprenda consultas ciudadanas en lenguaje natural (español);
- recupere información de documentos oficiales vigentes (TUPA MPJ 2023);
- genere respuestas fundamentadas con fuentes trazables;
- evite alucinaciones mediante evaluación de groundedness;
- opere en hardware académico de bajo costo y baja latencia.

## Requerimientos y necesidades de ingeniería (resumen)
- Funcionales: RF-01 a RF-10 (ver 02.4).
- No funcionales: bajo costo, baja latencia (< 3 s), local (sin nube), español, trazabilidad,
  mantenibilidad (TUPA actualizable).

## Estado real
- ✅ El sistema implementa SLM (Qwen 2.5 3B/Ollama) + RAG (BGE-M3 + pgvector) + evaluación de
  groundedness con confianza.
- ⚠️ La "evitación de alucinaciones" es cualitativa; sin abstención formal (G-04).