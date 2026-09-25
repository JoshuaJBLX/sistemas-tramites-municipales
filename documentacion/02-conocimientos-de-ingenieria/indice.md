# 02 — Conocimientos de Ingeniería

**Resumen:** aplicación de conocimientos de matemáticas, ciencias, computación e ingeniería
(atributo ICACIT AG-107; equiv. "2.Conocimientos de Ingenieria.docx" de a.md). Contrastado con
el código real, con leyenda: ✅ · ⚠️ · ❌ (G-XX).

**Índice y contenido breve:**

## Contenido de esta carpeta

| Archivo | Qué contiene |
|---|---|
| `01-problema-de-ingenieria.md` | Planteamiento del problema de ingeniería (SLM + RAG). |
| `02-requerimientos-de-ingenieria.md` | Necesidades del dominio y su traducción a requisitos. |
| `03-matrice-de-epicas-y-historias-de-usuario.md` | Matriz épicas-HU (18 HU) y criterios de aceptación. |
| `04-requerimientos-funcionales.md` | RF-01 a RF-10 con estado real por requerimiento. |
| `05-fundamentos-matematicos-y-cientificos.md` | Estadística del corpus y fundamentos matemáticos (similitud coseno, HNSW). |
| `06-conocimientos-de-computacion.md` | Algoritmos, BD, arquitectura, IA, redes, seguridad, cloud. |
| `07-conocimientos-fundamentales-y-especializados.md` | Requisitos, modelado de dominio, gobierno digital, gestión documental, NLP. |
| `08-seleccion-y-justificacion-de-tecnologias.md` | Selección del stack (Python/FastAPI, pgvector, BGE-M3, Qwen). |
| `09-trazabilidad-y-aplicacion-al-diseno.md` | Matriz de trazabilidad conocimiento → implementación. |

## Referencias externas

- Listado completo de las 18 HU (Given/When/Then): `../00-documentos-rectores/01-historias-de-usuario.md`.
- Estado de implementación por HU: `../00-documentos-rectores/02-implementacion-de-historias.md`.

## Relación con el repositorio

- Arquitectura hexagonal implementada en `backend/`.
- Clasificación de intención heurística: `backend/application/services/ServicioNLP.py`.