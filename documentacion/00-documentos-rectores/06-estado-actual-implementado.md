# 06 · Estado Actual Implementado — Documento Maestro

> **Documento rector y fuente única de verdad** del estado real del *Sistema de Trámites
> Municipales*. Reúne en un solo archivo: (A) el inventario completo de código con la función de
> cada archivo, (B) los flujos de ejecución del front-end y del back-end paso a paso, (C) la base de
> datos, (D) el **avance actualizado de las 18 HU y de los 3 PMV con porcentajes medidos**,
> (E) lo que falta, (F) el inventario unificado de todos los `.md` del repositorio y (G) las
> inconsistencias documentales que esta unificación corrige.
>
> **Contrasta y reemplaza** a `02-implementacion-de-historias.md`, `04-implementado-y-por-implementar.md`
> y `05-trazabilidad-por-pmv.md` en cuanto a cifras. Esos tres `.md` se conservan como respaldo
> histórico y se remiten desde aquí.
>
> **Fecha de verificación: 20 de octubre de 2026** · HEAD `0d86eaf`
> (`feat(chat): formato de respuesta con pasos+HU-09 compacta, contenidos RAG y corrección de
> enlaces 404`).
> Método: lectura íntegra de los 91 `.py`, 25 `.ts`/`.tsx` de fuente, 14 `.sql`, `instalar.ps1`,
> `docker-compose.yml` y de los 92 `.md`; **más consulta directa a PostgreSQL local** (esquema real,
> conteos de `tramites`/`documentos`/`fragmentos_documento`) y ejecución de `import main`. Cada
> afirmación de este documento es verificable con `grep` sobre el archivo que se cita.
>
> **Actualización del 20 de octubre:** se sincronizan las cifras vigentes (272 trámites, 45
> documentos 45/45 fragmentados, 56 fragmentos, 31 rutas, 91 `.py`, 14 `.sql`, 92 `.md`), se añaden
> los contenidos RAG (seeds MPH e institucionales), el formato de respuesta del chat y la corrección
> de los 20 enlaces 404 (`C-01..C-07` en `07-checklist-implementacion.md`). Todos los `.md` enlazan
> a este documento como fuente única de verdad.
>
> **Actualización del 16 de octubre:** incorpora el avance del PMV2 (commit `ea06c9a`) y corrige
> una inconsistencia heredada: la suma de puntos por HU hacía del PMV1 un **88 %**, no un 100 %
> (ver §12.7).

---

## 0. Resumen ejecutivo

| Dimensión | Resultado actual | Referencia |
|---|---|---|
| **Avance global de las 18 HU** | **82 %** (83/101 puntos de verificación) — verificado 20-oct-2026 | §10.1 |
| **PMV1 · Prototipo funcional** | **100 %** (24/24) — 4 HU ✅ | §10.4 |
| **PMV2 · Modelo RAG optimizado** | **100 %** (28/28) — 5 HU al 100 % (HU-04, HU-08, HU-10, HU-11, HU-12) | §10.5 |
| **PMV3 · Sistema integrado** | **63 %** (31/49) — 9 HU (HU-01 y HU-02 al 100 %) | §10.6 |
| HU completas al 100 % | **11 / 18** — HU-01, HU-02, HU-04, HU-05, HU-06, HU-07, HU-08, HU-09, HU-10, HU-11, HU-12 | §10.3 |
| HU iniciadas (⚠️ o ✅) | **15 / 18** | §10.3 |
| HU sin empezar (❌) | **3 / 18** — HU-15, HU-16, HU-18 | §10.3 |
| Pruebas automatizadas | **0 suites** | §13.2 |
| Catálogo de trámites | **252 TUPA** (272 en BD = 252 + 13 prototipos + 6 servicios MPH + 1 institucional) | §7 |
| Documentos indexados | **45** (20 TUPA + 19 MPH + 6 institucionales; 45/45 con embedding y **45/45 fragmentados**: `fragmentos_documento` = 56 filas) | §7 |
| Endpoints REST | **31 rutas servibles** (27 de API + 4 de documentación) | §6.2 |
| Archivos Python (backend) | **91** | §5 |
| Archivos `.ts`/`.tsx` de fuente | **25** (5 rutas + 16 componentes + 2 lib + 2 config) | §5 |
| Archivos SQL | **14** (6 migraciones, 6 seeds, 1 script, 1 schema) | §7 |
| Documentos Markdown | **92** | §11 |

**Lo que funciona de extremo a extremo (código):** el flujo ciudadano completo
`pregunta → clasificación de intención con confianza → persistencia → caché → recuperación vectorial →
generación con SLM local → evaluación de groundedness → identificación de trámite probable con datos
del catálogo → auditoría en PostgreSQL → respuesta con fuentes`, y desde el commit `ea06c9a` también
el **ciclo documental del PMV2**: carga con metadatos, validación de formato, chunking en fragmentos,
listado con filtros, baja lógica/física y panel de administración de documentos.

> ✅ **Resuelto el 16 de octubre (verificación en vivo):** los bloqueos D-14..D-21 están corregidos
> (`import main` → 30 rutas, migración 004 **y** 005 aplicadas, `instalar.ps1` lista ambas, deps en
> `requirements.txt`). La API sirve en `localhost:8000`, el panel admin carga los 272 trámites y la
> carga de un PDF real del TUPA devuelve **201** con texto extraído. Se corrigió además un bug no
> documentado: `DocumentoRepositoryImpl.guardar` enviaba `int` a la columna BOOLEAN `fragmentado`
> (rompía todo upsert de documentos). Detalle en §13.1.

**Lo que ya funciona de extremo a extremo (verificado hoy):** el ciclo documental completo del PMV2
(carga de PDF real → extracción → chunking → embeddings por fragmento → búsqueda vectorial por
fragmento → aprobación con metadatos obligatorios), el catálogo con **252 trámites del TUPA con
montos y áreas reales**, la recomendación de trámites relacionados (API + UI) y el dataset de la PoC
(200 consultas versionadas).

**Lo que no existe todavía:** autenticación y roles (G-01), guardrails anti *prompt-injection* (G-20),
métricas reales (G-16), pruebas automatizadas (G-18), retroalimentación ciudadana (G-05),
reportes (HU-18, G-07), manejo de PII (G-03), clasificador ML
(G-02) y la **validación SUS con 50 ciudadanos** (P2-17, actividad real no fabricable).

---

## 1. Identidad del proyecto

| Campo | Valor |
|---|---|
| Nombre del producto | **MUN AI** |
| Propósito | Orientación de trámites municipales mediante asistente conversacional RAG + SLM local |
| Entidad | **Municipalidad Provincial de Huancayo (MPH)** — provincia de Huancayo, departamento de Junín |
| Base normativa | TUPA 2023 (252 procedimientos) + ordinances y reglamentos oficiales |
| Portal de referencia | `munihuancayo.gob.pe` / `gob.pe/munihuancayo` |
| Modelo de lenguaje | `qwen2.5:3b` servido por Ollama (`OLLAMA_MODEL`) |
| Embeddings | **dual**: `OpenAIEmbeddingsAdapter` (API, 1024 dims) cuando existe `OPENAI_API_KEY`; si no, `BAAI/bge-m3` local en CPU (`container.py:227`) |
| Base de datos | PostgreSQL 16 + pgvector (`double precision[]` si la extensión no está) |
| Caché | Redis 7, TTL 3600 s |
| Front-end | Next.js 14.2.5 (App Router) + React 18.3 + TypeScript + Tailwind CSS 3.4 |

> ⚠️ **Inconsistencia activa de branding (ver §12.1).** El código y la base de datos dicen
> **Huancayo (MPH)** tras el commit `ff7a589`; en cambio `README.md`, `DOCUMENTACION.md` y
> `PRESENTACION-PMV1.md` siguen diciendo **Junín (MPJ)**, y
> `database/seeds/municipios.sql:10` todavía inserta *"Municipalidad Provincial de Junín"*
> (aunque `database/scripts/actualizar_huancayo.sql` corrige ese registro al ejecutarse).
> Este documento adopta **Huancayo (MPH)** por ser lo que el código implementa.

---

## 2. Índice de contenidos

| Sección | Contenido |
|---|---|
| §0 | Resumen ejecutivo con cifras actuales |
| §1 | Identidad del proyecto |
| §2 | Este índice |
| §3 | Inventario del repositorio (estructura de carpetas) |
| §4 | Arquitectura: las tres capas y por qué |
| §5 | Inventario detallado de código, archivo por archivo |
| §6 | **Flujo del back-end** (API REST, paso a paso) |
| §7 | **Flujo de la base de datos** y carga documental |
| §8 | **Flujo del front-end** (rutas, componentes, capa de API) |
| §9 | Flujo de instalación y ejecución |
| §10 | **Estado actualizado de las 18 HU y los 3 PMV con % medido** |
| §11 | **Inventario unificado de todos los `.md`** |
| §12 | Inconsistencias detectadas y plan de unificación documental |
| §13 | Defectos abiertos, vacíos G-XX y ruta de cierre |

---

## 3. Inventario del repositorio

```text
sistemas-tramites-municipales/            raíz del proyecto
├── backend/                                API REST · Python 3.11+ · FastAPI · arquitectura hexagonal
│   ├── main.py                             punto de entrada: app FastAPI, CORS, 6 routers, /health, lifespan
│   ├── domain/                             NÚCLEO — no importa nada de infrastructure
│   │   ├── entities/                       8 entidades (+ FragmentoDocumento)
│   │   ├── value_objects/                  8 value objects (+ FormatoDocumento)
│   │   └── ports/                          10 puertos (interfaces ABC, +3 del PMV2)
│   ├── application/                        LÓGICA DE APLICACIÓN — casos de uso y servicios
│   │   ├── use_cases/                      10 casos de uso (+ CargarDocumento, ProcesarDocumento)
│   │   └── services/                       8 servicios (+ ServicioChunking)
│   ├── infrastructure/                     ADAPTADORES — todo lo que toca el mundo exterior
│   │   ├── controllers/                    7 controllers FastAPI (tramite_admin ya con router, D-14 ✅)
│   │   ├── schemas/                        schemas Pydantic (documento_admin)
│   │   ├── repositories/                   Connection + 3 repositorios + base
│   │   ├── adapters/                       7 familias (rag, embeddings, slm, cache, catalog,
│   │   │                                   documents, extraction)
│   │   └── container.py                    inyección de dependencias
│   └── scripts/indexar_documentos.py      indexación masiva de embeddings BGE-M3
├── frontend-tramites/                      Next.js 14 (App Router) + TypeScript + Tailwind
│   ├── app/                                rutas: / · /chat · /tramites · /admin + layout + globals.css
│   ├── components/                         16 componentes (15 + icons.tsx, 20 iconos SVG)
│   └── lib/                                api.ts (contrato HTTP) · queries.ts (helpers)
├── database/
│   ├── schema.sql                          referencia consolidada del esquema
│   ├── migrations/                         001 base+extensión · 002 tablas+índices · 003 HNSW
│   │                                       · 004 PMV2 · 005 área responsable · 006 auditoría
│   ├── seeds/                              municipios (1) · tramites (22) · documentos (20)
│   │                                       · tramites_servicios (6) · documentos_mph (19)
│   │                                       · documentos_institucionales (6 + 1 servicio)
│   └── scripts/actualizar_huancayo.sql    corrección de entidad Junín → Huancayo
├── documentacion/
│   ├── 00-documentos-rectores/             7 documentos (este es el 06)
│   ├── 01-analisis-del-problema/           11 archivos
│   ├── 02-conocimientos-de-ingenieria/     10 archivos
│   ├── 03-el-ingeniero-y-la-sociedad/      14 archivos
│   ├── 04-gestion-de-proyecto/             11 archivos
│   ├── 05-uso-de-herramientas-modernas/    13 archivos
│   └── 06-prueba-de-concepto/              14 archivos
├── presentacion/                           6 archivos — documentación técnica para sustentación
├── instalar.ps1                            instalador idempotente de 7 pasos
├── docker-compose.yml                      postgres+pgvector · redis · ollama
├── requirements.txt                        11 dependencias Python fijadas
├── .env.example                            15 variables de entorno
├── README.md                               guía de puesta en marcha
├── DOCUMENTACION.md                        índice maestro de la documentación
├── PMV2_DOCUMENTOS.md                      alcance y **estado verificado** del PMV2
└── PRESENTACION-PMV1.md                    guion de demostración del PMV1  ⚠️ reescrito localmente (§12.2)
```

**Totales:** 91 archivos Python · 25 archivos `.ts`/`.tsx` de fuente · 14 archivos SQL · 92 archivos
Markdown · 1 script PowerShell · 1 archivo YAML.

---

## 4. Arquitectura

### 4.1 Las tres capas (arquitectura hexagonal / puertos y adaptadores)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CAPA DE ENTRADA — infrastructure/controllers/                          │
│  consulta_controller · documento_controller · documento_admin_controller│
│  tramite_controller · usuario_controller   (FastAPI: parsing, HTTP)     │
│  tramite_admin_controller  ✅ CON `router` → la app arranca (30 rutas, D-14)│
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ llama casos de uso (no adaptadores)
┌───────────────────────────────▼──────────────────────────────────────────┐
│  APLICACIÓN — application/                                               │
│  use_cases/   ClasificarIntencion · RegistrarConsulta · GenerarOrientacion│
│               IdentificarTramiteProbable · AuditarConsulta ·             │
│               GestionarDocumentos · ConsultarTramite · BuscarDocumentos   │
│               CargarDocumento · ProcesarDocumento                        │
│  services/    ServicioOrientacion · ServicioRAG · ServicioSLM ·           │
│               ServicioNLP · EvaluadorGroundedness · ServicioCache ·       │
│               ServicioAuditoria · ServicioChunking                        │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ depende SOLO de puertos (ABC)
┌───────────────────────────────▼──────────────────────────────────────────┐
│  DOMINIO — domain/     (sin imports de infrastructure: es testeable solo) │
│  entities/    Consulta · Documento · FragmentoDocumento · Respuesta ·     │
│               Fuente · Tramite · Usuario · Municipalidad                  │
│  value_objects/ IntencionConsulta(9) · ClasificacionIntencion ·           │
│               TramiteProbable · NivelConfianza(3) · EstadoDocumento(4) · │
│               TipoTramite(6) · FuenteOficial(4) · FormatoDocumento       │
│  ports/       CachePort · DocumentoRepository · FragmentoRepository ·     │
│               ExtraccionTextoPort · AlmacenamientoDocumentosPort ·        │
│               ConsultaRepository · BusquedaSemanticaPort ·                │
│               GeneracionRespuestaPort · AuditoriaPort ·                   │
│               TramiteCatalogoPort                                         │
└───────────────────────────────▲──────────────────────────────────────────┘
                                │ implementan los puertos
┌───────────────────────────────┴──────────────────────────────────────────┐
│  INFRAESTRUCTURA — infrastructure/                                       │
│  adapters/     BusquedaVectorialAdapter · BGE_M3Adapter · OllamaAdapter · │
│                RedisAdapter · TramiteCatalogoAdapter · DocumentStorage-  │
│                Adapter · ExtraccionTextoAdapter                           │
│  repositories/ Connection (pool asyncpg) · DocumentoRepositoryImpl ·      │
│                FragmentoRepositoryImpl · ConsultaRepositoryImpl ·         │
│                PostgreSQLRepository                                       │
│  container.py  construye y conecta todo el grafo (crear_container)        │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
        ┌───────────────┬───────┴────────┬──────────────────┐
   PostgreSQL        Redis           Ollama          disco (storage/)
   + pgvector        (caché)      (SLM qwen2.5:3b)   documentos
```

**Regla de dependencia:** las flechas apuntan hacia dentro. `domain/` no importa nada de
`application/` ni de `infrastructure/`; `application/` solo conoce `domain/ports/*` (interfaces
abstractas). La única pieza que conoce todas las implementaciones concretas es
`backend/infrastructure/container.py` — se documenta como tal en su docstring (líneas 1-5).

**Verificación de la regla:** `grep -r "from infrastructure" backend/domain backend/application`
no devuelve resultados.

### 4.2 Inyección de dependencias

`container.py:104-171` — la función `crear_container()` construye el grafo completo:

| Línea | Se construye | Puerto que satisface |
|---|---|---|
| `105` | `Connection(dsn)` | — (recurso compartido) |
| `107` | `BGE_M3Adapter()` | — (colaborador de embeddings) |
| `108` | `BusquedaVectorialAdapter(connection, embeddings)` | `BusquedaSemanticaPort` |
| `109` | `OllamaAdapter()` | `GeneracionRespuestaPort` |
| `110` | `RedisAdapter()` | `CachePort` |
| `111` | `DocumentStorageAdapter()` | `AlmacenamientoDocumentosPort` (PMV2) |
| `112` | `ExtraccionTextoAdapter()` | `ExtraccionTextoPort` (PMV2) |
| `113` | `_AuditoriaPostgreSQL(connection)` | `AuditoriaPort` |
| `115-117` | `DocumentoRepositoryImpl`, `ConsultaRepositoryImpl`, `FragmentoRepositoryImpl` | `DocumentoRepository`, `ConsultaRepository`, `FragmentoRepository` |
| `119` | `TramiteCatalogoAdapter(documento_repository)` | `TramiteCatalogoPort` |
| `121-137` | 8 servicios de aplicación (incluido `ServicioChunking`) | — |
| `139-145` | 3 casos de uso documentales: `GestionarDocumentos`, `ProcesarDocumento`, `CargarDocumento` | — |
| `160-171` | el resto de casos de uso ya inyectados | — |

`obtener_container(request)` (`container.py:154-156`) expone el contenedor como dependencia de
FastAPI mediante `app.state.container` (asignado en `main.py:29`). Todos los controllers la reciben
con `container: Container = Depends(obtener_container)`.

### 4.3 Stack tecnológico

| Capa | Tecnología | Versión | Archivo que lo fija |
|---|---|---|---|
| API | FastAPI | 0.111.0 | `requirements.txt:6` |
| Servidor ASGI | uvicorn[standard] | 0.30.1 | `requirements.txt:7` |
| Driver BD | asyncpg | 0.30.0 | `requirements.txt:12` |
| Extensión vectorial | pgvector (cliente) | 0.3.0 | `requirements.txt:13` |
| Caché | redis (asyncio) | 5.0.4 | `requirements.txt:16` |
| Cliente HTTP | httpx | 0.27.0 | `requirements.txt:19` |
| Validación | pydantic[email] | 2.10.4 | `requirements.txt:22` |
| Configuración | python-dotenv | 1.0.1 | `requirements.txt:23` |
| Embeddings (nube) | openai (cliente; OpenAI u OpenRouter) | 1.109.1 | `requirements.txt:27` |
| Embeddings (local) | sentence-transformers | 3.0.1 | `requirements-ml.txt` (solo local/Docker/Fly) |
| Cálculo numérico | numpy | ≥2.0 | `requirements.txt:27` |
| Front-end | next | 14.2.5 | `frontend-tramites/package.json:12` |
| UI | react / react-dom | ^18.3.1 | `frontend-tramites/package.json:13-14` |
| Estilos | tailwindcss / postcss / autoprefixer | 3.4.4 / 8.4.38 / 10.4.19 | `frontend-tramites/package.json:20-22` |
| Lenguaje | TypeScript | ^5.5.2 | `frontend-tramites/package.json:23` |

---

## 5. Inventario detallado de código

Cada fila indica el archivo, sus líneas y su función real verificada en el código.

### 5.1 Punto de entrada

| Archivo | Líneas | Función |
|---|---|---|
| `backend/main.py` | 74 | Crea la app FastAPI (`Sistema de Trámites Municipales API` v0.1.0), carga `.env` con `load_dotenv()`, configura CORS limitado a `localhost:3000` y `127.0.0.1:3000`, incluye los **7 routers** (líneas 58-66), expone `GET /health` y un `lifespan` que abre/cierra el pool de PostgreSQL y Redis. ✅ **Arranca**: **31 rutas** en `/openapi.json` (18 públicas + 9 admin + 4 de documentación). |

### 5.2 Capa de dominio — entidades (`backend/domain/entities/`)

| Archivo | Líneas | Contenido |
|---|---|---|
| `Consulta.py` | 19 | `id`, `usuario_id`, `pregunta`, `intencion`, `creada_en`; método `clasificada()`. |
| `Documento.py` | 69 | **Ampliado en PMV2**: `id`, `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado`, `embedding`, `actualizado_en`, `indexado`, `puntuacion_similitud` + metadatos `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`, `fragmentado`, `eliminado_en`. Métodos `esta_vigente()`, `esta_eliminado()` y `requiere_metadatos()` (exige `titulo`, `url_origen` y `version`; `fecha_publicacion` opcional). |
| `FragmentoDocumento.py` | 20 | **Nuevo (PMV2):** `id`, `documento_id`, `orden`, `contenido`, `embedding`, `creado_en` — la fila que materializa el *chunking* de HU-04. |
| `Respuesta.py` | 61 | Entidad central: `id`, `consulta_id`, `texto`, `confianza`, `fuentes`, `groundedness`, `confianza_intencion`, `pide_aclaracion`, `tramite_probable`. **Método clave `con_datos_estructurados()`** (líneas 31-66): anexa al texto del modelo los requisitos numerados, el arancel y el plazo **tomados de la base de datos**, más la URL de la ficha. Es lo que hace verificables los datos críticos (HU-07). |
| `Fuente.py` | 17 | `id`, `documento_id`, `tipo`, `url`, `fragmento`, `titulo`, `puntuacion_relevancia`. El campo `titulo` es el que permite que el front muestre la fuente (**D-3 corregido**). |
| `Tramite.py` | 21 | `id`, `municipalidad_id`, `nombre`, `descripcion`, `tipo`, `requisitos[]`, `costo`, `duracion_estimada_dias`; `agregar_requisito()`. |
| `Usuario.py` | 17 | `id`, `nombre`, `correo`, `rol`, `creado_en`; `es_administrador()` — **existe pero nunca se invoca** (defecto **D-8**). |
| `Municipalidad.py` | 14 | `id`, `nombre`, `departamento`, `provincia`, `distrito`, `sitio_web`. |
| `errors.py` (dominio) | 21 | **Nuevo (PMV2):** `FormatoNoSoportadoError`, `DocumentoIlegibleError`, `DocumentoInvalidoError` — errores de dominio que los controllers traducen a 422/400. |

### 5.3 Capa de dominio — value objects (`backend/domain/value_objects/`)

| Archivo | Líneas | Contenido |
|---|---|---|
| `IntencionConsulta.py` | 12 | Enum `str` con **9 intenciones**: `consultar_requisitos`, `consultar_costo`, `consultar_plazo`, `consultar_pasos`, `consultar_area`, `consultar_estado`, `consultar_ubicacion`, `saludo`, `otro`. |
| `ClasificacionIntencion.py` | 25 | `intencion` + `confianza` + `empata`. Propiedad `requiere_aclaracion` (líneas 22-29): verdadera si la intención es `OTRO`, si hay empate o si la confianza < `CONFIANZA_MINIMA = 0.5` (línea 13). Fábrica `sin_patron()` (líneas 31-33). |
| `TramiteProbable.py` | 21 | Value object que transporta el trámite detectado con `requisitos[]`, `costo`, `duracion_estimada_dias`, `fuente_url`, `documentos_coincidentes` y `puntaje_relevancia`; `resumen_requisitos(limite)`. |
| `NivelConfianza.py` | 6 | Enum `alta` / `media` / `baja`. |
| `EstadoDocumento.py` | 13 | Enum `vigente` / `obsoleto` / `en_revision` / **`derogado`** (añadido en PMV2). ⚠️ `derogado` solo es persistible cuando la migración `004` actualiza el `CHECK` de la BD (D-15). |
| `FormatoDocumento.py` | 41 | **Nuevo (PMV2):** VO que valida la extensión del archivo (`.pdf`, `.docx`, `.txt`, `.md`), expone `formatos_soportados()` y su MIME asociado. Base de la validación de HU-01 (**D-7**). |
| `TipoTramite.py` | 9 | Enum con 6 valores (`licencia_funcionamiento`, `partida_nacimiento`, `certificado_domicilio`, `licencia_construccion`, `pago_tributos`, `otro`). **Nota:** los 22 seeds usan 4 de estos 6 más `otro`. |
| `FuenteOficial.py` | 7 | Enum `portal_municipal`, `normativa_legal`, `tupa`, `documento_interno`. Todo documento sembrado se cita como `portal_municipal` (`ServicioRAG.py:50`). |

### 5.4 Capa de dominio — puertos (`backend/domain/ports/`)

Interfaces ABC que el dominio define y la infraestructura implementan. Son el punto donde se
podrían sustituir PostgreSQL, Redis u Ollama sin tocar la lógica.

| Archivo | Métodos abstractos | Implementación actual |
|---|---|---|
| `CachePort.py` | `obtener`, `guardar`, `eliminar` | `RedisAdapter` |
| `DocumentoRepository.py` | 45 líneas — `guardar`, `obtener_por_id`, `listar_por_tramite`, **`listar` (filtros)**, **`marcar_eliminado`**, **`eliminar_fisico`**, `eliminar` | `DocumentoRepositoryImpl` |
| `FragmentoRepository.py` | **Nuevo (PMV2):** `guardar_lote`, `listar_por_documento`, `eliminar_por_documento` | `FragmentoRepositoryImpl` |
| `ExtraccionTextoPort.py` | **Nuevo (PMV2):** `extraer_texto`, `formatos_soportados` | `ExtraccionTextoAdapter` |
| `AlmacenamientoDocumentosPort.py` | **Nuevo (PMV2):** `guardar`, `leer`, `eliminar`, `listar` | `DocumentStorageAdapter` |
| `ConsultaRepository.py` | `guardar`, `obtener_por_id`, `listar_por_usuario` | `ConsultaRepositoryImpl` |
| `BusquedaSemanticaPort.py` | `buscar`, `generar_embedding` | `BusquedaVectorialAdapter` |
| `GeneracionRespuestaPort.py` | `generar` | `OllamaAdapter` |
| `AuditoriaPort.py` | `registrar` | `_AuditoriaPostgreSQL` (en `container.py:55-71`) |
| `TramiteCatalogoPort.py` | `buscar_por_documentos` | `TramiteCatalogoAdapter` |

**10 puertos** (eran 7): los 3 nuevos son el contrato del PMV2 para extraer texto, almacenar el
archivo original y persistir los fragmentos.

### 5.5 Capa de aplicación — servicios (`backend/application/services/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `ServicioNLP.py` | 131 | **Clasificador léxico de intención.** Diccionario `_PATRONES_INTENCION` (líneas 12-75) con **raíces**, no palabras completas, para tolerar conjugaciones (`requisit` cubre requisito/requisitos/requiere/necesito). Lógica: normaliza (minúsculas, sin tildes, sin puntuación, línea 124-131), puntúa cada intención por nº de patrones coincidentes, desempata por especificidad (suma de longitudes, línea 110), y calcula `confianza = 0.55 + 0.15 × (patrones−1)` con tope 1.0 (líneas 78-79, 117); si hay empate técnico baja la confianza a 0.70 (línea 118-119). Sin patrones → `OTRO` con confianza 0. |
| `ServicioRAG.py` | 56 | Orquesta recuperación + generación. `recuperar()` (líneas 25-28) llama al `BusquedaSemanticaPort` y **filtra solo documentos vigentes**. `responder()` (30-41): sin documentos devuelve el texto de abstención del SLM con lista de fuentes vacía. `construir_fuentes()` estático (43-56): convierte cada documento en `Fuente` con `fragmento = contenido[:280]` y su `titulo`. |
| `ServicioSLM.py` | ~250 | Construye el formato de salida y delega. `INSTRUCCION_ESTRUCTURA` pide pasos numerados (máximo 4, título en negrita) + apartados REQUISITOS / PASOS / COSTO / PLAZO / OBSERVACIONES compactos (19-oct-2026); `INSTRUCCION_BREVE` para consultas generales. `generar(..., estructura)`: sin contexto devuelve la abstención *"No encontré información oficial…"*; con estructura aplica `garantizar_estructura` (fallback desde BD, HU-09) y `condensar` (pasos arriba, cada apartado ≤ 200 caracteres y total ≤ 1100 con "…"). `generar` delege al puerto con `instrucciones=…`. |
| `ServicioOrientacion.py` | 94 | **Orquestador del flujo de orientación.** `orientar()` (líneas 34-72): (1) si la clasificación requiere aclaración devuelve `ACLARACION_AMBIGUA` sin generar ni citar (41-42); (2) recupera documentos; (3) genera respuesta y fuentes; (4) calcula `groundedness` y confianza; (5) si confianza BAJA y hay fuentes, **agrega nota de advertencia visible** al texto (49-54); (6) llama a `IdentificarTramiteProbable` (56-58); (7) anexa los datos estructurados del catálogo (71-72). `ACLARACION_AMBIGUA` (líneas 14-18) es el texto que pide专业课 precisar requisitos/costo/lugar/estado. |
| `EvaluadorGroundedness.py` | 49 | **Control de alucinaciones por cobertura léxica.** Tokeniza la respuesta (palabras de >3 caracteres, línea 48-49), construye el vocabulario del contexto (contenido + título de cada documento) y calcula `coincidencias / términos_respuesta` (líneas 27-42). Umbrales: `ALTA ≥ 0.75`, `MEDIA ≥ 0.40`, si no `BAJA` (líneas 6-7, 18-25). `esta_grounded()` (44-45). |
| `ServicioCache.py` | 35 | Abstrae la caché de respuestas. `construir_clave()` (17-20): `consulta:` + SHA-256 de la pregunta normalizada (minúsculas, sin espacios extremos) — así `"¿Cuánto cuesta?"` y `"cuánto cuesta"` comparten entrada. `obtener_respuesta`, `guardar_respuesta` (TTL configurable), `invalidar`. |
| `ServicioAuditoria.py` | 28 | Centraliza `registrar_interaccion()` y `obtener_consulta()`; usa `AuditoriaPort` + `ConsultaRepository`. |
| `ServicioChunking.py` | 72 | **Nuevo (PMV2).** Segmentador determinista sin dependencias externas: normaliza saltos de línea, parte en párrafos, luego en oraciones y agrupa en bloques de ~800 caracteres con **solape de 120**. Devuelve `list[str]` que `ProcesarDocumento` convierte en `FragmentoDocumento` con su embedding. Es el `G-13` que antes figuraba como vacío (parcial: falta OCR y la recuperación RAG por fragmento). |

### 5.6 Capa de aplicación — casos de uso (`backend/application/use_cases/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `ClasificarIntencion.py` | 26 | `ejecutar()` devuelve solo la intención; `ejecutar_detallado()` devuelve la `ClasificacionIntencion` completa (intención + confianza + empate). Ambos validan que la pregunta no esté vacía. |
| `RegistrarConsulta.py` | 34 | Construye la entidad `Consulta` con `uuid4()` y `datetime.now(timezone.utc)` y la persiste vía `ConsultaRepository`. |
| `GenerarOrientacion.py` | 29 | Valida la pregunta y delega en `ServicioOrientacion.orientar()`, reenviando la `ClasificacionIntencion`. |
| `IdentificarTramiteProbable.py` | ~110 | **Deducción del trámite del catálogo.** `ejecutar(documentos)`: pide al `TramiteCatalogoPort` los trámites vinculados a los documentos recuperados; puntúa cada trámite **sumando la similitud semántica** de sus documentos (`_puntuar`), considerando solo los que superan `VOTO_MINIMO_DOC = 0.45` (evita que documentos genéricos como catálogo/TUPA acumulen puntos flojos). Descarta si el ganador no supera `PUNTAJE_MINIMO = 0.45` o si no supera al segundo por `MARGEN_MINIMO = 1.15` — **las variantes del mismo trámite** (p. ej. "Licencia de Funcionamiento" vs "Licencia de Funcionamiento Temporal", solapamiento de tokens ≥ 0.5) **no cuentan como rivales** para el margen (19-oct-2026). Si nada domina, **no propone ningún trámite** — decisión deliberada: es preferible callar antes que señalar el trámite equivocado. |
| `AuditarConsulta.py` | 20 | `ejecutar()` registra la trazabilidad; `consultar_trazabilidad()` recupera la consulta por id. |
| `GestionarDocumentos.py` | 128 | **Ampliado en PMV2:** `registrar()` genera el embedding, valida metadatos (`requiere_metadatos()`) y calcula `hash_contenido`; **`listar()`** con filtros `tramite_id`/`estado`/`incluir_eliminados` + paginación; `actualizar_estado()`; **`eliminar()` = baja lógica** (marca `eliminado_en`); **`eliminar_fisico()`** (borra filas). |
| `CargarDocumento.py` | 91 | **Nuevo (PMV2).** Orquesta la carga de un archivo: valida la extensión (`FormatoDocumento`) → extrae el texto (`ExtraccionTextoPort`) → almacena el original (`AlmacenamientoDocumentosPort`) → registra el documento con metadatos → indexa el embedding → fragmenta. Si el *chunking* falla, degrada sin romper la carga (solo deja `fragmentado=false`). |
| `ProcesarDocumento.py` | 65 | **Nuevo (PMV2).** Reprocesa un documento: borra sus fragmentos anteriores, ejecuta `ServicioChunking`, genera el embedding de cada fragmento con `BusquedaSemanticaPort` y los persiste en lote; al terminar marca `fragmentado=true`. **Idempotente**: se puede llamar N veces. |
| `ConsultarTramite.py` | 37 | Obtiene los documentos vigentes de un trámite, con caché propia (`tramite:{id}:documentos`, TTL 1800 s). |
| `BuscarDocumentos.py` | 19 | Búsqueda semántica directa, filtrando a vigentes. No lo invoca ningún controller (queda disponible para el endpoint de búsqueda). |

### 5.7 Capa de infraestructura — adaptadores (`backend/infrastructure/adapters/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `rag/BusquedaVectorialAdapter.py` | 117 | **Búsqueda semántica con doble modo.** Detecta pgvector con `Connection.es_pgvector()` (línea 84) y elige: **modo pgvector** — `1 - (embedding <=> $1::vector)` con índice HNSW (`QUERY_BUSQUEDA_VECTORIAL_PGVECTOR`, líneas 17-25); **modo sin pgvector** — trae todos los embeddings y calcula el coseno con numpy en Python (`_coseno`, líneas 40-52; `QUERY_BUSQUEDA_IN_MEMORIA`, 27-33). Ambos filtran `estado = 'vigente'` y `embedding IS NOT NULL`, y aplican `umbral_similitud = 0.3` (línea 75, constructor). `generar_embedding()` delega en BGE-M3. |
| `embeddings/BGE_M3Adapter.py` | 41 | Genera vectores de 1024 dimensiones con `BAAI/bge-m3` en CPU. Carga perezosa y en hilo (`asyncio.to_thread`, línea 36) para no bloquear el event loop. `normalize_embeddings=True` (línea 40). |
| `slm/OllamaAdapter.py` | ~65 | Cliente HTTP de Ollama (`OLLAMA_URL`, por defecto `localhost:11434`; modelo `qwen2.5:3b`). Payload: `temperature 0.2`, `num_predict 320`, `stream false`; acepta `instrucciones` del servicio y las concatena al prompt de sistema. `construir_prompt()` arma `Contexto:` con `Fuente: título (url)` + contenido, o avisa *"No se recuperó contexto documental"* si está vacío. Timeout 120 s. |
| `cache/RedisAdapter.py` | 89 | Caché tolerante a fallos: captura `RedisConnectionError`/`TimeoutError`, avisa **una sola vez** (`_advertir_una_vez`, 42-45) y sigue sin caché. El sistema no cae si Redis está apagado. `cerrar()` (86-89) para el apagado. |
| `catalog/TramiteCatalogoAdapter.py` | 48 | Resuelve trámites desde documentos con `JOIN documentos d ON d.tramite_id = t.id WHERE d.id = ANY($1::uuid[])` (líneas 9-18), devolviendo nombre, requisitos, costo, plazo, URL y nº de documentos coincidentes. |
| `documents/DocumentStorageAdapter.py` | 41 | **Ampliado en PMV2:** guarda, lee, elimina y lista archivos bajo `DOCUMENTS_PATH` (por defecto `./storage/documentos`), con nombre seguro `uuid4 + extensión`. Cumple `AlmacenamientoDocumentosPort`. ⚠️ `eliminar()` **nunca se invoca**: la baja física borra filas pero deja el archivo en disco (D-19). |
| `extraction/ExtraccionTextoAdapter.py` | 99 | **Nuevo (PMV2).** Implementa `ExtraccionTextoPort`: PDF con `pypdf`, DOCX con `python-docx`, y `.txt`/`.md` como texto plano (UTF-8 → Latin-1 → repetición, tolerante a codificación). Si falta la librería o el archivo es escaneado/vacío, lanza `DocumentoIlegibleError`. ⚠️ **`pypdf` y `python-docx` no están en `requirements.txt`** → hoy solo `.txt`/`.md` se procesan (D-17). |

### 5.8 Capa de infraestructura — repositorios (`backend/infrastructure/repositories/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `Connection.py` | 57 | Pool `asyncpg` (min 1 / max 10). Construye el DSN desde `POSTGRES_*` (líneas 17-24). `es_pgvector()` (46-57) comprueba `to_regtype('vector')` **una vez y cachea** el resultado. |
| `PostgreSQLRepository.py` | 28 | Clase base con `ejecutar`, `obtener_uno` (fetchrow), `obtener_muchos` (fetch). Todo el SQL va parametrizado con `$1..$n` → previene inyección SQL. |
| `DocumentoRepositoryImpl.py` | 161 | `QUERY_UPSERT` (líneas 10-22) con `ON CONFLICT (id) DO UPDATE` y `COALESCE(EXCLUDED.embedding, documentos.embedding)` — **esto evita que un cambio de estado borre el embedding** (defecto corregido n.º 3, ver `04-implementado-y-por-implementar.md`). `indexado` se calcula como `(embedding IS NOT NULL)`. `_formatear_vector()` (42-51) escribe `[...]` para pgvector o `{...}` para `double[]`. |
| `ConsultaRepositoryImpl.py` | 62 | Persistencia de consultas con upsert. `QUERY_SELECT_USUARIO` ordena por fecha desc. |

### 5.9 Capa de infraestructura — controladores (`backend/infrastructure/controllers/`)

| Archivo | Líneas | Rutas que expone |
|---|---|---|
| `consulta_controller.py` | 240 | `POST /api/consultas`, `GET /api/consultas/{consulta_id}`. Ver flujo detallado en §6. |
| `tramite_controller.py` | 64 | `GET /api/tramites` (opcional `?municipalidad_id=`), `GET /api/tramites/{id}` (incluye documentos vigentes). |
| `documento_controller.py` | 184 | `POST /api/documentos`, `POST /api/documentos/upload`, `GET /api/documentos` (filtros + paginación), `PUT /api/documentos/{id}/estado`, `GET /api/documentos/{id}`, `POST /api/documentos/{id}/procesar`, `DELETE /api/documentos/{id}` (baja lógica), `DELETE /api/documentos/{id}/fisico`. |
| `documento_admin_controller.py` | 145 | **Nuevo (PMV2)**, prefijo `/api/admin/documentos`: `GET ''`, `POST ''`, `POST /upload`, `POST /{id}/procesar`, `DELETE /{id}`, `DELETE /{id}/fisico`, `PUT /{id}/estado`. ✅ `ValueError` de `EstadoDocumento(estado)` capturado → **HTTP 422** (D-18 corregido). |
| `tramite_admin_controller.py` | 91+ líneas | ✅ **Ya no es un stub**: define `router` (resuelto D-14); enlazado en `main.py` con el resto. |
| `usuario_controller.py` | 84 | `POST /api/usuarios`, `GET /api/usuarios/{id}`, `GET /api/usuarios/{id}/consultas` (historial, `LIMIT 50`). |

`main.py` incluye los **7 routers** (líneas 58-66) y el arranque termina bien: **31 rutas**
registradas (20 públicas de documentos/consultas/trámites/usuarios + 7 admin + 4 de doc).

### 5.10 Scripts de backend

| Archivo | Líneas | Función |
|---|---|---|
| `backend/scripts/indexar_documentos.py` | 52 | Genera embeddings BGE-M3 para documentos `vigente` con `embedding IS NULL` (líneas 25-31) y los persiste. Funciona con y sin pgvector (literal `[...]` o lista `double[]`). Ejecutado por `instalar.ps1` en el paso 7. |

### 5.11 Capa de API del front-end (`frontend-tramites/lib/`)

| Archivo | Líneas | Función |
|---|---|---|
| `api.ts` | 225 | **Única capa de comunicación con el back-end.** `API_URL` desde `NEXT_PUBLIC_API_URL` (línea 1). Timeouts: consulta 45 000 ms, catálogo 10 000 ms (líneas 6-7). `pedir()` (62-82) envuelve `fetch` con `AbortController` y traduce `AbortError` a un mensaje en castellano; `leerDetalle()` (53-60) extrae el `detail` del backend. `enviarConsulta()` (80-123), `obtenerTramites()` (138-141), `obtenerEstadoServicios()` (157-165). **Bloque PMV2 (líneas 167-225):** `DocumentoAdmin`, `listarDocumentosAdmin()`, `subirDocumento()`, `reprocesarDocumento()`, `eliminarDocumentoLogico()`, `eliminarDocumentoFisico()`, `listarTramitesAdmin()`. ⚠️ `pedir()` hace `response.json()` incondicional → **D-20**; y `listarTramitesAdmin()` apunta a `GET /api/tramites/admin` → **D-21**. |
| `queries.ts` | 20 | Helpers `fetchTramites()` (captura errores → `[]`) y `filtrarTramites(tramites, q, categoria)`. |

### 5.12 Rutas del front-end (`frontend-tramites/app/`)

| Archivo | Líneas | Tipo | Función |
|---|---|---|---|
| `layout.tsx` | 30 | Server | Metadata (título, descripción), `Navbar`, `<main>`, `footer` institucional. |
| `page.tsx` | 120 | Server (`force-dynamic`) | Portada. Llama a `obtenerTramites()` con `.catch(() => [])`: si la BD falla muestra 0, **nunca una lista ficticia**. Muestra nº real de trámites, mockup móvil, catálogo destacado (4 primeros), chat compacto, y sección de métricas con `KpiCard`/`MiniCharts`/`ServiceStatus`/`AuditLog`. |
| `chat/page.tsx` | 73 | Client | Página del chat + mockup móvil estático + `RobotAgent`. |
| `tramites/page.tsx` | 65 | Client | Catálogo con buscador, filtro por categoría, estados de carga/error/vacío. |
| `admin/page.tsx` | 36 | Server (`force-dynamic`) | Dashboard **mixto**: KPIs y gráficos aún ficticios (252 / 1,236 / 98 %, líneas 22-24, **D-6**) + `MiniCharts`, `ServiceStatus`, `AuditLog` y, desde `ea06c9a`, **`DocumentManager` real** (línea 32). |
| `globals.css` | 142 | CSS | Sistema de diseño "cálido/orgánico": tokens, `glass`, `card-3d`, `bubble-user`/`bubble-bot`, `avatar-muni`, `chip`, `badge-*`, `btn-*`, animaciones `typing-dot`, `animate-float-y`, `blink-eye`. |
| `tailwind.config.ts` | 122 | Config | Paleta institucional (emerald/primary/amber), sombras suaves, keyframes. |
| `next.config.js` | 9 | Config | `reactStrictMode`, expone `NEXT_PUBLIC_API_URL`. |
| `postcss.config.js` | 6 | Config | Plugin Tailwind. |
| `tsconfig.json` | 23 | Config | TypeScript estricto. |

### 5.13 Componentes del front-end (`frontend-tramites/components/`) — 16 archivos

| Archivo | Líneas | Estado | Función |
|---|---|---|---|
| `ChatBox.tsx` | 74 | ✅ real | Estado del chat (`mensajes`, `entrada`, `cargando`), llama `enviarConsulta`, muestra sugerencias rápidas y `Loading`. Ante error, **muestra el error real** con `fallo: true`. |
| `ChatThread.tsx` | 81 | ✅ real | Renderiza burbujas, `MuniAvatar`, `TypingDots`, `GroundednessBadge`, `TramiteProbableCard` y el rótulo *"Necesito que precises tu consulta"* cuando `pideAclaracion`. Auto-scroll. |
| `GroundednessBadge.tsx` | 33 | ✅ real | Badge con % real de groundedness y hasta 2 títulos de fuente + "+N fuentes". `nivelColor()` mapea ≥0.9 verde, ≥0.75 ámbar, resto azul. |
| `TramiteProbableCard.tsx` | 46 | ✅ real | Tarjeta *"Trámite identificado"* con requisitos del catálogo, arancel, plazo y enlace a la ficha oficial. |
| `TramiteCard.tsx` | 42 | ✅ real | Tarjeta de trámite del catálogo (costo, plazo, 3 primeros requisitos). No inventa etiqueta de estado. |
| `Loading.tsx` | 10 | ✅ real | Indicador *"MUN AI está consultando fuentes oficiales…"*. |
| `ServiceStatus.tsx` | 59 | ⚠️ parcial | Muestra estado real de `/health`; lo no verificado se informa como *"sin verificar"*, no como operativo. |
| `Navbar.tsx` | 55 | ✅ real | Navegación con 4 enlaces, resaltado de ruta activa, menú móvil. |
| `QuickAccessCard.tsx` | 30 | ✅ real | Tarjetas de acceso rápido. |
| `RobotAgent.tsx` | 72 | ✅ real | SVG animado del asistente (MUN AI) con parpadeo, flotación y plataforma. |
| `DocumentManager.tsx` | 135 | ⚠️ **real, bloqueado** | **Nuevo (PMV2).** Carga con metadatos (`FormData` → `subirDocumento`), tabla con `indexado`/`fragmentado`/estado, y botones *Reprocesar* / *Dar de baja* / *Eliminar*. ⚠️ El `Promise.all` incluye `listarTramitesAdmin()` (**D-21**) y los `DELETE` chocan con `pedir()` (**D-20**): hoy la tabla no carga ni borra. |
| `KpiCard.tsx` | 25 | ⚠️ maqueta | Tarjeta KPI reutilizable; los **valores** los decide quien la usa (en `/admin` son ficticios). |
| `MiniCharts.tsx` | 60 | ⚠️ maqueta | Barras, donuts y línea de tendencia con **datos fijos**. |
| `AuditLog.tsx` | 27 | ⚠️ maqueta | 5 filas **hardcodeadas** ("Consulta #8.412…"). No consume la API. |
| `DragDropUpload.tsx` | 39 | ⚠️ maqueta | Arrastrar/soltar y selector de archivos, pero **solo guarda nombres en estado local**; no llama a la API (**G-12**). El que sí la llama es `DocumentManager`. |
| `icons.tsx` | 217 | ✅ real | 20 iconos SVG: `AlertIcon`, `AyudaIcon`, `ChartIcon`, `ChatIcon`, `CheckIcon`, `ClockIcon`, `CloseIcon`, `DirectorioIcon`, `DocIcon`, `HeartIcon`, `LinkIcon`, `MenuIcon`, `OrdenanzaIcon`, `SearchIcon`, `SendIcon`, `ShieldIcon`, `SparkIcon`, `TramiteIcon`, `UploadIcon`, `UsersIcon`. |

---

## 6. Flujo del back-end

### 6.1 Flujo principal: `POST /api/consultas` (RAG completo)

Este es el flujo más importante del sistema. Cada paso indica el archivo y las líneas donde ocurre.

```text
  Cliente (ChatBox.tsx)          POST /api/consultas {"pregunta": "..."}
          │
          ▼
  consulta_controller.crear_consulta()          [consulta_controller.py:94-161]
          │
          ├─(1) VALIDACIÓN      ConsultaRequest exige min_length=3   [consulta_controller.py:16-18]
          │
          ├─(2) CLASIFICACIÓN    ClasificarIntencion.ejecutar_detallado()
          │                       └─> ServicioNLP.clasificar()      [ServicioNLP.py:90-121]
          │                           normaliza → puntúa 9 intenciones → confianza 0.55-1.0
          │                           ¿empate o OTRO o confianza<0.5? → requiere_aclaracion
          │                                                   [ClasificacionIntencion.py:22-29]
          │                           ★ Si requiere aclaración, el flujo salta al paso (3-bis)
          │
          ├─(3) PERSISTENCIA     RegistrarConsulta.ejecutar()       [RegistrarConsulta.py:17-34]
          │                       └─> ConsultaRepositoryImpl.guardar() → INSERT consultas
          │                           (id=uuid4, creada_en=now UTC, intencion) 
          │
          ├─(4) CACHÉ            ServicioCache.obtener_respuesta()  [consulta_controller.py:115]
          │                       clave = "consulta:" + sha256(pregunta normalizada)
          │                       ├─ HIT + cuerpo válido → audita y devuelve   (líneas 122-130)
          │                       ├─ HIT + cuerpo corrupto → invalida y recalcula (118-121)
          │                       └─ MISS → sigue al paso (5)
          │
          ├─(5) ORIENTACIÓN      GenerarOrientacion.ejecutar()      [GenerarOrientacion.py:16-29]
          │       └─> ServicioOrientacion.orientar()                [ServicioOrientacion.py:34-72]
          │           │
          │           ├─(5a) ¿requiere_aclaracion? → Respuesta con ACLARACION_AMBIGUA,
          │           │         pide_aclaracion=true, SIN fuentes, SIN generar
          │           │                                             [ServicioOrientacion.py:41-42, 74-88]
          │           │
          │           ├─(5b) RECUPERACIÓN  ServicioRAG.recuperar()  [ServicioRAG.py:25-28]
          │           │       └─> BusquedaVectorialAdapter.buscar() [BusquedaVectorialAdapter.py:81-86]
          │           │           embedding de la pregunta (BGE-M3, 1024 dims)
          │           │           ¿pgvector? → operador <=> con índice HNSW
          │           │           ¿no?      → coseno con numpy sobre double precision[]
          │           │           filtro: estado='vigente' AND embedding IS NOT NULL
          │           │           umbral de similitud 0.3, top_k = RAG_TOP_K (5)
          │           │           → segundo filtro esta_vigente() en ServicioRAG
          │           │
          │           ├─(5c) GENERACIÓN    ServicioSLM.generar()     [ServicioSLM.py:27-35]
          │           │       └─> OllamaAdapter.generar()          [OllamaAdapter.py:30-46]
          │           │           POST localhost:11434/api/generate, qwen2.5:3b
          │           │           temperature 0.2 · num_predict 512
          │           │           sin contexto → texto de abstención
          │           │
          │           ├─(5d) FUENTES      ServicioRAG.construir_fuentes() [ServicioRAG.py:43-56]
          │           │       Fuente(url_origen, fragmento=contenido[:280], titulo)
          │           │
          │           ├─(5e) GROUNDEDNESS  EvaluadorGroundedness     [EvaluadorGroundedness.py:18-42]
          │           │       cobertura léxica → ALTA ≥0.75 | MEDIA ≥0.40 | BAJA
          │           │       ★ si BAJA y hay fuentes → anexa nota de advertencia al texto
          │           │                                                        [ServicioOrientacion.py:49-54]
          │           │
          │           ├─(5f) TRÁMITE PROBABLE IdentificarTramiteProbable.ejecutar()
          │           │       [IdentificarTramiteProbable.py:26-54]
          │           │       ├─> TramiteCatalogoAdapter.buscar_por_documentos()
          │           │       │       JOIN documentos d ON d.tramite_id = t.id
          │           │       │       [TramiteCatalogoAdapter.py:9-18]
          │           │       ├─ puntúa sumando similitud de cada documento      (56-72)
          │           │       ├─ descarta si < 0.45 (PUNTAJE_MINIMO)
          │           │       └─ descarta si no supera al 2º por 1.15× (MARGEN_MINIMO)
          │           │          → si no domina: tramite_probable = null
          │           │
          │           └─(5g) DATOS ESTRUCTURADOS Respuesta.con_datos_estructurados()
          │                   anexa requisitos numerados + arancel + plazo + ficha,
          │                   TOMADOS DE LA BASE DE DATOS, no del redactado del modelo
          │                                                       [Respuesta.py:26-61]
          │
          ├─(6) AUDITORÍA        AuditarConsulta.ejecutar()          [consulta_controller.py:152]
          │       └─> _AuditoriaPostgreSQL.registrar()  [container.py:59-69]
          │           INSERT auditoria_consultas (respuesta, confianza, fuentes=urls)
          │
          ├─(7) CACHÉ (escritura)  ServicioCache.guardar_respuesta() [consulta_controller.py:155]
          │
          └─(8) RESPUESTA        _cuerpo_respuesta()                [consulta_controller.py:60-91]
                  RespuestaResponse { texto, confianza, groundedness, confianza_intencion,
                                      pide_aclaracion, fuentes[{url,fragmento,titulo}],
                                      tramite_probable, consulta_id, intencion }
```

**Manejo de errores del flujo** (`consulta_controller.py`):

| Situación | Respuesta | Referencia |
|---|---|---|
| Ollama caído / no responde | **HTTP 503** con mensaje en castellano "El asistente no está disponible…" | líneas 139-149 |
| Pregunta vacía o < 3 caracteres | **HTTP 422** (validación Pydantic) | líneas 16-18 |
| `ValueError` de los casos de uso | **HTTP 400** | líneas 160-161 |
| Entrada de caché corrupta | Se **invalida y recalcula** (no se devuelve error) | líneas 117-121 |

**Caso especial — respuesta de aclaración (paso 5a).** Cuando `ClasificacionIntencion.requiere_aclaracion`
es verdadero, el sistema **no genera respuesta ni cita fuentes**: devuelve `ACLARACION_AMBIGUA`,
`pide_aclaracion: true`, `confianza: media`, `groundedness: 0.0` y `fuentes: []`
(`ServicioOrientacion.py:74-88`). El front lo rotula *"Necesito que precises tu consulta"*
(`ChatThread.tsx:65-69`).

**Llamada sobre caché (paso 4 HIT).** Para mantener trazabilidad completa, la auditoría se
ejecuta **también** en el acierto de caché: se reconstruye una `Respuesta` mínima con
`_respuesta_desde_cuerpo()` (líneas 179-221) y se registra en `auditoria_consultas`.

### 6.2 Los 27 endpoints de API (18 públicos + 9 admin) + 4 de documentación = 31 rutas

> ✅ **Todos servibles hoy (17-oct-2026, verificado en vivo contra `/openapi.json`):** la tabla
> describe el código escrito. Las 4 rutas extra son las de documentación
> (`/docs`, `/redoc`, `/openapi.json`, `/docs/oauth2-redirect`).

**Públicos (18):**

| # | Método | Ruta | Archivo:línea | Función |
|---|---|---|---|---|
| 1 | POST | `/api/consultas` | `consulta_controller.py` | Consulta RAG completa (flujo §6.1) |
| 2 | GET | `/api/consultas` | `consulta_controller.py` | **Listado de auditoría (HU-10/HU-14 ✅):** últimas consultas con su respuesta auditada (texto, confianza, groundedness, fuentes, banderas de bloqueo/fuera de dominio); `?limite=` (1..100) |
| 3 | GET | `/api/consultas/{id}` | `consulta_controller.py` | **Trazabilidad completa (HU-10/D-9 ✅):** la consulta **más** `respuesta`, `confianza`, `groundedness`, `fuentes` (con número/fecha/versión), `afirmaciones_bloqueadas`, `fuera_dominio`, `entidad_sugerida` y `registrado_en` |
| 4 | GET | `/api/tramites` | `tramite_controller.py:31` | Catálogo; filtro opcional `?municipalidad_id=` |
| 5 | GET | `/api/tramites/{id}` | `tramite_controller.py:43` | Detalle + documentos vigentes del trámite |
| 6 | GET | `/api/tramites/{id}/relacionados` | `tramite_controller` | Trámites relacionados por similitud (HU-12 ✅; embedding + fallback léxico, orden decreciente) |
| 7 | POST | `/api/documentos` | `documento_controller.py:55` | Registra documento **y genera su embedding**; 422 si formato/lectura inválidos |
| 8 | POST | `/api/documentos/upload` | `documento_controller.py:84` | Valida extensión, extrae texto, guarda archivo, registra, indexa y fragmenta (PMV2) |
| 9 | GET | `/api/documentos` | `documento_controller.py:115` | Listado con filtros `tramite_id`/`estado`/`incluir_eliminados` + `limite`/`desde` |
| 10 | PUT | `/api/documentos/{id}/estado` | `documento_controller.py:134` | Cambia `vigente`/`obsoleto`/`en_revision`/`derogado` |
| 11 | GET | `/api/documentos/{id}` | `documento_controller.py:148` | Detalle de un documento |
| 12 | POST | `/api/documentos/{id}/procesar` | `documento_controller.py:159` | Reprocesa: fragmenta + embeddea (PMV2) |
| 13 | DELETE | `/api/documentos/{id}` | `documento_controller.py:171` | **Baja lógica** (marca `eliminado_en`); 204 (PMV2) |
| 14 | DELETE | `/api/documentos/{id}/fisico` | `documento_controller.py:179` | **Baja física** de filas (borra fragmentos); 204 (PMV2) |
| 15 | POST | `/api/usuarios` | `usuario_controller.py:48` | Registro; valida rol con regex `^(ciudadano\|administrador)$` |
| 16 | GET | `/api/usuarios/{id}` | `usuario_controller.py:66` | Detalle de usuario |
| 17 | GET | `/api/usuarios/{id}/consultas` | `usuario_controller.py:77` | Historial del usuario (`LIMIT 50`) |
| 18 | GET | `/health` | `main.py:71` | `{"status":"ok"}` — **no** comprueba BD, Redis ni Ollama |

**Administración (9):**

| # | Método | Ruta | Archivo:línea | Función |
|---|---|---|---|---|
| 19 | GET | `/api/admin/documentos` | `documento_admin_controller.py:39` | Listado con filtros y paginación (hasta 500) |
| 20 | POST | `/api/admin/documentos` | `documento_admin_controller.py:59` | Crea por JSON y procesa en segundo plano (ignora fallos de fragmentado) |
| 21 | POST | `/api/admin/documentos/upload` | `documento_admin_controller.py:86` | Carga con `multipart/form-data` (`tramite_id`, `titulo`, `url_origen`, `version`, `fecha_publicacion`, `estado`, `archivo`) |
| 22 | POST | `/api/admin/documentos/{id}/procesar` | `documento_admin_controller.py:117` | Reprocesa un documento (404 si no existe) |
| 23 | PUT | `/api/admin/documentos/{id}/estado` | `documento_admin_controller` | Cambia estado con validación (422 si inválido o sin metadatos) — **P2-11 ✅** |
| 24 | DELETE | `/api/admin/documentos/{id}` | `documento_admin_controller.py:129` | Baja lógica; 204 |
| 25 | DELETE | `/api/admin/documentos/{id}/fisico` | `documento_admin_controller.py:137` | Baja física; 204 |
| 26 | GET | `/api/tramites/admin` | `tramite_admin_controller.py:40` | Listado ampliado para el panel admin (272 filas) |
| 27 | PUT | `/api/tramites/{id}/area` | `tramite_admin_controller.py:49` | Actualiza `area_responsable` (migración 005; HU-07 ✅) |

Los 9 admin **repiten** la funcionalidad pública bajo otro prefijo (7 bajo `/api/admin/documentos` y
2 bajo `/api/tramites`): son la superficie que el panel `DocumentManager.tsx` consume (✅ verificado
en vivo). Ninguno valida autenticación ni rol.

Documentación interactiva: <http://localhost:8000/docs> (Swagger, automático por FastAPI).

> ⚠️ **Ningún endpoint valida autenticación ni rol.** `es_administrador()` existe en
> `Usuario.py:16` pero no se invoca en ningún punto (**D-8**), y `container.py` expone el
> contenedor completo a cualquier petición.

---

## 7. Flujo de la base de datos

### 7.1 Migraciones

| Archivo | Contenido |
|---|---|
| `database/migrations/001_create_database.sql` | Crea la BD `tramites_municipales` si no existe (`\gexec`), se conecta y ejecuta `CREATE EXTENSION IF NOT EXISTS vector`. |
| `database/migrations/002_create_tables.sql` | Crea las 6 tablas, los 5 índices de apoyo (líneas 76-80) y decide el tipo de columna del embedding (líneas 84-94): `vector(1024)` si la extensión existe, si no `double precision[]`. |
| `database/migrations/003_create_vectors.sql` | Índice **HNSW** `idx_documentos_embedding_hnsw ON documentos USING hnsw (embedding vector_cosine_ops)` solo si hay pgvector; deja comentada la alternativa IVFFlat; añade `idx_tramites_tipo`. |
| `database/migrations/004_documentos_pmv2.sql` | **(PMV2), 29 líneas — ✅ CORREGIDA Y APLICADA (16-oct-2026).** Añade a `documentos` las columnas `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`, `fragmentado`, `eliminado_en`; crea la tabla `fragmentos_documento` con su índice; y reescribe el `CHECK` de `estado` para admitir `derogado`. Su línea 1 era un docstring Python → corregida a `--` (D-15); verificado: 20/20 documentos con metadatos. |
| `database/migrations/005_area_responsable.sql` | **Nuevo, ✅ APLICADO (16-oct-2026):** añade `area_responsable` a `tramites` y la expone en las respuestas (HU-07 ✅); 259/272 trámites con área. |
| `database/migrations/006_auditoria_trazabilidad.sql` | **Nuevo, ✅ APLICADO (17-oct-2026):** HU-10 — añade a `auditoria_consultas` las columnas `groundedness`, `fuentes_detalle JSONB`, `fuera_dominio`, `afirmaciones_bloqueadas` y `entidad_sugerida`, más índices por `consulta_id` y `registrado_en`. |
| `database/schema.sql` | Referencia consolidada del esquema (documentación, no se ejecuta). |

**Verificación (16-oct-2026, PostgreSQL local `tramites_municipales`):** `information_schema.columns`
de `documentos` devuelve **8 columnas** (sin metadatos), `fragmentos_documento` → relación inexistente,
y el `CHECK` de `estado` sigue en `(vigente, obsoleto, en_revision)`. Es decir: **004 no se ejecutó**
en ninguna BD.

### 7.2 Las 6 tablas base (+1 del PMV2)

| Tabla | Columnas | Relaciones |
|---|---|---|
| `municipalidades` | `id`, `nombre`, `departamento`, `provincia`, `distrito`, `sitio_web`, `creado_en` | — |
| `usuarios` | `id`, `nombre`, `correo` UNIQUE, `rol` CHECK in (ciudadano, administrador), `creado_en` | — |
| `tramites` | `id`, `municipalidad_id`, `nombre`, `descripcion`, `tipo`, `requisitos TEXT[]`, `costo NUMERIC(10,2)`, `duracion_estimada_dias INT`, `creado_en` | FK → `municipalidades` |
| `documentos` | `id`, `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado` CHECK in (vigente, obsoleto, en_revision), `embedding`, `actualizado_en` · **PMV2 (+7):** `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`, `fragmentado`, `eliminado_en` | FK → `tramites` |
| `consultas` | `id`, `usuario_id` (nullable), `pregunta`, `intencion`, `creada_en` | FK → `usuarios` (ON DELETE SET NULL) |
| `auditoria_consultas` | `id`, `consulta_id`, `respuesta`, `confianza` CHECK, `fuentes` TEXT, `registrado_en` | FK → `consultas` (CASCADE) |
| `fragmentos_documento` **(PMV2)** | `id`, `documento_id`, `orden`, `contenido`, `embedding vector(1024)`, `creado_en` | FK → `documentos` (ON DELETE CASCADE) |

Los 8 metadatos y `fragmentos_documento` **existen solo en el archivo 004**, no en la BD local
(**D-15**). Las consultas de escaneo y listado que filtran `eliminado_en IS NULL` fallarán con
`UndefinedColumn` hasta aplicar 004.

Índices: `idx_tramites_municipalidad`, `idx_documentos_tramite`, `idx_documentos_estado`, `idx_consultas_usuario`, `idx_consultas_creada_en`, `idx_tramites_tipo`, `idx_documentos_embedding_hnsw`, `idx_fragmentos_documento` (PMV2).

### 7.3 Semilla de datos (seeds)

| Archivo | Volumen | Contenido |
|---|---|---|
| `seeds/municipios.sql` | **1** Municipalidad | ⚠️ Sigue insertando *"Municipalidad Provincial de Junín"* (líneas 3, 10-11). `scripts/actualizar_huancayo.sql` lo corrige a Huancayo. |
| `seeds/tramites.sql` | **22** trámites | 5 registros civiles, 4 certificados/tributos, 4 licencias, 4 urbanismo, 2 comercio/eventos, 3 otros. Todos con `costo 0.00` (§13.4) y plazos de 1 a 30 días. |
| `seeds/documentos.sql` | **20** documentos | Textos de Procedimientos Administrativos por trámite, con `url_origen` del portal oficial, pensados para indexarse. |
| `seeds/documentos_mph.sql` | **19** documentos | Trámites y servicios MPH con requisitos, costo, pasos y vigencia (fuente: clippings gob.pe). |
| `seeds/tramites_servicios.sql` | **6** trámites | Servicios MPH fuera del TUPA (mesa de partes, carnet de sanidad, carnet/TUC de conductor, videos de seguridad). |
| `seeds/documentos_institucionales.sql` | **6** documentos (+1 servicio) | Contenido institucional MPH: catálogo oficial de gob.pe, contacto/sedes/horarios, emergencias, canales en línea, Portal de Transparencia y TUPA. Crea el servicio "Información institucional y contacto" porque `documentos.tramite_id` es NOT NULL. |

**Correspondencia catálogo ↔ documentos:** cada documento tiene `tramite_id`, que es el puente que permite a `IdentificarTramiteProbable` resolver el trámite y traer sus datos estructurados.

### 7.4 Consulta vectorial

Dos modos, mismos resultados lógicos:

```sql
-- Con pgvector (producción): índice HNSW aceleraría esta consulta
SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
       1 - (embedding <=> $1::vector) AS similitud
FROM documentos
WHERE embedding IS NOT NULL AND estado = 'vigente'
ORDER BY embedding <=> $1::vector
LIMIT $2;                                  -- filtra similitud >= 0.3 en Python
```

Sin pgvector: `BusquedaVectorialAdapter._buscar_en_memoria()` trae todos los embeddings vigentes,
calcula el coseno con numpy (`_coseno`, líneas 40-52), ordena y corta en `top_k`. Es correcto para
catálogos pequeños, pero **no escala**: con 20 documentos es viable; con miles sería un cuello de botella.

### 7.5 Escritura de documentos (upsert)

`DocumentoRepositoryImpl.QUERY_UPSERT` (líneas 10-22) usa `ON CONFLICT (id) DO UPDATE` con
`COALESCE(EXCLUDED.embedding, documentos.embedding)`: actualizar el estado de un documento **no
destruye** su embedding (defecto corregido n.º 3). `indexado` se deriva de `(embedding IS NOT NULL)`
porque los `SELECT` no necesitaban devolver el vector completo.

---

## 8. Flujo del front-end

### 8.1 Mapa de rutas

| Ruta | Archivo | Render | Datos | Estado |
|---|---|---|---|---|
| `/` | `app/page.tsx` | Server (`force-dynamic`) | `GET /api/tramites` | ✅ real |
| `/chat` | `app/chat/page.tsx` | Client | vía `ChatBox` | ✅ real |
| `/tramites` | `app/tramites/page.tsx` | Client | `GET /api/tramites` | ✅ real |
| `/admin` | `app/admin/page.tsx` | Server | KPIs/gráficos ficticios + **`DocumentManager` con datos reales** | ⚠️ mixto (D-6 / G-12) |

Rutas faltantes (brecha **G-11**): `/login`, `/tramites/[id]`, `/404`, `/mis-consultas` (**G-10**), sub-rutas `/admin/*`.

### 8.2 Flujo de una consulta desde el navegador

```text
 1. Usuario escribe y pulsa "Enviar" (o un chip de sugerencia)
       ChatBox.handleEnviar()                      [ChatBox.tsx:14-39]
          · guarda la pregunta como burbuja de usuario
          · setCargando(true) → Loading + TypingDots visibles

 2. enviarConsulta(pregunta)                        [api.ts:90-113]
       · POST http://localhost:8000/api/consultas  { pregunta }
       · AbortController con 45 000 ms              [api.ts:6, 62-82]
       · si !response.ok → lee el `detail` del backend y lo muestra
       · si AbortError → "La consulta está tardando demasiado…"

 3. Respuesta del backend (200)
       · texto, confianza, groundedness, confianza_intencion
       · pide_aclaracion, intencion, tramite_probable, fuentes[]

 4. ChatBox la convierte en mensaje del asistente   [ChatBox.tsx:22-27]

 5. ChatThread renderiza cada mensaje              [ChatThread.tsx:57-77]
       · pideAclaracion  → rótulo ámbar "Necesito que precises tu consulta"
       · tramiteProbable → TramiteProbableCard (datos de la BD)
       · groundedness+fuentes → GroundednessBadge (% real + títulos)
       · fallo → borde ámbar y sin badge

 6. Si el backend falla → burbuja con `fallo: true` y el mensaje real
       "No pude responder: <detalle real>"        [ChatBox.tsx:28-35]
       ★ Nunca se muestra una respuesta ficticia (D-1 corregido)
```

### 8.3 Capa de contrato HTTP (`lib/api.ts`)

| Función | Endpoint | Timeout | Notas de diseño |
|---|---|---|---|
| `enviarConsulta` | `POST /api/consultas` | 45 s | Sin fallback; propaga el error real |
| `obtenerTramites` | `GET /api/tramites` | 10 s | Mapea con `mapearTramite` |
| `obtenerEstadoServicios` | `GET /health` | 10 s | Solo la API es verificable; el resto = "sin verificar" |
| `listarDocumentosAdmin` | `GET /api/admin/documentos` | 10 s | Filtros `incluir_eliminados`, `limite`, `desde` (PMV2) |
| `subirDocumento` | `POST /api/admin/documentos/upload` | 10 s | `multipart/form-data` con metadatos (PMV2) |
| `reprocesarDocumento` | `POST /api/admin/documentos/{id}/procesar` | 10 s | Devuelve el documento (PMV2) |
| `eliminarDocumentoLogico` / `eliminarDocumentoFisico` | `DELETE /api/admin/documentos/{id}` y `…/{id}/fisico` | 10 s | ⚠️ **D-20**: 204 sin cuerpo rompe `pedir()` |
| `listarTramitesAdmin` | `GET /api/tramites/admin` | 10 s | ⚠️ **D-21**: ruta inexistente → 500 |

Interfaces TypeScript exportadas: `FuenteCitada`, `TramiteProbable`, `RespuestaConsulta`, `Tramite`, `EstadoServicios`.
Constante `SUGERENCIAS_RAPIDAS` (líneas 46-51): 4 preguntas de ejemplo.

### 8.4 Sistema de diseño

`app/globals.css` (127 líneas) define la identidad visual "cálida/orgánica":

| Clase | Uso |
|---|---|
| `glass` / `glass-strong` | Paneles translúcidos con `backdrop-blur` |
| `card-3d` / `btn-primary-3d` / `btn-neu` / `btn-emerald-3d` | Superficies con sombra y relieve |
| `bubble-user` / `bubble-bot` | Burbujas del chat |
| `avatar-muni` | Avatar del asistente (SVG en `ChatThread.tsx:19-31`) |
| `chip` / `badge-blue` / `badge-emerald` / `badge-amber` | Etiquetas |
| `skeleton` | Estado de carga del catálogo |
| `eyebrow` / `h-display` / `text-gradient-warm` | Jerarquía tipográfica |
| `animate-rise-in` / `typing-dot` / `animate-float-y` / `blink-eye` / `animate-pulse-ring` | Animaciones |

`tailwind.config.ts` (119 líneas) define los tokens de color (paleta emerald/primary/amber), sombras suaves y los keyframes.

Accesibilidad: `aria-label` en inputs y botones, `role="status"` en el indicador de carga, `role="img"` en el robot, `html lang="es"`. **No hay auditoría WCAG formal** (brecha G-26).

---

## 9. Flujo de instalación y ejecución

### 9.1 Instalador de un solo comando

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```

`instalar.ps1` (225 líneas) es **idempotente**: se puede repetir sin romper nada. Parámetros:
`-PostgresUser`, `-PostgresPassword`, `-AppUser`, `-AppPassword`, `-AppDatabase`, `-OllamaModel` (por defecto `qwen2.5:3b`), `-SinIndexar`.

| # | Paso | Qué hace | Líneas |
|---|---|---|---|
| 1/7 | Verificar herramientas | Comprueba `python`, `psql`, `node`, `npm`, `ollama`; `redis-server` es **opcional**. Si falta algo crítico, termina con código 1. | 62-82 |
| 2/7 | Archivo de configuración | Copia `.env.example` → `.env` si no existe. | 85-91 |
| 3/7 | Base de datos | Crea el rol `tramites`, la base `tramites_municipales`, y aplica en orden: `002_create_tables.sql`, `003_create_vectors.sql`, `seeds/municipios.sql`, `seeds/tramites.sql`, `seeds/documentos.sql` con `ON_ERROR_STOP=1`. **No aplica `004_documentos_pmv2.sql`** (líneas 94-137) **ni los seeds MPH/institucionales** → una instalación limpia queda sin los metadatos, sin `fragmentos_documento` y sin los 25 documentos ni los 7 servicios nuevos (**D-16**). | 94-137 |
| 4/7 | Dependencias Python | Crea `.venv` y ejecuta `pip install -r requirements.txt`. | 140-149 |
| 5/7 | Dependencias front-end | `npm install` en `frontend-tramites`. | 152-160 |
| 6/7 | Redis y Ollama | Comprueba puertos 6379/11434; arranca lo que falte; descarga el modelo `qwen2.5:3b`. | 163-190 |
| 7/7 | Embeddings | Ejecuta `python -m backend.scripts.indexar_documentos` (descarga BGE-M3 ~2,3 GB la primera vez). Se salta con `-SinIndexar`. | 193-200 |

Al final resume los fallos y muestra las URLs de arranque (líneas 202-225).

### 9.2 Ejecución

```powershell
# Terminal 1 — API
.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000

# Terminal 2 — front-end
cd frontend-tramites; npm run dev
```

| Servicio | URL |
|---|---|
| App | <http://localhost:3000> |
| API | <http://localhost:8000> |
| Swagger | <http://localhost:8000/docs> |

Comprobación: `curl http://localhost:8000/health` → `{"status":"ok"}`.

### 9.3 Alternativa con Docker

```bash
docker compose up -d      # postgres+pgvector, redis, ollama
```

`docker-compose.yml` define 3 servicios con healthchecks y volúmenes (`pgdata`, `redisdata`, `ollamadata`); monta `./database/migrations` en `docker-entrypoint-initdb.d` para ejecutar las migraciones automáticamente al primer arranque. Hay un bloque comentado para acelerar el SLM con GPU NVIDIA.

### 9.4 Variables de entorno (`.env.example`)

| Variable | Por defecto | Uso |
|---|---|---|
| `POSTGRES_HOST` / `_PORT` / `_USER` / `_PASSWORD` / `_DB` | localhost / 5432 / tramites / tramites / tramites_municipales | DSN en `Connection.py:17-24` |
| `REDIS_URL` | `redis://localhost:6379/0` | `RedisAdapter.py:32` |
| `CACHE_TTL_SEGUNDOS` | 3600 | `ServicioCache` vía `container.py:129` |
| `OLLAMA_URL` | `http://localhost:11434` | `OllamaAdapter.py:26` |
| `OLLAMA_MODEL` | `qwen2.5:3b` | `OllamaAdapter.py:27` |
| `EMBEDDING_MODEL` | `BAAI/bge-m3` | `BGE_M3Adapter.py:17-19` |
| `EMBEDDING_DEVICE` | `cpu` | `BGE_M3Adapter.py:20` |
| `RAG_TOP_K` | 5 | `container.py:120` |
| `DOCUMENTS_PATH` | `./storage/documentos` | `DocumentStorageAdapter.py:12` |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | `lib/api.ts:1` |
| `OPENAI_API_KEY` | — (sin valor: se usa BGE-M3 local) | `container.py:227`, `indexar_documentos.py:50` |
| `OPENAI_BASE_URL` | — (nube: `https://openrouter.ai/api/v1`) | `OpenAIEmbeddingsAdapter.py:30` |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-3-small` | `OpenAIEmbeddingsAdapter.py:28` |
| `OPENAI_EMBEDDING_DIMENSIONS` | 1536 (nube: `1024`, igual que `vector(1024)`) | `OpenAIEmbeddingsAdapter.py:33` |
| `OPENROUTER_API_KEY` | — (si existe se usa OpenRouter, si no Ollama) | `container.py:234` |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.3-70b-instruct` | `OpenRouterAdapter.py:34` |
| `VERCEL_FRONTEND_URL` | — (origen CORS permitido en producción) | `main.py:52` |

### 9.5 Rendimiento medido

| Operación | Latencia |
|---|---|
| Consulta repetida (acierto de caché) | **~5-30 ms** |
| Consulta nueva (embeddings + pgvector + SLM en CPU) | **4-17 s** (típicamente 4-14 s) |
| `GET /api/tramites` | < 100 ms |

> La latencia la domina el SLM en CPU: con GPU (bloque comentado en `docker-compose.yml:48-55`) baja sustancialmente. El objetivo de < 3 s de HU-06 **no es medible hoy** porque no existe instrumentación de latencia (brecha **G-16**).

### 9.6 Despliegue en la nube (Render + Vercel — 25-oct-2026)

| Pieza | Servicio | URL / identificador | Plan |
|---|---|---|---|
| Back-end FastAPI | Render Web Service `tramites-municipales-backend` (`srv-dbf916navr4c73d8lh90`), región Ohio, `rootDir: backend`, auto-deploy en `main` | <https://tramites-municipales-backend.onrender.com> | free (**512 MB**) |
| Base de datos | Render Postgres 18 + pgvector 0.8.7 (`dpg-dbe62savcj2c73br3tog-a`) | — | free (**caduca 2026-11-23**; reanudar/renombrar desde el dashboard) |
| Front-end Next.js | Vercel (`bl-inderex/tramites-municipales-frontend`, repo GitHub conectado) | <https://tramites-municipales-frontend.vercel.app> | Hobby |
| Embeddings | OpenRouter `openai/text-embedding-3-small` con `dimensions=1024` (calza con `vector(1024)`) | — | pago por uso |
| Generación de respuesta | OpenRouter `meta-llama/llama-3.3-70b-instruct` (`OPENROUTER_MODEL`) | — | pago por uso (≈ US$0.0003/consulta) |

**Por qué embeddings por API.** El plan free de Render da 512 MB: BGE-M3 (2,3 GB) y torch (~2,5 GB en build) no caben ni en la build ni en runtime (los deploys previos fallaban en `pip install`). El repo ya traía `OpenAIEmbeddingsAdapter`, que ahora es el generador por defecto cuando existe `OPENAI_API_KEY` (switch en `container.py:227` y `scripts/indexar_documentos.py:50`); sin esa variable se sigue usando `BGE_M3Adapter` local. El adaptador soporta `OPENAI_BASE_URL` (compatible con OpenRouter) y `OPENAI_EMBEDDING_DIMENSIONS=1024`.

**Split de dependencias.** `requirements.txt` (slim: `openai==1.109.1`, sin torch) es lo que instala Render; `requirements-ml.txt` (`sentence-transformers==3.0.1`) lo añaden el `Dockerfile`, el entorno local y la imagen de Fly.io, que siguen con BGE-M3 pre-cargado.

**Datos en la nube** (espejo del entorno local canónico): migración `supabase_complete_setup.sql` + 6 seeds → **272 trámites, 45 documentos**; indexación con la API → 45 embeddings; reproceso (`ProcesarDocumento`) → **56 fragmentos con embedding**, los que consulta el RAG.

**Correcciones necesarias durante el despliegue:**

| Síntoma | Causa | Corrección |
|---|---|---|
| Runtime `NameError: SentenceTransformer` | `BGE_M3Adapter` anotaba una clase inexistente sin `sentence-transformers` | `from __future__ import annotations` en `BGE_M3Adapter.py` |
| `POST /api/consultas` → 400 (`ascii codec can't encode`) | httpx codifica *headers* en ASCII y `X-Title` contenía «Municipa**á**l…» | `X-Title` sin acentos (`OpenRouterAdapter.py:65`) |
| Generación → 404 en `/chat/completions` | `meta-llama/llama-3-8b-instruct` ya no existe en OpenRouter | default `meta-llama/llama-3.3-70b-instruct` |

**Degradación conocida en la nube:** sin Redis la caché se deshabilita con aviso en logs (funciona igual, más lento); sin `SUPABASE_SERVICE_ROLE_KEY` los archivos se guardan en disco efímero.

**⚠️ Umbrales RAG a recalibrar:** `umbral_similitud = 0.3`, `UMBRAL_CONFIANZA_ALTA = 0.75` y `UMBRAL_CONFIANZA_MEDIA = 0.40` se calibraron sobre vectores BGE-M3; el espacio de `text-embedding-3-small` es distinto. Medición del 25-oct-2026 en producción: consulta de prueba → `groundedness 0.473` (confianza MEDIA) con 5 fuentes y trámite probable correcto. Conviene repetir la medición con el set de consultas de referencia antes de dar los umbrales por buenos.

**Reconstrucción desde cero (CLI autenticados):** `render services create` (env vars `POSTGRES_*`, `OPENAI_*`, `OPENROUTER_API_KEY`, `VERCEL_FRONTEND_URL`) → psql con `supabase_complete_setup.sql` y `database/seeds/*.sql` → `python -m backend.scripts.indexar_documentos` con las mismas env → reproceso de fragmentos → `vercel deploy --prod` con `NEXT_PUBLIC_API_URL` apuntando al back-end.

### 9.7 Fallback al catálogo para trámites sin documentos indexados (26-oct-2026)

**Problema detectado en producción:** solo **37 de 272 trámites** tienen documentos indexados (56 fragmentos). Una consulta como «Adopción Judicial o Notarial» no tenía fragmentos propios: el RAG recuperaba documentos de otros trámites (similitud floja ≥ 0.3), el SLM hablaba sin respaldo y el guardián de groundedness bloqueaba la respuesta (o se pedía aclaración). El catálogo (`tramites`) sí tenía los datos verificados: arancel S/ 44.00, plazo de 5 días, 2 requisitos, Sub Gerencia de Registro Civil.

**Solución (commit `22bdd9c`):** `TramiteCatalogoPort.buscar_por_texto` + implementación en `TramiteCatalogoAdapter` — búsqueda léxica sobre el nombre de los trámites (cobertura de tokens ≥ `COBERTURA_MINIMA_NOMBRE = 0.6`, margen ≥ `MARGEN_MINIMO_CATALOGO = 1.15` contra el segundo candidato). `ServicioOrientacion` lo usa como fallback en los dos puntos donde antes se rendía (consulta general sin documentos y respuesta bloqueada por bajo groundedness): si el catálogo nombra el trámite, responde con requisitos/arancel/plazo/área estructurados, fuente citable (ficha sintética del catálogo) y `tramite_probable` para la tarjeta del front.

**Medido en producción (26-oct-2026):**

| Consulta | Antes | Después |
|---|---|---|
| `Adopción Judicial o Notarial` | pide aclaración, 0 fuentes | groundedness 0.872, confianza ALTA, 1 fuente, trámite probable correcto |
| `¿Cuánto cuesta y en cuántos días…adopción judicial?` | bloqueo anti-alucinación | igual que arriba |
| `¿Qué requisitos…licencia de funcionamiento?` | RAG (sin cambio) | RAG, groundedness 0.646, 5 fuentes (sin regresión) |
| `quiero adoptar a un menor` (difusa) | pide aclaración | pide aclaración (el léxico no la resuelve; pendiente búsqueda semántica sobre el catálogo) |

**Timeouts del front:** Render free se duerme a los 15 min y el arranque en frío tarda ~30-60 s → `TIMEOUT_CATALOGO_MS` 10 s → **60 s** y `TIMEOUT_CONSULTA_MS` 45 s → **90 s** (`frontend-tramites/lib/api.ts`, commit `f4be69c`).

---

## 10. Estado actualizado de las 18 HU y los 3 PMV

### 10.1 Método de medición

Cada HU se descompone en **puntos de verificación objetivos** (sección Backend, Frontend, BD). Cada
punto corresponde a un archivo o una comprobación concreta, verificable con `grep`:

```
% avance de la HU = puntos ✅ / (puntos ✅ + puntos ❌) × 100
% global          = Σ puntos ✅ / Σ puntos totales × 100
```

No es una estimación subjetiva. Los mismos 101 puntos se reparten entre los PMV, de modo que
`PMV1 + PMV2 + PMV3 = global` de forma exacta.

**Leyenda:** ✅ implementado · ⚠️ parcial · ❌ no implementado

> La cifra, el método y el desglose punto a punto se documentan en
> [`02-implementacion-de-historias.md`](./02-implementacion-de-historias.md). Este documento
> reproduce las mismas cifras (son consistentes) y añade el desglose de **qué falta exactamente**
> en cada HU, con archivo y acción concreta.

### 10.2 Resumen por PMV

| PMV | Definición | HU incluidas | Puntos | % actual |
|---|---|---|---|---|
| **PMV1** · Prototipo funcional | Chat + SLM + 5 trámites | HU-05, HU-06, HU-07, HU-09 | **24/24** | **100 %** ✅ |
| **PMV2** · Modelo RAG optimizado | RAG 20+ trámites + abstención | HU-04, HU-08, HU-10, HU-11, HU-12 | **28/28** | **100 %** ✅ |
| **PMV3** · Sistema integrado | API + seguridad + UX + despliegue | HU-01, HU-02, HU-03, HU-13, HU-14, HU-15, HU-16, HU-17, HU-18 | 31/49 | **63 %** |
| **TOTAL** | | 18 HU | **83/101** | **82 %** |

> **Actualizado el 17-oct-2026 con verificación en vivo** (API `localhost:8000`, BD local, `tsc` y
> `next build`). El PMV1 está **cerrado al 100 %** y el PMV2 también: se cerraron HU-08 (umbral de
> rechazo), HU-10 (trazabilidad completa + bloqueo + fuentes con metadatos + panel real) y HU-11
> (clasificador de dominio). El PMV3 subió de 59 % a **63 %** (HU-14: respuesta completa en
> auditoría y panel real).

> **Reasignación (16-oct-2026):** la antigua fila "Transversal" se disolvió: **HU-11 → PMV2** y
> **HU-17 → PMV3**. Detalle en §10.7.

**Por qué ningún PMV total está aún al 100 %:** el avance se mide contra el alcance completo de
cada historia, no solo contra la demostración. El PMV1 y el PMV2 están **cerrados al 100 %** (aún
falta la validación con 50 ciudadanos, P2-17, que es una actividad real no fabricable); PMV3
concentra autenticación (HU-13), auditoría (búsqueda por filtros y marcado de inconsistentes),
retroalimentación (HU-15), métricas (HU-16), reportes (HU-18) y el bloque de
calidad/despliegue (pruebas, contenerización, monitoreo).

> ⚠️ **Historial de correcciones:** en versiones anteriores esta tabla decía 88/50/51 % (60/101),
> y antes 100 % para el PMV1 con un desglose que sumaba mal (`9+5+5+5`). El 16-oct-2026 las cifras
> fueron **24/24 + 20/28 + 29/49 = 73/101 = 72 %**; desde el 17-oct-2026 las válidas son las de
> arriba: **24/24 + 28/28 + 31/49 = 83/101 = 82 %** (§12.7).

### 10.3 Las 18 HU: estado, % y qué falta

| # | HU | Épica | Estado | ✅/Total | % | Qué falta (brecha principal) |
|---|---|---|---|---|---|---|
| HU-01 | Carga de documentos oficiales | Gestión documental | ✅ | 9/9 | **100 %** | — cerrada (extracción PDF/DOCX verificada con PDF real + aprobación de calidad) |
| HU-02 | Vigencia, versión y fuente | Gestión documental | ✅ | 8/8 | **100 %** | — cerrada (004 aplicada: 20/20 documentos con `version` y `fecha_publicacion`) |
| HU-03 | Aprobar/derogar documentos | Gestión documental | ⚠️ | 6/7 | **86 %** | Flujo con revisor/roles (depende de HU-13) |
| HU-04 | Procesamiento documental y RAG | RAG | ✅ | 9/9 | **100 %** | — cerrada (extracción, OCR con rapidocr, recuperación por fragmento: 20/20 docs fragmentados) |
| HU-05 | Consulta ciudadana | Consulta | ✅ | 9/9 | **100 %** | — cerrada |
| HU-06 | Clasificación de intención | NLP | ✅ | 5/5 | **100 %** | — cerrada |
| HU-07 | Orientación de requisitos | Orientación | ✅ | 5/5 | **100 %** | — cerrada (columna `area_responsable` + derivación con confianza baja) |
| HU-08 | Orientación de costos y plazos | Orientación | ✅ | 5/5 | **100 %** | — cerrada (umbral de rechazo por groundedness "no inventar" en `ServicioOrientacion`; montos del TUPA cargados) |
| HU-09 | Generación de respuestas con SLM | SLM | ✅ | 5/5 | **100 %** | — cerrada (estructura garantizada desde BD + derivación al funcionario) |
| HU-10 | Trazabilidad y anti-alucinación | Confianza | ✅ | 8/8 | **100 %** | — cerrada (`GET /api/consultas/{id}` con respuesta/fuentes/confianza, bloqueo de afirmaciones, fuentes con número/fecha/versión, `AuditLog` real vía `GET /api/consultas`) |
| HU-11 | Consultas fuera de dominio | Alcance | ✅ | 3/3 | **100 %** | — cerrada (`ServicioDominio` municipal vs. externo, distinción SUNAT/RENIEC/pensiones/… y respuesta de derivación con `entidad_sugerida`) |
| HU-12 | Trámites relacionados | Recomendación | ✅ | 3/3 | **100 %** | — cerrada (motor + endpoint + UI; embeddings y fallback léxico para los 252 TUPA) |
| HU-13 | Usuarios y seguridad | Seguridad | ⚠️ | 2/5 | **40 %** | Login, contraseñas, JWT, roles aplicados, eventos de seguridad (G-01) |
| HU-14 | Auditoría | Auditoría | ⚠️ | 4/6 | **67 %** | Búsqueda por fecha/trámite/usuario y marcado de registros inconsistentes (respuesta completa y panel real ✅ 17-oct-2026) |
| HU-15 | Retroalimentación ciudadana | Calidad | ❌ | 0/3 | **0 %** | Endpoints útil/no útil, tabla de evaluaciones, UI de votos (G-05) |
| HU-16 | Métricas y monitoreo | Métricas | ❌ | 0/3 | **0 %** | Endpoint de métricas agregadas y alertas; `/admin` es maqueta (G-16/G-06) |
| HU-17 | Derivación a atención municipal | Derivación | ⚠️ | 2/5 | **40 %** | Umbral de derivación, canal/área/teléfono, directorio de oficinas, casos de decisión (G-09) |
| HU-18 | Reportes y exportación | Reportes | ❌ | 0/3 | **0 %** | Reportes por periodo, exportación PDF/Excel, datos reales (G-07) |

Resumen: **11 HU al 100 %** (HU-01, HU-02, HU-04, HU-05, HU-06, HU-07, HU-08, HU-09, HU-10, HU-11, HU-12) · **4 HU parciales** (HU-03, HU-13, HU-14, HU-17) · **3 HU sin empezar** (HU-15, HU-16, HU-18) · **83/101 puntos = 82 % global** (verificado 17-oct-2026) · **0 suites de pruebas**.

### 10.4 PMV1 · Prototipo funcional — **100 %** (24/24) ✅

**Definición** (`04-gestion-de-proyecto/04-modelo-de-tres-pmv.md`): *¿El SLM procesa la intención y orienta
trámites básicos?* Objetivo: prototipo funcional con chat + SLM + 5 trámites.

| Componente del PMV1 | Estado | Evidencia en el código |
|---|---|---|
| Chat conversacional | ✅ | `app/chat/page.tsx`, `components/ChatBox.tsx`, `components/ChatThread.tsx` |
| SLM local que orienta trámites | ✅ | `adapters/slm/OllamaAdapter.py` (`qwen2.5:3b`), `services/ServicioSLM.py`, servicio Ollama en `docker-compose.yml` |
| Clasificación de intención | ✅ heurística | `services/ServicioNLP.py` (9 intenciones, confianza, desempate) |
| ≥5 trámites mínimos | ✅ superado | `seeds/tramites.sql`: **252 trámites TUPA 2023** (272 en BD) |

#### Desglose de las 4 HU del PMV1

| HU | % | Puntos cumplidos | Punto pendiente |
|---|---|---|---|
| **HU-05** Consulta ciudadana | **100 %** | 9/9 — intención con confianza, persistencia, caché, RAG, trámite probable, auditoría, chat con fuentes, sin datos ficticios | — |
| **HU-06** Clasificación de intención | **100 %** | 5/5 — 9 intenciones léxicas, confianza 0.55-1.0, desempate por especificidad, `requiere_aclaracion` | — |
| **HU-07** Orientación de requisitos | **100 %** | 5/5 — `area_responsable` en `tramites` (005), expuesta en `TramiteProbableResponse`, derivación textual al área con confianza BAJA | — |
| **HU-09** Respuestas con SLM | **100 %** | 5/5 — Ollama local, abstención sin contexto y por ambigüedad, estructura de apartados garantizada desde BD (`ServicioSLM`), derivación al funcionario | — |

**PMV1 = (9 + 5 + 5 + 5) / (9 + 5 + 5 + 5) = 24/24 = 100 %.**

> **Verificado el 16-oct-2026** contra la API real: `POST /api/consultas` devuelve `intencion`,
> `groundedness`, `tramite_probable.area` poblada, `fuentes` con título y los apartados
> REQUISITOS/PASOS/COSTO/PLAZO/OBSERVACIONES. Los 252 procedimientos del TUPA cargan con
> `area_responsable` (252/252) y costo (188 con monto > 0). El checklist de cierre está en
> [`07-checklist-implementacion.md`](./07-checklist-implementacion.md).

#### Qué faltaba para declarar PMV1 cerrado — **todo ejecutado y verificado**

| # | Acción | Archivo tocado | Estado |
|---|---|---|---|
| 1 | Columna `area_responsable` en `tramites` + exposición en respuesta | `database/migrations/005_area_responsable.sql`, `tramite_controller.py`, `consulta_controller.py` | ✅ |
| 2 | Derivación al área con confianza baja | `ServicioOrientacion.py` | ✅ |
| 3 | Estructura de apartados garantizada (fallback desde BD) | `ServicioSLM.py` | ✅ |
| 4 | Derivación al funcionario | `ServicioOrientacion.py` | ✅ |
| 5 | Montos reales del TUPA 2023 en `tramites.costo` | `seeds/tramites.sql` (regenerado por `backend/scripts/generar_seed_tupa.py`) | ✅ |
| 6 | 252 procedimientos del TUPA | `seeds/tramites.sql` | ✅ |
| 7 | Prueba automatizada del flujo RAG | `backend/tests/` | ⬜ queda para PMV3 (G-18) |

### 10.5 PMV2 · Modelo RAG optimizado — **100 %** (28/28) ✅

**Definición:** *¿La RAG reduce alucinaciones?* Objetivo: RAG con 20+ trámites, abstención y citas.

| Componente | Estado | Evidencia |
|---|---|---|
| RAG con búsqueda vectorial | ✅ | `BusquedaVectorialAdapter` (pgvector HNSW / coseno numpy, umbral 0.3) |
| 20+ trámites en base documental | ✅ superado | **45** documentos indexados (20 TUPA + 19 MPH + 6 institucionales; todos fragmentados: `fragmentos_documento` = 56) |
| Arquitectura hexagonal | ✅ | `domain/` + `application/` + `infrastructure/` + `container.py` |
| Citas / fuentes visibles | ✅ corregido (D-3) + enriquecido (HU-10/P3-08) | `Fuente` viaja con `titulo`, `numero`, `fecha` y `version`; `GroundednessBadge` las muestra en expandible con URL y fragmento |
| Carga con validación, metadatos y extracción | ✅ **verificado en vivo** | `POST /api/admin/documentos/upload` con PDF real del TUPA → **201**, texto extraído, `indexado=true`; `requirements.txt` con `pypdf`, `PyMuPDF`, `python-docx`, `rapidocr` |
| *Chunking* + tabla de fragmentos | ✅ **verificado en vivo** | `POST /api/admin/documentos/{id}/procesar` sobre los **45** documentos → 45 OK (19-oct-2026), `fragmentos_documento` = 56 filas; el adapter consulta fragmentos y hace fallback a documento completo |
| **Abstención / fuera de dominio** | ✅ completa (17-oct-2026) | Umbral de rechazo por groundedness en `ServicioOrientacion` (`BLOQUEO_AFIRMACIONES`, G-04) + `ServicioDominio` (HU-11) que deriva a SUNAT/RENIEC/pensiones/… antes de invocar al SLM |
| **Preguntas ambiguas / sin sentido** | ✅ completa (19-oct-2026) | `ServicioNLP`: saludo → bienvenida; texto sin palabras reconocibles → "no entendí" (`_sin_sentido` + `_sin_palabras_reconocibles`); sin patrón de intención → la consulta **primero intenta el RAG** (piso de similitud 0.45, `UMBRAL_CONSULTA_GENERAL`) y solo pide aclaración si no hay documento afín o el respaldo es insuficiente. La estructura HU-09 (REQUISITOS/COSTO/…) se aplica solo cuando hay intención de trámite; en consultas generales (horarios, teléfonos, catálogo) el modelo responde directo desde el contexto. Verificado en vivo: horarios, teléfono del serenazgo, catálogo de trámites y números de emergencia responden con fuentes; consultas sin contenido piden precisar. |
| Validación con 50 ciudadanos | ❌ | Sin prueba SUS (P2-17, no fabricable) |
| Dataset de la PoC | ✅ versionado | `documentacion/06-prueba-de-concepto/dataset-poc.csv`: **200 consultas** (50 por intención), regenerable con `backend/scripts/generar_dataset_poc.py` (G-21) |

| HU | % | Falta |
|---|---|---|
| HU-04 RAG | **100 %** (9/9) | — (extracción PDF/DOCX ✅, OCR con rapidocr ✅, recuperación por fragmento ✅) |
| HU-08 Costos y plazos | **100 %** (5/5) | — (umbral de rechazo "no inventar" ✅ 17-oct-2026: groundedness < 0.40 bloquea la afirmación y pide verificar con la municipalidad) |
| HU-10 Trazabilidad | **100 %** (8/8) | — (`GET /api/consultas/{id}` devuelve respuesta/fuentes/confianza ✅, bloqueo de afirmaciones ✅, fuentes con número/fecha/versión ✅, `AuditLog` real ✅) |
| HU-11 Fuera de dominio | **100 %** (3/3) | — (`ServicioDominio`: clasificador municipal vs. externo, distinción de entidad y respuesta de derivación con `entidad_sugerida`; anclas municipales como "predial" mantienen el flujo local) |
| HU-12 Trámites relacionados | **100 %** (3/3) | — (`RecomendarTramites` + endpoint + panel UI; embedding para trámites con documentos y **fallback léxico Jaccard** para los 252 TUPA sin documentos, con `similitud` en orden decreciente) |

**PMV2 = (9 + 5 + 8 + 3 + 3) / (9 + 5 + 8 + 3 + 3) = 28/28 = 100 %.** ✅

**PMV2 cerrado el 17-oct-2026.** Lo único que queda fuera del alcance del código es la
**validación SUS con 50 ciudadanos** (P2-17), actividad real no fabricable. Verificado en vivo:
consulta SUNAT → `fuera_dominio=true` con derivación; consulta municipal → flujo normal con fuentes
enriquecidas; consulta sin respaldo → bloqueo + derivación; `GET /api/consultas` y
`GET /api/consultas/{id}` devuelven la trazabilidad completa.

### 10.6 PMV3 · Sistema integrado — **63 %** (31/49)

**Definición:** *¿Producto seguro, accesible y de baja latencia?* Objetivo: API completa + seguridad + UX desplegable.

| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600, degradable sin Redis) |
| API completa | ✅ 27 endpoints de API (18 públicos + 9 admin) | 7 controllers; **arranca con 31 rutas** (D-14..D-23 corregidos; verificado contra `/openapi.json`) |
| Seguridad (login, roles, guardrails) | ❌ | G-01 (auth/JWT) y G-20 (anti prompt-injection); `es_administrador()` sin usar (D-8) |
| Accesibilidad y pruebas de carga | ❌ | G-26 (WCAG, k6/JMeter, SonarQube, ZAP) |
| Latencia < 3 s | ⚠️ no medible | caché sí; sin métricas de latencia (G-16) |

| HU | % | Falta |
|---|---|---|
| HU-01 | **100 %** (9/9) | — (extracción PDF/DOCX ✅ verificada con PDF real; aprobación de calidad ✅: `PUT /api/admin/documentos/{id}/estado` + botón "Aprobar") |
| HU-02 | **100 %** (8/8) | — (migración 004 aplicada: 20/20 documentos con `version` y `fecha_publicacion`) |
| HU-03 | 86 % (6/7) | flujo con revisor/roles (depende de HU-13) |
| HU-13 | 40 % | JWT, roles, eventos de seguridad |
| HU-14 | 67 % (4/6) | búsqueda de auditoría por filtros y marcado de registros inconsistentes (respuesta completa y panel real ✅ 17-oct-2026) |
| HU-15 | 0 % | retroalimentación ciudadana |
| HU-16 | 0 % | métricas agregadas |
| HU-17 | 40 % (2/5) | umbral de derivación, área/teléfono/canal, directorio de oficinas, casos de decisión |
| HU-18 | 0 % | reportes y exportación |

**PMV3 = (9+8+6+2+4+0+0+2+0) / (9+8+7+5+6+3+3+5+3) = 31/49 = 63 %.**

**Tres de sus nueve HU (HU-15, HU-16, HU-18) están en 0 %** — y HU-17 solo
tiene una nota genérica; es el frente con más trabajo.

### 10.7 Reasignación de HU-11 y HU-17 — **categoría "Transversal" eliminada** (16-oct-2026)

| HU | PMV anterior | PMV nuevo | Puntos |
|---|---|---|---|
| HU-11 Consultas fuera de dominio | Transversal | **PMV2** (§10.5) | 3/3 ✅ (cerrada 17-oct-2026) |
| HU-17 Derivación a atención municipal | Transversal | **PMV3** (§10.6) | 2/5 |

**Justificación:** ambas dependen de funcionalidades de un PMV concreto — HU-11 del clasificador
de intención y la abstención (PMV2), HU-17 del catálogo y la capa de seguridad (PMV3) — por lo que
se integraron a ellos en lugar de mantener una cuarta categoría. **El total global no cambia con la
reasignación.** Las cifras vigentes se encuentran en §10.2 (**83/101 = 82 %** desde el
17-oct-2026). Las cifras anteriores (Transversal 2/8 = 25 %) quedan
históricas en este documento.

---

## 11. Inventario unificado de todos los `.md` del repositorio

**90 documentos Markdown** en 9 ubicaciones (4 en la raíz, 7 rector, 73 temáticos, 6 de
presentación). Conteo verificado con `Get-ChildItem -Recurse -Filter *.md` el 16-oct-2026.

### 11.1 Raíz del repositorio (4 documentos)

| Archivo | Qué contiene | Se referencia desde |
|---|---|---|
| `README.md` | Guía de puesta en marcha: estructura, requisitos, instalación con `instalar.ps1`, ejecución, tabla de endpoints, flujo RAG en 5 pasos | `DOCUMENTACION.md`; punto de entrada de todo lector nuevo |
| `DOCUMENTACION.md` | Índice maestro de la documentación: árbol de las 7 carpetas, catálogo de vacíos G-XX, mapa de consistencia `a.md` ↔ código | `README.md`; este documento (§11) |
| `PRESENTACION-PMV1.md` | Guion de demostración del PMV1 para sustentación: cómo levantar, 4 demos (HU-09/06/07/05), resumen con % | `DOCUMENTACION.md:10-11` · cifras corregidas (§12.2) |
| `PMV2_DOCUMENTOS.md` | Alcance del PMV2 y su **estado verificado**: ✅ implementado, ⚠️ parcial, ❌ bloqueos B1-B8, avance 14/25 | Este documento (§10.5, §13.1) |

### 11.2 `documentacion/00-documentos-rectores/` (7 documentos) — transverse

| Archivo | Qué contiene | Se referencia desde |
|---|---|---|
| `indice.md` | Resumen e índice de la carpeta de documentos rectores | `DOCUMENTACION.md` |
| `01-historias-de-usuario.md` | Las 18 HU con épica y criterios Given/When/Then | `DOCUMENTACION.md`; `02-implementacion-de-historias.md` |
| `02-implementacion-de-historias.md` | Estado de implementación por HU, % medido, defectos D-1..D-21 — **marcado como histórico el 16-oct-2026** (sus cifras 59 %/60/101 corresponden al inicio de la jornada; las vigentes están en §10 de este doc) | Este doc (§10.1, §13); `04`, `05` |
| `03-ejecucion.md` | Guía de ejecución local: tabla de los 7 pasos del instalador + arranque | `README.md:49`; `presentacion/indice.md:24` |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ vs. pendiente, verificación local de octubre, G-XX priorizados, recomendación de cierre | Este doc (§2, §13); `05` |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3, backlog, distribución de las 18 HU, G-XX por PMV, ruta de cierre, proyección | Este doc (§10.2, §10.4-10.7) |
| **`06-estado-actual-implementado.md`** | **Este documento.** Inventario de código archivo por archivo, flujos front/back, BD, avance HU+PMV actualizado, inventario unificado de los `.md`, inconsistencias y ruta de cierre | — (documento rector actual) |

### 11.3 Carpetas temáticas de `documentacion/` (6 carpetas, 73 documentos)

Cada carpeta corresponde a un documento académico y tiene su `indice.md` de resumen.

| Carpeta | Documento | N.º | `indice.md` resume | Contenido (numerales) |
|---|---|---|---|---|
| `01-analisis-del-problema` | Doc. 1 — Diagnóstico (AG-T08) | 11 | `indice.md` | 10 numerales: contexto, situación problemática, AS-IS, causas, efectos, formulación, cuantitativos, restricciones, búsqueda, conclusiones |
| `02-conocimientos-de-ingenieria` | Doc. 2 — Conocimientos de ingeniería (AG-107) | 10 | `indice.md` | 9 numerales: problema, requerimientos, matriz épicas/HU, RF, fundamentos, computación, especializados, selección de tecnologías, trazabilidad |
| `03-el-ingeniero-y-la-sociedad` | Doc. 3 — Impacto y ética (AG-101/102) | 14 | `indice.md` | 13 numerales: contexto social, stakeholders, impactos (social/económico/ambiental), salud-seguridad, marco legal, ética, inclusión, análisis, mitigación, KPIs, conclusiones |
| `04-gestion-de-proyecto` | Doc. 4 — Gestión PMI/Scrum | 11 | `indice.md` | 10 numerales: charter, enfoque, tailoring Scrum, modelo 3 PMV, sprints, backlog, DoD, cambios, desempeño, retrospectiva |
| `05-uso-de-herramientas-modernas` | Doc. 5 — Herramientas TI (AG-I11) | 13 | `indice.md` | 12 numerales: criterios, selección, modelado, devops, datos/IA, gestión, calidad-pruebas-seguridad, aplicación al flujo, por PMV, métricas, limitaciones, matriz AG-I11 |
| `06-prueba-de-concepto` | Doc. 6 — Validación técnica (PoC) | 14 | `indice.md` | 13 numerales: identificación, hipótesis, corpus, dataset sintético, modelos, experimentos, resultados, validación vs. criterios, limitaciones, Go/No-Go, integración PMV, fórmula, conclusiones |

Cada archivo usa la convención `NN-titulo.md` y la leyenda ✅ / ⚠️ / ❌ (G-XX).

### 11.4 `presentacion/` (6 documentos) — para sustentación

| Archivo | Qué contiene |
|---|---|
| `indice.md` | Índice de la carpeta + reproducción rápida (Docker) |
| `01-arquitectura-de-software.md` | Arquitectura hexagonal, diagrama de dependencias, puertos/adaptadores, stack, despliegue |
| `02-frontend.md` | Frontend Next.js: rutas, sistema de diseño, contratos HTTP, componentes uno a uno, integración con `lib/api.ts` |
| `03-backend.md` | Backend FastAPI: entry point, DI, controllers, casos de uso, servicios, adaptadores, flujo de consulta |
| `04-base-de-datos.md` | PostgreSQL + pgvector: migraciones, 6 tablas, relaciones, índices, seeds, consultas vectoriales |
| `05-implementaciones.md` | Estado real implementado vs. pendiente, HU, G-XX, reproducción |

> Los `presentacion/01..05` **solapan en contenido** con las secciones §4-§9 de este documento
> (arquitectura, front, back, BD, estado). Se conservan como material de exposición y este
> documento es la versión canónica y actualizada. Ver §12.3.

### 11.5 Cómo se referencian entre sí

- `README.md` → `documentacion/00/03-ejecucion.md` (§49).
- `DOCUMENTACION.md` → `PRESENTACION-PMV1.md` y al árbol de las 7 carpetas.
- `00/indice.md` → `README.md`, `instalar.ps1`, los demás rectores.
- `00/02` → `01-historias-de-usuario.md`; es la base de las cifras de §10.
- `00/04` y `00/05` → `00/02` (defectos y %).
- `05-trazabilidad` → `02-implementacion` (método) y `04` (G-XX).
- Este `06` → todos los anteriores (es el que los unifica).

---

## 12. Inconsistencias detectadas y plan de unificación

### 12.1 ⚠️ Entidad del sistema: Huancayo vs. Junín

| Ubicación | Dice | Estado |
|---|---|---|
| `frontend-tramites/app/layout.tsx:8,20`, `Navbar.tsx:25`, `page.tsx:34,68`, `chat/page.tsx:35` | **Huancayo** | ✅ Correcto (branding `ff7a589`) |
| `database/scripts/actualizar_huancayo.sql` | Huancayo | ✅ Script de corrección |
| `database/seeds/tramites.sql` (descripción y contenido) | Huancayo | ✅ |
| `database/seeds/municipios.sql:3,10-11` | **Junín** | ❌ Desalineado |
| `README.md:3,9` | **Junín (MPJ)**, `munijunin.gob.pe` | ❌ Desalineado |
| `DOCUMENTACION.md:7-8` | **Junín (MPJ)** | ✅ Corregido al publicar este documento (ahora declara Huancayo/MPH y señala la inconsistencia) |
| `PRESENTACION-PMV1.md:3,34` | **Junín**, `munijunin.gob.pe` | ⚠️ Parcial: el título (línea 3) ya dice Huancayo/MPH; queda la URL de ejemplo de la línea 34 |
| `presentacion/01..05` y `documentacion/01..06/*` | **Junín (MPJ)** en ~35 archivos | ⚠️ Pendiente: son documentos académicos; el renombrado masivo requiere decisión del equipo (§12.6) |

**Acción:** alinear `README.md` y `database/seeds/municipios.sql` con el branding de Huancayo (MPH)
que ya usa el código (`database/scripts/actualizar_huancayo.sql` ya trae el SQL de corrección), y
decidir de una vez si el resto de la documentación académica se renombra a MPH o se declara
histórica. **Es una decisión de proyecto, no técnica** — pero debe resolverse antes de sustentar,
porque el nombre de la entidad aparece en la portada y en el pie de la app.

### 12.2 ✅ `PRESENTACION-PMV1.md` — cifras corregidas al publicar este documento

| Métrica | Decía `PRESENTACION-PMV1.md` | Real (§10) | Estado |
|---|---|---|---|
| PMV1 | **100 %** | **88 %** (21/24) | ⚠️ **Revisado el 16-oct**: la cifra "real" anterior (24/24) estaba mal sumada; ver §12.7 |
| HU-05 | 44 % | **100 %** (9/9) | ✅ Corregido |
| HU-06 | 40 % | **100 %** (5/5) | ✅ Corregido |
| HU-07 | 40 % | **80 %** (4/5) | ✅ Corregido |
| HU-09 | 60 % | 60 % (3/5) | ✅ Ya era correcto |

El guion de demostración **no se actualizó** tras el commit `04f91ff` (`feat(hu-05,06,07,09)`), que
cerró HU-05 y HU-06 y subió HU-07 a 80 %; la línea `**PMV1: 46 %**` era la fuente de error más
visible al sostener con ese documento.

**Estado:** la tabla de resumen de `PRESENTACION-PMV1.md` ya muestra los valores reales y enlaza
a este documento (§10). Verificar de nuevo las cifras antes de cada sustentación: este documento es
la fuente de verdad y `PRESENTACION-PMV1.md` es una copia derivada.

### 12.3 ⚠️ `presentacion/01..05` está desalineado con el código actual

| Afirmación en `presentacion/` | Real |
|---|---|
| "KPIs (252/1,236/98%)" en `app/page.tsx` (`02-frontend.md`) | Esos KPI se retiraron de la portada (`app/page.tsx:91-92` ahora muestra "—" con "Métrica no implementada") |
| `ServiceStatus` con "99.9% {estado}" (`02-frontend.md`) | Ahora informa "sin verificar" lo no comprobable |
| `lib/api.ts` con "**fallback demo**" (`04`, `presentacion/02`) | `respuestaDemo()` fue **eliminado** (D-1) |
| `IntencionConsulta` con **6** valores (`04`, `presentacion/03`) | Son **9** |
| "70 archivos" (`documentacion/01/…/indice.md`) | **90** |

**Acción:** el bloque "Inconsistencias" de `DOCUMENTACION.md:97-111` sigue siendo válido como mapa
`a.md` ↔ código, pero las cifras de `presentacion/` y de `04-implementado-y-por-implementar.md`
(§2.1 "IntencionConsulta 6", §2.3 "fallback demo") deben actualizarse o marcarse como histórico.

### 12.4 ✅ `00/indice.md` y `DOCUMENTACION.md` — cifras corregidas al publicar este documento

`documentacion/00-documentos-rectores/indice.md` decía *"37 % global"* y *"porcentajes
(46 % / 36 % / 34 %)"*. Hoy **ambos archivos** (y el resto de los rectores y de `presentacion/`)
están alineados con las cifras canónicas de §10: **82 % global** y **100 % / 100 % / 63 %**
(historial: 49 % → 59 % → 72 % → 82 %).
Ambos archivos enlazan a este documento como fuente de verdad y añaden una fila para
`06-estado-actual-implementado.md`.

### 12.5 ⚠️ `backend/scripts/indexar_documentos.py` no se ejecuta desde la raíz sin ajustar `sys.path`

El script inserta `backend/` en `sys.path` (líneas 19-20) y se invoca como
`python -m backend.scripts.indexar_documentos` desde la raíz. Funciona porque el propio módulo añade
`backend/` a la ruta, pero el `BACKEND_DIR` calculado en la línea 19 queda sin usar. Cosmético, no
bloqueante.

### 12.6 Plan de unificación — estado de ejecución

| Paso | Acción | Estado |
|---|---|---|
| 1 | Este documento (`06`) es la fuente canónica de cifras y de flujos | ✅ Hecho |
| 2 | `00/indice.md` y `DOCUMENTACION.md` enlazan a `06` y tienen sus cifras al día | ✅ Hecho |
| 3 | `PRESENTACION-PMV1.md` con las cifras reales de §10.4 | ✅ Hecho |
| 4 | Marcar `02`, `04`, `05` y `presentacion/01..05` con cabecera *"Documento histórico — cifras actualizadas en [06](06-estado-actual-implementado.md)"* | ⬜ Pendiente |
| 5 | Resolver la entidad (Huancayo vs. Junín) en `README.md`, `seeds/municipios.sql` y `presentacion/01..05` (§12.1) | ⬜ Pendiente — decisión de equipo |
| 6 | Mantener `01-historias-de-usuario.md` como fuente de requisitos (no cambia) | ✅ No requiere acción |
| 7 | Actualizar `02`, `04`, `05`, `indice.md`, `DOCUMENTACION.md`, `README.md` y `presentacion/01..05` a las cifras de 16-oct-2026 (**72 % global, PMV1 100 %, PMV2 71 %, PMV3 59 %, 30 rutas, 89 `.py`, 92 `.md`**) | ✅ Hecho — todos los rectores, `README`, `DOCUMENTACION`, `PMV2_DOCUMENTOS` y `presentacion/` alineados; `02` marcado como **histórico** con banner que apunta a §10 |
| 8 | Re-sincronizar todos los rectores y `presentacion/` a las cifras del 17-oct-2026 (**82 % global, PMV1 100 %, PMV2 100 %, PMV3 63 %, 31 rutas, 91 `.py`, 11 `.sql`, 92 `.md`**) tras cerrar HU-08, HU-10, HU-11 y los puntos de HU-14 | ✅ Hecho (17-oct-2026) |

### 12.7 ⚠️ Corrección del % del PMV1 y del global (16 de octubre de 2026)

| Cifra | Se publicó como | Real | Causa |
|---|---|---|---|
| PMV1 | 100 % (24/24) | **88 % (21/24)** | El desglose de §10.4 sumaba `9+5+5+5`; HU-07 es 4/5 y HU-09 es 3/5 |
| Global | 49 % (49/101) | **59 % (60/101)** | 11 puntos heredados del PMV1 mal contados + 11 puntos ganados por el PMV2 (`ea06c9a`) |
| PMV2 | 44 % (11/25) | **56 % (14/25)** | HU-01/02/03/04 avanzaron con el commit `ea06c9a` |
| PMV3 | 34 % (15/44) | **52 % (23/44)** | ídem (HU-01, HU-02, HU-03) |
| Endpoints | 13 | **22** (16 públicos + 6 admin) | controllers `documento_admin` y rutas nuevas de `documento_controller` |
| `.md` | 79 | **90** | `PMV2_DOCUMENTOS.md` + 10 documentos académicos no contabilizados antes |

Comprobación de consistencia: `21 + 14 + 23 + 2 = 60` ✅ y `24 + 25 + 44 + 8 = 101` ✅.

> **Actualización posterior (mismo 16 de octubre, verificación en vivo):** esas cifras quedan
> **históricas**. Tras cerrar PMV1 (migración 005 + derivación de área, estructura garantizada y
> derivación al funcionario) y el bloque P2-01..P2-16 + P2-18, el estado verificado fue
> **PMV1 24/24 = 100 %**, **PMV2 20/28 = 71 %**, **PMV3 29/49 = 59 %** → **73/101 = 72 % global**.
>
> **Actualización del 17 de octubre de 2026:** con el cierre de HU-08 (umbral de rechazo),
> HU-10 (trazabilidad completa, bloqueo, fuentes con metadatos, panel real) y HU-11 (clasificador
> de dominio), más 2 puntos de HU-14, las cifras vigentes son
> **PMV1 24/24 = 100 %**, **PMV2 28/28 = 100 %**, **PMV3 31/49 = 63 %** → **83/101 = 82 % global**
> (`24+28+31 = 83` ✅). Las cifras vigentes están en §0, §10.2 y §10.3.

---

## 13. Defectos, vacíos y ruta de cierre

### 13.1 Defectos D-1..D-8 (verificados en esta revisión)

| # | Defecto | Ubicación | Estado |
|---|---|---|---|
| D-1 | Timeout de 6 s < latencia real (4-17 s) con respuesta ficticia al agotarse | `lib/api.ts` | ✅ **Corregido** — timeout 45 s, `respuestaDemo()` eliminada |
| D-2 | `groundedness` fijo en 90 % | `lib/api.ts` | ✅ **Corregido** — se muestra el valor real |
| D-3 | Fuentes nunca mostradas (`{url, fragmento}` vs `titulo`) | `consulta_controller.py` | ✅ **Corregido** — las fuentes incluyen `titulo` |
| D-4 | El front llamaba `/api/health`; la ruta real es `/health` | `lib/api.ts` | ✅ **Corregido** — consulta `/health` |
| D-5 | Campos de trámites desalineados (`tipo`/`duracion_estimada_dias` ↔ `categoria`/`plazo`) | `tramite_controller.py` ↔ `lib/api.ts` | ✅ **Corregido** — `mapearTramite` traduce |
| D-6 | Datos de demostración presentados como reales | `app/admin/page.tsx` | ⚠️ **Parcial** — la portada ya no inventa KPI; `/admin` sigue maqueta |
| D-7 | `POST /api/admin/documentos/upload` acepta cualquier archivo | `documento_admin_controller.py` | ✅ **Resuelto 16-oct-2026** — valida extensión (`FormatoDocumento` → 422) y la extracción **funciona**: carga de PDF real del TUPA → 201 con texto extraído |
| D-8 | `es_administrador()` nunca se invoca | `domain/entities/Usuario.py:16` | ❌ **Abierto** — el campo `rol` no controla ningún acceso; afecta también a los 6 endpoints admin |

**Defectos nuevos detectados en esta revisión (2 de octubre de 2026):**

| # | Defecto | Ubicación | Impacto |
|---|---|---|---|
| D-9 | `GET /api/consultas/{id}` devuelve solo la consulta, no respuesta/fuentes/confianza | `consulta_controller.py` | ✅ **Corregido 17-oct-2026** — `TrazabilidadResponse` devuelve consulta + respuesta/confianza/groundedness/fuentes con metadatos y banderas (HU-10 8/8; habilita además el panel real de HU-14) |
| D-10 | `DELETE /api/documentos/{id}` borra físicamente | `documento_controller.py:104` | ✅ **Corregido en `ea06c9a`** — ahora es baja lógica (`eliminado_en`) y existe `DELETE /{id}/fisico` aparte (HU-03 5/7) |
| D-11 | `GET /health` solo comprueba el propio proceso | `main.py:71-74` | El panel muestra "sin verificar" para BD/Redis/Ollama (G-16) |
| D-12 | Branding inconsistente Huancayo vs. Junín | `README.md`, `PRESENTACION-PMV1.md`, `seeds/municipios.sql`, `presentacion/01..05`, `documentacion/01..06/*` | ⚠️ **Parcial** — `DOCUMENTACION.md` y el título de `PRESENTACION-PMV1.md` corregidos; quedan `README.md`, el seed y ~35 documentos académicos (§12.1) |
| D-13 | `preguntas` sin normalizar antes de la caché: `"¿Cuánto cuesta?"` y `"¿Cuánto cuesta ?"` generaron claves distintas hasta el primer acierto | `ServicioCache.construir_clave` | Solo afecta la tasa de acierto, no la corrección |

**Defectos detectados en la revisión del PMV2 (16 de octubre de 2026) — corregidos y verificados el mismo día:**

| # | Defecto | Ubicación | Impacto |
|---|---|---|---|
| D-14 | **La API no arranca:** `main.py:21` importaba `router` de un stub | `main.py` · `tramite_admin_controller.py` | ✅ **Corregido** — `tramite_admin_controller` con `router` real; `import main` → **30 rutas** |
| D-15 | **Migración 004 sin aplicar y no ejecutable** (docstring Python en SQL) | `004_documentos_pmv2.sql` · BD | ✅ **Corregido** — SQL válido, **aplicada**; 20/20 documentos con metadatos |
| D-16 | `instalar.ps1` no ejecutaba 004 | `instalar.ps1` | ✅ **Corregido** — lista 004 **y** 005 |
| D-17 | `pypdf`/`python-docx` ausentes | `requirements.txt` | ✅ **Corregido** — `pypdf`, `PyMuPDF`, `python-docx`, `rapidocr`, `onnxruntime` |
| D-18 | `EstadoDocumento(estado)` sin capturar → 500 | `documento_admin_controller.py` | ✅ **Corregido** — 422 con detalle |
| D-19 | La baja física no borraba el archivo en disco | `GestionarDocumentos.eliminar_fisico` | ✅ **Corregido** — invoca `AlmacenamientoDocumentosPort.eliminar`; verificado con baja física 204 |
| D-20 | `pedir()` rompía con 204 sin cuerpo | `lib/api.ts` | ✅ **Corregido** — `npx tsc --noEmit` y `npx next build` OK |
| D-21 | Panel admin llamaba `GET /api/tramites/admin` inexistente | `lib/api.ts` · `DocumentManager.tsx` | ✅ **Corregido** — panel carga los 272 trámites |

**Defecto nuevo detectado y corregido el 16 de octubre de 2026 (no documentado antes):**

| # | Defecto | Ubicación | Impacto |
|---|---|---|---|
| D-22 | `DocumentoRepositoryImpl.guardar` pasaba `1/0` (int) a la columna BOOLEAN `fragmentado` → `DataError` de asyncpg en **todo** upsert de documentos (cambio de estado y carga) | `DocumentoRepositoryImpl.py:122` | ✅ **Corregido** — `bool(documento.fragmentado)`; verificado: `PUT .../estado` → 200 y `POST .../upload` → 201 |
| D-23 | Publicar (`estado=vigente`) sin metadatos devolvía **500** en vez de **422** | `documento_admin_controller.py` (`cambiar_estado`) | ✅ **Corregido** — captura `DocumentoInvalidoError` → 422 ("faltan metadatos obligatorios"); los 20 documentos sembrados recibieron `version` y `fecha_publicacion` |

### 13.2 Vacíos G-XX por prioridad

| Prioridad | G-XX | Vacío | Bloquea |
|---|---|---|---|
| 🔴 Alta | ~~**D-14..D-21**~~ | ✅ **Resueltos 16-oct-2026** (§13.1) + D-22/D-23 corregidos | — |
| 🔴 Alta | **G-18** | Suite de pruebas automatizadas (pytest) — 0 suites hoy | PMV3 |
| 🔴 Alta | **G-16/G-06** | Métricas reales (endpoint, agregaciones) — el panel es maqueta | HU-16, PMV3 |
| 🔴 Alta | **G-01** | Autenticación, contraseñas, JWT, roles, control de acceso | HU-13, PMV3 |
| 🔴 Alta | **G-12** | ⬆️ **Parcial** — `DocumentManager` sube/lista/borra/aprueba de verdad (P2-10, P2-11); siguen ficticios los KPIs y gráficos de `/admin` | HU-01 ✅, HU-16 |
| 🟠 Media | ~~**G-04**~~ | ✅ **Resuelto 17-oct-2026** — umbral de rechazo por groundedness (`BLOQUEO_AFIRMACIONES` en `ServicioOrientacion`) + clasificador de dominio (`ServicioDominio`); HU-08 y HU-11 cerradas |
| 🟠 Media | **G-20** | Guardrails anti *prompt-injection* | HU-05, PMV3 |
| 🟠 Media | ~~**G-13**~~ | ✅ **Resuelto 16-oct-2026** — chunking, `fragmentos_documento`, OCR (rapidocr) y recuperación RAG por fragmento verificados (20/20 documentos fragmentados) | HU-04 ✅ |
| 🟠 Media | **G-11** | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas `/admin/*` | PMV3 |
| 🟠 Media | **G-14** | Consistencia de campos de trámite (parcialmente cerrada en D-5) | HU-02 ✅ |
| 🟠 Media | **G-07** | Reportes y exportación | HU-18 |
| 🟡 Baja | ~~**G-08**~~ | ✅ **Resuelto 16-oct-2026** — `RecomendarTramites` + endpoint + panel UI con % de afinidad | HU-12 ✅ |
| 🟡 Baja | **G-09** | Derivación a atención municipal (backend) | HU-17 |
| 🟡 Baja | **G-05** | Retroalimentación ciudadana + tabla `evaluaciones_calidad` | HU-15 |
| 🟡 Baja | **G-03** | Enmascaramiento de PII | PMV3 |
| 🟡 Baja | **G-02** | Clasificador ML (Random Forest/TF-IDF) y métricas F1 | — |
| 🟡 Baja | **G-10** | UI de historial ciudadano `/mis-consultas` (solo API) | HU-14 |
| 🟡 Baja | **G-15** | Fine-tuning QLoRA del SLM | — |
| 🟡 Baja | **G-17** | Contenerización front/back, balanceador, HTTPS, monitoreo | PMV3 |
| 🟡 Baja | ~~**G-21**~~ | ⬆️ **Parcial→✅ dataset** — `dataset-poc.csv` (200 consultas) versionado y regenerable (16-oct-2026); siguen faltando los **resultados de experimentos** de la PoC | PMV2 |
| 🟡 Baja | **G-23** | Rate limiting / protección contra saturación | PMV3 |
| 🟡 Baja | **G-24** | Auditoría de manipulación de documentos | HU-03 |
| 🟡 Baja | **G-25** | Aviso legal como política de API (solo en UI) | — |
| 🟡 Baja | **G-26** | Auditoría WCAG, pruebas de carga, SonarQube, ZAP | PMV2/PMV3 |

> El catálogo canónico de G-XX está en `DOCUMENTACION.md:69-95`. Este documento lo **reordena por
> prioridad** y lo cruza con las HU y los PMV que bloquea.

### 13.3 Ruta de cierre priorizada

| Orden | Bloque | Acción | Efecto en % |
|---|---|---|---|
| 0 | ✅ **Desbloqueo (hecho 16-oct)** | D-14..D-19 | ✅ API arranca (30 rutas), `004`/`005` aplicadas, deps completas |
| 0b | ✅ **Desbloqueo front (hecho 16-oct)** | D-20, D-21 (+ D-22, D-23) | ✅ Panel de documentos operativo; upload real → 201 |
| 0c | ✅ **Cierre PMV2 (hecho 17-oct)** | HU-08 umbral "no inventar" (G-04) + HU-10 trazabilidad/bloqueo/fuentes/panel (D-9) + HU-11 clasificador de dominio | ✅ **PMV2 71 % → 100 %**; HU-14 33 % → 67 %; global 72 % → **82 %** |
| 1 | Corrección inmediata | Resolver branding (§12.1) y actualizar `PRESENTACION-PMV1.md` (§12.2) | — (correctitud) |
| 2 | ✅ Dato crítico (hecho) | Montos reales del TUPA en `tramites.costo` | HU-08 60 % → 80 % |
| 3 | ✅ PMV2 (hecho) | Motor de trámites relacionados (HU-12) + recuperación por fragmento (G-13) | PMV2 56 % → 71 % |
| 4 | PMV3 bloque 1 | `pytest` del flujo RAG (G-18) + JWT y roles (G-01) | PMV3 → ~70 % |
| 5 | PMV3 bloque 2 | Endpoint de métricas (G-16) + guardrails (G-20) | PMV3 → ~80 % |
| 6 | ✅ PMV1 cierre (hecho) | Área responsable por trámite + estructura garantizada del SLM | PMV1 88 % → **100 %** ✅ |
| 7 | Validación | k6 + auditoría WCAG + SonarQube (G-26) + **P2-17 (SUS con 50 ciudadanos)** | habilita sustentación |
| 8 | ✅ Pendiente PMV2 (hecho 17-oct) | HU-11 (fuera de dominio) + umbral de abstención (G-04) | PMV2 71 % → **100 %** ✅ |

### 13.4 Proyección de avance

| Escenario | Global | PMV1 | PMV2 | PMV3 |
|---|---|---|---|---|
| **Estado anterior (previo al 16-oct)** | **59 %** | 88 % | 56 % | 52 % |
| Estado 16-oct-2026 | **72 %** | **100 %** | **71 %** | **59 %** |
| **Estado actual (verificado 17-oct-2026)** | **82 %** | **100 %** | **100 %** | **63 %** |
| + pytest (G-18) + JWT y roles (G-01) | ~87 % | 100 % | 100 % | ~70 % |
| + métricas + guardrails (G-16, G-20) | ~91 % | 100 % | 100 % | ~78 % |
| + retroalimentación + reportes + validación SUS (P2-17) | **94-98 %** | 100 % | 100 % | ~88 % |

> Los porcentajes de PMV2/PMV3 usan la fórmula por HU de §10.5/§10.6; el cierre total exige además
> los puntos de PMV3 que no dependen de HU (pruebas, contenerización, monitoreo).

---

## 14. Cómo verificar este documento

```bash
# Cifras de trámites y documentos
grep -c "^('" database/seeds/tramites.sql              # 252 (procedimientos TUPA)
grep -c "0.00" database/seeds/tramites.sql              # 93 filas gratuito/variable (188 con costo > 0 en API)
grep -c "^\s*('" database/seeds/documentos.sql          # 20

# Endpoints (30 rutas con la API arrancada)
grep -rn "@router\.\(get\|post\|put\|delete\)" backend/infrastructure/controllers/

# Puertos del dominio
ls backend/domain/ports/                                # 10 ABC

# La app debe importar sin errores (0 = OK; hoy imprime 30 rutas)
python -c "import sys; sys.path.insert(0,'backend'); import main; print(len(main.app.routes))"

# Migraciones PMV2 aplicadas (004 metadatos + fragmentos; 005 área responsable)
psql -U tramites -d tramites_municipales -c "SELECT COUNT(*) FROM documentos WHERE version IS NOT NULL AND fecha_publicacion IS NOT NULL;"   # 20
psql -U tramites -d tramites_municipales -c "SELECT COUNT(*) FROM fragmentos_documento;"                                                  # 20
psql -U tramites -d tramites_municipales -c "SELECT COUNT(*) FROM tramites WHERE area_responsable IS NOT NULL;"                            # 252

# Dataset de la PoC (G-21)
wc -l documentacion/06-prueba-de-concepto/dataset-poc.csv   # 201 (1 encabezado + 200 consultas)

# Intenciones soportadas
grep -c "= '" backend/domain/value_objects/IntencionConsulta.py   # 9

# Sin dependencias inversas (debe devolver vacío)
grep -r "from infrastructure" backend/domain backend/application

# Pruebas automatizadas (debe devolver vacío: 0 suites)
find . -name "test_*.py" -o -name "*.test.ts" -o -name conftest.py

# Respuesta ficticia eliminada (debe devolver vacío)
grep -rn "respuestaDemo" frontend-tramites/
```

**Comprobación funcional del flujo completo:**

```bash
curl -X POST http://localhost:8000/api/consultas \
  -H "Content-Type: application/json" \
  -d '{"pregunta":"¿Qué necesito para el permiso de funcionamiento de una cafetería?"}'
```

Esperado: `intencion: consultar_requisitos`, `confianza` alta/media, `groundedness` numérico real,
`tramite_probable` con requisitos del catálogo, `fuentes` con `titulo` y `url`.

Repitiendo la misma pregunta: latencia de **~5-30 ms** (acierto de caché).

---

*Documento maestro: generado el 2 de octubre de 2026 (HEAD `ff7a589`), actualizado el 16 de octubre
de 2026 con el PMV2 (HEAD `ea06c9a`) y **re-verificado el 16 de octubre de 2026 en vivo** contra la
API (`localhost:8000`, 30 rutas), PostgreSQL local (252 trámites TUPA con costo/área, 20 documentos
fragmentados) y el build del front (`npx next build` OK): PMV1 100 %, PMV2 71 %, PMV3 59 %, global
72 %. Se corrigieron D-14..D-23 (§13.1). Contrasta con el código real del repositorio. Cuando el
código cambie, actualiza §10 (cifras), §5 (inventario) y §12 (inconsistencias).*



