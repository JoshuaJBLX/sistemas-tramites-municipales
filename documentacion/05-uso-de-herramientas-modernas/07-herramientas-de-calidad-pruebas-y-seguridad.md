# 05.7 — Herramientas de Calidad, Pruebas y Seguridad

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Calidad / Testing
| Herramienta | Uso | Estado real |
|---|---|---|
| pytest | Pruebas unitarias/integración | ❌ No instalado (G-18) |
| Pydantic (validación) | Contratos de API | ✅ Ya activo |
| Pruebas manuales vía HTTP | Smoke del backend | ⚠️ README/EJECUCION |
| SonarQube | Calidad/cobertura | ❌ (G-26) |
| OWASP ZAP | Pentest | ❌ (G-26) |

## Seguridad
| Herramienta | Uso | Estado real |
|---|---|---|
| JWT/roles | Autenticación admin | ❌ (G-01) |
| Guardrails (prompt injection) | Protección del SLM | ❌ (G-20) |
| Rate limiting | Anti-abuso | ❌ (G-23) |
| Enmascaramiento PII | Privacidad | ❌ (G-03) |
| SQL parametrizado | Prevención inyección | ✅ asyncpg |

## Validación del modelo
| Indicador | Implementación |
|---|---|
| Groundedness (confianza) | ✅ `EvaluadorGroundedness.py` (alta/media/baja) |
| Abstención cuando no hay respaldo | ❌ (G-04) |
| Métricas formalizadas | ❌ (G-16) |