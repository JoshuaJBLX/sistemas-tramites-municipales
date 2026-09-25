# 01.6 — Formulación del Problema

> Parte de **01 — Análisis del Problema**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 6.1 Problema general
"La desorientación ciudadana y el elevado tiempo de atención de consultas sobre trámites
municipales en la Municipalidad Provincial de Junín" (en a.md: Huancayo/MPH).

## 6.2 Problemas específicos (PE1-PE8)
| PE | Descripción |
|---|---|
| PE1 | Falta de canal único y accesible |
| PE2 | Documentos con lenguaje técnico complejo |
| PE3 | Sin mecanismo de verificación de respuestas |
| PE4 | Personal dedica tiempo a consultas básicas |
| PE5 | Expedientes incompletos |
| PE6 | Sin trazabilidad de consultas |
| PE7 | Sin herramientas de actualización |
| PE8 | Información sin verificación de fuentes |

## 6.3 Correspondencia problemas - objetivos
| PE | Objetivo | Solución |
|---|---|---|
| PE1 | OE1 | Asistente web en lenguaje natural (✅) |
| PE2 | OE2 | SLM traduce lenguaje técnico (✅ parcial, G-04) |
| PE3 | OE3 | Módulo de groundedness (⚠️ confianza cualitativa) |
| PE4 | OE4 | Automatización de consultas básicas (✅ RAG+SLM) |
| PE5 | OE5 | Guía con requisitos completos (⚠️ desde contexto, sin abstención G-04) |
| PE6 | OE6 | Trazabilidad (✅ tabla `auditoria_consultas`) |
| PE7 | OE7 | Panel administrativo (⚠️ maqueta G-16) |
| PE8 | OE8 | Citación de fuentes (✅ url+fragmento; ❌ sin artículo/página G-13) |

## 6.4 Coherencia entre problemas y solución propuesta
- La solución (asistente SLM + RAG) ataca directamente PE1-PE6 y parcialmente PE7-PE8.

## Vacíos asociados
- ❌ G-04 (verificación con rechazo), ❌ G-13 (fuentes completas), ❌ G-16 (panel funcional).