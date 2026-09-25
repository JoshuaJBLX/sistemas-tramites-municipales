# 03.10 — Análisis de Impactos de la Solución

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Matriz de impactos
| Dimensión | Impacto esperado | Estado en el sistema |
|---|---|---|
| Social | Menos desorientación, más confianza | ✅ Canal funcionando; ⚠️ sin medición |
| Económica | Menos traslados/espera; ahorro municipal | ✅ Apalancado; ⚠️ sin cuantificar |
| Ambiental | Menos papel y cómputo en nube | ✅ SLM local |
| Seguridad | Nuevos vectores (prompt injection, PII) | ⚠️ Validación básica; ❌ sin guardrails (G-20) |
| Privacidad | Riesgo de PII en chats | ⚠️ No se persisten; ❌ sin enmascaramiento (G-03) |
| Ética | Alucinaciones/sesgos/opacidad | ⚠️ RAG + confianza; ❌ abstención (G-04) |
| Legal | Información no vinculante | ⚠️ Aviso legal UI (G-25) |

## Matriz poder/interés de impactos (información)
- Impacto alto con poder bajo (ciudadanos) → proteger con usabilidad y abstención.
- Impacto alto con poder alto (jurado) → evidencias y métricas (pendientes G-16).