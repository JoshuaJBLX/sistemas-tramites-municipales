# 03. Auditoría de Implementación FURPS+

**Fecha:** 2026-11-13  
**Rol ejecutado:** Auditor Independiente (Implementación).  
**Entradas:** `docs/01_auditoria_furps.md`, `docs/02_plan_furps.md`, estado actual del repositorio.  
**Fuente canónica contrastada:** `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (para distinguir avances propios del proyecto frente al plan de esta intervención).  
**Método:** verificación estática del workspace (código, configuración, scripts, CI, pruebas). No se asumió implementación sin evidencia.

## 1. Alcance y contexto

Este informe evalúa si las mejoras planificadas en `02_plan_furps.md` (**M-01..M-10**, plan de esta intervención) fueron aplicadas. **No evalúa** el cumplimiento de historias/PMV del proyecto: el rector 06 documenta cierres y avances propios (p. ej. HU-13/15/16/18, scripts de verificación) que son independientes de M-01..M-10. La revisión se realizó sobre el repositorio en esta fecha; **no se ejecutaron despliegues ni pruebas contra servicios externos** durante esta auditoría.

## 2. Comparación antes/después y estado por mejora

| Mejora | Estado | Evidencia actual | Observación |
|---|---|---|---|
| M-01 Suite smoke automatizada | **No implementada** | `README.md` indica "0 suites (pytest ausente, G-18)". Existe `backend/scripts/test_nuevos_endpoints.py` (script manual, no suite/runner estándar). No se hallaron `tests/`, `pytest.ini`, `tox.ini`. | Brecha persiste: sin red automatizada de regresión. |
| M-02 Pipeline CI mínimo | **No implementada** | No se encontró carpeta `.github/workflows/` ni archivos de pipeline CI en el repositorio. | Sin validación automática por commit/PR. |
| M-03 Matriz de regresión manual documentada | **Parcialmente implementada** | Existe documentación operativa/estado en `README.md`, `DESPLEGUE_RENDER.md`, `documentacion/00-documentos-rectores/*` (ejecución, checklist implementación, estado actual). No se evidencia una matriz de regresión FURPS específica derivada del plan 02 con casos/criterios de aceptación y responsable/fecha por release. | Hay base documental, pero no el artefacto puntual solicitado por el plan. |
| M-04 Logging estructurado y correlación | **No implementada** | Búsqueda de `logging/logger/print` en backend no mostró uso de logging estructurado; no se observaron middlewares de request-id. (Evidencia limitada a patrones buscados.) | Diagnóstico operativo sigue limitado. |
| M-05 Robustecer registro de eventos de seguridad | **No implementada** (según objetivo del plan) | `backend/infrastructure/controllers/dependencias.py`: `registrar_evento_seguridad` envuelve `INSERT` en `try/except Exception: pass` ("la auditoría no debe bloquear el flujo"), sin logging/metricación de fallo. | Comportamiento resiliente pero con riesgo de pérdida silenciosa, tal como señaló la auditoría inicial. |
| M-06 Healthchecks dependientes (readiness/liveness) | **No implementada** | `backend/main.py` expone solo `GET /health` que retorna `{'status':'ok'}` fijo; no verifica BD/Redis/Ollama. | Healthcheck superficial. |
| M-07 Instrumentación de métricas técnicas | **Parcialmente implementada** | `consulta_controller.py` calcula `duracion_ms` y lo persiste en auditoría (`auditar_consulta.ejecutar(..., duracion_ms=...)`); existen routers/módulos de métricas y reportes (`metrica_controller`, HU-16/18). No se evidencia exportación Prometheus/OpenTelemetry ni SLOs técnicos de infraestructura. | Métricas de negocio/tiempo parciales; métricas técnicas operativas no instrumentadas. |
| M-08 Pruebas de carga y SLOs iniciales | **No implementada** | No se hallaron scripts/herramientas de carga (k6, locust, jmeter) ni documentos de SLO/benchmark en `docs/`. | Sin evidencia de capacidad. |
| M-09 Backlog UX/accesibilidad con correcciones | **No implementada** (en este ciclo) | No se identificaron cambios específicos trazables al plan 02 ni reportes WCAG nuevos en `docs/`; README mantiene referencia a validación SUS pendiente (P2-17). | Requiere ciclo UX dedicado. |
| M-10 Documentación operativa (runbooks) | **Parcialmente implementada** | Existen `README.md`, `DESPLEGUE_RENDER.md`, `instalar.ps1`, `docker-compose.yml`, `database/migrations/README_SUPABASE.md` y documentación rectora en `documentacion/`. No hay runbooks específicos de incidentes (caída Ollama/Redis, rotación de secretos, contingencias) vinculados al plan. | Documentación de despliegue/instalación presente, runbooks de operación por consolidar. |

### Resumen cuantitativo

- **Implementadas:** 0
- **Parcialmente implementadas:** 3 (M-03, M-07, M-10)
- **No implementadas:** 7 (M-01, M-02, M-04, M-05, M-06, M-08, M-09)

## 3. Regresiones funcionales / nuevas incidencias observadas

- **No se detectaron regresiones funcionales introducidas por la aplicación del plan**, dado que no se evidencian cambios de implementación asociados a M-01..M-10 en el repositorio.
- **Pruebas ejecutadas:** no se ejecutaron suites automatizadas (no disponibles). No se puede afirmar "pruebas fallidas" ni "sin fallos en ejecución" por ausencia de ejecución formal.
- **Riesgo observado preexistente (no regresión nueva):** pérdida silenciosa potencial de eventos de seguridad por `except: pass` en auditoría (`dependencias.py`), ya identificado.

## 4. Riesgos residuales

| Riesgo residual | Estado | Comentario |
|---|---|---|
| Regresiones no detectadas | Alto | Persiste ausencia de smoke/CI. |
| Observabilidad insuficiente | Medio-Alto | Sin logging estructurado ni healthchecks profundos. |
| Capacidad/rendimiento no acreditado | Medio | Sin pruebas de carga ni SLOs. |
| Usabilidad/accesibilidad no validada | Medio | Pendiente evidencia WCAG/SUS. |
| Pérdida de eventos de seguridad | Medio | Persistente por diseño actual del manejador de auditoría. |

## 5. Conclusión de cumplimiento

**Cumplimiento del plan FURPS+: NO CUMPLIDO.**

El estado actual del repositorio no evidencia la ejecución de las mejoras priorizadas del `02_plan_furps.md`. Se observan únicamente capacidades parciales preexistentes o colaterales (documentación general, medición de `duracion_ms`, módulos de métricas/reporte) que no satisfacen los criterios definidos para M-01..M-10. Se recomienda iniciar por M-01/M-02/M-03 para habilitar un ciclo de mejora seguro e incremental, manteniendo compatibilidad y rollback según lo planificado.
