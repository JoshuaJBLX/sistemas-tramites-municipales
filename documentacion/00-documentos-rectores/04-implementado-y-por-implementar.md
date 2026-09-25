# Implementado y por Implementar — Estado real del sistema

> Inventario honesto de qué está construido (con código real) y qué queda pendiente,
> contrastado contra `a.md`, las 18 HU y los vacíos `G-XX`.

**Leyenda:** ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado

## 1. Situación general

El sistema es una **PoC funcional**: el flujo ciudadano completo (preguntar → RAG → SLM →
groundedness → responder con fuentes) opera de extremo a extremo. Las funciones de **administración
y gobierno** (login, métricas reales, carga documental conectada, reportes) son la parte pendiente
principal.

```
Flujo de consulta  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  (✅ casi completo, falta G-16/G-04)
Gestión documental ▓▓▓▓░░░░░░░░░░░░░░░░  (⚠️ backend existe, UI maqueta G-12/G-13)
Seguridad          ▓░░░░░░░░░░░░░░░░░░░  (❌ G-01, G-20, G-23)
Calidad/Métricas   ▓░░░░░░░░░░░░░░░░░░░  (❌ G-16, G-18, G-26)
```

## 2. Implementado (✅)

### 2.1 Backend (FastAPI, hexagonal)
- **Dominio**: entidades `Tramite`, `Documento`, `Consulta`, `Respuesta`, `Usuario`,
  `Municipalidad`, `Fuente`; value objects (`IntencionConsulta` 6, `NivelConfianza` 3,
  `EstadoDocumento` 3, `TipoTramite` 6); puertos ABC.
- **Aplicación**: 7 casos de uso y servicios `ServicioNLP` (regex), `ServicioRAG` (top_k=5),
  `ServicioSLM` (Qwen 2.5 3B), `EvaluadorGroundedness` (cobertura léxica, ALTA ≥0.75 / MEDIA ≥0.40),
  `ServicioCache` (Redis, TTL 3600), `ServicioAuditoria`.
- **Infraestructura**: adaptadores `BusquedaVectorialAdapter` (pgvector, umbral 0.3, `estado='vigente'`),
  `BGE_M3Adapter` (embeddings 1024 dims, CPU, async), `OllamaAdapter` (temperatura 0.2),
  `RedisAdapter`, `DocumentStorageAdapter`; repositorios `asyncpg` con pool 1-10 y SQL parametrizado.
- **API**: controllers con rutas `/api/consultas`, `/api/consultas/{id}`, `/api/tramites`,
  `/api/tramites/{id}`, `/api/documentos*`, `/api/usuarios*`, `/health`; DI central en `container.py`.

### 2.2 Base de datos (PostgreSQL 16 + pgvector)
- Migraciones 001 (BD + extensión vector), 002 (6 tablas), 003 (índice **HNSW** `vector_cosine_ops`).
- Seeds reales TUPA 2023 **MPJ**: 1 municipio, 10 trámites, 6 documentos con fuente `gob.pe/munijunin`.
- Búsqueda por similitud de coseno (`embedding <=> $1::vector`).

### 2.3 Frontend (Next.js 14)
- Rutas `/`, `/chat`, `/tramites`, `/admin`; **15 componentes** + set de 23 iconos SVG.
- Chat con sugerencias, `GroundednessBadge` (confianza + fuentes), catálogo con buscador/filtros,
  dashboard de métricas de demostración.
- Integración real en `lib/api.ts` (`enviarConsulta`, `obtenerTramites`, `obtenerEstadoServicios`)
  con **fallback demo** si el backend está caído.

### 2.4 Infraestructura
- `docker-compose.yml` con 3 servicios (postgres+pgvector, redis, ollama), healthchecks y volúmenes.

## 3. Parcial (⚠️) y por implementar (❌)

### 3.1 Vacíos de código `G-XX` (detalle en `02-implementacion-de-historias.md`)

| Código | Vacío | Prioridad |
|---|---|---|
| G-18 | **Suite de pruebas automatizadas (pytest)** | 🔴 Alta |
| G-16 / G-06 | **Métricas reales** del panel (hoy maqueta) | 🔴 Alta |
| G-01 | **Autenticación, JWT, roles y control de acceso** | 🔴 Alta |
| G-12 | **Carga de documentos conectada a `/api/documentos`** (hoy maqueta) | 🔴 Alta |
| G-04 | Abstención / rechazo por groundedness baja | 🟠 Media |
| G-20 | Guardrails anti prompt-injection | 🟠 Media |
| G-13 | Chunking documental, `version`, `fecha_publicacion`, página de fuente | 🟠 Media |
| G-14 | Consistencia `tipo`/`duracion_estimada_dias` ↔ `categoria`/`plazo` | 🟠 Media |
| G-07 | Reportes y exportación | 🟠 Media |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas admin | 🟠 Media |
| G-10 | UI de historial ciudadano `/mis-consultas` | 🟡 Baja |
| G-08 | Recomendación de trámites relacionados | 🟡 Baja |
| G-09 | Derivación a atención municipal | 🟡 Baja |
| G-02 | Clasificador ML (Random Forest/TF-IDF) con métricas F1 | 🟡 Baja |
| G-03 | Enmascaramiento de PII | 🟡 Baja |
| G-05 | Retroalimentación ciudadana (útil/no útil) | 🟡 Baja |
| G-15 | Fine-tuning QLoRA del SLM | 🟡 Baja |
| G-17 | Contenerización frontend/CI, HTTPS, monitoreo | 🟡 Baja |
| G-21 | Artefactos de PoC (dataset, resultados de experimentos) | 🟡 Baja |
| G-23 | Rate limiting | 🟡 Baja |
| G-24 | Auditoría de manipulación de documentos | 🟡 Baja |
| G-25 | Aviso legal como política de API | 🟡 Baja |
| G-26 | Accesibilidad WCAG, pruebas de carga, SonarQube, ZAP | 🟡 Baja |

### 3.2 HU sin soporte en interfaz (❌)
- **HU-11** Consultas fuera de dominio · **HU-12** Trámites relacionados · **HU-15**
  Retroalimentación · **HU-18** Reportes y exportación.

### 3.3 Diferencias con `a.md` (documentadas)
- `a.md` proponía: 7 contenedores, API `/api/v1/consulta`, clasificador Random Forest, 16 rutas,
  groundedness coseno con rechazo, tabla `evaluaciones_calidad`. **Lo implementado**: 3 servicios,
  `/api/consultas`, regex, 4 rutas, confianza cualitativa, sin tabla de evaluaciones.

## 4. Recomendación de cierre (siguiente iteración)

1. **G-18** prueba todo el flujo RAG (pytest + `httpx`/`pytest-asyncio`).
2. **G-01** login JWT + roles para proteger `/admin` y `/api/documentos`.
3. **G-16** endpoint de métricas agregadas (consultas por día, groundedness promedio, latencia).
4. **G-12** conectar `DragDropUpload` a `/api/documentos/upload`.
5. **G-04** rechazo/derivación cuando la groundedness es baja.