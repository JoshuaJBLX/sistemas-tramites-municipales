# Trazabilidad por PMV — Estado del desarrollo del proyecto

> Mapa de qué se construyó en qué **PMV** (Producto Mínimo Viable), qué queda por cerrar en cada
> uno y cómo avanza el proyecto hacia los 3 PMV definidos en **04.4**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).
>
> **Porcentajes verificados el 16 de octubre de 2026** (HEAD `ea06c9a`) sobre 101 puntos de
> comprobación (véase el método en [`02-implementacion-de-historias.md`](./02-implementacion-de-historias.md);
> cifras canónicas en `06-estado-actual-implementado.md` §10).

## Resumen de avance

| Dimensión | Resultado |
|---|---|
| **Avance global de las 18 HU** | **59 %** (60/101 puntos) |
| **PMV1** · Prototipo funcional | **88 %** (21/24) — 4 HU |
| **PMV2 · Modelo RAG optimizado** | **50 %** (14/28) — 5 HU |
| **PMV3 · Sistema integrado** | **51 %** (25/49) — 9 HU |
| HU completas al 100 % | 2 / 18 — HU-05, HU-06 |
| HU iniciadas | 13 / 18 |
| HU sin empezar | 5 / 18 (HU-11, HU-12, HU-15, HU-16, HU-18) |
| Pruebas automatizadas | 0 suites |

> Ningún PMV está al 100 % porque el avance se mide contra el alcance completo de las historias
> (que incluye OCR, recuperación por fragmento, seguridad, métricas y reportes; el versionado y el
> chunking ya existen en código). El **núcleo conversacional RAG funciona de extremo a extremo**,
> pero el HEAD actual no arranca la API por los defectos bloqueantes **D-14..D-21**.

## 1. Definición de los tres PMV (04.4)

| Aspecto | **PMV1** | **PMV2** | **PMV3** |
|---|---|---|---|
| Pregunta clave | ¿El SLM procesa la intención y orienta trámites básicos? | ¿La RAG reduce alucinaciones? | ¿Producto seguro, accesible y de baja latencia? |
| Objetivo | Prototipo funcional | Modelo optimizado con RAG y citas | Sistema integrado desplegable |
| Funcionalidades | Chat + SLM + 5 trámites | RAG 20+ trámites + abstención | API completa + seguridad + UX |
| Arquitectura | Capas local | Hexagonal + pgvector | Hexagonal + Docker + Redis |
| Validación | 15 usuarios | 50 ciudadanos | 100+ / SUS / carga |

## 2. Estado real del repositorio por PMV

### PMV1 — Prototipo funcional (✅ 88 %)
| Componente | Estado | Evidencia |
|---|---|---|
| Chat conversacional | ✅ | `frontend-tramites/app/chat` + `ChatBox`/`ChatThread` |
| SLM local que orienta trámites | ✅ | `Dockerfile` de Ollama (`docker-compose.yml`), `OllamaAdapter` (qwen2.5:3b) |
| Clasificación de intención | ✅ (heurística) | `ServicioNLP` (regex, 6 intenciones) |
| 5 trámites mínimos | ✅ superado | Seeds: **22 trámites** TUPA 2023 (`database/seeds/tramites.sql`) |

### PMV2 — Modelo RAG optimizado (⚠️ 56 %)
| Componente | Estado | Evidencia |
|---|---|---|
| RAG con búsqueda vectorial | ✅ | `BusquedaVectorialAdapter` (pgvector HNSW, umbral 0.3) |
| 20+ trámites en base documental | ✅ superado | Seeds: **20 documentos** vigentes (`database/seeds/documentos.sql`) |
| Arquitectura hexagonal | ✅ | `backend/domain|application|infrastructure` + DI en `container.py` |
| Citas / fuentes en la respuesta | ✅ | Backend envía `titulo` + `fragmento` y el badge los muestra (D-3 corregido) |
| **Abstención** cuando falta contexto | ⚠️ | El asistente pide aclaración ante consulta ambigua y se abstiene sin contexto; el rechazo por groundedness baja sigue en G-04 |
| Gestión documental PMV2 (`ea06c9a`) | ⚠️ | Validación de formato (422), metadatos obligatorios, estado `derogado`, baja lógica, chunking (`ServicioChunking` 800/120), reprocesado y 6 endpoints admin — **bloqueados en runtime por D-14..D-21** |
| Validación con 50 ciudadanos | ❌ | G-26 (sin prueba SUS/reproducibilidad) |

### PMV3 — Sistema integrado desplegable (⚠️ 52 %, infraestructura a medias)
| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600) |
| API completa | ⚠️ | Controllers /api/consultas, /api/tramites, /api/documentos, /api/admin/documentos, /api/usuarios, /health (22 endpoints declarados), pero el HEAD actual **no arranca** por **D-14** |
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
> El global no cambia (60/101 = 59 %); solo se redistribuyen sus puntos (HU-11: 0/3, HU-17: 2/5).

| PMV | HU | % por HU | Justificación |
|---|---|---|---|
| **PMV1** (88 %) | HU-05 · HU-06 · HU-07 · HU-09 | **100** · **100** · 80 · 60 % | Consulta ciudadana, clasificación, requisitos y respuesta SLM = núcleo del prototipo |
| **PMV2** (50 %) | HU-04 · HU-08 · HU-10 · HU-11 · HU-12 | 78 · 60 · 50 · **0** · **0 %** | Procesamiento RAG, costos/plazos, trazabilidad, consultas fuera de dominio y trámites relacionados |
| **PMV3** (51 %) | HU-01 · HU-02 · HU-03 · HU-13 · HU-14 · HU-15 · HU-16 · HU-17 · HU-18 | 78 · 88 · 71 · 40 · 33 · **0** · **0** · 40 · **0 %** | Gestión documental + usuarios/seguridad + auditoría + métricas + derivación + reportes |

### El dato relevante por PMV

- **PMV1 (88 %)** con **HU-05 y HU-06 al 100 %**: la clasificación de intención
  con confianza y aclaración, el trámite probable y los requisitos verificados contra el catálogo
  funcionan de extremo a extremo. Quedan pendientes la derivación al área responsable (HU-07) y la
  estructura garantizada de la respuesta (HU-09).
- **PMV2 (50 %)** ganó el PMV2 documental del commit `ea06c9a`: HU-04 subió a **78 %** (chunking,
  reprocesado, panel de documentos). Desde la reasignación del 16-oct-2026 incluye **HU-11 (0 %)** —
  el clasificador de consultas fuera de dominio no existe — y sigue arrastrando a **HU-12 = 0 %** (el
  motor de trámites relacionados no existe) y HU-08 en 60 % (los montos del TUPA no están cargados en
  la base de datos). Además, los defectos **D-14..D-21** impiden arrancar la API y desplegar lo
  construido.
- **PMV3 (51 %)** subió porque HU-01 (78 %), HU-02 (88 %) y HU-03 (71 %) recogieron el avance del
  PMV2 documental; desde la reasignación del 16-oct-2026 incluye **HU-17 (40 %)** —derivación con
  solo una nota genérica—; aún **3 de sus 9 HU están en 0 %** (HU-15 retroalimentación, HU-16
  métricas y HU-18 reportes), y las otras 6 siguen en estado parcial.

## 5. Catálogo G-XX por PMV bloqueado

| Bloquea | Vacíos |
|---|---|
| **PMV1** | — (ninguno crítico; prototipo funcional) |
| **PMV2** | G-04 (abstención), G-08 (relacionados), G-13 (chunking ⬆️ parcial: falta OCR y recuperación por fragmento), G-14 (consistentación de campos de trámite), G-21 (artefactos PoC) |
| **PMV3** | G-01 (auth), G-20 (guardrails), G-16 (métricas), G-18 (pytest), G-23 (rate limit), G-26 (accesibilidad/carga), G-05 (feedback), G-07 (reportes), G-09 (derivación), G-11/G-10 (rutas UI) |

## 6. Ubicación actual del avance

Estricto a la definición de 04.4 y contrastado con el código:

- **Funcional:** el repositorio está en **PMV1 (88 %)** y consolidando **PMV2 (56 %)** — el RAG con
  20+ trámites y fuentes citadas opera, la abstención por ambigüedad también, y el PMV2 documental
  ya tiene validación de formato, metadatos, `derogado`, baja lógica, chunking, reprocesado y el
  panel `DocumentManager` en código. **Pero el HEAD `ea06c9a` no arranca la API (D-14)**: hasta
  corregirlo, 0 de 22 endpoints son servibles.
- **Medido:** PMV1 **88 %** · PMV2 **50 %** · PMV3 **51 %** · global **59 %**.
  Ningún PMV llega al 100 % porque el alcance de las historias incluye OCR, recuperación RAG por
  fragmento, autenticación, métricas y reportes que aún no existen (el versionado y el chunking ya
  sí existen en código).
- **Infraestructura:** la capa de **PMV3** está parcialmente adelantada en el repo (Docker Compose,
  Redis, API completa ya existen), pero eso no se refleja en el avance funcional de sus HU.
- **Pendiente prioritario para declarar PMV2 cerrado:** corregir los bloqueos **D-14..D-21**
  (arranque de la API, migración 004, dependencias de extracción, panel de documentos), cerrar
  **HU-12 (trámites relacionados) al 0 %**, G-21 (dataset y resultados de la PoC) y **cargar los
  montos reales del TUPA** en `tramites.costo`, hoy en 0.00, que es lo que impide cerrar HU-08.
- **Pendiente para PMV3:** seguridad (G-01/G-20), métricas (G-16), pruebas (G-18/G-26) y validación
  con usuarios (SUS). De los defectos del documento 02, **D-1..D-5 y D-10 están corregidos**;
  D-6, D-7 y D-12 son parciales; D-8, D-9 y D-11 siguen abiertos; D-13 es menor; y **D-14..D-21**
  son los bloqueantes nuevos del PMV2 (16-oct-2026).

## 7. Ruta de cierre sugerida (por PMV)

1. ~~**Corrección inmediata (antes que funcionalidad nueva):** subir el timeout del front, eliminar
   el fallback `respuestaDemo()` (**D-1**), enviar `groundedness` real (**D-2**) y alinear el contrato
   de fuentes (**D-3**)~~ — **hecho**: D-1 a D-5 corregidos y verificados contra la API en ejecución.
2. **Cerrar PMV2 (56 %):** corregir los bloqueos **D-14..D-21** (arrancar la API, aplicar la
   migración 004, añadir `pypdf`/`python-docx`, arreglar el panel de documentos y el manejo de
   DELETE 204) → cargar los montos reales del TUPA en `tramites.costo` → **HU-12 trámites
   relacionados (0 %)** → dataset de consultas sintéticas y resultados (G-21).
3. **Avanzar PMV3 (52 %), bloque 1:** pytest del flujo RAG (G-18) y autenticación JWT + roles (G-01).
4. **Avanzar PMV3, bloque 2:** endpoint de métricas (G-16) y guardrails anti prompt-injection (G-20).
5. **Validación final:** pruebas de carga (k6) + auditoría WCAG + SonarQube (G-26) y medición de
   latencia < 3 s.

## 8. Proyección si se cierra lo pendiente

| Escenario | Avance estimado |
|---|---|
| Estado actual (16-oct-2026) | **59 %** |
| ~~+ corregir D-1..D-5 (datos falsos en el chat)~~ | ~~42 %~~ — **superado** |
| + corregir D-14..D-21 (la API arranca y el PMV2 es desplegable) | habilita medir lo ya construido |
| + cargar montos del TUPA (cierra HU-08) | ~61 % |
| + autenticación, métricas y pytest | ~70 % |
| + retroalimentación, reportes y validación SUS | ~75–80 % |

