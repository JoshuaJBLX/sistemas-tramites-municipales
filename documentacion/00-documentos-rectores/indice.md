# 00 — Documentos Rectores (referencia raíz)

> **Actualizado el 16 de octubre de 2026** (HEAD `ea06c9a`). Cifras verificadas contra
> `06-estado-actual-implementado.md` (§10 y §13) y contra `PMV2_DOCUMENTOS.md`.

**Resumen:** documentos transversales del proyecto que antes vivían en la raíz y ahora se
centralizan aquí, siguiendo la convención `NN-titulo.md` de `documentacion/`. Son la fuente de
verdad de requisitos (HU), su estado de implementación y la guía de ejecución.

**Cifras de referencia (16-oct-2026):**

| Métrica | Valor |
|---|---|
| Avance global | **59 %** — **60/101** puntos |
| PMV1 · Prototipo funcional | **88 %** — 21/24 (antes se publicaba 100 %; error de suma, ver §10.4 del doc. 06) |
| PMV2 · Modelo RAG optimizado | **56 %** — 14/25 |
| PMV3 · Sistema integrado | **52 %** — 23/44 |
| Transversal (HU-11, HU-17) | **25 %** — 2/8 |
| Endpoints | **22** declarados (16 públicos + 6 admin) — **0 servibles** hoy por D-14 |
| Inventario | 86 `.py` · 25 `.ts`/`.tsx` · 9 `.sql` · 90 `.md` · 6 controllers (1 stub) · 10 puertos · 16 componentes |
| Estado de la demostración PMV2 | 🔴 Bloqueada por los defectos **D-14..D-21** (la API no arranca): ver [`../../PMV2_DOCUMENTOS.md`](../../PMV2_DOCUMENTOS.md) |

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene | Origen |
|---|---|---|
| `01-historias-de-usuario.md` | Las 18 historias de usuario (HU-01..18) con épica, criterios de aceptación Given/When/Then. | `./HU.md` (raíz) |
| `02-implementacion-de-historias.md` | Estado de implementación por HU con **% de avance medido** (**59 %** global sobre 101 puntos; cifras aún pendientes de reconciliar con el doc. 06) y los defectos D-1..D-8 detectados. | `./IMPLEMENTACION-HU.md` (raíz) |
| `03-ejecucion.md` | Guía de ejecución local: instalación con un solo comando (`instalar.ps1`) y arranque del sistema. | `./EJECUCION.md` (raíz) |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ de lo implementado vs. pendiente, con brechas G-XX priorizadas. | Nuevo |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3 con **porcentajes** (**88 % / 56 % / 52 %**), backlog, distribución de las 18 HU y vacíos G-XX. ⚠️ El archivo aún muestra las cifras anteriores a la corrección del 16-oct-2026: pendiente de actualizar (§12.6 del doc. 06). | Nuevo |
| **`06-estado-actual-implementado.md`** | **Documento maestro**: consolida los 90 `.md` del repositorio, inventaría el código archivo por archivo (backend + front-end), documenta los flujos completos de front-end, back-end y base de datos, y fija el **estado real** de las 18 HU y los 3 PMV (**59 % global** — 60/101; PMV1 **88 %**, PMV2 **56 %**, PMV3 **52 %**) con lo que falta en detalle, los defectos **D-1..D-21** y la ruta de cierre. **Punto de partida para leer la documentación.** | Nuevo |
| **`08-tablero-scrum.md`** | **Tablero Scrum del proyecto (4 sep – 20 nov 2026)**: Product Backlog de las 18 HU por código con criterios Gherkin, plan de **4 sprints** (Sprint 3 en curso), columnas del tablero (Refinamiento, TODO, In Progress, QA/Testing, Done), **roles de Scrum** del equipo (PO, Scrum Master, Arquitecto, Back-End, BD, Integración IA/API) y ceremonias (Daily, Sprint Review, Sprint Retrospective). | Nuevo (16-oct-2026) |

> **Fuente de verdad de las cifras:** `06-estado-actual-implementado.md` (§10 y §13) es el
> documento rector de referencia (actualizado el 16-oct-2026); para el alcance y los bloqueos del
> PMV2, `../../PMV2_DOCUMENTOS.md`. `02-implementacion-de-historias.md` y
> `05-trazabilidad-por-pmv.md` siguen siendo la fuente primaria del detalle por HU y por PMV,
> **pero sus porcentajes aún no se han reconciliado con el 16-oct-2026** (§12.6): cualquier cifra
> citada en `PRESENTACION-PMV1.md`, en `presentacion/01..05` o en los resúmenes de
> `DOCUMENTACION.md` debe reconciliarse contra el §10 del documento 06.

## Relación con el repositorio

- Índice maestro de toda la documentación: `../../DOCUMENTACION.md`.
- **Punto de partida recomendado**: `06-estado-actual-implementado.md` (consolida este
  directorio y el resto de `documentacion/`).
- Alcance, avance y bloqueos del PMV2 (16-oct-2026): `../../PMV2_DOCUMENTOS.md`.
- Guía completa de puesta en marcha (instalación + ejecución): `03-ejecucion.md` y `../../README.md`.
- Instalador de un solo comando: `../../instalar.ps1` (idempotente).
- Los archivos citan código real de `backend/`, `frontend-tramites/`, `database/` y
  `docker-compose.yml`.