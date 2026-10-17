# Presentación Técnica — Sistema de Orientación de Trámites Municipales

> **Actualizado el 17 de octubre de 2026 (verificación en vivo).** Cifras verificadas contra la API y la BD local en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md): global **82 %** (83/101), PMV1 **100 %** ✅, PMV2 **100 %** ✅, PMV3 **63 %**; la API arranca (31 rutas) y los defectos D-14..D-23 están corregidos.

**Resumen:** documentación técnica del sistema implementado (SLM + RAG local), lista para
exponer en la presentación del proyecto. Cada tema es un `.md` independiente, contrastado con
el código real del repositorio y con las rutas de archivo referenciadas.

**Índice y contenido breve:**

| Archivo | Qué contiene |
|---|---|
| `01-arquitectura-de-software.md` | Arquitectura hexagonal por capas, diagrama de dependencias, puertos/adaptadores (10 puertos), stack tecnológico y despliegue (Docker). |
| `02-frontend.md` | Frontend Next.js detallado: rutas, sistema de diseño, apartado de interfaces (contratos HTTP y modelos TypeScript), 16 componentes analizados uno a uno e integración con el backend (`lib/api.ts`). |
| `03-backend.md` | Backend FastAPI detallado: entry point, inyección de dependencias, controllers y endpoints (22 declarados: 16 públicos + 6 admin), casos de uso, servicios, adaptadores y flujo de una consulta. |
| `04-base-de-datos.md` | Base de datos PostgreSQL + pgvector: migraciones (incluida `004_documentos_pmv2.sql`, ✅ aplicada), 6 tablas + `fragmentos_documento`, relaciones, índices (HNSW), seeds y consultas vectoriales. |
| `05-implementaciones.md` | Estado real de implementación: qué está implementado vs. pendiente, HU por estado y porcentaje, vacíos G-XX, defectos D-XX y cómo reproducir el sistema. |

## Reproducción rápida (resumen)

1. `Copy-Item .env.example .env`
2. `docker compose up -d` e `ollama pull qwen2.5:3b`
3. Backend: `uvicorn main:app --port 8000` (en `backend/`)
4. Frontend: `npm run dev` (en `frontend-tramites/`)

> ✅ **Estado de arranque (17-oct-2026, verificado):** el paso 3 funciona — la API arranca con
> **31 rutas** (D-14..D-23 corregidos). Detalle en
> [05-implementaciones.md](05-implementaciones.md).

Detalle completo: `../documentacion/00-documentos-rectores/03-ejecucion.md`