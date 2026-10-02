# 00 — Documentos Rectores (referencia raíz)

**Resumen:** documentos transversales del proyecto que antes vivían en la raíz y ahora se
centralizan aquí, siguiendo la convención `NN-titulo.md` de `documentacion/`. Son la fuente de
verdad de requisitos (HU), su estado de implementación y la guía de ejecución.

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene | Origen |
|---|---|---|
| `01-historias-de-usuario.md` | Las 18 historias de usuario (HU-01..18) con épica, criterios de aceptación Given/When/Then. | `./HU.md` (raíz) |
| `02-implementacion-de-historias.md` | Estado de implementación por HU con **% de avance medido** (**49 %** global sobre 101 puntos) y los defectos D-1..D-8 detectados. | `./IMPLEMENTACION-HU.md` (raíz) |
| `03-ejecucion.md` | Guía de ejecución local: instalación con un solo comando (`instalar.ps1`) y arranque del sistema. | `./EJECUCION.md` (raíz) |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ de lo implementado vs. pendiente, con brechas G-XX priorizadas. | Nuevo |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3 con **porcentajes** (88 % / 44 % / 34 %), backlog, distribución de las 18 HU y vacíos G-XX. | Nuevo |
| **`06-estado-actual-implementado.md`** | **Documento maestro**: consolida los 79 `.md` del repositorio, inventaría el código archivo por archivo (backend + front-end), documenta los flujos completos de front-end, back-end y base de datos, y fija el **estado real** de las 18 HU y los 3 PMV (**49 % global**; PMV1 **88 %**, PMV2 44 %, PMV3 34 %) con lo que falta en detalle, los defectos D-1..D-13 y la ruta de cierre. **Punto de partida para leer la documentación.** | Nuevo |

> **Fuente de verdad de las cifras:** `06-estado-actual-implementado.md` (§10) es el
> documento rector de referencia. `02-implementacion-de-historias.md` y
> `05-trazabilidad-por-pmv.md` siguen siendo la fuente primaria del detalle por HU y por PMV,
> pero cualquier porcentaje citado en `PRESENTACION-PMV1.md`, en `presentacion/01..05` o en
> los resúmenes de `DOCUMENTACION.md` debe reconciliarse contra el §10 del documento 06.

## Relación con el repositorio

- Índice maestro de toda la documentación: `../../DOCUMENTACION.md`.
- **Punto de partida recomendado**: `06-estado-actual-implementado.md` (consolida este
  directorio y el resto de `documentacion/`).
- Guía completa de puesta en marcha (instalación + ejecución): `03-ejecucion.md` y `../../README.md`.
- Instalador de un solo comando: `../../instalar.ps1` (idempotente).
- Los archivos citan código real de `backend/`, `frontend-tramites/`, `database/` y
  `docker-compose.yml`.