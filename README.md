# Sistema de Trámites Municipales

Plataforma de orientación de trámites de la **Municipalidad Provincial de Junín** (MPJ),
que permite a los ciudadanos consultar procedimientos municipales mediante un
asistente conversacional basado en **RAG** (PostgreSQL + pgvector para la búsqueda
semántica) y un **SLM local** servido con **Ollama**.

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
├── docker-compose.yml        # PostgreSQL + pgvector, Redis y Ollama
├── requirements.txt          # Dependencias Python
└── .env                      # Variables de entorno
```

## Requisitos previos

- Docker y Docker Compose
- Python 3.11+
- Node.js 18+

## Puesta en marcha

### 1. Infraestructura

```bash
docker compose up -d
```

Levanta:
- **PostgreSQL 16 con pgvector** (puerto 5432). Las migraciones de `database/migrations`
  se ejecutan automáticamente en el primer arranque.
- **Redis 7** (puerto 6379) para la caché de respuestas.
- **Ollama** (puerto 11434) para el modelo de lenguaje local. Descarga un modelo:
  `docker exec -it tramites-ollama ollama pull qwen2.5:3b`

### 2. Datos de ejemplo

Los seeds cargan la Municipalidad Provincial de Junín y trámites reales del TUPA 2023
(registro civil, licencias, certificados, tributos y urbanismo).

```bash
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/municipios.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/tramites.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/documentos.sql
```

### 3. Back-end

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate            # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

Documentación interactiva: <http://localhost:8000/docs>

### 4. Front-end

```bash
cd frontend-tramites
npm install
npm run dev
```

Disponible en <http://localhost:3000>

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
