# 00 — Documentos Rectores (referencia raíz)
> **Documento relacionado:** [06 · Estado actual implementado](06-estado-actual-implementado.md) — documento rector y fuente única de verdad del estado y las cifras.

> **Estado vigente: 100 % (101/101)** — 18/18 HU, PMV1/PMV2/PMV3 al 100 %, 40 rutas servibles.
> Cifras verificadas contra `06-estado-actual-implementado.md` (§10 y §13).

**Resumen:** documentos transversales del proyecto que antes vivían en la raíz y ahora se
centralizan aquí, siguiendo la convención `NN-titulo.md` de `documentacion/`. Son la fuente de
verdad de requisitos (HU), su estado de implementación y la guía de ejecución.

**Cifras de referencia (estado vigente):**

| Métrica | Valor |
|---|---|
| Avance global | **100 %** — **101/101** puntos (18/18 HU) |
| PMV1 · Prototipo funcional | **100 %** — 24/24 ✅ (cerrado: área responsable, estructura garantizada, derivación al funcionario) |
| PMV2 · Modelo RAG optimizado | **100 %** — 28/28 ✅ (cerrado: umbral "no inventar" G-04, trazabilidad HU-10, clasificador de dominio HU-11) |
| PMV3 · Sistema integrado | **100 %** — 49/49 ✅ (auth/RBAC, auditoría, métricas, reportes, derivación, feedback) |
| Endpoints | **40 rutas servibles** |
| Inventario | 104 `.py` · 27 `.ts`/`.tsx` · 18 `.sql` · 94 `.md` · 7 controllers · 11 puertos · 16 componentes |
| Estado de la demostración | 🟢 **Completo**: D-14..D-23 corregidos, migraciones 004–009 aplicadas, PDF real carga 201, 20/20 documentos fragmentados |

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene | Origen |
|---|---|---|
| `01-historias-de-usuario.md` | Las 18 historias de usuario (HU-01..18) con épica, criterios de aceptación Given/When/Then. | `./HU.md` (raíz) |
| `02-implementacion-de-historias.md` | Estado de implementación por HU con **% de avance medido** y los defectos D-1..D-8 detectados. ⚠️ Sus cifras son **históricas** (snapshot 16-oct-2026); las vigentes (**100 % global, 101/101**) están en el doc. 06. | `./IMPLEMENTACION-HU.md` (raíz) |
| `03-ejecucion.md` | Guía de ejecución local: instalación con un solo comando (`instalar.ps1`) y arranque del sistema. | `./EJECUCION.md` (raíz) |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ de lo implementado vs. pendiente, con brechas G-XX priorizadas. | Nuevo |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3 con **porcentajes** (**100 % / 100 % / 100 %**, estado vigente), backlog, distribución de las 18 HU y vacíos G-XX. | Nuevo |
| **`06-estado-actual-implementado.md`** | **Documento maestro**: consolida los `.md` del repositorio, inventaría el código archivo por archivo (backend + front-end), documenta los flujos completos de front-end, back-end y base de datos, y fija el **estado real** de las 18 HU y los 3 PMV (**100 % global** — 101/101; PMV1 **100 %**, PMV2 **100 %**, PMV3 **100 %**) con el detalle de cierre y los defectos **D-1..D-23**. **Punto de partida para leer la documentación.** | Nuevo |
| **`08-tablero-scrum.md`** | **Tablero Scrum del proyecto (4 sep – 20 nov 2026)**: Product Backlog de las 18 HU por código con criterios Gherkin, plan de **4 sprints** (Sprint 3 en curso), columnas del tablero (Refinamiento, TODO, In Progress, QA/Testing, Done), **roles de Scrum** del equipo (PO, Scrum Master, Arquitecto, Back-End, BD, Integración IA/API) y ceremonias (Daily, Sprint Review, Sprint Retrospective). | Nuevo (16-oct-2026) |

> **Fuente de verdad de las cifras:** `06-estado-actual-implementado.md` (§10 y §13) es el
> documento rector de referencia (actualizado el 17-oct-2026). `02-implementacion-de-historias.md` y
> `05-trazabilidad-por-pmv.md` son la fuente del detalle por HU y por PMV; sus porcentajes se
> reconciliaron el 17-oct-2026 contra el §10 del documento 06. Las cifras citadas en
> `presentacion/01..05` y en los resúmenes de `DOCUMENTACION.md`
> deben reconciliarse contra el §10 del documento 06.

## Relación con el repositorio

- Índice maestro de toda la documentación: `../../DOCUMENTACION.md`.
- **Punto de partida recomendado**: `06-estado-actual-implementado.md` (consolida este
  directorio y el resto de `documentacion/`).
- Guía completa de puesta en marcha (instalación + ejecución): `03-ejecucion.md` y `../../README.md`.
- Instalador de un solo comando: `../../instalar.ps1` (idempotente).
- Los archivos citan código real de `backend/`, `frontend-tramites/`, `database/` y
  `docker-compose.yml`.