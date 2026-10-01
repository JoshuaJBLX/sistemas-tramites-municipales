# 00 — Documentos Rectores (referencia raíz)

**Resumen:** documentos transversales del proyecto que antes vivían en la raíz y ahora se
centralizan aquí, siguiendo la convención `NN-titulo.md` de `documentacion/`. Son la fuente de
verdad de requisitos (HU), su estado de implementación y la guía de ejecución.

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene | Origen |
|---|---|---|
| `01-historias-de-usuario.md` | Las 18 historias de usuario (HU-01..18) con épica, criterios de aceptación Given/When/Then. | `./HU.md` (raíz) |
| `02-implementacion-de-historias.md` | Estado de implementación por HU con **% de avance medido** (37 % global sobre 101 puntos) y los defectos D-1..D-8 detectados. | `./IMPLEMENTACION-HU.md` (raíz) |
| `03-ejecucion.md` | Guía de ejecución local: instalación con un solo comando (`instalar.ps1`) y arranque del sistema. | `./EJECUCION.md` (raíz) |
| `04-implementado-y-por-implementar.md` | Inventario ✅/⚠️/❌ de lo implementado vs. pendiente, con brechas G-XX priorizadas. | Nuevo |
| `05-trazabilidad-por-pmv.md` | Avance por PMV1/PMV2/PMV3 con **porcentajes** (46 % / 36 % / 34 %), backlog, distribución de las 18 HU y vacíos G-XX. | Nuevo |

## Relación con el repositorio

- Índice maestro de toda la documentación: `../../DOCUMENTACION.md`.
- Guía completa de puesta en marcha (instalación + ejecución): `03-ejecucion.md` y `../../README.md`.
- Instalador de un solo comando: `../../instalar.ps1` (idempotente).
- Los archivos citan código real de `backend/`, `frontend-tramites/`, `database/` y
  `docker-compose.yml`.