# 05 — Implementaciones

> Estado real, qué se construyó, qué falta (G-XX) y cómo reproducirlo

## 1. ¿Qué está implementado de verdad? (resumen)

**Núcleo RAG funcional (backend):**

- ✅ API REST completa: consultas, trámites, documentos y usuarios (`backend/infrastructure/controllers/`).
- ✅ Flujo de consulta end-to-end: clasificación de intención → registro → caché → RAG → SLM →
  groundedness → auditoría (`consulta_controller.py`, `container.py`).
- ✅ Búsqueda semántica con **pgvector + HNSW** y umbral 0.3 (`BusquedaVectorialAdapter.py`).
- ✅ Embeddings **BGE-M3** (1024 dims, CPU, async) (`BGE_M3Adapter.py`).
- ✅ SLM local **Qwen 2.5 3B** vía Ollama con temperatura 0.2 (`OllamaAdapter.py`).
- ✅ Evaluador de **groundedness** por cobertura léxica (alta/media/baja) (`EvaluadorGroundedness.py`).
- ✅ Caché de respuestas en **Redis** (TTL 3600 s) (`ServicioCache.py`, `RedisAdapter.py`).
- ✅ Auditoría persistida en `auditoria_consultas` (`container.py:42-64`).
- ✅ Gestión documental: registrar (con indexado automático), cambiar estado, upload (storage local),
  consultar y eliminar.
- ✅ Usuarios: registro, consulta e historial (últimas 50).

**Frontend funcional:**

- ✅ Chat con sugerencias rápidas, burbujas, groundedness y fuentes (`ChatBox`, `ChatThread`,
  `GroundednessBadge`).
- ✅ Catálogo TUPA con buscador y filtros (`/tramites`).
- ✅ Landing y dashboard (`/` y `/admin`) con diseño cálido rediseñado.
- ✅ Integración real con `POST /api/consultas`, `GET /api/tramites`, `GET /api/health`, con
  **fallback demo** si el backend cae (`lib/api.ts`).

**Infraestructura:**

- ✅ Docker Compose de 3 servicios (PostgreSQL+pgvector, Redis, Ollama) con healthchecks y volúmenes.
- ✅ Migraciones automáticas y seeds TUPA 2023 (10 trámites / 6 documentos / 1 municipalidad).

## 2. Estado por Historia de Usuario (las 18)

| ID | Historia | Estado | Brecha principal |
|---|---|---|---|
| HU-01 | Carga de documentos | ⚠️ | Sin validación PDF ni extracción de texto (G-12) |
| HU-02 | Vigencia/versión/fuente | ⚠️ | Sin campos `version`/`fecha` (G-13) |
| HU-03 | Aprobar/derogar documentos | ⚠️ | Sin flujo por roles, sin baja lógica |
| HU-04 | Procesamiento documental y RAG | ⚠️ | Sin chunking ni OCR (G-13) |
| HU-05 | Consulta ciudadana | ⚠️ | No identifica "trámite probable" |
| HU-06 | Clasificación de intención | ⚠️ | Regex, sin confianza ni ML (G-02) |
| HU-07 | Orientación de requisitos | ⚠️ | Sin lista estructurada garantizada |
| HU-08 | Costos y plazos | ⚠️ | El chat ignora `costo`/`duracion` del catálogo (G-14) |
| HU-09 | Respuestas con SLM | ⚠️ | Basicamente ✅; sin plantilla de salida formal |
| HU-10 | Trazabilidad/anti-alucinación | ⚠️ | API no devuelve respuesta/fuentes (G-16) |
| HU-11 | Fuera de dominio | ❌ | Sin clasificador de dominio |
| HU-12 | Trámites relacionados | ❌ | (G-08) |
| HU-13 | Usuarios y seguridad | ⚠️ | Solo registro; sin login/roles (G-01) |
| HU-14 | Auditoría | ⚠️ | Solo persistencia; UI mock (G-07) |
| HU-15 | Retroalimentación | ❌ | (G-05) |
| HU-16 | Métricas y monitoreo | ❌ | Solo maqueta (G-06/G-16) |
| HU-17 | Derivación municipal | ⚠️ | Solo nota genérica (G-09) |
| HU-18 | Reportes y exportación | ❌ | (G-07) |

## 3. Catálogo de vacíos de código (G-XX) — resumen

| Código | Vacío |
|---|---|
| G-01 | Autenticación/JWT/roles y control de acceso |
| G-02 | Clasificador ML (actual: regex heurístico) |
| G-03 | Enmascaramiento de PII en la entrada |
| G-04 | Abstención / umbral de groundedness con rechazo |
| G-05 | Retroalimentación ciudadana (útil/no útil) |
| G-06 / G-16 | Métricas reales (KPIs, latencia) — hoy maqueta |
| G-07 | Reportes / exportación |
| G-08 | Recomendación de trámites relacionados |
| G-09 | Derivación a atención municipal |
| G-10 | UI de historial `/mis-consultas` |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas admin |
| G-12 | Carga de documentos conectada al backend (maqueta) |
| G-13 | Chunking, `version`, `fecha_publicacion`, página de la fuente |
| G-14 | Consistencia `tipo`/`duracion_estimada_dias` vs `categoria`/`plazo` |
| G-15 | Fine-tuning QLoRA del SLM |
| G-17 | Contenerización frontend/backend, balanceador, HTTPS, monitoreo |
| G-18 | Suite de pruebas automatizadas (pytest) |
| G-20 | Guardrails anti prompt-injection |
| G-21 | Artefactos de PoC (dataset, resultados) |
| G-23 | Rate limiting |
| G-24 | Auditoría de manipulación de documentos |
| G-25 | Aviso legal como política de API (solo UI) |
| G-26 | WCAG, pruebas de carga, SonarQube, ZAP |

## 4. Decisiones de diseño tomadas e implementadas

1. **Huancayo (a.md) → Junín (código)**: los datos y seeds usan la **MPJ** (TUPA 2023).
2. **Paleta azul fría → estilo cálido/orgánico**: rediseño UI completo (`globals.css`).
3. **RAG por defecto**: la respuesta siempre pasa por recuperación semántica (no hay modo
   "solo SLM" en producción); abstención si no hay contexto.
4. **Fallo → demo**: el frontend no se rompe sin backend (respuestas fundamentadas locales).
5. **Embeddings al registrar**: `GestionarDocumentos.registrar` indexa el documento en el mismo
   paso del alta (upsert con `embedding`).
6. **Groundedness = cobertura léxica** simple (no coseno de embeddings) — documentado como
   limitación cualitativa.

## 5. Cómo reproducir el sistema (paso a paso)

### Infraestructura (una vez)
```powershell
Copy-Item .env.example .env                                  # configuración
docker compose up -d                                          # postgres + redis + ollama
docker exec -it tramites-ollama ollama pull qwen2.5:3b        # SLM local
docker compose ps                                             # esperar a healthy
```

### Backend (puerto 8000)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```
- Docs: http://localhost:8000/docs · Health: http://localhost:8000/health

### Frontend (puerto 3000)
```powershell
cd frontend-tramites
npm install
npm run dev
```
- App: http://localhost:3000

### Datos (si no se aplicaron los seeds)
```powershell
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/municipios.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/tramites.sql
psql -h localhost -U tramites -d tramites_municipales -f database/seeds/documentos.sql
```

### Prueba rápida de la API
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/consultas `
  -ContentType 'application/json' `
  -Body '{"pregunta":"¿Qué necesito para la licencia de funcionamiento?"}'
```

## 6. Grafos de implementación (qué falta para "producción")

```
HU 100%  ▓▓▓▓▓▓▓▓░░░░░░░░░░░░   (HU-01..10 y 13/14 parciales, 11/12/15/16/18 ausentes)
Gaps     ▓░░░░░░░░░░░░░░░░░░░   (G-01, G-04, G-12, G-16, G-18 prioritarios)
```
**Prioridad sugerida** para cerrar presentación y validación: **G-18 (pytest)** → **G-16
(métricas)** → **G-01 (auth)** → **G-12 (upload real)** → **G-04 (abstención)**.