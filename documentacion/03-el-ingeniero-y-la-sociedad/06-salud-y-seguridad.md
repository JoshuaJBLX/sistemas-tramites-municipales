# 03.6 — Salud y Seguridad

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Seguridad de la Información (confidencialidad)
| Riesgo | Medida | Estado |
|---|---|---|
| Ingreso accidental de PII (DNI, teléfono, dirección) | Enmascaramiento regex/NLU | ❌ G-03 |
| Exposición de PII en BD/logs | Minimización (no se registran PII) | ✅ |
| Acceso no autorizado | Autenticación/JWT/roles | ❌ G-01 |

## Integridad del servicio (anti-hacking / inyección)
| Riesgo | Medida | Estado |
|---|---|---|
| Prompt injection | Guardrails de entrada | ❌ G-20 |
| Inyección SQL | Consultas parametrizadas (asyncpg) | ✅ |
| Entrada malformada | Validación Pydantic (min_length, email, regex) | ✅ |

## Disponibilidad y continuidad operacional
| Riesgo | Medida | Estado |
|---|---|---|
| Caída del servicio | Health check `/health` | ✅ |
| Saturación (DoS) | Rate limiting | ❌ G-23 |
| Escalado | Escalado horizontal/balanceador | ❌ G-17 |

## Salud y ergonomía digital
| Riesgo | Medida | Estado |
|---|---|---|
| Fatiga visual | Diseño cálido, alto contraste, tipografía legible | ✅ |
| Sobrecarga de texto | Respuestas resumidas con viñetas | ⚠️ (depende del SLM) |
| Accesibilidad | Modo claro/oscuro, tamaño de fuente | ❌ sin auditoría WCAG (G-26) |