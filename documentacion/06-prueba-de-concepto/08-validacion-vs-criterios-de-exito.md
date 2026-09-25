# 06.8 — Validación de la Solución (vs Criterios de Éxito)

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Validación cuantitativa (a.md 19.8)
| Criterio | Evidencia en el repo |
|---|---|
| Groundedness ≥ 0.8 (o 80%) | ⚠️ Confianza cualitativa (alta/media/baja) sin puntaje numérico (G-16) |
| Latencia > 3 s mejora | ❌ Sin medición (G-16) |
| Fuentes citadas | ✅ `url` + `fragmento` (limitación: sin artículo/página — G-13) |
| IPC > 100 dentro de 1 hora (PoC informal) | ❌ No instrumentado (G-21) |

## Validación cualitativa (tabla a.md)
- ⚠️ Sujetividad/interpretación del evaluador: sin rúbricas versionadas (G-21).

## Validación estadística (t-test pareados, ANOVA, correlación)
- ❌ Sin scripts estadísticos ni dataset de resultados (G-16/G-21).

## Conclusión del estado actual
- La solución del repo **es validable** (API, confianza, fuentes) pero **carece de la evidencia
  numérica** que exige la PoC (G-16/G-21).