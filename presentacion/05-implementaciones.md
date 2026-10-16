# 05 — Implementaciones

> **Actualizado el 16 de octubre de 2026 (HEAD `ea06c9a`).** Cifras y estado verificados contra el código en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md) y [PMV2_DOCUMENTOS.md](../PMV2_DOCUMENTOS.md): global **59 %**, PMV1 **88 %**, PMV2 **56 %**, PMV3 **52 %**; la API aún no arranca (D-14).

> Estado real, qué se construyó, qué falta (G-XX / D-XX) y cómo reproducirlo

## 1. ¿Qué está implementado de verdad? (resumen)

> ⚠️ **Código escrito ≠ sistema en marcha.** Todo lo de abajo está verificado en el código, pero
> **hoy la API no arranca** (`ImportError` en `main.py:21` por `tramite_admin_controller`, **D-14**):
> 0 de los 22 endpoints son servibles, la migración `004` no está aplicada (**D-15**) y el panel
> de documentos del `/admin` no carga (**D-20/D-21**). Son los cuatro defectos a corregir primero
> (§3).

**Núcleo RAG funcional (backend):**

- ✅ API REST **escrita**: 22 endpoints (16 públicos + 6 admin) en 6 controllers
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
- ✅ Usuarios: registro, consulta e historial (últimas 50).

**Frontend funcional:**

- ✅ Chat con sugerencias rápidas, burbujas, groundedness **real**, fuentes y trámite probable
  (`ChatBox`, `ChatThread`, `GroundednessBadge`, `TramiteProbableCard`).
- ✅ Catálogo TUPA con buscador y filtros (`/tramites`); campos alineados con el backend vía
  `mapearTramite` (D-5).
- ✅ Landing y dashboard (`/` y `/admin`) con diseño cálido rediseñado; la portada ya **no inventa
  KPIs** (D-6 parcial).
- ✅ **PMV2:** `DocumentManager` (135 líneas) con carga de metadatos, tabla y acciones reales
  sobre `/api/admin/documentos` — G-12 ⬆️ parcial (pero bloqueado por D-14/D-20/D-21).
- ⚠️ Integración real con `POST /api/consultas`, `GET /api/tramites`, `GET /health` y las 6
  funciones admin (`lib/api.ts`, 225 líneas). **No hay fallback de demostración**:
  `respuestaDemo()`/`TRAMITES_DEMO` se eliminaron (D-1) — el error se muestra tal cual.

**Infraestructura:**

- ✅ Docker Compose de 3 servicios (PostgreSQL+pgvector, Redis, Ollama) con healthchecks y volúmenes.
- ✅ Migraciones automáticas `001`-`003` y seeds TUPA 2023 (22 trámites / 20 documentos /
  1 municipalidad). ⚠️ La `004` del PMV2 **no se aplica automáticamente** y ni siquiera es
  SQL válido en su línea 1 (D-15/D-16).
- ❌ **0 suites de pruebas automatizadas** (G-18).

## 2. Estado por Historia de Usuario (las 18)

Puntos de verificación y % medidos (método en `06-estado-actual-implementado.md` §10):
**60/101 = 59 % global** · PMV1 **88 %** (21/24) · PMV2 **50 %** (14/28, incl. HU-11) ·
PMV3 **51 %** (25/49, incl. HU-17). *(HU-11 y HU-17, antes "Transversal", se reasignaron el 16-oct-2026.)*

| ID | Historia | Estado | ✅/Total | % | Brecha principal |
|---|---|---|---|---|---|
| HU-01 | Carga de documentos | ⚠️ | 7/9 | **78 %** | Extracción de PDF/DOCX sin dependencias instaladas (D-17); confirmación/firma de calidad |
| HU-02 | Vigencia/versión/fuente | ⚠️ | 7/8 | **88 %** | Columnas `version`/`fecha_publicacion` solo en la migración `004`, sin aplicar (D-15) |
| HU-03 | Aprobar/derogar documentos | ⚠️ | 5/7 | **71 %** | Baja lógica ya existe; faltan edición de `titulo`/`contenido` y flujo por roles (D-8) |
| HU-04 | Procesamiento documental y RAG | ⚠️ | 7/9 | **78 %** | **Chunking ya existe** (`ServicioChunking` + `fragmentos_documento`); faltan OCR y recuperación RAG *por fragmento* |
| HU-05 | Consulta ciudadana | ✅ | 9/9 | **100 %** | — cerrada |
| HU-06 | Clasificación de intención | ✅ | 5/5 | **100 %** | — cerrada (9 intenciones con confianza) |
| HU-07 | Orientación de requisitos | ✅ | 4/5 | **80 %** | Derivación al área responsable (no hay columna de área en BD) |
| HU-08 | Costos y plazos | ⚠️ | 3/5 | **60 %** | `tramites.costo` sembrado en 0.00: faltan los montos reales del TUPA |
| HU-09 | Respuestas con SLM | ⚠️ | 3/5 | **60 %** | Estructura de apartados no garantizada; derivación al funcionario |
| HU-10 | Trazabilidad/anti-alucinación | ⚠️ | 4/8 | **50 %** | `GET /api/consultas/{id}` devuelve solo la consulta, sin respuesta/fuentes/confianza (D-9) |
| HU-11 | Fuera de dominio | ❌ | 0/3 | **0 %** | Clasificador de dominio y respuesta de derivación (G-04) |
| HU-12 | Trámites relacionados | ❌ | 0/3 | **0 %** | Motor de recomendación inexistente (G-08) |
| HU-13 | Usuarios y seguridad | ⚠️ | 2/5 | **40 %** | Solo registro; sin login/JWT/roles (G-01, D-8) |
| HU-14 | Auditoría | ⚠️ | 2/6 | **33 %** | Solo persistencia; `GET /{id}` incompleto (D-9) y UI mock (G-07) |
| HU-15 | Retroalimentación | ❌ | 0/3 | **0 %** | Endpoints y tabla de evaluaciones (G-05) |
| HU-16 | Métricas y monitoreo | ❌ | 0/3 | **0 %** | `/admin` sigue maqueta en KPIs/gráficos/logs (G-16/G-06, D-6) |
| HU-17 | Derivación municipal | ⚠️ | 2/5 | **40 %** | Umbral, canal/área/teléfono y directorio (G-09) |
| HU-18 | Reportes y exportación | ❌ | 0/3 | **0 %** | Reportes y exportación (G-07) |

Resumen: **2 HU al 100 %** (HU-05, HU-06) · **11 parciales** · **5 sin empezar** (HU-11, HU-12,
HU-15, HU-16, HU-18) · **60/101 = 59 %** · **0 suites de pruebas**.

> ⚠️ **Corrección de cifra (16-oct-2026):** el PMV1 figuraba **antes** como 100 % (24/24, cifra
> errónea por un error de suma); con HU-07 en 4/5 y HU-09 en 3/5 es **88 % (21/24)** y el global
> pasó de **49 % (antes)** a **59 %** actual.

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
| G-12 | ⬆️ **Parcial** — `DocumentManager` sube/lista/borra de verdad; `DragDropUpload` sigue maqueta |
| G-13 | ⬆️ **Parcial** — `ServicioChunking` + tabla `fragmentos_documento` existen; faltan OCR y la recuperación RAG *por fragmento* |
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

### 3.1 Defectos activos D-14..D-21 (verificados el 16 de octubre de 2026)

Estos defectos **bloquean la demostración**: hasta corregirlos, el PMV2 no puede mostrarse.

| # | Defecto | Ubicación | Impacto |
|---|---|---|---|
| D-14 | **La API no arranca:** `main.py:21` importa `router` de `tramite_admin_controller`, un stub de 91 bytes sin `router` → `ImportError` | `main.py:21,56` · `tramite_admin_controller.py` | 🔴 **0 de 22 endpoints servibles** |
| D-15 | **Migración `004` sin aplicar y no ejecutable:** su línea 1 es un docstring Python (`"""…"""`), no SQL; la BD local no tiene los 7 metadatos, ni `fragmentos_documento`, ni `derogado` | `004_documentos_pmv2.sql:1` | 🔴 Cualquier upsert PMV2 falla con `UndefinedColumn` |
| D-16 | `instalar.ps1` no ejecuta la migración `004` | `instalar.ps1` | 🟠 Instalación limpia ≠ BD preparada para PMV2 |
| D-17 | `pypdf` y `python-docx` ausentes de `requirements.txt` | `requirements.txt` | 🟠 `.pdf`/`.docx` → `DocumentoIlegibleError` → 422 |
| D-18 | `EstadoDocumento(estado)` sin capturar en el listado admin → 500 en vez de 422 | `documento_admin_controller.py:48` | 🟡 Error genérico ante `?estado=` inválido |
| D-19 | La baja física borra filas pero no el archivo de `storage/documentos` | `GestionarDocumentos.eliminar_fisico` | 🟡 Archivos huérfanos en disco |
| D-20 | `pedir()` hace `response.json()` incondicional y los `DELETE` devuelven **204 sin cuerpo** → `SyntaxError` | `lib/api.ts:69` | 🔴 Las bajas fallan desde la UI |
| D-21 | El panel admin llama a `GET /api/tramites/admin`, ruta inexistente, dentro de un `Promise.all` | `lib/api.ts:224` · `DocumentManager.tsx:35` | 🔴 **El panel de documentos no carga** |

Defectos relacionados ya conocidos: **D-6** (KPIs/gráficos/logs de `/admin` siguen ficticios:
252 / 1,236 / 98 %), **D-8** (`es_administrador()` nunca se invoca: ningún endpoint valida rol),
**D-9** (`GET /api/consultas/{id}` no devuelve respuesta/fuentes/confianza), **D-11**
(`/health` no comprueba BD/Redis/Ollama: el front informa "sin verificar").

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
- ⚠️ **Hoy `uvicorn` falla al arrancar** con `ImportError` (`tramite_admin_controller` no define
  `router`, **D-14**): no hay `/docs` ni endpoints hasta corregir ese archivo. Después habrá que
  aplicar la migración `004` (**D-15**) e instalar `pypdf`/`python-docx` (**D-17**).

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
Global 59%  ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░   60/101 puntos (18 HU)
PMV1   88%  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░   21/24  (HU-05, 06, 07, 09)
PMV2   56%  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   14/25  (HU-04, 08, 10, 12)
PMV3   52%  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   23/44  (HU-01, 02, 03, 13, 14, 15, 16, 18)
Trans. 25%  ▓▓▓░░░░░░░░░░░░░░░░░    2/8   (HU-11, 17)
Defectos    🔴 D-14..D-21 bloquean arranque, migración 004 y panel admin
```

**Prioridad sugerida** para cerrar presentación y validación: **desbloqueo D-14..D-21** (arranque,
`004`, deps, panel) → **G-18 (pytest)** → **G-16/métricas (D-6)** → **G-01/auth (D-8)** →
**G-04 (abstención)** → **G-13 (recuperación por fragmento)**.