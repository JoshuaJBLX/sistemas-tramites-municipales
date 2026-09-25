# 02.2 — Requerimientos y Necesidades de Ingeniería

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Necesidades derivadas del dominio municipal
1. Modelar trámites, requisitos, costos, plazos y áreas responsables (TUPA).
2. Mantener documentos oficiales con vigencia controlada.
3. Atender consultas en lenguaje natural.
4. Clasificar la intención de la consulta.
5. Recuperar fuentes y generar respuestas fundamentadas.
6. Auditar interacciones para trazabilidad.
7. Permitir administración (documentos, usuarios, métricas).

## Traducción a requisitos
| Necesidad | Requisito de ing. | Estado |
|---|---|---|
| 1 | Entidades `Tramite`/`Documento` + seeds TUPA | ✅ `domain/entities`, `database/seeds/` |
| 2 | Campo `estado` de documento | ✅ (sin versión: ⚠️ G-13) |
| 3 | Chat + API RAG | ✅ `app/chat`, `POST /api/consultas` |
| 4 | Clasificador de intención | ⚠️ Regex (`ServicioNLP.py`), sin ML (G-02) |
| 5 | Búsqueda vectorial + SLM | ✅ `BusquedaVectorialAdapter`, `OllamaAdapter` |
| 6 | Auditoría de consultas | ✅ tabla `auditoria_consultas` |
| 7 | Panel administrativo | ⚠️ Maqueta (G-16) |

## Vacíos
- ❌ G-01 (auth para administración) · ❌ G-02 (ML) · ❌ G-13 (versión) · ❌ G-16 (métricas).