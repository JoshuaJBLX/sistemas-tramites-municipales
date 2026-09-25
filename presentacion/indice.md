# Presentación Técnica — Sistema de Orientación de Trámites Municipales

**Resumen:** documentación técnica del sistema implementado (SLM + RAG local), lista para
exponer en la presentación del proyecto. Cada tema es un `.md` independiente, contrastado con
el código real del repositorio y con las rutas de archivo referenciadas.

**Índice y contenido breve:**

| Archivo | Qué contiene |
|---|---|
| `01-arquitectura-de-software.md` | Arquitectura hexagonal por capas, diagrama de dependencias, puertos/adaptadores, stack tecnológico y despliegue (Docker). |
| `02-frontend.md` | Frontend Next.js detallado: rutas, sistema de diseño, apartado de interfaces (contratos HTTP y modelos TypeScript), 15 componentes analizados uno a uno e integración con el backend (`lib/api.ts`). |
| `03-backend.md` | Backend FastAPI detallado: entry point, inyección de dependencias, controllers y endpoints, casos de uso, servicios, adaptadores y flujo de una consulta. |
| `04-base-de-datos.md` | Base de datos PostgreSQL + pgvector: migraciones, 6 tablas, relaciones, índices (HNSW), seeds y consultas vectoriales. |
| `05-implementaciones.md` | Estado real de implementación: qué está implementado vs. pendiente, HU por estado, vacíos G-XX y cómo reproducir el sistema. |

## Reproducción rápida (resumen)

1. `Copy-Item .env.example .env`
2. `docker compose up -d` e `ollama pull qwen2.5:3b`
3. Backend: `uvicorn main:app --port 8000` (en `backend/`)
4. Frontend: `npm run dev` (en `frontend-tramites/`)

Detalle completo: `../documentacion/00-documentos-rectores/03-ejecucion.md`