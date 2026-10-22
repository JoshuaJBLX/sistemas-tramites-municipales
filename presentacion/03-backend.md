# 03 — Backend
> **Documento relacionado:** [06 · Estado actual implementado](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md) — documento rector y fuente única de verdad del estado y las cifras.

> **Actualizado el 17 de octubre de 2026 (verificación en vivo).** Cifras verificadas contra la API y la BD local en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md): global **82 %** (83/101), PMV1 **100 %** ✅, PMV2 **100 %** ✅, PMV3 **63 %**; la API arranca (31 rutas) y los defectos D-14..D-23 están corregidos.

> FastAPI 0.111 · Python 3.11+ · Arquitectura hexagonal · RAG + SLM

## 1. Entry point (`backend/main.py`)

- `load_dotenv()` lee `.env` de la raíz.
- *lifespan* abre el **pool de PostgreSQL** y crea el contenedor de dependencias al arrancar;
  cierra el pool y la conexión Redis al apagar (`main.py:24-36`).
- Aplica **CORS** (orígenes del frontend local), incluye **7 routers** (consulta, tramite,
  documento, usuario, documento_admin, tramite_admin y administración) y expone `GET /health`.
- ✅ **La app arranca (17-oct-2026):** verificado con `import main` → **31 rutas** servibles
  (los defectos D-14..D-23 están corregidos).

## 2. Inyección de dependencias (`infrastructure/container.py`)

Único punto de cableado. `crear_container()` construye:

```
Connection (asyncpg pool)
→ BGE_M3Adapter (embeddings)
→ BusquedaVectorialAdapter (pgvector)     → BusquedaSemanticaPort
→ OllamaAdapter (SLM)                     → GeneracionRespuestaPort
→ RedisAdapter                            → CachePort
→ DocumentStorageAdapter (archivos)       → AlmacenamientoDocumentosPort  [PMV2]
→ ExtraccionTextoAdapter (PDF/DOCX/TXT)   → ExtraccionTextoPort           [PMV2]
→ _AuditoriaPostgreSQL                    → AuditoriaPort
→ DocumentoRepositoryImpl / ConsultaRepositoryImpl / FragmentoRepositoryImpl [PMV2]
→ TramiteCatalogoAdapter                  → TramiteCatalogoPort
→ 8 servicios (NLP, SLM, RAG, Orientacion, Cache, Auditoria, Groundedness, Chunking)
→ 10 casos de uso (los 7 clásicos + IdentificarTramiteProbable, CargarDocumento y ProcesarDocumento)
```

El cableado vive en `container.py:104-171`. Parámetros configurables vía entorno: `RAG_TOP_K` (5),
`CACHE_TTL_SEGUNDOS` (3600).

## 3. Endpoints de la API

**31 rutas servibles: 18 públicas + 9 admin + 4 de documentación**, repartidos en 7 controllers. ✅ **Todos servibles hoy (17-oct-2026): `import main` → 31 rutas** (D-14..D-23 corregidos).

### 3.1 Consultas (`/api/consultas`)

| Método | Ruta | Descripción | Respuesta |
|---|---|---|---|
| POST | `/api/consultas` | Clasifica intención, registra, cachea, genera orientación RAG y audita | `{consulta_id, intencion, texto, confianza, groundedness, confianza_intencion, pide_aclaracion, tramite_probable, fuentes[{titulo, url, fragmento, numero, fecha, version}], afirmaciones_bloqueadas, fuera_dominio, entidad_sugerida}` |
| GET | `/api/consultas` | **Listado de auditoría (HU-10/HU-14 ✅):** `?limite=` (1..100) | `[{id, usuario_id, pregunta, intencion, creada_en, respuesta, confianza, groundedness, fuentes, ...}]` |
| GET | `/api/consultas/{id}` | **Trazabilidad completa (HU-10/D-9 ✅):** consulta + respuesta, confianza, groundedness, fuentes (número/fecha/versión), bloqueo y fuera de dominio | `{id, usuario_id, pregunta, intencion, creada_en, respuesta, confianza, groundedness, fuentes, afirmaciones_bloqueadas, fuera_dominio, entidad_sugerida, registrado_en}` |

Entrada: `{pregunta: str (min 3), usuario_id?: UUID}` — validada con Pydantic (la UI envía solo
`pregunta`).

### 3.2 Trámites (`/api/tramites`)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tramites?municipalidad_id=` | Lista del catálogo (JOIN municipalidades) |
| GET | `/api/tramites/{id}` | Detalle + `documentos[]` vigentes del trámite (uso de `ConsultarTramite` + caché Redis 30 min) |

### 3.3 Documentos (`/api/documentos`) — Gestión documental

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/documentos` | Registra documento por JSON; **genera embedding** automáticamente e indexa; valida metadatos (`requiere_metadatos()`) |
| POST | `/api/documentos/upload` | Valida extensión (`FormatoDocumento`), extrae texto, guarda el archivo en `storage/documentos`, registra, indexa y fragmenta (PMV2) |
| GET | `/api/documentos` | Listado con filtros `tramite_id`/`estado`/`incluir_eliminados` + `limite`/`desde` (PMV2) |
| PUT | `/api/documentos/{id}/estado` | Cambia vigencia (`vigente\|obsoleto\|en_revision\|derogado`) |
| GET | `/api/documentos/{id}` | Consulta un documento |
| POST | `/api/documentos/{id}/procesar` | Reprocesa: `ServicioChunking` + embedding por fragmento, idempotente (PMV2) |
| DELETE | `/api/documentos/{id}` | **Baja lógica**: marca `eliminado_en` y devuelve 204 (PMV2) |
| DELETE | `/api/documentos/{id}/fisico` | **Baja física** de filas (borra fragmentos) y devuelve 204 (PMV2) |

### 3.4 Administración de documentos (`/api/admin/documentos`) — PMV2

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/admin/documentos` | Listado con filtros y paginación (hasta 500) |
| POST | `/api/admin/documentos` | Crea por JSON y procesa en segundo plano |
| POST | `/api/admin/documentos/upload` | Carga `multipart/form-data` (`tramite_id`, `titulo`, `url_origen`, `version`, `fecha_publicacion`, `estado`, `archivo`) |
| POST | `/api/admin/documentos/{id}/procesar` | Reprocesa un documento (404 si no existe) |
| DELETE | `/api/admin/documentos/{id}` | Baja lógica; 204 |
| DELETE | `/api/admin/documentos/{id}/fisico` | Baja física; 204 |

Estos 6 repiten la funcionalidad pública bajo otro prefijo y son la superficie que consume
`DocumentManager.tsx`. ⚠️ Ninguno valida autenticación ni rol (**D-8**); `documento_admin_controller.py:48`
puede devolver 500 en vez de 422 ante un `estado` inválido (**D-18**).

### 3.5 Usuarios (`/api/usuarios`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/usuarios` | Registra usuario (`rol`: ciudadano/administrador, `correo` EmailStr) |
| GET | `/api/usuarios/{id}` | Detalle de usuario |
| GET | `/api/usuarios/{id}/consultas` | Historial (últimas 50 consultas) |

### 3.6 Operación

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | `{status:'ok'}` — **no** comprueba BD, Redis ni Ollama (**D-11**) |

Docs interactivas en `http://localhost:8000/docs` (OpenAPI automática de FastAPI) — hoy
inaccesibles mientras persista D-14.

## 4. Capa de aplicación

### 4.1 Casos de uso (`application/use_cases/`)

| Caso de uso | Responsabilidad |
|---|---|
| `ClasificarIntencion` | Devuelve la intención o la `ClasificacionIntencion` completa (intención + confianza) |
| `RegistrarConsulta` | Valida y persiste la consulta |
| `GenerarOrientacion` | Orquesta la orientación ciudadana (RAG + grounding) |
| `IdentificarTramiteProbable` | Deduce el trámite del catálogo sumando similitudes; si nada domina, no propone ninguno |
| `ConsultarTramite` | Documentos vigentes de un trámite (con caché Redis) |
| `BuscarDocumentos` | Recuperación semántica de documentos vigentes |
| `GestionarDocumentos` | CRUD + indexación (embedding) + `listar()` con filtros + baja lógica/física (PMV2) |
| `AuditarConsulta` | Persiste y consulta trazabilidad |
| `CargarDocumento` | **Nuevo (PMV2):** valida extensión → extrae texto → almacena → registra con metadatos → indexa → fragmenta |
| `ProcesarDocumento` | **Nuevo (PMV2):** borra fragmentos, ejecuta `ServicioChunking`, embeddea y persiste en lote; idempotente |

### 4.2 Servicios (`application/services/`)

- **`ServicioNLP`** — clasificador de intención **heurístico** por raíces léxicas + normalización
  Unicode (sin tildes/puntuación), con confianza `0.55 + 0.15 × (patrones−1)` y desempate por
  especificidad. **9 intenciones**: `consultar_requisitos`, `consultar_costo`, `consultar_plazo`,
  `consultar_pasos`, `consultar_area`, `consultar_estado`, `consultar_ubicacion`, `saludo`,
  `otro`. *(Si se cae a `OTRO`, pide aclaración; no usa ML, G-02.)*
- **`ServicioRAG`** — recupera con `BusquedaSemanticaPort` (top_k=5), filtra `vigente`, construye
  fuentes (`titulo` + `url` + primer fragmento de 280 chars) y delega la respuesta al SLM.
- **`ServicioSLM`** — plantilla de sistema anti-alucinación ("responde solo con el contexto") y
  abstención si no hay documentos recuperados.
- **`EvaluadorGroundedness`** — **cobertura léxica**: proporción de términos (>3 letras) de la
  respuesta presentes en el contexto. Umbrales: **ALTA ≥ 0.75, MEDIA ≥ 0.40**, si no → BAJA.
- **`ServicioOrientacion`** — orquesta el flujo completo: aclaración ambigua, recuperación,
  generación, groundedness, nota de advertencia si `BAJA`, identificación del trámite probable y
  anexo de datos estructurados (requisitos, arancel, plazo) tomados de la BD.
- **`ServicioCache`** — clave `consulta:{sha256(pregunta.lower)}`, TTL configurable.
- **`ServicioAuditoria`** — delega el registro en `AuditoriaPort`.
- **`ServicioChunking`** — **nuevo (PMV2)**: segmentador determinista sin dependencias externas —
  párrafos → oraciones → bloques de ~800 caracteres con **solape de 120**. Es el cumplimiento
  parcial de G-13 (faltan OCR y la recuperación RAG *por fragmento*).

## 5. Capa de dominio

### 5.1 Entidades (`domain/entities/`) — 8
`Tramite` · `Documento` (con `esta_vigente()`, `esta_eliminado()`, `requiere_metadatos()` y los
metadatos `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`,
`fragmentado`, `eliminado_en`) · **`FragmentoDocumento` (nuevo, PMV2)** · `Consulta` · `Respuesta`
(con `es_confiable()` y `con_datos_estructurados()`) · `Usuario` · `Municipalidad` · `Fuente`.
Además `domain/errors.py` define los errores de dominio `FormatoNoSoportadoError`,
`DocumentoIlegibleError` y `DocumentoInvalidoError`.

### 5.2 Value Objects (`domain/value_objects/`) — 8
`IntencionConsulta` (**9** valores) · `ClasificacionIntencion` · `TramiteProbable` ·
`NivelConfianza` (alta/media/baja) · `EstadoDocumento` (vigente/obsoleto/en_revision/
**derogado**) · **`FormatoDocumento`** (nuevo, PMV2: `.pdf/.docx/.txt/.md` → MIME) ·
`TipoTramite` (6 tipos) · `FuenteOficial`.

### 5.3 Puertos (`domain/ports/`) — 10 interfaces ABC
`BusquedaSemanticaPort` · `GeneracionRespuestaPort` · `CachePort` · `AuditoriaPort` ·
`DocumentoRepository` · `ConsultaRepository` · `TramiteCatalogoPort` · **`AlmacenamientoDocumentosPort`**
· **`ExtraccionTextoPort`** · **`FragmentoRepository`** (los 3 últimos, nuevos en el PMV2; eran 7
puertos antes de `ea06c9a`).

## 6. Adaptadores (`infrastructure/adapters/`)

| Adaptador | Tecnología | Detalle |
|---|---|---|
| `BusquedaVectorialAdapter` | PostgreSQL + pgvector | SQL con `embedding <=> $1::vector`, filtro `estado='vigente'`, `LIMIT`, umbral similitud **0.3**, reconstruye `Documento` |
| `BGE_M3Adapter` | sentence-transformers | Modelo `BAAI/bge-m3`, 1024 dims, CPU (configurable `EMBEDDING_DEVICE`), ejecución en `asyncio.to_thread` para no bloquear el loop |
| `OllamaAdapter` | httpx → Ollama | `qwen2.5:3b`, system prompt propio, `temperature=0.2`, `num_predict=512`, `stream=False`, timeout 120 s |
| `RedisAdapter` | redis.asyncio | JSON serializado, TTL, cierre de cliente; degradable (si Redis cae, sigue sin caché) |
| `TramiteCatalogoAdapter` | PostgreSQL | Resuelve los trámites vinculados a los documentos recuperados (`JOIN documentos`), para `IdentificarTramiteProbable` |
| `DocumentStorageAdapter` | filesystem | Guarda/lee/elimina/lista archivos en `storage/documentos` con nombre `uuid4.ext` — cumple `AlmacenamientoDocumentosPort` (PMV2). ✅ `eliminar()` se invoca en la baja física (D-19 cerrado) |
| `ExtraccionTextoAdapter` | pypdf / python-docx | **Nuevo (PMV2):** extrae texto de `.pdf`, `.docx`, `.txt` y `.md`; si falta la librería o el archivo es escaneado lanza `DocumentoIlegibleError`. ✅ `pypdf`/`python-docx` en `requirements.txt` (D-17 cerrado) |

## 7. Repositorios (`infrastructure/repositories/`)

- `Connection` — pool `asyncpg` (min 1, max 10), DSN desde entorno (`POSTGRES_*`).
- `PostgreSQLRepository` — helpers `fetch`, `fetchrow`, `execute`.
- `DocumentoRepositoryImpl` — **upsert** con `ON CONFLICT DO UPDATE` (incluye `embedding`),
  listado por trámite, `listar()` con filtros, `marcar_eliminado()` y `eliminar_fisico()` (PMV2).
- `ConsultaRepositoryImpl` — insert/upsert con actualización de intención, consultas por id/usuario.
- `FragmentoRepositoryImpl` — **nuevo (PMV2):** `guardar_lote`, `listar_por_documento` y
  `eliminar_por_documento` sobre `fragmentos_documento` (✅ tabla creada y poblada con 004).

## 8. Seguridad implementada

- ✅ Validación Pydantic v2 (límites, `EmailStr`, regex en rol).
- ✅ SQL 100% parametrizado (`$1..$n`) con asyncpg → previene inyección.
- ✅ CORS solo para localhost:3000.
- ⚠️ Pendiente: autenticación/JWT/roles (G-01), guardrails anti prompt-injection (G-20),
  rate limiting (G-23), enmascaramiento PII (G-03).
- ⚠️ **`Usuario.es_administrador()` existe pero nunca se invoca (D-8):** ningún endpoint —ni los 9
  de administración— comprueba autenticación ni rol; `container.py` expone el contenedor
  completo a cualquier petición.

## 9. Cómo se relaciona con el frontend

El frontend consume **4 endpoints públicos** (`POST /api/consultas`, `GET /api/consultas`,
`GET /api/tramites`, `GET /health`) y, desde el PMV2, **funciones de administración**
(`/api/admin/documentos*` más `GET /api/tramites/admin`) a través de `lib/api.ts`. El resto de la API
(documentos públicos, usuarios) existe para gestión y trazabilidad.

✅ **Todo funciona (17-oct-2026):** la API arranca (31 rutas), los `DELETE` devuelven `204` sin
error en el front (D-20) y el panel admin opera con rutas existentes (D-21). Las llamadas del
frontend al panel admin usan ahora `PUT /api/admin/documentos/{id}/estado` (nuevo, D-23).