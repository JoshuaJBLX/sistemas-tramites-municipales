# 00 — Documentos Rectores (referencia raíz)

**Resumen:** documentos transversales del proyecto que antes vivían en la raíz y ahora se
centralizan aquí, siguiendo la convención `NN-titulo.md` de `documentacion/`. Son la fuente de
verdad de requisitos (HU), su estado de implementación y la guía de ejecución.

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene | Origen |
|---|---|---|
| `01-historias-de-usuario.md` | Las 18 historias de usuario (HU-01..18) con épica, criterios de aceptación Given/When/Then. | `./HU.md` (raíz) |
| `02-implementacion-de-historias.md` | Estado de implementación por HU: checklists, archivos reales, brechas G-XX y prioridades. | `./IMPLEMENTACION-HU.md` (raíz) |
| `03-ejecucion.md` | Guía resumida de ejecución: infraestructura (Docker), backend y frontend. | `./EJECUCION.md` (raíz) |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ de lo implementado vs. pendiente, con brechas G-XX priorizadas. | Nuevo |

## Relación con el repositorio

- Índice maestro de toda la documentación: `../../DOCUMENTACION.md`.
- Guía completa de puesta en marcha: `../../README.md`.
- Los archivos citan código real de `backend/`, `frontend-tramites/`, `database/` y
  `docker-compose.yml`.