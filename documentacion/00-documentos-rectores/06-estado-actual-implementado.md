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
> **Fecha de verificación: 2 de octubre de 2026** · HEAD `ff7a589`
> (`feat(branding): proyecto MUN AI para la Municipalidad Provincial de Huancayo`).
> Método: lectura íntegra de los 53 `.py`, 26 archivos de front-end, 6 `.sql`, `instalar.ps1`,
> `docker-compose.yml` y de los 79 `.md`. Cada afirmación de este documento es verificable con
> `grep` sobre el archivo que se cita.

---

## 0. Resumen ejecutivo

| Dimensión | Resultado actual | Referencia |
|---|---|---|
| **Avance global de las 18 HU** | **49 %** (49/101 puntos de verificación) | §10.1 |
| **PMV1 · Prototipo funcional** | **88 %** (21/24) — 4 HU | §10.2 |
| **PMV2 · Modelo RAG optimizado** | **44 %** (11/25) — 4 HU | §10.2 |
| **PMV3 · Sistema integrado** | **34 %** (15/44) — 8 HU | §10.2 |
| **Transversal** (fuera de dominio, derivación) | **25 %** (2/8) — 2 HU | §10.2 |
| HU completas al 100 % | **2 / 18** — HU-05, HU-06 | §10.3 |
| HU iniciadas (⚠️ o ✅) | **13 / 18** | §10.3 |
| HU sin empezar (❌) | **5 / 18** — HU-11, HU-12, HU-15, HU-16, HU-18 | §10.3 |
| Pruebas automatizadas | **0 suites** | §13.2 |
| Catálogo de trámites | **22** (meta PMV1: 5) | §7 |
| Documentos indexables | **20** (meta PMV2: 20) | §7 |
| Endpoints REST | **13** | §6.2 |
| Archivos Python | **53** (≈1 830 líneas) | §5 |
| Archivos de front-end | **26** | §5 |
| Documentos Markdown | **79** | §11 |

**Lo que funciona de extremo a extremo:** el flujo ciudadano completo
`pregunta → clasificación de intención con confianza → persistencia → caché → recuperación vectorial →
generación con SLM local → evaluación de groundedness → identificación de trámite probable con datos
del catálogo → auditoría en PostgreSQL → respuesta con fuentes`.

**Lo que no existe todavía:** autenticación y roles (G-01), guardrails anti *prompt-injection* (G-20),
métricas reales (G-16), pruebas automatizadas (G-18), retroalimentación ciudadana (G-05),
recomendación de trámites relacionados (HU-12, G-08), reportes (HU-18, G-07), manejo de PII (G-03),
carga documental conectada a la UI (G-12), OCR y *chunking* documental (G-13), clasificador ML (G-02).

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
| Embeddings | `BAAI/bge-m3`, 1024 dimensiones, CPU (`BGE_M3Adapter.py:25`) |
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
│   ├── main.py                             punto de entrada: app FastAPI, CORS, routers, /health, lifespan
│   ├── domain/                             NÚCLEO — no importa nada de infrastructure
│   │   ├── entities/                       7 entidades
│   │   ├── value_objects/                  7 value objects
│   │   └── ports/                          7 puertos (interfaces ABC)
│   ├── application/                        LÓGICA DE APLICACIÓN — casos de uso y servicios
│   │   ├── use_cases/                      8 casos de uso
│   │   └── services/                       7 servicios
│   ├── infrastructure/                     ADAPTADORES — todo lo que toca el mundo exterior
│   │   ├── controllers/                    4 controllers FastAPI
│   │   ├── repositories/                   Connection + 2 repositorios + base
│   │   ├── adapters/                       6 adaptadores (rag, embeddings, slm, cache, catalog, documents)
│   │   └── container.py                    inyección de dependencias
│   └── scripts/indexar_documentos.py      indexación masiva de embeddings BGE-M3
├── frontend-tramites/                      Next.js 14 (App Router) + TypeScript + Tailwind
│   ├── app/                                rutas: / · /chat · /tramites · /admin + layout + globals.css
│   ├── components/                         15 componentes + icons.tsx (20 iconos SVG)
│   └── lib/                                api.ts (contrato HTTP) · queries.ts (helpers)
├── database/
│   ├── schema.sql                          referencia consolidada del esquema
│   ├── migrations/                         001 base+extensión · 002 tablas+índices · 003 HNSW
│   ├── seeds/                              municipios (1) · tramites (22) · documentos (20)
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
└── PRESENTACION-PMV1.md                    guion de demostración del PMV1  ⚠️ desactualizado (§12.2)
```

**Totales:** 53 archivos Python · 26 archivos de front-end · 6 archivos SQL · 79 archivos Markdown ·
1 script PowerShell · 1 archivo YAML.

---

## 4. Arquitectura

### 4.1 Las tres capas (arquitectura hexagonal / puertos y adaptadores)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CAPA DE ENTRADA — infrastructure/controllers/                          │
│  consulta_controller · documento_controller · tramite_controller ·        │
│  usuario_controller          (FastAPI: parsing, validación, HTTP)        │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ llama casos de uso (no adaptadores)
┌───────────────────────────────▼──────────────────────────────────────────┐
│  APLICACIÓN — application/                                               │
│  use_cases/   ClasificarIntencion · RegistrarConsulta · GenerarOrientacion│
│               IdentificarTramiteProbable · AuditarConsulta ·             │
│               GestionarDocumentos · ConsultarTramite · BuscarDocumentos   │
│  services/    ServicioOrientacion · ServicioRAG · ServicioSLM ·           │
│               ServicioNLP · EvaluadorGroundedness · ServicioCache ·       │
│               ServicioAuditoria                                           │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ depende SOLO de puertos (ABC)
┌───────────────────────────────▼──────────────────────────────────────────┐
│  DOMINIO — domain/     (sin imports de infrastructure: es testeable solo) │
│  entities/    Consulta · Documento · Respuesta · Fuente · Tramite ·      │
│               Usuario · Municipalidad                                        │
│  value_objects/ IntencionConsulta(9) · ClasificacionIntencion ·           │
│               TramiteProbable · NivelConfianza(3) · EstadoDocumento(3) · │
│               TipoTramite(6) · FuenteOficial(4)                           │
│  ports/       CachePort · DocumentoRepository · ConsultaRepository ·      │
│               BusquedaSemanticaPort · GeneracionRespuestaPort ·            │
│               AuditoriaPort · TramiteCatalogoPort                          │
└───────────────────────────────▲──────────────────────────────────────────┘
                                │ implementan los puertos
┌───────────────────────────────┴──────────────────────────────────────────┐
│  INFRAESTRUCTURA — infrastructure/                                       │
│  adapters/     BusquedaVectorialAdapter · BGE_M3Adapter · OllamaAdapter · │
│                RedisAdapter · TramiteCatalogoAdapter · DocumentStorageAdapter│
│  repositories/ Connection (pool asyncpg) · DocumentoRepositoryImpl ·      │
│                ConsultaRepositoryImpl · PostgreSQLRepository              │
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

`container.py:95-151` — la función `crear_container()` construye el grafo completo:

| Línea | Se construye | Puerto que satisface |
|---|---|---|
| `97` | `Connection(dsn)` | — (recurso compartido) |
| `100` | `BGE_M3Adapter()` | — (colaborador de embeddings) |
| `101` | `BusquedaVectorialAdapter(connection, embeddings)` | `BusquedaSemanticaPort` |
| `102` | `OllamaAdapter()` | `GeneracionRespuestaPort` |
| `103` | `RedisAdapter()` | `CachePort` |
| `104` | `DocumentStorageAdapter()` | — (almacenamiento de archivos) |
| `105` | `_AuditoriaPostgreSQL(connection)` | `AuditoriaPort` |
| `108-109` | `DocumentoRepositoryImpl`, `ConsultaRepositoryImpl` | `DocumentoRepository`, `ConsultaRepository` |
| `112` | `TramiteCatalogoAdapter(documento_repository)` | `TramiteCatalogoPort` |
| `115-130` | 7 servicios de aplicación | — |
| `133-151` | 8 casos de uso ya inyectados | — |

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
| Embeddings | sentence-transformers | 3.0.1 | `requirements.txt:26` |
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
| `backend/main.py` | 47 | Crea la app FastAPI (`Sistema de Trámites Municipales API` v0.1.0), carga `.env` con `load_dotenv()` (línea 14), configura CORS limitado a `localhost:3000` y `127.0.0.1:3000` (líneas 45-51), incluye los 4 routers (líneas 53-56), expone `GET /health` (líneas 59-62) y un `lifespan` que abre el pool de PostgreSQL al arrancar y cierra pool + Redis al apagar (líneas 24-35). |

### 5.2 Capa de dominio — entidades (`backend/domain/entities/`)

| Archivo | Líneas | Contenido |
|---|---|---|
| `Consulta.py` | 14 | `id`, `usuario_id`, `pregunta`, `intencion`, `creada_en`; método `clasificada()`. |
| `Documento.py` | 19 | `id`, `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado`, `embedding`, `actualizado_en`, `indexado`, `puntuacion_similitud`; `esta_vigente()` (línea 23). |
| `Respuesta.py` | 49 | Entidad central: `id`, `consulta_id`, `texto`, `confianza`, `fuentes`, `groundedness`, `confianza_intencion`, `pide_aclaracion`, `tramite_probable`. **Método clave `con_datos_estructurados()`** (líneas 26-61): anexa al texto del modelo los requisitos numerados, el arancel y el plazo **tomados de la base de datos**, más la URL de la ficha. Es lo que hace verificables los datos críticos (HU-07). |
| `Fuente.py` | 13 | `id`, `documento_id`, `tipo`, `url`, `fragmento`, `titulo`, `puntuacion_relevancia`. El campo `titulo` es el que permite que el front muestre la fuente (**D-3 corregido**). |
| `Tramite.py` | 16 | `id`, `municipalidad_id`, `nombre`, `descripcion`, `tipo`, `requisitos[]`, `costo`, `duracion_estimada_dias`; `agregar_requisito()`. |
| `Usuario.py` | 13 | `id`, `nombre`, `correo`, `rol`, `creado_en`; `es_administrador()` — **existe pero nunca se invoca** (defecto **D-8**). |
| `Municipalidad.py` | 11 | `id`, `nombre`, `departamento`, `provincia`, `distrito`, `sitio_web`. |

### 5.3 Capa de dominio — value objects (`backend/domain/value_objects/`)

| Archivo | Líneas | Contenido |
|---|---|---|
| `IntencionConsulta.py` | 12 | Enum `str` con **9 intenciones**: `consultar_requisitos`, `consultar_costo`, `consultar_plazo`, `consultar_pasos`, `consultar_area`, `consultar_estado`, `consultar_ubicacion`, `saludo`, `otro`. |
| `ClasificacionIntencion.py` | 25 | `intencion` + `confianza` + `empata`. Propiedad `requiere_aclaracion` (líneas 22-29): verdadera si la intención es `OTRO`, si hay empate o si la confianza < `CONFIANZA_MINIMA = 0.5` (línea 13). Fábrica `sin_patron()` (líneas 31-33). |
| `TramiteProbable.py` | 21 | Value object que transporta el trámite detectado con `requisitos[]`, `costo`, `duracion_estimada_dias`, `fuente_url`, `documentos_coincidentes` y `puntaje_relevancia`; `resumen_requisitos(limite)`. |
| `NivelConfianza.py` | 6 | Enum `alta` / `media` / `baja`. |
| `EstadoDocumento.py` | 6 | Enum `vigente` / `obsoleto` / `en_revision`. |
| `TipoTramite.py` | 9 | Enum con 6 valores (`licencia_funcionamiento`, `partida_nacimiento`, `certificado_domicilio`, `licencia_construccion`, `pago_tributos`, `otro`). **Nota:** los 22 seeds usan 4 de estos 6 más `otro`. |
| `FuenteOficial.py` | 7 | Enum `portal_municipal`, `normativa_legal`, `tupa`, `documento_interno`. Todo documento sembrado se cita como `portal_municipal` (`ServicioRAG.py:50`). |

### 5.4 Capa de dominio — puertos (`backend/domain/ports/`)

Interfaces ABC que el dominio define y la infraestructura implementan. Son el punto donde se
podrían sustituir PostgreSQL, Redis u Ollama sin tocar la lógica.

| Archivo | Métodos abstractos | Implementación actual |
|---|---|---|
| `CachePort.py` | `obtener`, `guardar`, `eliminar` | `RedisAdapter` |
| `DocumentoRepository.py` | `guardar`, `obtener_por_id`, `listar_por_tramite`, `eliminar` | `DocumentoRepositoryImpl` |
| `ConsultaRepository.py` | `guardar`, `obtener_por_id`, `listar_por_usuario` | `ConsultaRepositoryImpl` |
| `BusquedaSemanticaPort.py` | `buscar`, `generar_embedding` | `BusquedaVectorialAdapter` |
| `GeneracionRespuestaPort.py` | `generar` | `OllamaAdapter` |
| `AuditoriaPort.py` | `registrar` | `_AuditoriaPostgreSQL` (en `container.py:53-69`) |
| `TramiteCatalogoPort.py` | `buscar_por_documentos` | `TramiteCatalogoAdapter` |

### 5.5 Capa de aplicación — servicios (`backend/application/services/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `ServicioNLP.py` | 116 | **Clasificador léxico de intención.** Diccionario `_PATRONES_INTENCION` (líneas 12-75) con **raíces**, no palabras completas, para tolerar conjugaciones (`requisit` cubre requisito/requisitos/requiere/necesito). Lógica: normaliza (minúsculas, sin tildes, sin puntuación, línea 124-131), puntúa cada intención por nº de patrones coincidentes, desempata por especificidad (suma de longitudes, línea 110), y calcula `confianza = 0.55 + 0.15 × (patrones−1)` con tope 1.0 (líneas 78-79, 117); si hay empate técnico baja la confianza a 0.70 (línea 118-119). Sin patrones → `OTRO` con confianza 0. |
| `ServicioRAG.py` | 46 | Orquesta recuperación + generación. `recuperar()` (líneas 25-28) llama al `BusquedaSemanticaPort` y **filtra solo documentos vigentes**. `responder()` (30-41): sin documentos devuelve el texto de abstención del SLM con lista de fuentes vacía. `construir_fuentes()` estático (43-56): convierte cada documento en `Fuente` con `fragmento = contenido[:280]` y su `titulo`. |
| `ServicioSLM.py` | 36 | Construye el prompt y delega. `PLANTILLA_SISTEMA` (líneas 6-10): *"Responde únicamente con la información del contexto... si no la contiene, indícalo explícitamente"*. `INSTRUCCION_ESTRUCTURA` (13-18): exige apartados REQUISITOS / PASOS / COSTO / PLAZO / OBSERVACIONES y la frase *"No especificado en la base documental"* cuando falte respaldo. `generar()` (27-35): si no hay contexto devuelve la abstención *"No encontré información oficial... Te recomiendo acudir a la oficina de trámites"* (líneas 29-33). |
| `ServicioOrientacion.py` | 80 | **Orquestador del flujo de orientación.** `orientar()` (líneas 34-72): (1) si la clasificación requiere aclaración devuelve `ACLARACION_AMBIGUA` sin generar ni citar (41-42); (2) recupera documentos; (3) genera respuesta y fuentes; (4) calcula `groundedness` y confianza; (5) si confianza BAJA y hay fuentes, **agrega nota de advertencia visible** al texto (49-54); (6) llama a `IdentificarTramiteProbable` (56-58); (7) anexa los datos estructurados del catálogo (71-72). `ACLARACION_AMBIGUA` (líneas 14-18) es el texto que pide专业课 precisar requisitos/costo/lugar/estado. |
| `EvaluadorGroundedness.py` | 35 | **Control de alucinaciones por cobertura léxica.** Tokeniza la respuesta (palabras de >3 caracteres, línea 48-49), construye el vocabulario del contexto (contenido + título de cada documento) y calcula `coincidencias / términos_respuesta` (líneas 27-42). Umbrales: `ALTA ≥ 0.75`, `MEDIA ≥ 0.40`, si no `BAJA` (líneas 6-7, 18-25). `esta_grounded()` (44-45). |
| `ServicioCache.py` | 25 | Abstrae la caché de respuestas. `construir_clave()` (17-20): `consulta:` + SHA-256 de la pregunta normalizada (minúsculas, sin espacios extremos) — así `"¿Cuánto cuesta?"` y `"cuánto cuesta"` comparten entrada. `obtener_respuesta`, `guardar_respuesta` (TTL configurable), `invalidar`. |
| `ServicioAuditoria.py` | 21 | Centraliza `registrar_interaccion()` y `obtener_consulta()`; usa `AuditoriaPort` + `ConsultaRepository`. |

### 5.6 Capa de aplicación — casos de uso (`backend/application/use_cases/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `ClasificarIntencion.py` | 18 | `ejecutar()` devuelve solo la intención; `ejecutar_detallado()` devuelve la `ClasificacionIntencion` completa (intención + confianza + empate). Ambos validan que la pregunta no esté vacía. |
| `RegistrarConsulta.py` | 26 | Construye la entidad `Consulta` con `uuid4()` y `datetime.now(timezone.utc)` y la persiste vía `ConsultaRepository`. |
| `GenerarOrientacion.py` | 22 | Valida la pregunta y delega en `ServicioOrientacion.orientar()`, reenviando la `ClasificacionIntencion`. |
| `IdentificarTramiteProbable.py` | 58 | **Deducción del trámite del catálogo.** `ejecutar(documentos)` (líneas 26-54): pide al `TramiteCatalogoPort` los trámites vinculados a los documentos recuperados; puntúa cada trámite **sumando la similitud semántica** de sus documentos (`_puntuar`, 56-72); descarta si el ganador no supera `PUNTAJE_MINIMO = 0.45` (línea 10, 45-46) o si no supera al segundo por `MARGEN_MINIMO = 1.15` (línea 8, 49-51). Si nada domina, **no propone ningún trámite** — decisión deliberada: es preferible callar antes que señalar el trámite equivocado. |
| `AuditarConsulta.py` | 13 | `ejecutar()` registra la trazabilidad; `consultar_trazabilidad()` recupera la consulta por id. |
| `GestionarDocumentos.py` | 33 | `registrar()` **genera el embedding antes de persistir** (líneas 22-27); `listar()`, `actualizar_estado()` (32-40), `eliminar()` (42-43). |
| `ConsultarTramite.py` | 27 | Obtiene los documentos vigentes de un trámite, con caché propia (`tramite:{id}:documentos`, TTL 1800 s). |
| `BuscarDocumentos.py` | 12 | Búsqueda semántica directa, filtrando a vigentes. No lo invoca ningún controller (queda disponible para el endpoint de búsqueda). |

### 5.7 Capa de infraestructura — adaptadores (`backend/infrastructure/adapters/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `rag/BusquedaVectorialAdapter.py` | 95 | **Búsqueda semántica con doble modo.** Detecta pgvector con `Connection.es_pgvector()` (línea 84) y elige: **modo pgvector** — `1 - (embedding <=> $1::vector)` con índice HNSW (`QUERY_BUSQUEDA_VECTORIAL_PGVECTOR`, líneas 17-25); **modo sin pgvector** — trae todos los embeddings y calcula el coseno con numpy en Python (`_coseno`, líneas 40-52; `QUERY_BUSQUEDA_IN_MEMORIA`, 27-33). Ambos filtran `estado = 'vigente'` y `embedding IS NOT NULL`, y aplican `umbral_similitud = 0.3` (línea 75, constructor). `generar_embedding()` delega en BGE-M3. |
| `embeddings/BGE_M3Adapter.py` | 32 | Genera vectores de 1024 dimensiones con `BAAI/bge-m3` en CPU. Carga perezosa y en hilo (`asyncio.to_thread`, línea 36) para no bloquear el event loop. `normalize_embeddings=True` (línea 40). |
| `slm/OllamaAdapter.py` | 44 | Cliente HTTP de Ollama (`OLLAMA_URL`, por defecto `localhost:11434`; modelo `qwen2.5:3b`). Payload: `temperature 0.2`, `num_predict 512`, `stream false` (líneas 33-39). `construir_prompt()` (48-56) arma `Contexto:` con `Fuente: título (url)` + contenido, o avisa *"No se recuperó contexto documental"* si está vacío. Timeout 120 s. |
| `cache/RedisAdapter.py` | 70 | Caché tolerante a fallos: captura `RedisConnectionError`/`TimeoutError`, avisa **una sola vez** (`_advertir_una_vez`, 42-45) y sigue sin caché. El sistema no cae si Redis está apagado. `cerrar()` (86-89) para el apagado. |
| `catalog/TramiteCatalogoAdapter.py` | 39 | Resuelve trámites desde documentos con `JOIN documentos d ON d.tramite_id = t.id WHERE d.id = ANY($1::uuid[])` (líneas 9-18), devolviendo nombre, requisitos, costo, plazo, URL y nº de documentos coincidentes. |
| `documents/DocumentStorageAdapter.py` | 27 | Guarda/lee/elimina archivos en disco bajo `DOCUMENTS_PATH` (por defecto `./storage/documentos`). **No valida extensión ni extrae texto** (defecto **D-7**). |

### 5.8 Capa de infraestructura — repositorios (`backend/infrastructure/repositories/`)

| Archivo | Líneas | Función real |
|---|---|---|
| `Connection.py` | 46 | Pool `asyncpg` (min 1 / max 10). Construye el DSN desde `POSTGRES_*` (líneas 17-24). `es_pgvector()` (46-57) comprueba `to_regtype('vector')` **una vez y cachea** el resultado. |
| `PostgreSQLRepository.py` | 19 | Clase base con `ejecutar`, `obtener_uno` (fetchrow), `obtener_muchos` (fetch). Todo el SQL va parametrizado con `$1..$n` → previene inyección SQL. |
| `DocumentoRepositoryImpl.py` | 85 | `QUERY_UPSERT` (líneas 10-22) con `ON CONFLICT (id) DO UPDATE` y `COALESCE(EXCLUDED.embedding, documentos.embedding)` — **esto evita que un cambio de estado borre el embedding** (defecto corregido n.º 3, ver `04-implementado-y-por-implementar.md`). `indexado` se calcula como `(embedding IS NOT NULL)`. `_formatear_vector()` (42-51) escribe `[...]` para pgvector o `{...}` para `double[]`. |
| `ConsultaRepositoryImpl.py` | 50 | Persistencia de consultas con upsert. `QUERY_SELECT_USUARIO` ordena por fecha desc. |

### 5.9 Capa de infraestructura — controladores (`backend/infrastructure/controllers/`)

| Archivo | Líneas | Rutas que expone |
|---|---|---|
| `consulta_controller.py` | 203 | `POST /api/consultas`, `GET /api/consultas/{consulta_id}`. Ver flujo detallado en §6. |
| `tramite_controller.py` | 53 | `GET /api/tramites` (opcional `?municipalidad_id=`), `GET /api/tramites/{id}` (incluye documentos vigentes). |
| `documento_controller.py` | 89 | `POST /api/documentos`, `POST /api/documentos/upload`, `GET /api/documentos/{id}`, `PUT /api/documentos/{id}/estado`, `DELETE /api/documentos/{id}`. |
| `usuario_controller.py` | 67 | `POST /api/usuarios`, `GET /api/usuarios/{id}`, `GET /api/usuarios/{id}/consultas` (historial, `LIMIT 50`). |

### 5.10 Scripts de backend

| Archivo | Líneas | Función |
|---|---|---|
| `backend/scripts/indexar_documentos.py` | 52 | Genera embeddings BGE-M3 para documentos `vigente` con `embedding IS NULL` (líneas 25-31) y los persiste. Funciona con y sin pgvector (literal `[...]` o lista `double[]`). Ejecutado por `instalar.ps1` en el paso 7. |

### 5.11 Capa de API del front-end (`frontend-tramites/lib/`)

| Archivo | Líneas | Función |
|---|---|---|
| `api.ts` | 168 | **Única capa de comunicación con el back-end.** `API_URL` desde `NEXT_PUBLIC_API_URL` (línea 1). Timeouts: consulta 45 000 ms, catálogo 10 000 ms (líneas 6-7). `pedir()` (62-82) envuelve `fetch` con `AbortController` y traduce `AbortError` a un mensaje en castellano. `leerDetalle()` (53-60) extrae el `detail` del backend para propagar mensajes reales (ej. "el SLM no está disponible"). `enviarConsulta()` (90-113) **no tiene respuesta alternativa**: si el backend falla, propaga el error; `groundedness` usa el valor real, o 0 si no llega (**D-2**). `mapearTramite()` (139-150) traduce `costo`/`duracion_estimada_dias`/`tipo` al modelo de UI (**D-5**). `obtenerEstadoServicios()` (179-185) consulta `/health` (**D-4**) y marca lo no verificado como `"sin verificar"`. |
| `queries.ts` | 17 | Helpers `fetchTramites()` (captura errores → `[]`) y `filtrarTramites(tramites, q, categoria)`. |

### 5.12 Rutas del front-end (`frontend-tramites/app/`)

| Archivo | Líneas | Tipo | Función |
|---|---|---|---|
| `layout.tsx` | 28 | Server | Metadata (título, descripción), `Navbar`, `<main>`, `footer` institucional. |
| `page.tsx` | 117 | Server (`force-dynamic`) | Portada. Llama a `obtenerTramites()` con `.catch(() => [])` (línea 21): si la BD falla muestra 0, **nunca una lista ficticia**. Muestra nº real de trámites, mockup móvil, catálogo destacado (4 primeros), chat compacto, y sección de métricas con `KpiCard`/`MiniCharts`/`ServiceStatus`/`AuditLog`. |
| `chat/page.tsx` | 69 | Client | Página del chat + mockup móvil estático + `RobotAgent`. |
| `tramites/page.tsx` | 62 | Client | Catálogo con buscador, filtro por categoría, estados de carga/error/vacío. |
| `admin/page.tsx` | 55 | Server (`force-dynamic`) | Dashboard **maqueta**: KPIs fijos (252 / 1,236 / 98 %), `MiniCharts`, `ServiceStatus`, `AuditLog`, `DragDropUpload`, tabla documental ficticia (**D-6** abierto). |
| `globals.css` | 127 | CSS | Sistema de diseño "cálido/orgánico": tokens, `glass`, `card-3d`, `bubble-user`/`bubble-bot`, `avatar-muni`, `chip`, `badge-*`, `btn-*`, animaciones `typing-dot`, `animate-float-y`, `blink-eye`. |
| `tailwind.config.ts` | 119 | Config | Paleta institucional (emerald/primary/amber), sombras suaves, keyframes. |
| `next.config.js` | 8 | Config | `reactStrictMode`, expone `NEXT_PUBLIC_API_URL`. |
| `postcss.config.js` | 6 | Config | Plugin Tailwind. |
| `tsconfig.json` | — | Config | TypeScript estricto. |

### 5.13 Componentes del front-end (`frontend-tramites/components/`)

| Archivo | Líneas | Estado | Función |
|---|---|---|---|
| `ChatBox.tsx` | 69 | ✅ real | Estado del chat (`mensajes`, `entrada`, `cargando`), llama `enviarConsulta`, muestra sugerencias rápidas y `Loading`. Ante error, **muestra el error real** con `fallo: true` (líneas 28-35). |
| `ChatThread.tsx` | 77 | ✅ real | Renderiza burbujas, `MuniAvatar`, `TypingDots`, `GroundednessBadge`, `TramiteProbableCard` y el rótulo *"Necesito que precises tu consulta"* cuando `pideAclaracion`. Auto-scroll. |
| `GroundednessBadge.tsx` | 31 | ✅ real | Badge con % real de groundedness y hasta 2 títulos de fuente + "+N fuentes". `nivelColor()` mapea ≥0.9 verde, ≥0.75 ámbar, resto azul. |
| `TramiteProbableCard.tsx` | 42 | ✅ real | Tarjeta *"Trámite identificado"* con requisitos del catálogo, arancel, plazo y enlace a la ficha oficial. |
| `TramiteCard.tsx` | 39 | ✅ real | Tarjeta de trámite del catálogo (costo, plazo, 3 primeros requisitos). No inventa etiqueta de estado. |
| `Loading.tsx` | 10 | ✅ real | Indicador *"MUN AI está consultando fuentes oficiales…"*. |
| `ServiceStatus.tsx` | 52 | ⚠️ parcial | Muestra estado real de `/health`; lo no verificado se informa como *"sin verificar"*, no como operativo. |
| `Navbar.tsx` | 52 | ✅ real | Navegación con 4 enlaces, resaltado de ruta activa, menú móvil. |
| `QuickAccessCard.tsx` | 27 | ✅ real | Tarjetas de acceso rápido. |
| `RobotAgent.tsx` | 72 | ✅ real | SVG animado del asistente (MUN AI) con parpadeo, flotación y plataforma. |
| `KpiCard.tsx` | 23 | ⚠️ maqueta | Tarjeta KPI reutilizable; los **valores** los decide quien la usa (en `/admin` son ficticios). |
| `MiniCharts.tsx` | 58 | ⚠️ maqueta | Barras, donuts y línea de tendencia con **datos fijos**. |
| `AuditLog.tsx` | 26 | ⚠️ maqueta | 5 filas **hardcodeadas** ("Consulta #8.412…"). No consume la API. |
| `DragDropUpload.tsx` | 38 | ⚠️ maqueta | Arrastrar/soltar y selector de archivos, pero **solo guarda nombres en estado local**: no llama a `/api/documentos/upload` (**G-12**). |
| `icons.tsx` | 198 | ✅ real | 20 iconos SVG: `AlertIcon`, `AyudaIcon`, `ChartIcon`, `ChatIcon`, `CheckIcon`, `ClockIcon`, `CloseIcon`, `DirectorioIcon`, `DocIcon`, `HeartIcon`, `LinkIcon`, `MenuIcon`, `OrdenanzaIcon`, `SearchIcon`, `SendIcon`, `ShieldIcon`, `SparkIcon`, `TramiteIcon`, `UploadIcon`, `UsersIcon`. |

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

### 6.2 Los 13 endpoints REST

| # | Método | Ruta | Archivo:línea | Función |
|---|---|---|---|---|
| 1 | POST | `/api/consultas` | `consulta_controller.py:94` | Consulta RAG completa (flujo §6.1) |
| 2 | GET | `/api/consultas/{id}` | `consulta_controller.py:224` | Trazabilidad: **solo** `id`, `usuario_id`, `pregunta`, `intencion`, `creada_en` — **no** devuelve respuesta, fuentes ni confianza (brecha HU-10/HU-14) |
| 3 | GET | `/api/tramites` | `tramite_controller.py:31` | Catálogo; filtro opcional `?municipalidad_id=` |
| 4 | GET | `/api/tramites/{id}` | `tramite_controller.py:43` | Detalle + documentos vigentes del trámite |
| 5 | POST | `/api/documentos` | `documento_controller.py:44` | Registra documento **y genera su embedding** |
| 6 | POST | `/api/documentos/upload` | `documento_controller.py:66` | Guarda el archivo en disco — **no valida ni extrae texto** (D-7) |
| 7 | GET | `/api/documentos/{id}` | `documento_controller.py:93` | Detalle de un documento |
| 8 | PUT | `/api/documentos/{id}/estado` | `documento_controller.py:78` | Cambia `vigente`/`obsoleto`/`en_revision` |
| 9 | DELETE | `/api/documentos/{id}` | `documento_controller.py:104` | **Borrado físico** (no es baja lógica — brecha HU-03) |
| 10 | POST | `/api/usuarios` | `usuario_controller.py:48` | Registro; valida rol con regex `^(ciudadano\|administrador)$` |
| 11 | GET | `/api/usuarios/{id}` | `usuario_controller.py:66` | Detalle de usuario |
| 12 | GET | `/api/usuarios/{id}/consultas` | `usuario_controller.py:77` | Historial del usuario (`LIMIT 50`) |
| 13 | GET | `/health` | `main.py:59` | `{"status":"ok"}` — **no** comprueba BD, Redis ni Ollama |

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
| `database/migrations/003_create_vectors.sql` | Índice **HNSW** `idx_documentos_embedding_hnsw ON documentos USING hnsw (embedding vector_cosine_ops)` solo si hay pgvector; deja commented la alternativa IVFFlat; añade `idx_tramites_tipo`. |
| `database/schema.sql` | Referencia consolidada del esquema (documentación, no se ejecuta). |

### 7.2 Las 6 tablas

| Tabla | Columnas | Relaciones |
|---|---|---|
| `municipalidades` | `id`, `nombre`, `departamento`, `provincia`, `distrito`, `sitio_web`, `creado_en` | — |
| `usuarios` | `id`, `nombre`, `correo` UNIQUE, `rol` CHECK in (ciudadano, administrador), `creado_en` | — |
| `tramites` | `id`, `municipalidad_id`, `nombre`, `descripcion`, `tipo`, `requisitos TEXT[]`, `costo NUMERIC(10,2)`, `duracion_estimada_dias INT`, `creado_en` | FK → `municipalidades` |
| `documentos` | `id`, `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado` CHECK in (vigente, obsoleto, en_revision), `embedding`, `actualizado_en` | FK → `tramites` |
| `consultas` | `id`, `usuario_id` (nullable), `pregunta`, `intencion`, `creada_en` | FK → `usuarios` (ON DELETE SET NULL) |
| `auditoria_consultas` | `id`, `consulta_id`, `respuesta`, `confianza` CHECK, `fuentes` TEXT, `registrado_en` | FK → `consultas` (CASCADE) |

Índices: `idx_tramites_municipalidad`, `idx_documentos_tramite`, `idx_documentos_estado`, `idx_consultas_usuario`, `idx_consultas_creada_en`, `idx_tramites_tipo`, `idx_documentos_embedding_hnsw`.

### 7.3 Semilla de datos (seeds)

| Archivo | Volumen | Contenido |
|---|---|---|
| `seeds/municipios.sql` | **1** Municipalidad | ⚠️ Sigue insertando *"Municipalidad Provincial de Junín"* (líneas 3, 10-11). `scripts/actualizar_huancayo.sql` lo corrige a Huancayo. |
| `seeds/tramites.sql` | **22** trámites | 5 registros civiles, 4 certificados/tributos, 4 licencias, 4 urbanismo, 2 comercio/eventos, 3 otros. Todos con `costo 0.00` (§13.4) y plazos de 1 a 30 días. |
| `seeds/documentos.sql` | **20** documentos | Textos de Procedimientos Administrativos por trámite, con `url_origen` del portal oficial, pensados para indexarse. |

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
| `/admin` | `app/admin/page.tsx` | Server | ninguno (ficticio) | ⚠️ maqueta |

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
| 3/7 | Base de datos | Crea el rol `tramites`, la base `tramites_municipales`, y aplica en orden: `002_create_tables.sql`, `003_create_vectors.sql`, `seeds/municipios.sql`, `seeds/tramites.sql`, `seeds/documentos.sql` con `ON_ERROR_STOP=1`. | 94-137 |
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

### 9.5 Rendimiento medido

| Operación | Latencia |
|---|---|
| Consulta repetida (acierto de caché) | **~5-30 ms** |
| Consulta nueva (embeddings + pgvector + SLM en CPU) | **4-17 s** (típicamente 4-14 s) |
| `GET /api/tramites` | < 100 ms |

> La latencia la domina el SLM en CPU: con GPU (bloque comentado en `docker-compose.yml:48-55`) baja sustancialmente. El objetivo de < 3 s de HU-06 **no es medible hoy** porque no existe instrumentación de latencia (brecha **G-16**).

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
`PMV1 + PMV2 + PMV3 + Transversal = global` de forma exacta.

**Leyenda:** ✅ implementado · ⚠️ parcial · ❌ no implementado

> La cifra, el método y el desglose punto a punto se documentan en
> [`02-implementacion-de-historias.md`](./02-implementacion-de-historias.md). Este documento
> reproduce las mismas cifras (son consistentes) y añade el desglose de **qué falta exactamente**
> en cada HU, con archivo y acción concreta.

### 10.2 Resumen por PMV

| PMV | Definición | HU incluidas | Puntos | % actual |
|---|---|---|---|---|
| **PMV1** · Prototipo funcional | Chat + SLM + 5 trámites | HU-05, HU-06, HU-07, HU-09 | 21/24 | **88 %** |
| **PMV2** · Modelo RAG optimizado | RAG 20+ trámites + abstención | HU-04, HU-08, HU-10, HU-12 | 11/25 | **44 %** |
| **PMV3** · Sistema integrado | API + seguridad + UX + despliegue | HU-01, HU-02, HU-03, HU-13, HU-14, HU-15, HU-16, HU-18 | 15/44 | **34 %** |
| **Transversal** | Fuera de dominio + derivación | HU-11, HU-17 | 2/8 | **25 %** |
| **TOTAL** | | 18 HU | **49/101** | **49 %** |

**Ninguna HU del PMV2/PMV3/Transversal llega al 100 %** porque el avance se mide contra el alcance
completo de cada historia (que incluye versionado documental, chunking, OCR, autenticación, métricas
y reportes), no solo contra la demostración.

### 10.3 Las 18 HU: estado, % y qué falta

| # | HU | Épica | Estado | ✅/Total | % | Qué falta (brecha principal) |
|---|---|---|---|---|---|---|
| HU-01 | Carga de documentos oficiales | Gestión documental | ⚠️ | 4/9 | **44 %** | Validación PDF/DOCX, extracción de texto, metadatos junto al archivo, y conectar la UI de carga (G-12) |
| HU-02 | Vigencia, versión y fuente | Gestión documental | ⚠️ | 4/8 | **50 %** | Columnas `version` y `fecha_emision`; validación de metadatos obligatorios |
| HU-03 | Aprobar/derogar documentos | Gestión documental | ⚠️ | 3/7 | **43 %** | Estado "derogado" literal, endpoint de edición, flujo con revisor/roles, baja lógica (hoy DELETE físico) |
| HU-04 | Procesamiento documental y RAG | RAG | ⚠️ | 4/9 | **44 %** | Chunking, extracción de PDF, OCR para escaneados, job de reprocesamiento (G-13) |
| HU-05 | Consulta ciudadana | Consulta | ✅ | 9/9 | **100 %** | — cerrada |
| HU-06 | Clasificación de intención | NLP | ✅ | 5/5 | **100 %** | — cerrada |
| HU-07 | Orientación de requisitos | Orientación | ✅ | 4/5 | **80 %** | Derivación al área responsable (no hay columna de área en BD) |
| HU-08 | Orientación de costos y plazos | Orientación | ⚠️ | 3/5 | **60 %** | Cargar montos reales del TUPA (`costo` = 0.00); "no inventar" validado como dato, no solo por prompt |
| HU-09 | Generación de respuestas con SLM | SLM | ⚠️ | 3/5 | **60 %** | Estructura de apartados garantizada; derivación al funcionario |
| HU-10 | Trazabilidad y anti-alucinación | Confianza | ⚠️ | 4/8 | **50 %** | `GET /api/consultas/{id}` devuelve solo la consulta (sin respuesta/fuentes/confianza); bloqueo de afirmaciones; fuentes con número/fecha/página |
| HU-11 | Consultas fuera de dominio | Alcance | ❌ | 0/3 | **0 %** | Clasificador de dominio municipal vs. externo; respuesta de derivación |
| HU-12 | Trámites relacionados | Recomendación | ❌ | 0/3 | **0 %** | Motor de recomendación y UI de complementarios (G-08) |
| HU-13 | Usuarios y seguridad | Seguridad | ⚠️ | 2/5 | **40 %** | Login, contraseñas, JWT, roles aplicados, eventos de seguridad (G-01) |
| HU-14 | Auditoría | Auditoría | ⚠️ | 2/6 | **33 %** | Búsqueda por fecha/trámite/usuario; respuesta completa en auditoría; panel real (hoy mock) |
| HU-15 | Retroalimentación ciudadana | Calidad | ❌ | 0/3 | **0 %** | Endpoints útil/no útil, tabla de evaluaciones, UI de votos (G-05) |
| HU-16 | Métricas y monitoreo | Métricas | ❌ | 0/3 | **0 %** | Endpoint de métricas agregadas y alertas; `/admin` es maqueta (G-16/G-06) |
| HU-17 | Derivación a atención municipal | Derivación | ⚠️ | 2/5 | **40 %** | Umbral de derivación, canal/área/teléfono, directorio de oficinas, casos de decisión (G-09) |
| HU-18 | Reportes y exportación | Reportes | ❌ | 0/3 | **0 %** | Reportes por periodo, exportación PDF/Excel, datos reales (G-07) |

Resumen: **2 HU al 100 %** (HU-05, HU-06) · **11 HU parciales** · **5 HU sin empezar** (HU-11, HU-12, HU-15, HU-16, HU-18) · **0 suites de pruebas**.

### 10.4 PMV1 · Prototipo funcional — **88 %** (21/24) — lo más avanzado

**Definición** (`04-gestion-de-proyecto/04-modelo-de-tres-pmv.md`): *¿El SLM procesa la intención y orienta
trámites básicos?* Objetivo: prototipo funcional con chat + SLM + 5 trámites.

| Componente del PMV1 | Estado | Evidencia en el código |
|---|---|---|
| Chat conversacional | ✅ | `app/chat/page.tsx`, `components/ChatBox.tsx`, `components/ChatThread.tsx` |
| SLM local que orienta trámites | ✅ | `adapters/slm/OllamaAdapter.py` (`qwen2.5:3b`), `services/ServicioSLM.py`, servicio Ollama en `docker-compose.yml` |
| Clasificación de intención | ✅ heurística | `services/ServicioNLP.py` (9 intenciones, confianza, desempate) |
| ≥5 trámites mínimos | ✅ superado | `seeds/tramites.sql`: **22** trámites TUPA 2023 |

#### Desglose de las 4 HU del PMV1

| HU | % | Puntos cumplidos | Punto pendiente |
|---|---|---|---|
| **HU-05** Consulta ciudadana | **100 %** | 9/9 — intención con confianza, persistencia, caché, RAG, trámite probable, auditoría, chat con fuentes, sin datos ficticios | — |
| **HU-06** Clasificación de intención | **100 %** | 5/5 — 9 intenciones léxicas, confianza 0.55-1.0, desempate por especificidad, `requiere_aclaracion` | — |
| **HU-07** Orientación de requisitos | **80 %** | 4/5 — `tramites.requisitos TEXT[]` expuesto, RAG cita fuente, lista numerada garantizada desde BD, verificación vía JOIN | **Falta:** derivación al área responsable — no existe columna de área en `tramites` |
| **HU-09** Respuestas con SLM | **60 %** | 3/5 — Ollama local, abstención sin contexto y por ambigüedad, fuentes citadas y evaluadas | **Faltan 2:** (a) estructura de apartados garantizada (`qwen2.5:3b` puede no respetar la plantilla; los datos críticos ya no dependen del modelo porque se anexan desde BD); (b) derivación al funcionario |

**PMV1 = (9 + 5 + 4 + 3) / (9 + 5 + 5 + 5) = 21/24 = 88 %.**

#### Qué falta para declarar PMV1 cerrado (7 puntos)

| # | Acción | Archivo a tocar | Esfuerzo |
|---|---|---|---|
| 1 | Añadir columna `area_responsable` a `tramites` y exponerla en `TramiteProbableResponse` | nueva migración + `tramite_controller.py` + `consulta_controller.py` + `TramiteProbable.py` | Bajo |
| 2 | Derivar al área cuando la confianza sea baja y haya trámite probable | `ServicioOrientacion.py` | Bajo |
| 3 | Validar la estructura del SLM: si el modelo no devuelve los apartados, componerlos desde BD | `ServicioSLM.py` | Medio |
| 4 | Cargar los **montos reales del TUPA 2023** en `tramites.costo` (hoy 0.00) | `seeds/tramites.sql` / script de carga | Medio (dato) |
| 5 | Confirmar los 252 procedimientos del TUPA, no solo 22 | `seeds/tramites.sql` | Medio (dato) |
| 6 | Añadir `version` y `fecha_emision` a `documentos` | migración + `schema.sql` + `Documento.py` | Bajo |
| 7 | Prueba automatizada del flujo RAG completo | nuevo `backend/tests/` | Medio |

### 10.5 PMV2 · Modelo RAG optimizado — **44 %** (11/25)

**Definición:** *¿La RAG reduce alucinaciones?* Objetivo: RAG con 20+ trámites, abstención y citas.

| Componente | Estado | Evidencia |
|---|---|---|
| RAG con búsqueda vectorial | ✅ | `BusquedaVectorialAdapter` (pgvector HNSW / coseno numpy, umbral 0.3) |
| 20+ trámites en base documental | ✅ superado | `seeds/documentos.sql`: **20** documentos vigentes |
| Arquitectura hexagonal | ✅ | `domain/` + `application/` + `infrastructure/` + `container.py` |
| Citas / fuentes visibles | ✅ corregido (D-3) | `Fuente.titulo` viaja en la respuesta y `GroundednessBadge` lo muestra |
| **Abstención / fuera de dominio** | ⚠️ parcial | `ServicioSLM.generar` (sin contexto) y `ServicioOrientacion._respuesta_de_aclaracion` (ambigüedad) ya se abstienen; **falta** el umbral por groundedness que rechace outright (G-04) |
| Validación con 50 ciudadanos | ❌ | Sin prueba SUS ni reproducibilidad (G-26, G-21) |

| HU | % | Falta |
|---|---|---|
| HU-04 RAG | 44 % | chunking, extracción PDF, OCR (G-13) |
| HU-08 Costos y plazos | 60 % | montos del TUPA sin cargar; validación "no inventar" |
| HU-10 Trazabilidad | 50 % | API de trazabilidad incompleta; fuentes detalladas |
| HU-12 Trámites relacionados | **0 %** | motor de recomendación inexistente (G-08) |

**PMV2 = (4 + 3 + 4 + 0) / (9 + 5 + 8 + 3) = 11/25 = 44 %.**

**Qué bloquea cerrar PMV2:** HU-12 al 0 %, dataset de la PoC (G-21) y los montos reales del TUPA.

### 10.6 PMV3 · Sistema integrado — **34 %** (15/44)

**Definición:** *¿Producto seguro, accesible y de baja latencia?* Objetivo: API completa + seguridad + UX desplegable.

| Componente | Estado | Evidencia |
|---|---|---|
| Docker Compose (BD+Redis+Ollama) | ✅ | `docker-compose.yml` (3 servicios con healthchecks) |
| Caché de respuestas | ✅ | `ServicioCache` + `RedisAdapter` (TTL 3600, degradable sin Redis) |
| API completa | ✅ 13 endpoints | los 4 controllers + `/health` |
| Seguridad (login, roles, guardrails) | ❌ | G-01 (auth/JWT) y G-20 (anti prompt-injection); `es_administrador()` sin usar (D-8) |
| Accesibilidad y pruebas de carga | ❌ | G-26 (WCAG, k6/JMeter, SonarQube, ZAP) |
| Latencia < 3 s | ⚠️ no medible | caché sí; sin métricas de latencia (G-16) |

| HU | % | Falta |
|---|---|---|
| HU-01 | 44 % | validación y carga PDF conectadas |
| HU-02 | 50 % | `version` / `fecha_emision` |
| HU-03 | 43 % | roles, edición, baja lógica |
| HU-13 | 40 % | JWT, roles, eventos de seguridad |
| HU-14 | 33 % | búsqueda de auditoría, panel real |
| HU-15 | 0 % | retroalimentación ciudadana |
| HU-16 | 0 % | métricas agregadas |
| HU-18 | 0 % | reportes y exportación |

**PMV3 = (4+4+3+2+2+0+0+0) / (9+8+7+5+6+3+3+3) = 15/44 = 34 %.**

**Tres de sus ocho HU (HU-15, HU-16, HU-18) están en 0 %** — es el frente con más trabajo.

### 10.7 Transversal — **25 %** (2/8)

| HU | % | Falta |
|---|---|---|
| HU-11 Consultas fuera de dominio | 0 % | clasificador de dominio (municipal vs. externo), respuesta de derivación a la entidad correspondiente |
| HU-17 Derivación a atención municipal | 40 % | umbral de derivación, área/teléfono/canal, directorio de oficinas, casos de decisión |

**Transversal = (0 + 2) / (3 + 5) = 2/8 = 25 %.**

---

## 11. Inventario unificado de todos los `.md` del repositorio

**79 documentos Markdown** en 9 ubicaciones. Esta tabla es el índice unificado: dice qué contiene
cada uno y desde dónde se referencia.

### 11.1 Raíz del repositorio (3 documentos)

| Archivo | Qué contiene | Se referencia desde |
|---|---|---|
| `README.md` | Guía de puesta en marcha: estructura, requisitos, instalación con `instalar.ps1`, ejecución, tabla de endpoints, flujo RAG en 5 pasos | `DOCUMENTACION.md`; punto de entrada de todo lector nuevo |
| `DOCUMENTACION.md` | Índice maestro de la documentación: árbol de las 7 carpetas, catálogo de vacíos G-XX, mapa de consistencia `a.md` ↔ código | `README.md`; este documento (§11) |
| `PRESENTACION-PMV1.md` | Guion de demostración del PMV1 para sustentación: cómo levantar, 4 demos (HU-09/06/07/05), resumen con % | `DOCUMENTACION.md:10-11` · ⚠️ **desactualizado** (§12.2) |

### 11.2 `documentacion/00-documentos-rectores/` (7 documentos) — transverse

| Archivo | Qué contiene | Se referencia desde |
|---|---|---|
| `indice.md` | Resumen e índice de la carpeta de documentos rectores | `DOCUMENTACION.md` |
| `01-historias-de-usuario.md` | Las 18 HU con épica y criterios Given/When/Then | `DOCUMENTACION.md`; `02-implementacion-de-historias.md` |
| `02-implementacion-de-historias.md` | Estado de implementación por HU, % medido (49 % global / 101 pts), defectos D-1..D-8 | Este doc (§10.1, §13); `04`, `05` |
| `03-ejecucion.md` | Guía de ejecución local: tabla de los 7 pasos del instalador + arranque | `README.md:49`; `presentacion/indice.md:24` |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ vs. pendiente, verificación local de octubre, G-XX priorizados, recomendación de cierre | Este doc (§2, §13); `05` |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3, backlog, distribución de las 18 HU, G-XX por PMV, ruta de cierre, proyección | Este doc (§10.2, §10.4-10.7) |
| **`06-estado-actual-implementado.md`** | **Este documento.** Inventario de código archivo por archivo, flujos front/back, BD, avance HU+PMV actualizado, inventario unificado de los `.md`, inconsistencias y ruta de cierre | — (documento rector actual) |

### 11.3 Carpetas temáticas de `documentacion/` (6 carpetas, 66 documentos)

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
| `02-frontend.md` | Frontend Next.js: rutas, sistema de diseño, contratos HTTP, 15 componentes uno a uno, integración con `lib/api.ts` |
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
| PMV1 | **46 %** | **88 %** (21/24) | ✅ Corregido |
| HU-05 | 44 % | **100 %** (9/9) | ✅ Corregido |
| HU-06 | 40 % | **100 %** (5/5) | ✅ Corregido |
| HU-07 | 40 % | **80 %** (4/5) | ✅ Corregido |
| HU-09 | 60 % | 60 % | ✅ Ya era correcto |

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
| "70 archivos" (`documentacion/01/…/indice.md`) | **79** |

**Acción:** el bloque "Inconsistencias" de `DOCUMENTACION.md:97-111` sigue siendo válido como mapa
`a.md` ↔ código, pero las cifras de `presentacion/` y de `04-implementado-y-por-implementar.md`
(§2.1 "IntencionConsulta 6", §2.3 "fallback demo") deben actualizarse o marcarse como histórico.

### 12.4 ✅ `00/indice.md` y `DOCUMENTACION.md` — cifras corregidas al publicar este documento

`documentacion/00-documentos-rectores/indice.md` decía *"37 % global"* y *"porcentajes
(46 % / 36 % / 34 %)"`. Los valores reales son **49 % global** y **88 % / 44 % / 34 %**.
Ambos archivos (`00/indice.md` y `DOCUMENTACION.md`) ya están corregidos, enlazan a este documento
como fuente de verdad y añaden una fila para `06-estado-actual-implementado.md`.

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
| D-7 | `POST /api/documentos/upload` acepta cualquier archivo | `documento_controller.py:66` | ❌ **Abierto** — sin validación de extensión/MIME, sin extracción de texto, `tramite_id` sin usar |
| D-8 | `es_administrador()` nunca se invoca | `domain/entities/Usuario.py:16` | ❌ **Abierto** — el campo `rol` no controla ningún acceso |

**Defectos nuevos detectados en esta revisión (2 de octubre de 2026):**

| # | Defecto | Ubicación | Impacto |
|---|---|---|---|
| D-9 | `GET /api/consultas/{id}` devuelve solo la consulta, no respuesta/fuentes/confianza | `consulta_controller.py:224-240` | La trazabilidad por API está incompleta (HU-10, HU-14) |
| D-10 | `DELETE /api/documentos/{id}` borra físicamente | `documento_controller.py:104` | No hay baja lógica; se pierde la auditoría documental (HU-03) |
| D-11 | `GET /health` solo comprueba el propio proceso | `main.py:59-62` | El panel muestra "sin verificar" para BD/Redis/Ollama (G-16) |
| D-12 | Branding inconsistente Huancayo vs. Junín | `README.md`, `PRESENTACION-PMV1.md`, `seeds/municipios.sql`, `presentacion/01..05`, `documentacion/01..06/*` | ⚠️ **Parcial** — `DOCUMENTACION.md` y el título de `PRESENTACION-PMV1.md` corregidos; quedan `README.md`, el seed y ~35 documentos académicos (§12.1) |
| D-13 | `preguntas` sin normalizar antes de la caché: `"¿Cuánto cuesta?"` y `"¿Cuánto cuesta ?"` generaron claves distintas hasta el primer acierto | `ServicioCache.construir_clave` | Solo afecta la tasa de acierto, no la corrección |

### 13.2 Vacíos G-XX por prioridad

| Prioridad | G-XX | Vacío | Bloquea |
|---|---|---|---|
| 🔴 Alta | **G-18** | Suite de pruebas automatizadas (pytest) — 0 suites hoy | PMV3 |
| 🔴 Alta | **G-16/G-06** | Métricas reales (endpoint, agregaciones) — el panel es maqueta | HU-16, PMV3 |
| 🔴 Alta | **G-01** | Autenticación, contraseñas, JWT, roles, control de acceso | HU-13, PMV3 |
| 🔴 Alta | **G-12** | Carga de documentos conectada al backend (`DragDropUpload` es maqueta) | HU-01 |
| 🟠 Media | **G-04** | Abstención por umbral de groundedness con rechazo / fuera de dominio | HU-11, PMV2 |
| 🟠 Media | **G-20** | Guardrails anti *prompt-injection* | HU-05, PMV3 |
| 🟠 Media | **G-13** | Chunking documental, campos `version`/`fecha_publicacion`/página | HU-02, HU-04 |
| 🟠 Media | **G-11** | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas `/admin/*` | PMV3 |
| 🟠 Media | **G-14** | Consistencia de campos de trámite (parcialmente cerrada en D-5) | HU-02 |
| 🟠 Media | **G-07** | Reportes y exportación | HU-18 |
| 🟡 Baja | **G-08** | Recomendación de trámites relacionados | HU-12, PMV2 |
| 🟡 Baja | **G-09** | Derivación a atención municipal (backend) | HU-17 |
| 🟡 Baja | **G-05** | Retroalimentación ciudadana + tabla `evaluaciones_calidad` | HU-15 |
| 🟡 Baja | **G-03** | Enmascaramiento de PII | PMV3 |
| 🟡 Baja | **G-02** | Clasificador ML (Random Forest/TF-IDF) y métricas F1 | — |
| 🟡 Baja | **G-10** | UI de historial ciudadano `/mis-consultas` (solo API) | HU-14 |
| 🟡 Baja | **G-15** | Fine-tuning QLoRA del SLM | — |
| 🟡 Baja | **G-17** | Contenerización front/back, balanceador, HTTPS, monitoreo | PMV3 |
| 🟡 Baja | **G-21** | Artefactos de PoC (dataset sintético, resultados) | PMV2 |
| 🟡 Baja | **G-23** | Rate limiting / protección contra saturación | PMV3 |
| 🟡 Baja | **G-24** | Auditoría de manipulación de documentos | HU-03 |
| 🟡 Baja | **G-25** | Aviso legal como política de API (solo en UI) | — |
| 🟡 Baja | **G-26** | Auditoría WCAG, pruebas de carga, SonarQube, ZAP | PMV2/PMV3 |

> El catálogo canónico de G-XX está en `DOCUMENTACION.md:69-95`. Este documento lo **reordena por
> prioridad** y lo cruza con las HU y los PMV que bloquea.

### 13.3 Ruta de cierre priorizada

| Orden | Bloque | Acción | Efecto en % |
|---|---|---|---|
| 1 | Corrección inmediata | Resolver branding (§12.1) y actualizar `PRESENTACION-PMV1.md` (§12.2) | — (correctitud) |
| 2 | Dato crítico | Cargar montos reales del TUPA en `tramites.costo` | HU-08 → 100 % |
| 3 | PMV2 | Motor de trámites relacionados (HU-12, G-08) | PMV2 44 % → ~60 % |
| 4 | PMV3 bloque 1 | `pytest` del flujo RAG (G-18) + JWT y roles (G-01) | PMV3 → ~45 % |
| 5 | PMV3 bloque 2 | Endpoint de métricas (G-16) + guardrails (G-20) | PMV3 → ~55 % |
| 6 | PMV1 cierre | Área responsable por trámite + estructura garantizada del SLM | PMV1 → ~100 % |
| 7 | Validación | k6 + auditoría WCAG + SonarQube (G-26) + dataset PoC (G-21) | habilita sustentación |

### 13.4 Proyección de avance

| Escenario | Global | PMV1 | PMV2 | PMV3 |
|---|---|---|---|---|
| **Estado actual (verificado)** | **49 %** | **88 %** | **44 %** | **34 %** |
| + montos TUPA y cierre HU-08 | ~52 % | 96 % | ~52 % | 34 % |
| + HU-12 + G-21 | ~56 % | 96 % | ~72 % | 34 % |
| + pytest + JWT (G-18, G-01) | ~62 % | 96 % | ~72 % | ~45 % |
| + métricas + guardrails (G-16, G-20) | ~68 % | 96 % | ~80 % | ~55 % |
| + retroalimentación + reportes + validación SUS | **75-80 %** | 100 % | ~88 % | ~70 % |

---

## 14. Cómo verificar este documento

```bash
# Cifras de trámites y documentos
grep -c "^\s*('" database/seeds/tramites.sql        # 22
grep -c "^\s*('" database/seeds/documentos.sql      # 20

# Endpoints
grep -rn "@router\.\(get\|post\|put\|delete\)" backend/infrastructure/controllers/

# Puertos del dominio
ls backend/domain/ports/                            # 7 ABC

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

*Documento maestro generado el 2 de octubre de 2026 a partir de HEAD `ff7a589`. Contrasta con el
código real del repositorio. Cuando el código cambie, actualiza §10 (cifras), §5 (inventario) y
§12 (inconsistencias).*

