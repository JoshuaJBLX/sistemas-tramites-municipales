# 05.3 — Herramientas de Ingeniería y Modelado (SysML/UML)

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

| Herramienta | Uso | Entregable | Estado |
|---|---|---|---|
| Draw.io / Lucidchart | Diagramas SysML-UML | Diagramas del sistema | ❌ No versionados (G-21) |
| StarUML | Modelado UML | Clases/componentes | ❌ No versionados |

## Vistas del modelado en el repositorio
- ⚠️ No hay archivos `.drawio`/`.jpg` de diagramas; la arquitectura hexagonal es **inferible**
  de la estructura `backend/domain|application|infrastructure` y documentada en este índice.

## Relación con el código
| Vista documental | Evidencia real |
|---|---|
| Modelo estructural (entidades) | `backend/domain/entities/*.py`, migraciones 001-003 |
| Vista de componentes (hexagonal) | `domain/ports`, `application/services`, `infrastructure/adapters` |
| Vista de despliegue | `docker-compose.yml` (3 servicios) |

## Vacío
- ❌ G-21: diagramas/modelo SysML no están en el repositorio.