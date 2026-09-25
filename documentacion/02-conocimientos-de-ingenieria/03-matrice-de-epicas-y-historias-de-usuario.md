# 02.3 — Matriz de Épicas, Historias de Usuario y Criterios de Aceptación

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Épicas y HU (18)
| Épica | HU |
|---|---|
| Gestión documental | HU-01 (cargar), HU-02 (vigencia/versión), HU-03 (aprobar/derogar) |
| Procesamiento documental y RAG | HU-04 (extraer/procesar/indexar) |
| Consulta ciudadana | HU-05 (lenguaje natural), HU-07 (requisitos), HU-08 (costos/plazos) |
| Clasificación de intención | HU-06 |
| IA / SLM | HU-09 (generación de respuestas) |
| Trazabilidad | HU-10 (control de alucinaciones), HU-11 (fuera de dominio) |
| Recomendación | HU-12 (trámites relacionados) |
| Usuarios y seguridad | HU-13 |
| Auditoría | HU-14 |
| Retroalimentación | HU-15 |
| Métricas y monitoreo | HU-16 |
| Derivación | HU-17 |
| Reportes | HU-18 |

- Formato completo (Given/When/Then): `../00-documentos-rectores/01-historias-de-usuario.md`.
- **Estado por HU** (checklists + archivos): `../00-documentos-rectores/02-implementacion-de-historias.md`.

## Criterios de aceptación (ejemplo HU-01)
- Escenario 1: archivo PDF válido → el sistema valida, almacena y confirma (⚠️ la carga real no
  existe en el backend; el registro es por texto/JSON — G-12).
- Escenario 2: formato inválido → rechazo con formatos permitidos (❌ no implementado).

## Estado resumen
- ⚠️ HU-01..10, 13, 14, 17 parciales; ❌ HU-11, 12, 15, 16, 18 no implementadas.