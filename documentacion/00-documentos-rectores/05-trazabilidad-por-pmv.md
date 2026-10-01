# Trazabilidad por PMV — Estado del desarrollo del proyecto

> Mapa de qué se construyó en qué **PMV** (Producto Mínimo Viable), qué queda por cerrar en cada
> uno y cómo avanza el proyecto hacia los 3 PMV definidos en **04.4**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 1. Definición de los tres PMV (04.4)

| Aspecto | **PMV1** | **PMV2** | **PMV3** |
|---|---|---|---|
| Pregunta clave | ¿El SLM procesa la intención y orienta trámites básicos? | ¿La RAG reduce alucinaciones? | ¿Producto seguro, accesible y de baja latencia? |
| Objetivo | Prototipo funcional | Modelo optimizado con RAG y citas | Sistema integrado desplegable |
| Funcionalidades | Chat + SLM + 5 trámites | RAG 20+ trámites + abstención | API completa + seguridad + UX |
| Arquitectura | Capas local | Hexagonal + pgvector | Hexagonal + Docker + Redis |
| Validación | 15 usuarios | 50 ciudadanos | 100+ / SUS / carga |

## 2. Estado real del repositorio por PMV

### PMV1 — Prototipo funcional (✅ casi completo)
| Componente | Estado | Evidencia |
|---|---|---|
| Chat conversacional | ✅ | `frontend-tramites/app/chat` + `ChatBox`/`ChatThread` |
| SLM local que orienta trámites | ✅ | `Dockerfile` de Ollama (`docker-compose.yml`), `OllamaAdapter` (qwen2.5:3b) |
| Clasificación de intención | ✅ (heurística) | `ServicioNLP` (regex, 6 intenciones) |
| 5 trámites mínimos | ✅ superado | Seeds: **22 trámites** TUPA 2023 (`database/seeds/tramites.sql`) |

### PMV2 — Modelo RAG optimizado (🟠 mayormente listo)
| Componente | Estado | Evidencia |
|---|---|---|
| RAG con búsqueda vectorial | ✅ | `BusquedaVectorialAdapter` (pgvector HNSW, umbral 0.3) |
| 20+ trámites en base documental | ✅ superado | Seeds: **20 documentos** vigentes (`database/seeds/documentos.sql`) |
| Arquitectura hexagonal | ✅ | `backend/domain|application|infrastructure` + DI en `container.py` |
| Citas / fuentes en la respuesta | ✅ | `FuenteCitada` + `GroundednessBadge` en el chat |
| **Abstención** cuando falta contexto | ❌ | G-04 (hoy responde genérico; no se abstiene) |
| Validación con 50 ciudadanos | ❌ | G-26 (sin prueba SUS/reproducibilidad) |

### PMV3 — Sistema integrado desplegable (⚠️ infraestructura a medias)
| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600) |
| API completa | ✅ | Controllers /api/consultas, /api/tramites, /api/documentos, /api/usuarios, /health |
| Seguridad (login, roles, guardrails) | ❌ | G-01 (auth/JWT) y G-20 (anti prompt-injection) |
| Accesibilidad y pruebas de carga | ❌ | G-26 (WCAG, k6/JMeter, SonarQube, ZAP) |
| Latencia < 3 s medible | ⚠️ | Caché ✅; sin métricas de latencia (G-16) |

## 3. Backlog prioritario (a.md 5.2) → estado real

| Historia (a.md) | PMV | Estado | Brecha |
|---|---|---|---|
| HU-01 Consultar requisitos | PMV1 | ⚠️ | Parcial (desde contexto RAG; no lista estructurada garantizada) |
| HU-02 Costos y plazos | PMV1 | ⚠️ | Desajuste `tipo`/`duracion_estimada_dias` ↔ `categoria`/`plazo` (G-14) |
| HU-03 Consultar base vectorial de normas | PMV2 | ✅ | RAG implementado |
| HU-04 Calificar respuesta | PMV2 | ❌ | G-05 (sin tabla de evaluaciones ni UI) |
| HU-05 Filtro de entradas | PMV3 | ⚠️ | Pydantic ✅; guardrails ❌ (G-20) |
| HU-06 Respuesta < 3 s | PMV3 | ⚠️ | Caché ✅; sin medición (G-16) |

## 4. Distribución TENTATIVA de las 18 HU por PMV

> Las 18 HU del documento 02 no tienen PMV asignado explícito; esta tabla propone uno coherente
> con los objetivos de cada PMV (validable en la planificación de sprints, 04.5).

| PMV | HU | Justificación |
|---|---|---|
| **PMV1** | HU-05, HU-06, HU-07, HU-09 | Consulta ciudadana, clasificación, requisitos y respuesta SLM = núcleo del prototipo |
| **PMV2** | HU-04, HU-08, HU-10, HU-12 | Procesamiento RAG, costos/plazos, trazabilidad y trámites relacionados |
| **PMV3** | HU-01, HU-02, HU-03, HU-13, HU-14, HU-15, HU-16, HU-18 | Gestión documental + usuarios/seguridad + auditoría + métricas + reportes |
| Transversal | HU-11, HU-17 | Fuera de dominio y derivación (dependen de G-04 en PMV2/3) |

## 5. Catálogo G-XX por PMV bloqueado

| Bloquea | Vacíos |
|---|---|
| **PMV1** | — (ninguno crítico; prototipo funcional) |
| **PMV2** | G-04 (abstención), G-08 (relacionados), G-13 (chunking), G-21 (artefactos PoC) |
| **PMV3** | G-01 (auth), G-20 (guardrails), G-16 (métricas), G-18 (pytest), G-23 (rate limit), G-26 (accesibilidad/carga) |
| Transversal | G-05 (feedback), G-07 (reportes), G-09 (derivación), G-11/G-10 (rutas UI), G-14 (consistentación campos) |

## 6. Ubicación actual del avance

Estricto a la definición de 04.4 y contrastado con el código:

- **Funcional:** el repositorio está **entre PMV1 (cerrado) y PMV2 (funcionalmente listo)** — el
  RAG con 20+ trámites y fuentes citadas ya opera; falta la **abstención** (G-04) y la validación.
- **Infraestructura:** la capa de **PMV3** está parcialmente adelantada en el repo (Docker Compose,
  Redis, API completa ya existen).
- **Pendiente prioritario para declarar PMV2 cerrado:** G-04 (abstención/rechazo) y G-21
  (dataset y resultados de la PoC).
- **Pendiente para PMV3:** seguridad (G-01/G-20), métricas (G-16), pruebas (G-18/G-26) y validación
  con usuarios (SUS).

## 7. Ruta de cierre sugerida (por PMV)

1. **Cerrar PMV2:** implementar abstención por umbral de groundedness (G-04) → añadir el dataset de
   consultas sintéticas y resultados (G-21) → documentar validación con ~50 consultas.
2. **Avanzar PMV3 (bloque 1):** pytest del flujo RAG (G-18) y autenticación JWT + roles (G-01).
3. **Avanzar PMV3 (bloque 2):** endpoint de métricas (G-16) y guardrails anti prompt-injection (G-20).
4. **Validación final:** pruebas de carga (k6) + auditoría WCAG + SonarQube (G-26) y medición de
   latencia < 3 s.