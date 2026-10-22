# 03.11 — Medidas de Mitigación y Sostenibilidad
> **Documento relacionado:** [06 · Estado actual implementado](../00-documentos-rectores/06-estado-actual-implementado.md) — documento rector y fuente única de verdad del estado y las cifras.

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Plan de mitigación
| Dimensión | Riesgo | Mitigación | Estado |
|---|---|---|---|
| Social | Desconfianza | Fuentes citadas visibles | ⚠️ url+fragmento (G-13) |
| Económica | Sobre-costo operativo | Código abierto + SLM local | ✅ |
| Ambiental | Consumo energético | SLM 3B local | ✅ |
| Seguridad | Inyección de prompts | Guardrails + validación | ⚠️ Pydantic ✅; guardrails ❌ (G-20) |
| Privacidad | PII accidental | Enmascaramiento → no almacenar | ✅ no almacenar; ❌ enmascarar (G-03) |
| Ética | Alucinaciones | RAG + groundedness | ⚠️ confianza cualitativa (G-04) |
| Legal | Exposición municipal | Aviso de orientación | ⚠️ solo UI (G-25) |

## Sostenibilidad operativa
- ✅ Arquitectura hexagonal (bajo acoplamiento, componentes reemplazables).
- ⚠️ Actualización de contenido: `documentos` vía API, pero el panel de administración es maqueta
  (G-16).
- ⚠️ Evolución del modelo: cuantización/vLLM y fine-tuning futuros documentados (G-15/G-17).