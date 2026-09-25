# 06.9 — Limitaciones de la Prueba de Concepto

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Limitaciones de datos
- Dataset sintético pequeño (200 consultas).
- Corpus centrado en TUPA; cobertura parcial de ordenanzas generales.
- ❌ Dataset/corpus no versionados (G-21) → hallazgos no reproducibles.

## Limitaciones del modelo
- SLM 3B: menor capacidad de razonamiento; contexto limitado (mitigado con RAG).
- Alucinaciones residuales pese al groundedness (⚠️ sin abstención G-04).

## Limitaciones de la evaluación
- ⚠️ Evaluación manual/cualitativa; sin automatización ni muestreo estadístico (G-16).
- Indicadores interpretados, no medidos (latencia, CPU/RAM — G-16).

## Limitaciones operativas
- ML determinista (regex) para intención — G-02.
- Un solo nodo de BD/modelo (sin HA) — G-17.
- Sin pruebas de carga y sin auditoría de seguridad (G-23/G-26).