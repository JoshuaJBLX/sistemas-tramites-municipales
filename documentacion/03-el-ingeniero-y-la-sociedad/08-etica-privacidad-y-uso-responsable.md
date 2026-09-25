# 03.8 — Ética, Privacidad y Uso Responsable de TI (Dilemas)

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Dilemas en el uso de IA
| Dilema | Riesgo | Mitigación implementada |
|---|---|---|
| Alucinación y desinformación | Requisitos/montos/plazos incorrectos → perjuicio económico o pérdida de plazos | ⚠️ RAG + confianza alta/media/baja; ❌ sin abstención (G-04) |
| Sesgo algorítmico | Modismos regionales mal interpretados | ⚠️ Normalización + patrones léxicos; ❌ sin ML entrenado (G-02) |
| Privacidad (PII) | Ciudadanos ingresan datos sensibles por error | ❌ Sin enmascaramiento (G-03); ✅ no se almacenan |
| Opacidad vs. explicabilidad | Sin norma citada no hay auditoría | ⚠️ Fuentes `url`+`fragmento` (❌ artículo/página G-13) |
| Sustitución indebida | Un sistema que "interpreta" normas con discrecionalidad | ✅ Aviso de orientación (⚠️ G-25); derivación humana (⚠️ G-09) |

## Principios aplicados
- Beneficencia: ✅ orientación gratuita y verificable.
- No maleficencia: ⚠️ mitigación de alucinaciones parcial.
- Transparencia: ⚠️ fuentes visibles; falta explicabilidad completa.
- Privacidad: ✅ minimización de datos.
- Responsabilidad: ⚠️ pendiente trazabilidad de decisiones del modelo (G-16).