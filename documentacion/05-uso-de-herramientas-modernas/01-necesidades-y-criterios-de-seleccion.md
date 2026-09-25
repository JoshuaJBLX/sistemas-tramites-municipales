# 05.1 — Necesidades y Criterios de Selección de Herramientas

> Parte de **05 — Uso de herramientas modernas** (a.md "5.Uso de herramientas modernas.docx",
> AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Necesidades tecnológicas
1. Desarrollar un SLM para consultas en lenguaje natural.
2. Buscar documentos/artículos en la base vectorial.
3. Orquestar servicios y despliegue (repo, CI/CD).
4. Virtualizar entornos de desarrollo (construcción, despliegue, distribución).
5. Asistencia en el manejo de la caché.
6. Contenedores: construir el frontend/backend, base de datos y modelos.

## Criterios de selección (a.md 17.3)
| Criterio | Peso |
|---|---|
| Rendimiento | 25% |
| Escalabilidad | 20% |
| Facilidad de uso | 15% |
| Integración | 15% |
| Costo | 15% |
| Comunidad/soporte | 10% |

## Estado real
- ✅ SLM, RAG/pgvector, Docker Compose, Redis y caché **implementados** (necesidades 1,2,4,5,6).
- ❌ CI/CD no presente (necesidad 3 — G-17).