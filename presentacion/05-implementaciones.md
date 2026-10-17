# 05 — Implementaciones

> **Actualizado el 17 de octubre de 2026 (verificación en vivo).** Cifras verificadas contra la API y la BD local en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md): global **82 %** (83/101), PMV1 **100 %** ✅, PMV2 **100 %** ✅, PMV3 **63 %**; la API arranca (31 rutas), las migraciones `004`/`005`/`006` están aplicadas y los defectos D-14..D-23 están corregidos.

> Estado real, qué se construyó, qué falta (G-XX / D-XX) y cómo reproducirlo

## 1. ¿Qué está implementado de verdad? (resumen)

> ✅ **Código escrito = sistema en marcha (17-oct-2026).** Todo lo de abajo está verificado contra
> la API en ejecución: **la API arranca (31 rutas)**, las migraciones `004`/`005`/`006` están
> aplicadas y el panel de documentos del `/admin` carga y opera (defectos D-14..D-23 corregidos; §3).

**Núcleo RAG funcional (backend):**

- ✅ API REST **en marcha**: 31 rutas (18 públicas + 9 admin + 4 de doc) en 7 controllers
  (`backend/infrastructure/controllers/`).
- ✅ Flujo de consulta end-to-end: clasificación de intención con confianza → registro → caché →
  RAG → SLM → groundedness → identificación de trámite probable → auditoría
  (`consulta_controller.py`, `container.py`).
- ✅ Búsqueda semántica con **pgvector + HNSW** (y modo coseno en memoria sin pgvector) con umbral
  0.3 (`BusquedaVectorialAdapter.py`).
- ✅ Embeddings **BGE-M3** (1024 dims, CPU, async) (`BGE_M3Adapter.py`).
- ✅ SLM local **Qwen 2.5 3B** vía Ollama con temperatura 0.2 (`OllamaAdapter.py`).
- ✅ Evaluador de **groundedness** por cobertura léxica (alta/media/baja) (`EvaluadorGroundedness.py`).
- ✅ Caché de respuestas en **Redis** (TTL 3600 s) (`ServicioCache.py`, `RedisAdapter.py`).
- ✅ Auditoría persistida en `auditoria_consultas` (`container.py`).
- ✅ Gestión documental: registrar (con indexado automático), listar con filtros, cambiar estado
  (incluido `derogado`), upload con validación de formato, reprocesar, **baja lógica y física**.
- ✅ **PMV2:** chunking real (`ServicioChunking`, bloques de 800 con 120 de solape), entidades
  `Documento` con metadatos y `FragmentoDocumento`, 3 puertos nuevos, casos de uso
  `CargarDocumento`/`ProcesarDocumento`, `ExtraccionTextoAdapter` (PDF/DOCX) y
  `FragmentoRepositoryImpl`.
- ✅ **PMV2 (17-oct-2026):** umbral de rechazo "no inventar" por groundedness (`BLOQUEO_AFIRMACIONES`,
  G-04/HU-08), trazabilidad completa con bloqueo de afirmaciones y fuentes con número/fecha/versión
  (HU-10/D-9), clasificador de dominio con derivación a la entidad (HU-11) y panel `AuditLog` real
  (HU-14). **PMV2 = 100 %.**
- ✅ Usuarios: registro, consulta e historial (últimas 50).

**Frontend funcional:**

- ✅ Chat con sugerencias rápidas, burbujas, groundedness **real**, fuentes y trámite probable
  (`ChatBox`, `ChatThread`, `GroundednessBadge`, `TramiteProbableCard`).
- ✅ Catálogo TUPA con buscador y filtros (`/tramites`); campos alineados con el backend vía
  `mapearTramite` (D-5).
- ✅ Landing y dashboard (`/` y `/admin`) con diseño cálido rediseñado; la portada ya **no inventa
  KPIs** (D-6 parcial).
- ✅ **PMV2:** `DocumentManager` (135 líneas) con carga de metadatos, tabla y acciones reales
  sobre `/api/admin/documentos` — G-12 ✅.
- ✅ Integración real con `POST /api/consultas`, `GET /api/consultas` (trazabilidad),
  `GET /api/tramites`, `GET /health` y las funciones admin (`lib/api.ts`).
  **No hay fallback de demostración**: `respuestaDemo()`/`TRAMITES_DEMO` se eliminaron (D-1) — el
  error se muestra tal cual.

**Infraestructura:**

- ✅ Docker Compose de 3 servicios (PostgreSQL+pgvector, Redis, Ollama) con healthchecks y volúmenes.
- ✅ Migraciones `001`-`006` y seeds TUPA 2023 (**252 procedimientos** / 20 documentos /
  1 municipalidad). `004`/`005`/`006` aplicadas.
- ❌ **0 suites de pruebas automatizadas** (G-18).

## 2. Estado por Historia de Usuario (las 18)

Puntos de verificación y % medidos (método en `06-estado-actual-implementado.md` §10,
**verificado en vivo el 17-oct-2026**):
**83/101 = 82 % global** · PMV1 **100 %** (24/24) ✅ · PMV2 **100 %** (28/28, incl. HU-11) ✅ ·
PMV3 **63 %** (31/49, incl. HU-17). *(HU-11 y HU-17, antes "Transversal", se reasignaron el 16-oct-2026.)*

| ID | Historia | Estado | ✅/Total | % | Brecha principal |
|---|---|---|---|---|---|
| HU-01 | Carga de documentos | ✅ | 9/9 | **100 %** | — cerrada (extracción PDF/DOCX verificada; aprobación con metadatos obligatorios) |
| HU-02 | Vigencia/versión/fuente | ✅ | 8/8 | **100 %** | — cerrada (004 aplicada: 20/20 documentos con metadatos) |
| HU-03 | Aprobar/derogar documentos | ⚠️ | 6/7 | **86 %** | Flujo con revisor/roles (depende de HU-13) |
| HU-04 | Procesamiento documental y RAG | ✅ | 9/9 | **100 %** | — cerrada (OCR con rapidocr + recuperación por fragmento: 20/20 docs) |
| HU-05 | Consulta ciudadana | ✅ | 9/9 | **100 %** | — cerrada |
| HU-06 | Clasificación de intención | ✅ | 5/5 | **100 %** | — cerrada (9 intenciones con confianza) |
| HU-07 | Orientación de requisitos | ✅ | 5/5 | **100 %** | — cerrada (columna `area_responsable` + derivación con confianza baja) |
| HU-08 | Costos y plazos | ✅ | 5/5 | **100 %** | — cerrada (montos del TUPA cargados + umbral "no inventar", G-04) |
| HU-09 | Respuestas con SLM | ✅ | 5/5 | **100 %** | — cerrada (estructura garantizada + derivación al funcionario) |
| HU-10 | Trazabilidad/anti-alucinación | ✅ | 8/8 | **100 %** | — cerrada (trazabilidad completa + bloqueo de afirmaciones + fuentes con metadatos) |
| HU-11 | Fuera de dominio | ✅ | 3/3 | **100 %** | — cerrada (clasificador de dominio + derivación a la entidad) |
| HU-12 | Trámites relacionados | ✅ | 3/3 | **100 %** | — cerrada (motor + endpoint + UI; embeddings y fallback léxico) |
| HU-13 | Usuarios y seguridad | ⚠️ | 2/5 | **40 %** | Solo registro; sin login/JWT/roles (G-01, D-8) |
| HU-14 | Auditoría | ⚠️ | 4/6 | **67 %** | Búsqueda por fecha/trámite/usuario y marcado de registros inconsistentes (respuesta completa y panel real ✅) |
| HU-15 | Retroalimentación | ❌ | 0/3 | **0 %** | Endpoints y tabla de evaluaciones (G-05) |
| HU-16 | Métricas y monitoreo | ❌ | 0/3 | **0 %** | `/admin` sigue maqueta en KPIs/gráficos/logs (G-16/G-06, D-6) |
| HU-17 | Derivación municipal | ⚠️ | 2/5 | **40 %** | Umbral, canal/área/teléfono y directorio (G-09) |
| HU-18 | Reportes y exportación | ❌ | 0/3 | **0 %** | Reportes y exportación (G-07) |

Resumen: **11 HU al 100 %** (HU-01, HU-02, HU-04–HU-12) · **4 parciales** (HU-03, HU-13, HU-14, HU-17) · **3 sin empezar**
(HU-15, HU-16, HU-18) · **83/101 = 82 %** · **0 suites de pruebas**.

> ✅ **Actualización (17-oct-2026, verificación en vivo):** **PMV1 y PMV2 están cerrados al 100 %.**
> El PMV1 se cerró el 16-oct (HU-07/HU-09: migración 005, derivación de área, estructura
> garantizada y derivación al funcionario); el PMV2 se cerró el 17-oct con HU-08 (umbral "no
> inventar", G-04), HU-10 (trazabilidad completa, bloqueo y fuentes con metadatos, D-9), HU-11
> (clasificador de dominio) y 2 puntos de HU-14. Los defectos D-14..D-23 están corregidos.

## 3. Catálogo de vacíos de código (G-XX) — resumen

| Código | Vacío |
|---|---|
| G-01 | Autenticación/JWT/roles y control de acceso |
| G-02 | Clasificador ML (actual: regex heurístico) |
| G-03 | Enmascaramiento de PII en la entrada |
| G-04 | ✅ **Cerrado (17-oct-2026)** — umbral de rechazo por groundedness + clasificador de dominio (HU-08/HU-11) |
| G-05 | Retroalimentación ciudadana (útil/no útil) |
| G-06 / G-16 | Métricas reales (KPIs, latencia) — hoy maqueta |
| G-07 | Reportes / exportación |
| G-08 | ✅ **Cerrado (16-oct-2026)** — recomendación de trámites relacionados (embedding + fallback léxico + UI) |
| G-09 | Derivación a atención municipal |
| G-10 | UI de historial `/mis-consultas` |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas admin |
| G-12 | ✅ **Cerrado (16-oct-2026)** — `DocumentManager` sube/lista/borra/aprueba de verdad |
| G-13 | ✅ **Cerrado (16-oct-2026)** — *chunking* + `fragmentos_documento` + OCR + recuperación RAG por fragmento (20/20) |
| G-14 | ✅ **Cerrado (D-5)** — `mapearTramite()` traduce `tipo`/`duracion_estimada_dias` a `categoria`/`plazo` |
| G-15 | Fine-tuning QLoRA del SLM |
| G-17 | Contenerización frontend/backend, balanceador, HTTPS, monitoreo |
| G-18 | Suite de pruebas automatizadas (pytest) |
| G-20 | Guardrails anti prompt-injection |
| G-21 | Artefactos de PoC (dataset, resultados) |
| G-23 | Rate limiting |
| G-24 | Auditoría de manipulación de documentos |
| G-25 | Aviso legal como política de API (solo UI) |
| G-26 | WCAG, pruebas de carga, SonarQube, ZAP |

### 3.1 Defectos D-14..D-21 — ✅ corregidos (16 de octubre de 2026, verificados en vivo)

Verificación: `python -c "import main"` → **31 rutas**; carga de PDF real → **201**; panel admin
carga la lista (265 trámites); `PUT .../estado` → 200/422 según corresponda.

| # | Defecto | Estado |
|---|---|---|
| D-14 | **La API no arranca:** `main.py:21` importaba `router` de un stub | ✅ `tramite_admin_controller` con `router` real → **31 rutas** |
| D-15 | Migración `004` sin aplicar y línea 1 inválida | ✅ Corregida y aplicada (+ `005`, `006`); 20/20 documentos con metadatos |
| D-16 | `instalar.ps1` no ejecutaba `004` | ✅ Lista `004`/`005`/`006` |
| D-17 | `pypdf`/`python-docx` ausentes de `requirements.txt` | ✅ `pypdf`, `PyMuPDF`, `python-docx`, `rapidocr` en `requirements.txt` |
| D-18 | `estado` inválido → 500 | ✅ 422 (también en `PUT /{id}/estado`) |
| D-19 | La baja física no borraba el archivo | ✅ 204 sin huérfanos en `storage/documentos` |
| D-20 | `pedir()` hacía `response.json()` en 204 | ✅ Manejo del 204; `tsc` sin errores |
| D-21 | Panel admin llamaba a `/api/tramites/admin` inexistente | ✅ Panel carga (265 trámites) |
| D-22 | `fragmentado` con `1/0` a columna BOOLEAN | ✅ `bool(fragmentado)` en `DocumentoRepositoryImpl` |
| D-23 | Publicar sin metadatos → 500 | ✅ 422 capturando `DocumentoInvalidoError` |

Defectos relacionados: **D-6** (KPIs/gráficos/logs de `/admin` siguen ficticios:
252 / 1,236 / 98 %), **D-8** (`es_administrador()` nunca se invoca: ningún endpoint valida rol),
**D-11** (`/health` no comprueba BD/Redis/Ollama: el front informa "sin verificar").
✅ **D-9 cerrado (17-oct-2026):** `GET /api/consultas/{id}` devuelve respuesta, fuentes, confianza
y banderas; se añadió `GET /api/consultas` para el listado.

## 4. Decisiones de diseño tomadas e implementadas

1. **Entidad del expediente**: desde el commit `ff7a589` el **código y la BD usan Huancayo (MPH)**
   (el seed y varios `.md` aún dicen Junín (MPJ) — inconsistencia documental **D-12**; en la
   práctica `database/scripts/actualizar_huancayo.sql` corrige el registro). Los datos siguen
   siendo el TUPA 2023 con 22 trámites sembrados.
2. **Paleta azul fría → estilo cálido/orgánico**: rediseño UI completo (`globals.css`).
3. **RAG por defecto**: la respuesta siempre pasa por recuperación semántica (no hay modo
   "solo SLM" en producción); abstención si no hay contexto.
4. **Sin respuestas ficticias**: se eliminaron `respuestaDemo()` y `TRAMITES_DEMO` (D-1); si el
   backend falla, la interfaz **muestra el error** en lugar de simular datos (D-1).
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
- ✅ **La API arranca (17-oct-2026):** `import main` → 31 rutas; migraciones `004`/`005`/`006`
  aplicadas. Recordatorio: aplicar las migraciones manualmente con `psql` y tener `pypdf`/
  `python-docx` instalados.

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
Global 82%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░   83/101 puntos (18 HU)
PMV1  100%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   24/24  (HU-05, 06, 07, 09) ✅ cerrado
PMV2  100%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   28/28  (HU-04 ✅, 08 ✅, 10 ✅, 11 ✅, 12 ✅) ✅ cerrado
PMV3   63%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░   31/49  (HU-01 ✅, 02 ✅, 03, 13, 14, 15, 16, 17, 18)
Pendiente   🔴 PMV3: auth/métricas/reportes · 🟠 validación SUS (P2-17)
Defectos    ✅ D-14..D-23 corregidos (16-oct-2026): API arranca, 004/005/006 aplicadas, panel OK
```

**Prioridad sugerida** para llegar a producción: **G-18 (pytest)** → **G-01/auth (D-8)** →
**G-16/métricas (D-6)** → **G-07 (reportes)** → **P2-17 (validación SUS con 50 ciudadanos)**.