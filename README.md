# Sistema de Trámites Municipales

Plataforma de orientación de trámites de la **Municipalidad Provincial de Junín** (MPJ),
que permite a los ciudadanos consultar procedimientos municipales mediante un
asistente conversacional basado en **RAG** (PostgreSQL + búsqueda semántica) y un
**SLM local** servido con **Ollama**.

La base de datos de conocimiento se alimenta del TUPA 2023 (252 procedimientos) y de
la documentación oficial publicada en <https://www.gob.pe/munijunin>.

## Estado del proyecto (16 de octubre de 2026, HEAD `ea06c9a`)

| Métrica | Valor |
| --- | --- |
| Avance global | **60/101 = 59 %** (PMV1 21/24 = **88 %** · PMV2 14/25 = **56 %** · PMV3 23/44 = **52 %** · Transversal 2/8 = 25 %) |
| Inventario | 86 `.py` de backend · 25 `.ts`/`.tsx` · 9 `.sql` · 90 `.md` · 6 controllers (1 stub) · 10 puertos · 16 componentes front-end |
| Endpoints | **22** declarados (16 públicos + 6 admin) — **0 servibles** hoy |
| Pruebas | 0 suites (`pytest` ausente, G-18) |

> ⚠️ **El backend PMV2 está escrito pero hoy no arranca**: `main.py` falla con `ImportError`
> (`tramite_admin_controller` es un stub), la migración `004` no está aplicada y faltan
> `pypdf`/`python-docx` en `requirements.txt`. Hasta cerrar los defectos **D-14..D-21** la
> demostración de carga y fragmentación de documentos está bloqueada.
> Detalle y plan de cierre en [`PMV2_DOCUMENTOS.md`](PMV2_DOCUMENTOS.md).

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

## API principal (22 endpoints: 16 públicos + 6 admin)

> ⚠️ **16-oct-2026:** el recuento publicado antes era de 13 rutas; hoy hay **22 endpoints
> declarados** (ver `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` §6.2), pero
> **0 son servibles** hasta resolver **D-14** (la API no arranca) y **D-15** (migración `004`
> sin aplicar). Ninguno valida autenticación ni rol (D-8).

**Públicos (16):**

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| POST | `/api/consultas` | Consulta en lenguaje natural (RAG + SLM) |
| GET | `/api/consultas/{id}` | Trazabilidad de una consulta |
| GET | `/api/tramites` | Catálogo de trámites |
| GET | `/api/tramites/{id}` | Detalle del trámite y documentos vigentes |
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

**Administración (6) — prefijo `/api/admin/documentos`:**

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/api/admin/documentos` | Listado con filtros y paginación |
| POST | `/api/admin/documentos` | Crea por JSON y procesa en segundo plano |
| POST | `/api/admin/documentos/upload` | Carga `multipart/form-data` con metadatos (PMV2) |
| POST | `/api/admin/documentos/{id}/procesar` | Reprocesa un documento |
| DELETE | `/api/admin/documentos/{id}` | Baja lógica |
| DELETE | `/api/admin/documentos/{id}/fisico` | Baja física |

## Flujo de una consulta (RAG)

1. `ClasificarIntencion` clasifica la pregunta (ServicioNLP).
2. `RegistrarConsulta` persiste la consulta en PostgreSQL.
3. `ServicioRAG` recupera documentos con búsqueda vectorial (pgvector, HNSW) y
   genera la respuesta con el SLM de Ollama.
4. `EvaluadorGroundedness` calcula la confianza (alta/media/baja) para limitar
   alucinaciones.
5. `AuditarConsulta` registra la interacción y sus fuentes.
