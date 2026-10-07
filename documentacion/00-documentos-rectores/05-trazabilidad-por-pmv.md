# Trazabilidad por PMV — Estado del desarrollo del proyecto

> Mapa de qué se construyó en qué **PMV** (Producto Mínimo Viable), qué queda por cerrar en cada
> uno y cómo avanza el proyecto hacia los 3 PMV definidos en **04.4**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).
>
> **Porcentajes verificados el 1 de octubre de 2026** sobre 101 puntos de comprobación
> (véase el método en [`02-implementacion-de-historias.md`](./02-implementacion-de-historias.md)).

## Resumen de avance

| Dimensión | Resultado |
|---|---|
| **Avance global de las 18 HU** | **49 %** (49/101 puntos) |
| **PMV1 | 100 % (24/24) — 4 HU |
| **PMV2 · Modelo RAG optimizado** | **44 %** (11/25) — 4 HU |
| **PMV3 · Sistema integrado** | **34 %** (15/44) — 8 HU |
| **Transversal** (fuera de dominio, derivación) | **25 %** (2/8) — 2 HU |
| HU completas al 100 % | 2 / 18 — HU-05, HU-06 |
| HU iniciadas | 13 / 18 |
| HU sin empezar | 5 / 18 (HU-11, HU-12, HU-15, HU-16, HU-18) |
| Pruebas automatizadas | 0 suites |

> Los tres PMV están **por debajo del 100 %** porque el avance se mide contra el alcance completo de
> las historias (que incluye versionado, chunking, OCR, seguridad, métricas y reportes), no solo
> contra la demo. El **núcleo conversacional RAG funciona de extremo a extremo**.

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
| Citas / fuentes en la respuesta | ⚠️ | `FuenteCitada` existe, pero el front no las muestra: backend devuelve `{url, fragmento}` y el badge lee `f.titulo` (**D-3**) |
| **Abstención** cuando falta contexto | ❌ | G-04 (hoy responde genérico; no se abstiene) |
| Validación con 50 ciudadanos | ❌ | G-26 (sin prueba SUS/reproducibilidad) |

### PMV3 — Sistema integrado desplegable (⚠️ infraestructura a medias)
| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600) |
| API completa | ✅ | Controllers /api/consultas, /api/tramites, /api/documentos, /api/usuarios, /health |
| Seguridad (login, roles, guardrails) | ❌ | G-01 (auth/JWT) y G-20 (anti prompt-injection); `es_administrador()` existe pero nunca se invoca (**D-8**) |
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
> Los **% por HU** son los verificados en el documento 02.

| PMV | HU | % por HU | Justificación |
|---|---|---|---|
| **PMV1 | 100 %) | HU-05 · HU-06 · HU-07 · HU-09 | **100** · **100** · 80 · 60 % | Consulta ciudadana, clasificación, requisitos y respuesta SLM = núcleo del prototipo |
| **PMV2** (44 %) | HU-04 · HU-08 · HU-10 · HU-12 | 44 · 60 · 50 · **0 %** | Procesamiento RAG, costos/plazos, trazabilidad y trámites relacionados |
| **PMV3** (34 %) | HU-01 · HU-02 · HU-03 · HU-13 · HU-14 · HU-15 · HU-16 · HU-18 | 44 · 50 · 43 · 40 · 33 · **0** · **0** · **0 %** | Gestión documental + usuarios/seguridad + auditoría + métricas + reportes |
| **Transversal** (25 %) | HU-11 · HU-17 | **0** · 40 % | Fuera de dominio y derivación (dependen de G-04 en PMV2/3) |

### El dato relevante por PMV

- **PMV1 | 100 %)** con **HU-05 y HU-06 al 100 %**: la clasificación de intención
  con confianza y aclaración, el trámite probable y los requisitos verificados contra el catálogo
  funcionan de extremo a extremo. Quedan pendientes la derivación al área responsable (HU-07) y la
  estructura garantizada de la respuesta (HU-09).
- **PMV2 (44 %)** arrastra a **HU-12 = 0 %**: el motor de trámites relacionados no existe, así que
  uno de los cuatro pilares del PMV2 no ha empezado. HU-08 quedó en 60 % porque el chat ya usa
  `costo` y `duracion_estimada_dias`, pero los montos del TUPA no están cargados en la base de datos.
- **PMV3 (34 %)** es el que más trabajo tiene: **3 de sus 8 HU están en 0 %** (HU-15 retroalimentación,
  HU-16 métricas y HU-18 reportes), y las otras 5 siguen en estado parcial.
- **Transversal (25 %)**: HU-11 sin clasificador de dominio y HU-17 solo con una nota genérica.

## 5. Catálogo G-XX por PMV bloqueado

| Bloquea | Vacíos |
|---|---|
| **PMV1** | — (ninguno crítico; prototipo funcional) |
| **PMV2** | G-04 (abstención), G-08 (relacionados), G-13 (chunking), G-21 (artefactos PoC) |
| **PMV3** | G-01 (auth), G-20 (guardrails), G-16 (métricas), G-18 (pytest), G-23 (rate limit), G-26 (accesibilidad/carga) |
| Transversal | G-05 (feedback), G-07 (reportes), G-09 (derivación), G-11/G-10 (rutas UI), G-14 (consistentación campos) |

## 6. Ubicación actual del avance

Estricto a la definición de 04.4 y contrastado con el código:

- **Funcional:** el repositorio está **en PMV1 | 100 %)** y entrando en PMV2 — el RAG con 20+
  trámites y fuentes citadas ya opera, y ahora también la abstención (G-04): el asistente pide
  aclaración cuando la consulta es ambigua y se abstiene cuando no encuentra documentos oficiales.
- **Medido:** PMV1 | 100 %** · PMV2 **44 %** · PMV3 **34 %** · global **49 %**.
  Ningún PMV llega al 100 % porque el alcance de las historias incluye versionado documental,
  chunking, OCR, autenticación, métricas y reportes que aún no existen.
- **Infraestructura:** la capa de **PMV3** está parcialmente adelantada en el repo (Docker Compose,
  Redis, API completa ya existen), pero eso no se refleja en el avance funcional de sus HU.
- **Pendiente prioritario para declarar PMV2 cerrado:** **HU-12 (trámites relacionados) al 0 %**,
  G-21 (dataset y resultados de la PoC) y **cargar los montos reales del TUPA** en `tramites.costo`,
  hoy en 0.00, que es lo que impide cerrar HU-08.
- **Pendiente para PMV3:** seguridad (G-01/G-20), métricas (G-16), pruebas (G-18/G-26) y validación
  con usuarios (SUS). Los defectos **D-1 a D-5** del documento 02 ya están corregidos; quedan D-6
  (panel admin como maqueta), D-7 (upload sin validación) y D-8 (autorización sin usar).

## 7. Ruta de cierre sugerida (por PMV)

1. ~~**Corrección inmediata (antes que funcionalidad nueva):** subir el timeout del front, eliminar
   el fallback `respuestaDemo()` (**D-1**), enviar `groundedness` real (**D-2**) y alinear el contrato
   de fuentes (**D-3**)~~ — **hecho**: D-1 a D-5 corregidos y verificados contra la API en ejecución.
2. **Cerrar PMV2 (44 %):** cargar los montos reales del TUPA en `tramites.costo` → **HU-12 trámites
   relacionados (0 %)** → dataset de consultas sintéticas y resultados (G-21).
3. **Avanzar PMV3 (34 %), bloque 1:** pytest del flujo RAG (G-18) y autenticación JWT + roles (G-01).
4. **Avanzar PMV3, bloque 2:** endpoint de métricas (G-16) y guardrails anti prompt-injection (G-20).
5. **Validación final:** pruebas de carga (k6) + auditoría WCAG + SonarQube (G-26) y medición de
   latencia < 3 s.

## 8. Proyección si se cierra lo pendiente

| Escenario | Avance estimado |
|---|---|
| Estado actual | **49 %** |
| ~~+ corregir D-1..D-4 (datos falsos en el chat)~~ | ~~42 %~~ — **superado** |
| + cargar montos del TUPA y abstención ya hecha | ~52 % |
| + autenticación, métricas y pytest | ~62 % |
| + retroalimentación, reportes y validación SUS | ~75–80 % |

