# 05.10 — Métricas Objetivo y Desempeño de Herramientas

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Métricas objetivo (a.md 17.4)
| Categoría | Métrica | Meta |
|---|---|---|
| Costo | COCOMO (SLOC) | Presupuesto/KLDC |
| Utilización de recursos | CPU/RAM | < 70% |
| Latencia | p95 de respuestas | < 3.0 s |
| Productividad | Puntos de historia/sprint | ↑ |
| Precisión | F1 reach | → 1 |
| Alcance | N.º trámites atendidos | TUPA 252 |

## Desempeño instrumentado en el código
| Métrica | Instrumentación real |
|---|---|
| Latencia | ❌ Sin métricas/trazas (G-16) |
| CPU/RAM | ❌ Sin monitoreo (G-16) |
| F1 | ❌ Sin dataset de validación (G-21) |
| Recursos de infraestructura | ⚠️ Estimable desde `docker-compose.yml` |
| Costo (SLOC) | ⚠️ Estimable por líneas del repo |

## Conclusiones
- Las metas existen en a.md, pero **no hay instrumentación** para verificarlas en este punto
  (G-16/G-21/G-26).