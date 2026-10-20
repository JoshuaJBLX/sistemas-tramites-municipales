# Implementado y por Implementar — Estado real del sistema

> Inventario honesto de qué está construido (con código real) y qué queda pendiente,
> contrastado contra `a.md`, las 18 HU y los vacíos `G-XX`.

**Leyenda:** ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado

> **Trazabilidad por PMV:** ver `05-trazabilidad-por-pmv.md` (qué se construyó en PMV1/PMV2/PMV3).

> **Cifras canónicas verificadas el 17 de octubre de 2026** (verificación en vivo contra API +
> PostgreSQL local; detalle en `06-estado-actual-implementado.md` §0 y §10):
>
> | Dimensión | Valor |
> |---|---|
> | Avance global de las 18 HU | **83/101 = 82 %** |
> | PMV1 | **24/24 = 100 %** ✅ |
> | PMV2 | **28/28 = 100 %** ✅ (incluye HU-11) |
> | PMV3 | **31/49 = 63 %** (incluye HU-17) |

## 0. Verificación local (octubre 2026)

El back-end se ejecutó de extremo a extremo en esta máquina con servicios nativos
(PostgreSQL 18 local, Redis y Ollama), sin Docker:

| Prueba | Resultado |
|---|---|
| `/health` | ✅ 200 `{"status":"ok"}` |
| `GET /api/tramites` | ✅ 22 trámites con su municipalidad |
| `GET /api/tramites/{id}` | ✅ incluye sus documentos vigentes |
| `POST /api/consultas` (RAG) | ✅ BGE-M3 → top-5 → Qwen 2.5 3B → confianza + 5 fuentes |
| `POST /api/consultas` (caché) | ✅ 30 ms vs ~5-9 s de la generación completa |
| `GET /api/consultas/{id}` | ✅ trazabilidad registrada |
| Consulta fuera de dominio | ✅ confianza **baja** + nota de verificación (sigue G-04) |
| `POST/PUT/DELETE /api/documentos` | ✅ indexado, cambio de estado y borrado |

Correcciones aplicadas durante esa verificación (ver commit `fix(backend)`):
1. `obtener_container` sin anotar `request` → FastAPI exigía un query param en toda ruta.
2. Fuentes de la respuesta cacheada se serializaban como `str(...)` → error de validación.
3. Actualizar el estado de un documento **borraba su embedding** (upsert con NULL) → `COALESCE`.
4. `indexado` siempre `false` porque los SELECT no leían la columna → flag `(embedding IS NOT NULL)`.
5. pgvector ahora es **opcional**: sin la extensión la columna es `double precision[]` y el
   coseno se calcula en Python (`Connection.es_pgvector()`).

> **Nota (16-oct-2026, verificación en vivo):** esa verificación de arranque fue previa al cierre de
> los defectos. **Hoy la API arranca con 31 rutas** (20 públicas + 7 admin + 4 de doc), las
> migraciones `004`/`005`/`006` están aplicadas y todos los endpoints declarados son servibles
> (D-14..D-23 corregidos; ver `06-estado-actual-implementado.md` §13.1).

## 1. Situación general

El sistema es una **PoC funcional**: el flujo ciudadano completo (preguntar → RAG → SLM →
groundedness → responder con fuentes) opera de extremo a extremo **y la API despliega**. Las
funciones de **administración y gobierno** (login, métricas reales, reportes) son la parte pendiente
principal.

```
Flujo de consulta  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  (✅ casi completo, falta G-16/G-04)
Gestión documental ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  (✅ PMV2 E2E verificado; G-12/G-13 completos)
Seguridad          ▓░░░░░░░░░░░░░░░░░░░  (❌ G-01, G-20, G-23)
Calidad/Métricas   ▓░░░░░░░░░░░░░░░░░░░  (❌ G-16, G-18, G-26)
```

## 2. Implementado (✅)

### 2.1 Backend (FastAPI, hexagonal)
- **Dominio**: entidades `Tramite`, `Documento`, `Consulta`, `Respuesta`, `Usuario`,
  `Municipalidad`, `Fuente`; value objects (`IntencionConsulta` 6, `NivelConfianza` 3,
  `EstadoDocumento` 3, `TipoTramite` 6); puertos ABC.
- **Aplicación**: 9 casos de uso (incluidos `CargarDocumento` y `ProcesarDocumento` del PMV2) y
  servicios `ServicioNLP` (regex), `ServicioRAG` (top_k=5), `ServicioChunking` (800/120),
  `ServicioSLM` (Qwen 2.5 3B), `EvaluadorGroundedness` (cobertura léxica, ALTA ≥0.75 / MEDIA ≥0.40),
  `ServicioCache` (Redis, TTL 3600), `ServicioAuditoria`.
- **Infraestructura**: adaptadores `BusquedaVectorialAdapter` (pgvector, umbral 0.3, `estado='vigente'`),
  `BGE_M3Adapter` (embeddings 1024 dims, CPU, async), `OllamaAdapter` (temperatura 0.2),
  `RedisAdapter`, `DocumentStorageAdapter`, `ExtraccionTextoAdapter`; repositorios `asyncpg` con
  pool 1-10, SQL parametrizado y `FragmentoRepositoryImpl` (fragmentos del PMV2).
- **API**: 7 controllers con rutas `/api/consultas*` (incl. `GET ''` y `/{id}` de trazabilidad),
  `/api/tramites*` (incl. `relacionados` y `PUT /{id}/area`), `/api/documentos*`, `/api/usuarios*`,
  `/api/admin/documentos*` (7 endpoints admin) y `/health`: **27 endpoints de API (20 públicos +
  7 admin) + 4 de documentación = 31 rutas servibles**; DI central en `container.py`.

### 2.2 Base de datos (PostgreSQL 16 + pgvector)
- Migraciones 001 (BD + extensión vector), 002 (6 tablas), 003 (índice **HNSW** `vector_cosine_ops`),
  004 (`documentos_pmv2`: metadatos, `fragmentos_documento`, `derogado`) y 005
  (`area_responsable`) — **las 004 y 005 están aplicadas** (45/45 documentos con metadatos;
  259 trámites con área).
- Seeds reales TUPA 2023 **MPJ**: 1 municipio, **252 procedimientos**, 20 documentos con fuente
  `gob.pe/munijunin`. **Seeds MPH (19-oct-2026):** `documentos_mph.sql` (19 documentos),
  `tramites_servicios.sql` (6 servicios) y `documentos_institucionales.sql` (6 documentos + 1
  servicio); base documental total **45 documentos** y catálogo **272 trámites**.
- Búsqueda por similitud de coseno (`embedding <=> $1::vector`, con fallback Python sin pgvector).

### 2.3 Frontend (Next.js 14)
- Rutas `/`, `/chat`, `/tramites`, `/admin`; **16 componentes** + set de 23 iconos SVG.
- Chat con sugerencias, `GroundednessBadge` (confianza + fuentes), catálogo con buscador/filtros,
  dashboard de métricas de demostración y panel real de gestión documental `DocumentManager.tsx`
  en `/admin` (conectado a la API, aunque hoy no carga por **D-14**/**D-21**).
- Integración real en `lib/api.ts` (`enviarConsulta`, `obtenerTramites`, `obtenerEstadoServicios`)
  con **fallback demo** si el backend está caído; ojo: `pedir()` rompe con los DELETE en 204 (**D-20**).

### 2.4 Infraestructura
- `docker-compose.yml` con 3 servicios (postgres+pgvector, redis, ollama), healthchecks y volúmenes.

### 2.5 PMV2 documental recién implementado (commit `ea06c9a`, 16-oct-2026)
- **Validación de formato** de carga: `FormatoDocumento` responde **422** con extensión no admitida.
- **Metadatos obligatorios**: `version`, `fecha_publicacion`, `hash_contenido`, `archivo_nombre`,
  `mime_type`, `fragmentado`, `eliminado_en`.
- **Estado `derogado`** y **baja lógica**: `DELETE /api/documentos/{id}` marca `eliminado_en`
  (**D-10 corregido**); existe además `DELETE /{id}/fisico` que **sí borra el archivo** (D-19 ✅).
- **Chunking** (`ServicioChunking` 800/120) + tabla `fragmentos_documento` + `FragmentoRepositoryImpl`.
- **Reprocesado** (`POST /api/documentos/{id}/procesar`) y casos de uso `CargarDocumento` y
  `ProcesarDocumento`.
- **Listados con filtros**: `GET /api/documentos` y `GET /api/admin/documentos`; **7 endpoints admin**.
- **Panel real** `DocumentManager.tsx` en `/admin` (**G-12 ✅**: carga, sube, aprueba y borra;
  los KPIs/gráficos de `/admin` siguen ficticios, D-6).
- **Inventario del repo (17-oct-2026):** 91 `.py` de backend, 25 `.ts`/`.tsx` de fuente, 11 `.sql`,
  92 `.md`, 7 controllers (ninguno stub), 27 endpoints de API + 4 de documentación = 31 rutas,
  11 puertos de dominio, 16 componentes front-end.

### 2.6 Defectos bloqueantes del PMV2 — ✅ todos corregidos (16-oct-2026)

| # | Defecto | Estado |
|---|---------|--------|
| D-14 | La API no arrancaba (`ImportError` de `router` en un stub) | ✅ **31 rutas servibles** |
| D-15 | Migración `004` sin aplicar y con línea 1 inválida | ✅ `004`/`005` aplicadas |
| D-16 | `instalar.ps1` no aplicaba la 004 | ✅ ambas listadas |
| D-17 | `pypdf`/`python-docx` ausentes de `requirements.txt` | ✅ deps completas |
| D-18 | `estado` inválido → 500 | ✅ 422 |
| D-19 | La baja física no borraba el archivo | ✅ sin huérfanos |
| D-20 | `response.json()` incondicional en DELETE 204 | ✅ 204 manejado |
| D-21 | Front llamaba a `/api/tramites/admin` inexistente | ✅ panel carga |
| D-22/D-23 | `fragmentado` BOOLEAN / publicar sin metadatos → 500 | ✅ corregidos |

> El catálogo completo de defectos (D-1..D-23) está en la sección de defectos de
> `02-implementacion-de-historias.md` y en `06-estado-actual-implementado.md` §13.

## 3. Parcial (⚠️) y por implementar (❌)

### 3.1 Vacíos de código `G-XX` (detalle en `02-implementacion-de-historias.md`)

| Código | Vacío | Prioridad |
|---|---|---|
| G-18 | **Suite de pruebas automatizadas (pytest)** | 🔴 Alta |
| G-16 / G-06 | **Métricas reales** del panel (hoy maqueta) | 🔴 Alta |
| G-01 | **Autenticación, JWT, roles y control de acceso** | 🔴 Alta |
| G-12 | **Carga de documentos conectada a `/api/documentos`** — ✅ **cerrado (16-oct-2026)**: `DocumentManager.tsx` sube, lista, aprueba y borra de verdad (los KPIs/gráficos de `/admin` siguen ficticios, D-6/G-06) | ✅ |
| G-04 | Abstención / rechazo por groundedness baja — ✅ **cerrado (17-oct-2026)**: umbral de rechazo (`BLOQUEO_AFIRMACIONES`) en `ServicioOrientacion` + clasificador de dominio (`ServicioDominio`) que deriva a la entidad correspondiente | ✅ |
| G-20 | Guardrails anti prompt-injection | 🟠 Media |
| G-13 | Chunking documental — ✅ **cerrado (16-oct-2026)**: `ServicioChunking` (800/120), tabla `fragmentos_documento`, migración `004` aplicada, OCR (`rapidocr`) y recuperación RAG **por fragmento** verificadas (20/20 docs) | ✅ |
| G-14 | Consistencia `tipo`/`duracion_estimada_dias` ↔ `categoria`/`plazo` | 🟠 Media |
| G-07 | Reportes y exportación | 🟠 Media |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas admin | 🟠 Media |
| G-10 | UI de historial ciudadano `/mis-consultas` | 🟡 Baja |
| G-08 | Recomendación de trámites relacionados — ✅ **cerrado (16-oct-2026)**: motor de similitud (embedding + fallback léxico), endpoint y UI | ✅ |
| G-09 | Derivación a atención municipal | 🟡 Baja |
| G-02 | Clasificador ML (Random Forest/TF-IDF) con métricas F1 | 🟡 Baja |
| G-03 | Enmascaramiento de PII | 🟡 Baja |
| G-05 | Retroalimentación ciudadana (útil/no útil) | 🟡 Baja |
| G-15 | Fine-tuning QLoRA del SLM | 🟡 Baja |
| G-17 | Contenerización frontend/CI, HTTPS, monitoreo | 🟡 Baja |
| G-21 | Artefactos de PoC (dataset, resultados de experimentos) | 🟡 Baja |
| G-23 | Rate limiting | 🟡 Baja |
| G-24 | Auditoría de manipulación de documentos | 🟡 Baja |
| G-25 | Aviso legal como política de API | 🟡 Baja |
| G-26 | Accesibilidad WCAG, pruebas de carga, SonarQube, ZAP | 🟡 Baja |

### 3.2 HU sin soporte en interfaz (❌)
- **HU-15** Retroalimentación · **HU-18** Reportes y exportación. (HU-11 y HU-12 quedaron sin
  interfaz dedicada, pero ambas tienen backend funcional y se benefician del chat; HU-11 cerró
  el 17-oct-2026.)

### 3.3 Diferencias con `a.md` (documentadas)
- `a.md` proponía: 7 contenedores, API `/api/v1/consulta`, clasificador Random Forest, 16 rutas,
  groundedness coseno con rechazo, tabla `evaluaciones_calidad`. **Lo implementado**: 3 servicios,
  `/api/consultas`, regex, 4 rutas, confianza cualitativa, sin tabla de evaluaciones.

## 4. Recomendación de cierre (siguiente iteración)

0. ~~**D-14..D-21** (bloqueantes del PMV2)~~ ✅ corregidos (16-oct-2026).
1. **G-18** prueba todo el flujo RAG (pytest + `httpx`/`pytest-asyncio`).
2. **G-01** login JWT + roles para proteger `/admin` y `/api/documentos`.
3. **G-16** endpoint de métricas agregadas (consultas por día, groundedness promedio, latencia).
4. **G-12** completar la gestión documental (KPIs reales de `/admin`).
5. ~~**G-04** rechazo/derivación cuando la groundedness es baja~~ ✅ cerrado (17-oct-2026);
   ~~G-13~~ ✅ cerrado (16-oct-2026).