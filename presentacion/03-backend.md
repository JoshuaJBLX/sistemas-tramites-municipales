# 03 — Backend

> FastAPI 0.111 · Python 3.11+ · Arquitectura hexagonal · RAG + SLM

## 1. Entry point (`backend/main.py`)

- `load_dotenv()` lee `.env` de la raíz.
- *lifespan* abre el **pool de PostgreSQL** y crea el contenedor de dependencias al arrancar;
  cierra el pool y la conexión Redis al apagar (`main.py:24-36`).
- Aplica **CORS** (orígenes del frontend local), incluye 4 routers y expone `GET /health`.

## 2. Inyección de dependencias (`infrastructure/container.py`)

Único punto de cableado. `crear_container()` construye:

```
Connection (asyncpg pool)
→ BGE_M3Adapter (embeddings)
→ BusquedaVectorialAdapter (pgvector)     → BusquedaSemanticaPort
→ OllamaAdapter (SLM)                     → GeneracionRespuestaPort
→ RedisAdapter                            → CachePort
→ DocumentStorageAdapter (archivos)
→ _AuditoriaPostgreSQL                    → AuditoriaPort
→ DocumentoRepositoryImpl / ConsultaRepositoryImpl
→ Servicios (NLP, SLM, RAG, Orientacion, Cache, Auditoria, Groundedness)
→ 7 casos de uso
```

Parámetros configurables vía entorno: `RAG_TOP_K` (5), `CACHE_TTL_SEGUNDOS` (3600).

## 3. Endpoints de la API

### 3.1 Consultas (`/api/consultas`)

| Método | Ruta | Descripción | Respuesta |
|---|---|---|---|
| POST | `/api/consultas` | Clasifica intención, registra, cachea, genera orientación RAG y audita | `{consulta_id, intencion, texto, confianza, fuentes[{url, fragmento}]}` |
| GET | `/api/consultas/{id}` | Trazabilidad básica de la consulta | `{id, usuario_id, pregunta, intencion, creada_en}` |

Entrada: `{pregunta: str (min 3), usuario_id?: UUID}` — validada con Pydantic.

### 3.2 Trámites (`/api/tramites`)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tramites?municipalidad_id=` | Lista del catálogo (JOIN municipalidades) |
| GET | `/api/tramites/{id}` | Detalle + `documentos[]` vigentes del trámite (uso de `ConsultarTramite` + caché Redis 30 min) |

### 3.3 Documentos (`/api/documentos`) — Gestión documental

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/documentos` | Registra documento por JSON; **genera embedding** automáticamente e indexa |
| POST | `/api/documentos/upload` | Guarda el archivo original en disco (`storage/documentos`) |
| PUT | `/api/documentos/{id}/estado` | Cambia vigencia (`vigente|obsoleto|en_revision`) |
| GET | `/api/documentos/{id}` | Consulta un documento |
| DELETE | `/api/documentos/{id}` | Borra físicamente |

### 3.4 Usuarios (`/api/usuarios`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/usuarios` | Registra usuario (`rol`: ciudadano/administrador, `correo` EmailStr) |
| GET | `/api/usuarios/{id}` | Detalle de usuario |
| GET | `/api/usuarios/{id}/consultas` | Historial (últimas 50 consultas) |

### 3.5 Operación

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | `{status:'ok'}` |

Docs interactivas en `http://localhost:8000/docs` (OpenAPI automática de FastAPI).

## 4. Capa de aplicación

### 4.1 Casos de uso (`application/use_cases/`)

| Caso de uso | Responsabilidad |
|---|---|
| `ClasificarIntencion` | Encapsula la clasificación de intención |
| `RegistrarConsulta` | Valida y persiste la consulta |
| `ConsultarTramite` | Documentos vigentes de un trámite (con caché Redis) |
| `BuscarDocumentos` | Recuperación semántica de documentos vigentes |
| `GenerarOrientacion` | Orquesta la orientación ciudadana (RAG + grounding) |
| `GestionarDocumentos` | CRUD + indexación (embedding) de documentos |
| `AuditarConsulta` | Persiste y consulta trazabilidad |

### 4.2 Servicios (`application/services/`)

- **`ServicioNLP`** — clasificador de intención **heurístico** (regex + normalización Unicode,
  sin tildes/puntuación). 6 intenciones: `consultar_requisitos`, `consultar_costo`,
  `consultar_estado`, `consultar_ubicacion`, `saludo`, `otro`. *(Si se cae a `OTRO`, responde
  genérico; no usa ML, G-02.)*
- **`ServicioRAG`** — recupera con `BusquedaSemanticaPort` (top_k=5), filtra `vigente`, construye
  fuentes (`url` + primer fragmento de 280 chars) y delega la respuesta al SLM.
- **`ServicioSLM`** — plantilla de sistema anti-alucinación ("responde solo con el contexto") y
  abstención si no hay documentos recuperados.
- **`EvaluadorGroundedness`** — **cobertura léxica**: proporción de términos (>3 letras) de la
  respuesta presentes en el contexto. Umbrales: **ALTA ≥ 0.75, MEDIA ≥ 0.40**, si no → BAJA.
- **`ServicioOrientacion`** — si `BAJA` pero con fuentes, agrega nota de advertencia al texto.
- **`ServicioCache`** — clave `consulta:{sha256(pregunta.lower)}`, TTL configurable.
- **`ServicioAuditoria`** — delega el registro en `AuditoriaPort`.

## 5. Capa de dominio

### 5.1 Entidades (`domain/entities/`)
`Tramite` · `Documento` (con `esta_vigente()` y `embedding`) · `Consulta` · `Respuesta`
(con `es_confiable()`) · `Usuario` · `Municipalidad` · `Fuente`.

### 5.2 Value Objects (`domain/value_objects/`)
`IntencionConsulta` (6) · `NivelConfianza` (alta/media/baja) · `EstadoDocumento`
(vigente/obsoleto/en_revision) · `TipoTramite` (6 tipos) · `FuenteOficial`.

### 5.3 Puertos (`domain/ports/`) — interfaces ABC
`BusquedaSemanticaPort` · `GeneracionRespuestaPort` · `CachePort` · `AuditoriaPort` ·
`DocumentoRepository` · `ConsultaRepository`.

## 6. Adaptadores (`infrastructure/adapters/`)

| Adaptador | Tecnología | Detalle |
|---|---|---|
| `BusquedaVectorialAdapter` | PostgreSQL + pgvector | SQL con `embedding <=> $1::vector`, filtro `estado='vigente'`, `LIMIT`, umbral similitud **0.3**, reconstruye `Documento` |
| `BGE_M3Adapter` | sentence-transformers | Modelo `BAAI/bge-m3`, 1024 dims, CPU (configurable `EMBEDDING_DEVICE`), ejecución en `asyncio.to_thread` para no bloquear el loop |
| `OllamaAdapter` | httpx → Ollama | `qwen2.5:3b`, system prompt propio, `temperature=0.2`, `num_predict=512`, `stream=False`, timeout 120 s |
| `RedisAdapter` | redis.asyncio | JSON serializado, TTL, cierre de cliente |
| `DocumentStorageAdapter` | filesystem | Guarda/lee/elimina listado en `storage/documentos` |

## 7. Repositorios (`infrastructure/repositories/`)

- `Connection` — pool `asyncpg` (min 1, max 10), DSN desde entorno (`POSTGRES_*`).
- `PostgreSQLRepository` — helpers `fetch`, `fetchrow`, `execute`.
- `DocumentoRepositoryImpl` — **upsert** con `ON CONFLICT DO UPDATE` (incluye `embedding`),
  listado por trámite, borrado.
- `ConsultaRepositoryImpl` — insert/upsert con actualización de intención, consultas por id/usuario.

## 8. Seguridad implementada

- ✅ Validación Pydantic v2 (límites, `EmailStr`, regex en rol).
- ✅ SQL 100% parametrizado (`$1..$n`) con asyncpg → previene inyección.
- ✅ CORS solo para localhost:3000.
- ⚠️ Pendiente: autenticación/JWT/roles (G-01), guardrails anti prompt-injection (G-20),
  rate limiting (G-23), enmascaramiento PII (G-03).

## 9. Cómo se relaciona con el frontend

El frontend consume **solo 3 endpoints** (`POST /api/consultas`, `GET /api/tramites`,
`GET /api/health`) a través de `lib/api.ts`. El resto de la API (documentos, usuarios) existe
para gestión y trazabilidad, y queda disponible para el panel administrativo futuro (G-16).