# Sistema de Trámites Municipales

Plataforma de orientación de trámites de la **Municipalidad Provincial de Junín** (MPJ),
que permite a los ciudadanos consultar procedimientos municipales mediante un
asistente conversacional basado en **RAG** (PostgreSQL + búsqueda semántica) y un
**SLM local** servido con **Ollama**.

La base de datos de conocimiento se alimenta del TUPA 2023 (252 procedimientos) y de
la documentación oficial publicada en <https://www.gob.pe/munijunin>.

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

## API principal

| Método | Ruta                       | Descripción                                    |
| ------ | -------------------------- | ---------------------------------------------- |
| POST   | `/api/consultas`           | Consulta en lenguaje natural (RAG + SLM)       |
| GET    | `/api/consultas/{id}`      | Trazabilidad de una consulta                   |
| GET    | `/api/tramites`            | Catálogo de trámites                           |
| GET    | `/api/tramites/{id}`       | Detalle del trámite y documentos vigentes      |
| POST   | `/api/documentos`          | Registra e indexa un documento (embeddings)    |
| PUT    | `/api/documentos/{id}/estado` | Cambia el estado de vigencia                |
| POST   | `/api/usuarios`            | Registro de usuarios                           |
| GET    | `/health`                  | Estado del servicio                            |

## Flujo de una consulta (RAG)

1. `ClasificarIntencion` clasifica la pregunta (ServicioNLP).
2. `RegistrarConsulta` persiste la consulta en PostgreSQL.
3. `ServicioRAG` recupera documentos con búsqueda vectorial (pgvector, HNSW) y
   genera la respuesta con el SLM de Ollama.
4. `EvaluadorGroundedness` calcula la confianza (alta/media/baja) para limitar
   alucinaciones.
5. `AuditarConsulta` registra la interacción y sus fuentes.
