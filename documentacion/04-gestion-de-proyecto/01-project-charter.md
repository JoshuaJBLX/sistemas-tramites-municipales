# 04.1 — Project Charter

> Parte de **04 — Gestión de Proyecto** (a.md "4.Gestiòn de Proyecto.docx", PMI/Scrum).
> Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Project details
| Elemento | Descripción |
|---|---|
| Necesidad/objetivo | Reducir desorientación y demoras en trámites municipales (MPJ, TUPA 2023, 252 procedimientos) |
| Requisitos del proyecto | Asistente SLM + RAG, fuentes oficiales, trazabilidad, bajo costo |
| Descripción del producto/entregables | Frontend funcional · Backend (lógica de negocio) · BD persistente · Integración IA/API |
| El proyecto no incluye | Producción municipal, mesa de partes, WhatsApp, automatización de trámites, PII |
| Recursos preasignados | 5 integrantes académicos, hardware propio, software open source |

## Lista de partes interesadas
Ciudadanos · funcionarios municipales · comité académico/jurado · equipo de desarrollo.

## Resumen del cronograma de hitos
| Hito | Ventana |
|---|---|
| H1 | 17-23 ago 2026 |
| H2 | 24-30 ago 2026 |
| H3 | 31 ago – 20 sep 2026 |
| H4 | 21 sep – 11 oct 2026 |
| H5 | 12-26 oct 2026 |

## Consideraciones del proyecto
- **Riesgos de alto nivel (10):** datos TUPA ambiguos, alucinaciones, latencia, prompt injection,
  continuidad de equipo, cuotas GPU, dataset reducido, frametime, dependencias, alcance.
- **Criterios de aceptación:**
  1. Funcionales: consultas en lenguaje natural, citas de fuente, abstención/aclaraciones.
  2. Rendimiento IA: groundedness, cero alucinaciones, latencia aceptable.
  3. Seguridad: enmascaramiento PII, accesibilidad móvil.
- **Supuestos:** TUPA públicos, participación de funcionarios, accesos móviles, idioma español,
  uso orientativo.
- **Restricciones:** solo Junín, sin resolución formal de trámites, sin PII, alcance académico.

## Estado real
- ✅ Se cumplen los entregables del charter en el repositorio (frontend, backend, BD, IA).
- ⚠️ Criterios de aceptación: funcionales parciales (falta abstención G-04), IA sin métricas
  (G-16), seguridad sin auth/PII (G-01/G-03).