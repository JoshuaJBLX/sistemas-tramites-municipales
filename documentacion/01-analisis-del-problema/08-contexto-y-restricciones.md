# 01.8 — Contexto y Restricciones

> Parte de **01 — Análisis del Problema**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 8.1 Matriz de restricciones y su estado
| Tipo | Restricción | Nivel | Estado en el sistema |
|---|---|---|---|
| Económicas | Presupuesto limitado | Alto | ✅ Código abierto + SLM local |
| Económicas | Personal especializado limitado | Alto | ✅ Equipo académico con roles |
| Tecnológicas | GPU para inferencia | Medio | ⚠️ Ollama CPU por defecto; GPU comentada en compose |
| Tecnológicas | Almacenamiento índices vectoriales | Bajo | ✅ pgvector en PostgreSQL |
| Infraestructura | Conectividad variable | Medio | ✅ Interfaz ligera + demo offline (`lib/api.ts`) |
| Interoperabilidad | APIs municipales no disponibles | Alto | ✅ Sin integración; info pública |
| Seguridad | Exposición de PII | Alto | ⚠️ No se persisten PII; ❌ sin enmascaramiento (G-03) |
| Privacidad | Ley 29733 | Alto | ✅ Minimización de datos |
| Accesibilidad | Baja alfabetización digital | Medio | ✅ Lenguaje claro |
| Accesibilidad | Discapacidad | Medio | ❌ sin auditoría WCAG (G-26) |
| Legales | Info oficial validada | Alto | ✅ Aviso de orientación (⚠️ G-25 en API) |
| Legales | Propiedad intelectual | Medio | ✅ Citación `url_origen` |
| Sostenibilidad | Mantenimiento/actualización | Medio | ⚠️ Panel maqueta (G-16) |
| Sostenibilidad | Consumo energético | Bajo | ✅ SLM cuantizable y local |
| Organizacionales | Resistencia al cambio | Medio | — (documental) |
| Organizacionales | Burocracia para acceso a info | Alto | ✅ Trabajo con info pública |
| Tiempo | Plazo académico | Alto | ✅ Alcance acotado |
| Tiempo | Entrenamiento ML | Medio | ⚠️ Sin fine-tuning (G-15) |
| Usuarios | Nivel educativo variable | Alto | ✅ Respuestas en lenguaje natural |
| Usuarios | Diversidad de perfiles | Medio | ✅ Múltiples formatos (UI) |

## 8.2 Análisis de riesgos y condiciones
- Riesgo principal atendido: información desactualizada → control de `estado='vigente'` en la
  búsqueda (✅).
- Condiciones no resueltas: medición (G-16), pruebas (G-18), seguridad de acceso (G-01).

## 8.3 Condiciones de desarrollo sostenible
- SLM local = menor huella de cómputo vs. LLMs en nube (✅).
- Actualización sostenible: panel administrativo pendiente (⚠️ G-16).