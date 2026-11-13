# 01. Auditoría FURPS+

**Fecha:** 2026-11-13  
**Alcance:** Repositorio `sistemas-tramites-municipales` (estado estático en workspace).  
**Rol ejecutado:** Auditor Senior de Calidad de Software (modelo FURPS+).  
**Restricción aplicada:** Sin modificación de código; conclusiones basadas en evidencia observable.  
**Revisión cruzada:** contrastado con `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (fuente única de verdad del estado/cifras; verificado 27-oct-2026, HEAD `3cf1ff5`).

## 1. Resumen ejecutivo

El sistema implementa la plataforma **MUN AI** de orientación de trámites municipales con arquitectura hexagonal en backend (FastAPI/Python), frontend Next.js, PostgreSQL/pgvector, Redis y SLM/embeddings (Ollama local o embeddings por API según entorno). Según el documento rector 06, la entidad implementada en código es **Municipalidad Provincial de Huancayo (MPH)** (existe inconsistencia documental pendiente en `README.md`/algunos seeds y documentos académicos que aún mencionan Junín/MPJ), el avance global es **100 % (101/101)**, con PMV1, PMV2 y PMV3 cerrados al **100 %** (18/18 HU completas), **40 rutas servibles** (36 operaciones + 4 de documentación), 104 `.py`, 27 `.ts/.tsx`, 18 `.sql` y 94 `.md`.

El rector confirma cierres relevantes de calidad/funcionalidad: HU-13 (autenticación JWT, contraseñas PBKDF2, RBAC aplicado a endpoints admin, eventos de seguridad), HU-15/16/18 (evaluación ciudadana, métricas con alerta, reportes y exportación CSV), HU-14/17 (auditoría operativa y derivación), panel `/admin` con datos reales, y scripts de verificación (`probar_hu13.py`, `probar_hu151618.py`) además de 0 suites pytest formales (G-18). Como backlog transversal de mejora continua (fuera del porcentaje de HU) persisten aspectos como guardrails anti prompt-injection (G-20), pruebas automatizadas/CI, manejo de PII (G-03) y validaciones no funcionales formales (p. ej. SUS/carga/accesibilidad).

Desde calidad FURPS+, el proyecto muestra **fortalezas claras en funcionalidad de dominio, soporte arquitectónico y mantenibilidad estructural**, pero presenta **brechas relevantes en aseguramiento verificable**: ausencia de suites automatizadas de pruebas en el árbol (`README.md`: "0 suites (pytest ausente, G-18)"; no se hallaron workflows CI en `.github/`), observabilidad/logging limitada en código de aplicación, y varios riesgos operativos/de configuración para producción (dependencia de servicios externos locales, secretos/configuración por entorno, controles de rendimiento no evidenciados con métricas).

**Dictamen de calidad (FURPS+):** Cumplimiento **parcial-alto** para el alcance implementado, con brechas de aseguramiento verificable. Apto para operación controlada y mejora continua; no se acredita calidad de producción completa por falta de pruebas automatizadas formales/CI, hardening operacional y validaciones no funcionales sistemáticas.

## 2. Puntaje por categoría

| Categoría | Puntaje (0-5) | Estado | Justificación breve |
|---|---:|---|---|
| Functionality | 4.5 | Bueno | Cobertura amplia (RAG, catálogo, documentos, auth/RBAC, auditoría, evaluación, métricas, reportes/exportación, derivación) y **18/18 HU al 100 % (101/101)** según rector 06. Brecha principal: ausencia de regresión automatizada formal (G-18) y validaciones no funcionales pendientes. |
| Usability | 3.2 | Parcial | Frontend con flujos de consulta, transparencia (confianza/groundedness/fuentes/derivación), voto ciudadano y panel admin con datos reales; accesibilidad/WCAG y validación SUS (P2-17) pendientes de evidencia. |
| Reliability | 3.3 | Parcial | Manejo de errores, caché degradable, auditoría y eventos de seguridad; dependencias externas críticas y falta de pruebas/CI/monitoreo integral. |
| Performance | 2.7 | Parcial | Caché, pgvector/HNSW, fragmentación, medición `duracion_ms` y métricas agregadas; sin SLOs por percentil ni pruebas de carga/benchmarks publicados. |
| Supportability | 3.7 | Parcial-Bueno | Arquitectura hexagonal, DI, migraciones 001–009, documentación rectora extensa y scripts de verificación; débil en CI, pytest formal y observabilidad estandarizada. |

**Puntaje global estimado:** **3.5 / 5.0** (ajustado tras revisión con documento rector 06).

## 3. Hallazgos y evidencias

### 3.1 Functionality

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-FUN-01 | Cobertura funcional amplia de dominio municipal y RAG | `README.md` y rector 06 (40 rutas servibles, flujo RAG pasos 1-5), `backend/main.py` incluye routers consulta/trámite/documento/usuario/auth/oficina/métrica/evaluación/reporte/admin; `consulta_controller.py` implementa creación de consulta, caché, auditoría, trazabilidad, marcar inconsistente, evaluación ciudadana. | Alto positivo: soporta casos de uso clave. |
| F-FUN-02 | Gestión documental y ciclo de vida implementados | `documento_controller.py`: registro JSON, upload multipart, listado con filtros, cambio de estado (revisor), reproceso, baja lógica/física; errores de formato/ilegibilidad mapeados a 422. | Alto positivo. |
| F-FUN-03 | Autenticación y RBAC presentes en backend | `auth_controller.py` login `/api/auth/login`, `/api/auth/me`; `dependencias.py` `obtener_usuario_actual`, `requiere_administrador`, `requiere_revisor`; `main.py` protege routers admin con `Depends(requiere_administrador)`. | Alto positivo. |
| F-FUN-04 | Verificación funcional automatizada insuficiente | Rector 06: "0 suites pytest (G-18)" aunque existen scripts de verificación (`scripts/probar_hu13.py`, `scripts/probar_hu151618.py`); no se evidenció CI/workflows. | Alto negativo: riesgo de regresión no controlado a escala de cambios. |

### 3.2 Usability

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-USA-01 | Cliente frontend centraliza consumo API y manejo de sesión/errores | `frontend-tramites/lib/api.ts`: timeouts diferenciados, adjunta Bearer token, parseo defensivo de respuestas, mensajes de abort/error, descarga CSV, tipos TS para respuestas. | Medio positivo. |
| F-USA-02 | Feedback de negocio en flujo conversacional | `consulta_controller.py` y API types incluyen `confianza`, `groundedness`, `pide_aclaracion`, `afirmaciones_bloqueadas`, `fuera_dominio`, `derivacion`; soporta transparencia al ciudadano. | Medio positivo. |
| F-USA-03 | Evidencia limitada de accesibilidad y UX validada | No se encontraron reportes de accesibilidad/WCAG, pruebas de usabilidad ni componentes etiquetados explícitamente en revisión estática limitada; README menciona SUS pendiente (P2-17). | Medio: riesgo de barreras de uso. |

### 3.3 Reliability

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-REL-01 | Manejo de fallos comunes en consultas | `consulta_controller.py`: captura `ValueError`→400, errores de conexión/timeout a SLM→503 con mensaje claro, descarta caché inválida (`_cuerpo_valido`), audita también cache-hit. | Medio positivo. |
| F-REL-02 | Registro de eventos de seguridad sin bloquear flujo | `dependencias.py` `registrar_evento_seguridad` captura excepciones (`pass`) para no tumbar petición; registra token inválido, acceso denegado; `auth_controller.py` registra login fallido/exitoso y actualiza último acceso. | Medio positivo (resiliencia) / riesgo de pérdida silenciosa de auditoría. |
| F-REL-03 | Dependencias críticas externas para disponibilidad | `docker-compose.yml` define postgres/redis/ollama; `main.py` conecta pool al arrancar; RAG depende de SLM/embeddings. Sin HA/fallbacks completos evidenciados. | Medio-alto. |
| F-REL-04 | Sin evidencia de pruebas de regresión/estabilidad | Ausencia de suites automatizadas y CI. | Alto. |

### 3.4 Performance

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-PER-01 | Mecanismos de eficiencia presentes | Caché Redis (`RedisAdapter`, `servicio_cache` en flujo), pgvector/HNSW según README/migraciones, paginación/límites en listados (`listar_documentos`, auditoría con tope 100). | Medio positivo. |
| F-PER-02 | Operaciones potencialmente costosas | Upload/procesamiento documental con extracción (pypdf/PyMuPDF/python-docx), OCR (`rapidocr`, `onnxruntime`), embeddings, generación SLM; reproceso síncrono en endpoint `/procesar`. | Medio. |
| F-PER-03 | Falta de evidencia de desempeño | No hay benchmarks, profiling, métricas de latencia p95 ni pruebas de carga en repositorio. `consulta_controller.py` guarda `duracion_ms` en auditoría (base útil), pero sin explotación/SLO formal. | Medio-alto. |

### 3.5 Supportability

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-SUP-01 | Arquitectura modular y mantenible | Estructura `domain/application/infrastructure`, contenedor DI (`crear_container`), routers separados, puertos/adapters referenciados. | Alto positivo. |
| F-SUP-02 | Evolución de datos controlada | `database/migrations/001`–`009` y scripts Supabase; README documenta estado, despliegue y pasos. | Alto positivo. |
| F-SUP-03 | Documentación funcional extensa | Carpeta `documentacion/` con análisis, ingeniería, gestión, PMV, etc.; README operativo. | Medio-alto positivo. |
| F-SUP-04 | Débil aseguramiento automatizado | Sin CI/workflows, sin configuración visible de linters/tests en raíz; `frontend-tramites/package.json` solo scripts dev/build/start/typecheck. | Alto negativo. |

## 4. Brechas identificadas

1. **Calidad verificable:** falta de pruebas unitarias/integración/E2E y pipeline CI.
2. **Observabilidad:** logging estructurado, trazas y alertas operativas no evidenciados de forma transversal.
3. **Usabilidad/accesibilidad:** ausencia de evidencia de cumplimiento WCAG, pruebas con usuarios y consistencia UI sistemática.
4. **Rendimiento:** sin SLOs, sin pruebas de carga y sin estrategia documentada para picos (OCR/SLM/embeddings).
5. **Operación:** manejo de degradación parcial (Redis/Ollama/pgvector opcional) documentado parcialmente, pero sin runbooks técnicos completos en repo.

## 5. Riesgos detectados

| Riesgo | Severidad | Probabilidad | Descripción |
|---|---|---|---|
| Regresiones en cambios futuros | Alta | Alta | Sin pruebas automatizadas/CI. |
| Degradación de disponibilidad por dependencias externas | Media-Alta | Media | Dependencia de BD, Redis, Ollama y procesamiento documental. |
| Pérdida de trazabilidad de eventos de seguridad | Media | Media | `registrar_evento_seguridad` silencia excepciones de inserción. |
| Deuda de rendimiento en producción | Media | Media | Cargas OCR/embeddings/SLM sin benchmarks ni límites operativos evidenciados. |
| Barreras de accesibilidad/experiencia | Media | Media | SUS y accesibilidad pendientes/no evidenciadas. |

## 6. Recomendaciones de alto nivel

1. Implementar un **baseline de pruebas** (smoke API, casos críticos RAG, auth/RBAC, documentos) y CI mínimo en cada cambio.
2. Incorporar **observabilidad**: logging estructurado, métricas técnicas (latencia, errores, colas), y alarmas.
3. Formalizar **SLOs y pruebas de rendimiento** para consulta y carga/procesado de documentos.
4. Ejecutar evaluación de **accesibilidad y usabilidad** (WCAG + pruebas guiadas) y cerrar hallazgos priorizados.
5. Fortalecer **resiliencia operativa**: timeouts/retries/circuit breakers donde aplique, healthchecks dependientes y runbooks de contingencia.
6. Endurecer auditoría para evitar pérdida silenciosa de eventos críticos (estrategia de fallback/cola).
