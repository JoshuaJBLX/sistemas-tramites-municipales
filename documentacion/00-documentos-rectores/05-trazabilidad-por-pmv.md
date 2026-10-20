# Trazabilidad por PMV — Estado del desarrollo del proyecto

> Mapa de qué se construyó en qué **PMV** (Producto Mínimo Viable), qué queda por cerrar en cada
> uno y cómo avanza el proyecto hacia los 3 PMV definidos en **04.4**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).
>
> **Porcentajes verificados el 17 de octubre de 2026** sobre 101 puntos de
> comprobación (véase el método en [`02-implementacion-de-historias.md`](./02-implementacion-de-historias.md);
> cifras canónicas en `06-estado-actual-implementado.md` §10).

## Resumen de avance

| Dimensión | Resultado |
|---|---|
| **Avance global de las 18 HU** | **82 %** (83/101 puntos) — verificado 17-oct-2026 |
| **PMV1** · Prototipo funcional | **100 %** (24/24) — 4 HU ✅ |
| **PMV2 · Modelo RAG optimizado** | **100 %** (28/28) ✅ — 5 HU (HU-04, HU-08, HU-10, HU-11, HU-12) |
| **PMV3 · Sistema integrado** | **63 %** (31/49) — 9 HU (HU-01 y HU-02 al 100 %) |
| HU completas al 100 % | 11 / 18 — HU-01, HU-02, HU-04–HU-12 |
| HU iniciadas | 15 / 18 |
| HU sin empezar | 3 / 18 (HU-15, HU-16, HU-18) |
| Pruebas automatizadas | 0 suites |

> Actualizado el **17-oct-2026**: la API arranca con **31 rutas** (20 públicas + 7 admin + 4 doc),
> migraciones `004`/`005`/`006` aplicadas, `tsc` y `next build` OK. Los defectos **D-14..D-23**
> quedaron corregidos el 16-oct y el 17-oct se cerraron **HU-08** (umbral "no inventar", G-04),
> **HU-10** (trazabilidad completa + bloqueo + fuentes con metadatos, D-9), **HU-11** (clasificador
> de dominio) y 2 puntos de **HU-14** (panel de auditoría real). **PMV1 y PMV2 están cerrados
> (100 %)**; solo queda P2-17 (validación SUS, no fabricable) fuera de alcance de código, y PMV3
> concentra seguridad, auditoría, métricas y reportes.

## 1. Definición de los tres PMV (04.4)

| Aspecto | **PMV1** | **PMV2** | **PMV3** |
|---|---|---|---|
| Pregunta clave | ¿El SLM procesa la intención y orienta trámites básicos? | ¿La RAG reduce alucinaciones? | ¿Producto seguro, accesible y de baja latencia? |
| Objetivo | Prototipo funcional | Modelo optimizado con RAG y citas | Sistema integrado desplegable |
| Funcionalidades | Chat + SLM + 5 trámites | RAG 20+ trámites + abstención | API completa + seguridad + UX |
| Arquitectura | Capas local | Hexagonal + pgvector | Hexagonal + Docker + Redis |
| Validación | 15 usuarios | 50 ciudadanos | 100+ / SUS / carga |

## 2. Estado real del repositorio por PMV

### PMV1 — Prototipo funcional (✅ 100 %)
| Componente | Estado | Evidencia |
|---|---|---|
| Chat conversacional | ✅ | `frontend-tramites/app/chat` + `ChatBox`/`ChatThread` |
| SLM local que orienta trámites | ✅ | `Dockerfile` de Ollama (`docker-compose.yml`), `OllamaAdapter` (qwen2.5:3b) |
| Clasificación de intención | ✅ (heurística) | `ServicioNLP` (regex, 6 intenciones) |
| 5 trámites mínimos | ✅ superado | Seeds: **252 procedimientos TUPA** (272 trámites en BD) |
| **PMV1 · Cierre** | ✅ **100 %** (24/24) | HU-05, HU-06, HU-07, HU-09 cerradas (migración 005 + área responsable + SLM) |

### PMV2 — Modelo RAG optimizado (✅ 100 %)
| Componente | Estado | Evidencia |
|---|---|---|
| RAG con búsqueda vectorial | ✅ | `BusquedaVectorialAdapter` (pgvector HNSW, umbral 0.3) |
| 20+ trámites en base documental | ✅ superado | Seeds: **20 documentos** vigentes (`database/seeds/documentos.sql`) |
| Arquitectura hexagonal | ✅ | `backend/domain|application|infrastructure` + DI en `container.py` |
| Citas / fuentes en la respuesta | ✅ | Backend envía `titulo` + `numero` + `fecha` + `version` + `fragmento` (HU-10) y el badge los muestra |
| **Abstención** / fuera de dominio | ✅ (17-oct) | Umbral de rechazo por groundedness (`BLOQUEO_AFIRMACIONES`, G-04) + `ServicioDominio` (HU-11) que deriva a la entidad correspondiente |
| Gestión documental PMV2 (D-14..D-23) | ✅ | Validación de formato (422), metadatos obligatorios, estado `derogado`, baja lógica, chunking (`ServicioChunking` 800/120), reprocesado y **31 rutas servibles**; PDF real → 201 |
| Recuperación por fragmento (G-13) | ✅ | 20/20 documentos fragmentados; `obtenerFragmentos()` por `documento_id` |
| Trámites relacionados (HU-12) | ✅ | `TramiteCatalogoAdapter.relacionados()` (embedding + fallback léxico) + UI |
| Trazabilidad completa (HU-10) | ✅ (17-oct) | `GET /api/consultas/{id}` con respuesta/fuentes/confianza/bloqueo/`fuera_dominio`; `GET /api/consultas` lista; panel `AuditLog` real |
| Validación con 50 ciudadanos | ❌ | P2-17 (sin prueba SUS/reproducibilidad) |

### PMV3 — Sistema integrado desplegable (63 %, infraestructura a medias)
| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600) |
| API completa | ⚠️ | 31 rutas servibles (arranca y responde `/health` 200), pero faltan auth, métricas y reportes |
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
>
> **Reasignación (16-oct-2026):** se elimina la categoría "Transversal" y se distribuye: **HU-11
> (consultas fuera de dominio) → PMV2** y **HU-17 (derivación a atención municipal) → PMV3**.
> **Cifras verificadas el 17-oct-2026:** global **82 %** (83/101).

| PMV | HU | % por HU | Justificación |
|---|---|---|---|
| **PMV1** (**100 %** ✅) | HU-05 · HU-06 · HU-07 · HU-09 | **100** · **100** · **100** · **100 %** | Consulta ciudadana, clasificación, requisitos y respuesta SLM = núcleo del prototipo |
| **PMV2** (**100 %** ✅) | HU-04 · HU-08 · HU-10 · HU-11 · HU-12 | **100** · **100** · **100** · **100** · **100 %** | Procesamiento RAG, costos/plazos (umbral "no inventar"), trazabilidad/bloqueo, consultas fuera de dominio y trámites relacionados |
| **PMV3** (63 %) | HU-01 · HU-02 · HU-03 · HU-13 · HU-14 · HU-15 · HU-16 · HU-17 · HU-18 | **100** · **100** · 86 · 40 · 67 · **0** · **0** · 40 · **0 %** | Gestión documental + usuarios/seguridad + auditoría + métricas + derivación + reportes |

### El dato relevante por PMV

- **PMV1 (100 % ✅, 24/24)** con las 4 HU cerradas: la clasificación de intención
  con confianza y aclaración, el trámite probable, los requisitos verificados contra el catálogo,
  la **derivación al área responsable** (HU-07, migración 005) y la **estructura garantizada de la
  respuesta con derivación al funcionario** (HU-09) funcionan de extremo a extremo.
- **PMV2 (100 % ✅, 28/28)** está cerrado: las 5 HU al 100 % — chunking, OCR, recuperación por
  fragmento, panel de documentos y motor de trámites relacionados (HU-04, HU-12); montos del TUPA
  con umbral "no inventar" (HU-08); trazabilidad completa con bloqueo y fuentes enriquecidas
  (HU-10); clasificador de dominio con derivación (HU-11). **La API arranca con 31 rutas**
  (D-14..D-23 corregidos el 16-oct). Solo queda la **validación SUS (P2-17)**, no fabricable.
- **PMV3 (63 %)** subió porque HU-01 (100 %), HU-02 (100 %), HU-03 (86 %) y **HU-14 (67 %)**
  recogieron el avance del PMV2 documental y de la trazabilidad; incluye **HU-17 (40 %)**
  —derivación con solo una nota genérica—; aún **3 de sus 9 HU están en 0 %** (HU-15
  retroalimentación, HU-16 métricas y HU-18 reportes), y las otras siguen en estado parcial
  (auth, búsqueda de auditoría, reportes…).

## 5. Catálogo G-XX por PMV bloqueado

| Bloquea | Vacíos |
|---|---|
| **PMV1** | — (ninguno crítico; prototipo funcional) |
| **PMV2** | ~~G-04~~ ✅ cerrado (17-oct-2026); G-14 (consistencia de campos de trámite), G-21 (dataset ✅ hecho, faltan resultados); ~~G-08~~ ✅ y ~~G-13~~ ✅ cerrados el 16-oct-2026 |
| **PMV3** | G-01 (auth), G-20 (guardrails), G-16 (métricas), G-18 (pytest), G-23 (rate limit), G-26 (accesibilidad/carga), G-05 (feedback), G-07 (reportes), G-09 (derivación), G-11/G-10 (rutas UI) |

## 6. Ubicación actual del avance

Estricto a la definición de 04.4 y contrastado con el código:

- **Funcional:** el repositorio **cierra el PMV1 (100 %)** y **PMV2 (100 %)** — el RAG con
  fuentes citadas opera, la abstención y el rechazo por groundedness baja también (G-04), el
  clasificador de dominio deriva a la entidad correspondiente (HU-11), el ciclo documental (carga →
  OCR → chunking → aprobación con metadatos → fragmentos) fue verificado de extremo a extremo con un
  PDF real del TUPA, y el motor de trámites relacionados responde (HU-12 ✅). **La API arranca con
  31 rutas** (D-14..D-23 corregidos el 16-oct-2026).
- **Medido:** PMV1 **100 %** (24/24) · PMV2 **100 %** (28/28) · PMV3 **63 %** (31/49) · global
  **82 %** (83/101). Ningún PMV adicional llega al 100 % porque el alcance incluye
  autenticación, métricas, reportes y validación SUS que aún no existen.
- **Infraestructura:** la capa de **PMV3** está parcialmente adelantada en el repo (Docker Compose,
  Redis, API completa ya existen), pero eso no se refleja en el avance funcional de sus HU.
- **Pendiente para cerrar PMV2:** solo la **validación SUS con 50 ciudadanos (P2-17)** (actividad
  real, no de código).
- **Pendiente para PMV3:** seguridad (G-01/G-20), búsqueda de auditoría por filtros (HU-14),
  métricas (G-16), pruebas (G-18/G-26), feedback (G-05), reportes (G-07) y derivación (G-09). De
  los defectos, **D-1..D-5, D-9, D-10, D-14..D-23 están corregidos**; D-6, D-7, D-12 son parciales;
  D-8 y D-11 siguen abiertos; D-13 es menor.

## 7. Ruta de cierre sugerida (por PMV)

1. ~~**Corrección inmediata (antes que funcionalidad nueva):** subir el timeout del front, eliminar
   el fallback `respuestaDemo()` (**D-1**), enviar `groundedness` real (**D-2**) y alinear el contrato
   de fuentes (**D-3**)~~ — **hecho**: D-1 a D-5 corregidos y verificados contra la API en ejecución.
2. ~~**Cerrar PMV2:** D-14..D-23, montos del TUPA, HU-12, dataset PoC, HU-11, G-04, HU-08 y HU-10~~
   — **hecho** (16 y 17-oct-2026): API con 31 rutas, 20/20 documentos con metadatos y fragmentados,
   HU-12 ✅, `dataset-poc.csv` (200 consultas), umbral de rechazo (G-04), clasificador de dominio
   (HU-11), "no inventar" (HU-08) y trazabilidad completa (HU-10). **PMV2 = 100 % ✅.** Queda solo
   **P2-17 (validación SUS)**.
3. **Avanzar PMV3 (63 %), bloque 1:** pytest del flujo RAG (G-18) y autenticación JWT + roles (G-01).
4. **Avanzar PMV3, bloque 2:** endpoint de métricas (G-16) y guardrails anti prompt-injection (G-20).
5. **Validación final:** pruebas de carga (k6) + auditoría WCAG + SonarQube (G-26) y medición de
   latencia < 3 s.

## 8. Proyección si se cierra lo pendiente

| Escenario | Avance estimado |
|---|---|
| Estado 16-oct-2026 (verificado) | **72 %** |
| ~~+ corregir D-1..D-5 (datos falsos en el chat)~~ | ~~42 %~~ — **superado** |
| ~~+ corregir D-14..D-23 (la API arranca y el PMV2 es desplegable)~~ | ~~habilita medir lo ya construido~~ — **superado** |
| ~~+ cerrar HU-11 y G-04 (abstención), HU-08 y HU-10~~ | — **superado (17-oct-2026): PMV2 = 100 %** |
| **Estado actual (17-oct-2026, verificado)** | **82 %** |
| + autenticación, métricas y pytest | ~91 % |
| + retroalimentación, reportes y validación SUS | ~97–100 % |

