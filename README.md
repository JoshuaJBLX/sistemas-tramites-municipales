# Sistema de Trámites Municipales
> **Documento relacionado:** [06 · Estado actual implementado](documentacion/00-documentos-rectores/06-estado-actual-implementado.md) — documento rector y fuente única de verdad del estado y las cifras.

Plataforma de orientación de trámites de la **Municipalidad Provincial de Junín** (MPJ),
que permite a los ciudadanos consultar procedimientos municipales mediante un
asistente conversacional basado en **RAG** (PostgreSQL + búsqueda semántica) y un
**SLM local** servido con **Ollama**.

La base de datos de conocimiento se alimenta del TUPA 2023 (252 procedimientos) y de
la documentación oficial publicada en <https://www.gob.pe/munijunin>.

## Estado del proyecto (vigente, según documento rector 06)

| Métrica | Valor |
| --- | --- |
| Avance global | **101/101 = 100 %** (PMV1 24/24 = **100 %** · PMV2 28/28 = **100 %** · PMV3 49/49 = **100 %**, 18/18 HU completas) |
| Inventario | 104 `.py` de backend · 27 `.ts`/`.tsx` de fuente · 18 `.sql` · 94 `.md` |
| Endpoints | **40 rutas servibles** (36 operaciones en `/openapi.json` + 4 de documentación) |
| Catálogo | **252 procedimientos TUPA** con costo y área reales (272 trámites en BD) |
| Documentos | **45/45** con metadatos completos y **45/45 fragmentados** (56 fragmentos; RAG por fragmento activo) |
| Pruebas | 0 suites pytest formales (G-18); existen scripts de verificación (`scripts/probar_hu13.py`, `scripts/probar_hu151618.py`) |

> ✅ **PMV1, PMV2 y PMV3 cerrados al 100 %**. Las 18 historias de usuario están completas (**101/101 puntos**) según la fuente canónica: [`documentacion/00-documentos-rectores/06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md).
>
> **Nota:** el documento rector indica que la entidad implementada en código es **Huancayo (MPH)**; `README.md` mantiene referencias históricas a Junín/MPJ en secciones descriptivas (inconsistencia documental pendiente de decisión). Las cifras vigentes de estado son las de la tabla anterior y el documento 06.

## Estructura del proyecto

```
sistema-tramites-municipales/
├── frontend-tramites/        # Front-end (Next.js 14 + Tailwind CSS)
│   ├── app/                  # Rutas: /, /chat, /admin, /tramites
│   ├── components/           # ChatBox, TramiteCard, Navbar, Loading
│   └── lib/                  # api.ts y queries.ts (comunicación con el backend)
│
├── backend/                  # Back-end (Python + FastAPI, arquitectura hexagonal)
│   ├── domain/               # Núcleo: entities, value_objects, ports (interfaces)
│   ├── application/          # Casos de uso y servicios de aplicación (RAG, SLM, NLP)
│   └── infrastructure/       # Controllers (FastAPI), repositories (pgvector) y adapters
│
├── database/                 # Migraciones SQL, seeds y schema de referencia
├── instalar.ps1              # Instalador de un solo comando (idempotente)
├── docker-compose.yml        # PostgreSQL + pgvector, Redis y Ollama (opcional)
├── requirements.txt          # Dependencias Python
└── .env                      # Variables de entorno
```

## Requisitos previos

- Python 3.11+ (probado en 3.13)
- PostgreSQL 13+ (pgvector es **opcional**)
- Node.js 18+
- Ollama

## Instalación (una sola vez)

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```

El script instala y configura todo: verificaciones, `.env`, rol y base de datos, migraciones,
seeds, entorno virtual de Python, dependencias del front-end, Redis, modelo `qwen2.5:3b` y los
embeddings BGE-M3 de los documentos. Es **idempotente**: se puede repetir sin romper nada.

Detalle de cada paso en [`documentacion/00-documentos-rectores/03-ejecucion.md`](documentacion/00-documentos-rectores/03-ejecucion.md).

## Ejecución (cada vez)

```powershell
# API
.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000
```

```powershell
# Front-end, en otra terminal
cd frontend-tramites; npm run dev
```

- API → <http://localhost:8000> · Swagger → <http://localhost:8000/docs>
- App → <http://localhost:3000>

**Sobre pgvector:** la migración `002` crea la extensión `vector` cuando el servidor la tiene
disponible; si no, la columna `documentos.embedding` se crea como `double precision[]` y
`BusquedaVectorialAdapter` calcula la similitud de coseno en Python. El flujo RAG es idéntico
en ambos casos; con pgvector se usa el operador `<=>` y el índice HNSW (recomendado para producción).

## API principal (40 rutas servibles, según documento rector 06)

> **Nota:** la cantidad y clasificación de rutas/endpoints debe tomarse de `GET /openapi.json` y del documento rector [`06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md) (§6.2). El sistema incluye autenticación JWT y protección por roles en endpoints administrativos (HU-13/G-01 cerrados); algunas rutas permanecen públicas por diseño (p. ej. consulta ciudadana, evaluación, trazabilidad según política implementada). La tabla siguiente es un resumen orientativo y puede no reflejar la totalidad de rutas vigentes.

**Públicos (18):**

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| POST | `/api/consultas` | Consulta en lenguaje natural (RAG + SLM) |
| GET | `/api/consultas` | Listado de auditoría (`?limite=`) |
| GET | `/api/consultas/{id}` | Trazabilidad completa (respuesta, fuentes, confianza, banderas) |
| GET | `/api/tramites` | Catálogo de trámites |
| GET | `/api/tramites/{id}` | Detalle del trámite y documentos vigentes |
| GET | `/api/tramites/{id}/relacionados` | Trámites relacionados (HU-12) |
| POST | `/api/documentos` | Registra e indexa un documento (embeddings) |
| POST | `/api/documentos/upload` | Carga con validación de formato y extracción de texto (PMV2) |
| GET | `/api/documentos` | Listado con filtros `tramite_id`/`estado`/`incluir_eliminados` (PMV2) |
| GET | `/api/documentos/{id}` | Detalle de un documento |
| PUT | `/api/documentos/{id}/estado` | Cambia el estado (`vigente`/`obsoleto`/`en_revision`/`derogado`) |
| POST | `/api/documentos/{id}/procesar` | Reprocesa: fragmenta + embeddea (PMV2) |
| DELETE | `/api/documentos/{id}` | Baja lógica (marca `eliminado_en`) |
| DELETE | `/api/documentos/{id}/fisico` | Baja física de filas (borra fragmentos) |
| POST | `/api/usuarios` | Registro de usuarios |
| GET | `/api/usuarios/{id}` | Detalle de usuario |
| GET | `/api/usuarios/{id}/consultas` | Historial del usuario |
| GET | `/health` | Estado del servicio |

**Administración (9):**

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/api/admin/documentos` | Listado con filtros y paginación |
| POST | `/api/admin/documentos` | Crea por JSON y procesa en segundo plano |
| POST | `/api/admin/documentos/upload` | Carga `multipart/form-data` con metadatos (PMV2) |
| POST | `/api/admin/documentos/{id}/procesar` | Reprocesa un documento |
| PUT | `/api/admin/documentos/{id}/estado` | Cambia estado con validación (P2-11) |
| DELETE | `/api/admin/documentos/{id}` | Baja lógica |
| DELETE | `/api/admin/documentos/{id}/fisico` | Baja física |
| GET | `/api/tramites/admin` | Listado ampliado para el panel admin (272 filas) |
| PUT | `/api/tramites/{id}/area` | Actualiza `area_responsable` (HU-07) |

## Flujo de una consulta (RAG)

1. `ClasificarIntencion` clasifica la pregunta (ServicioNLP).
2. `RegistrarConsulta` persiste la consulta en PostgreSQL.
3. `ServicioRAG` recupera documentos con búsqueda vectorial (pgvector, HNSW) y
   genera la respuesta con el SLM de Ollama.
4. `EvaluadorGroundedness` calcula la confianza (alta/media/baja) para limitar
   alucinaciones.
5. `AuditarConsulta` registra la interacción y sus fuentes.
