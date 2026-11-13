# 02. Plan de Mejora FURPS+

**Fecha:** 2026-11-13  
**Entrada:** `docs/01_auditoria_furps.md`  
**Rol ejecutado:** Arquitecto de Software Senior.

## Restricción principal

**EL SISTEMA YA FUNCIONA** (rector 06: proyecto al **100 % = 101/101**, 18/18 HU, API operativa). Ninguna mejora debe romper funcionalidades existentes, flujos de negocio, APIs, datos ni integraciones. Cambios **incrementales, compatibles, con validación y rollback**.

## 1. Roadmap

| Fase | Horizonte | Objetivo | Resultado esperado |
|---|---|---|---|
| F0 - Estabilización de aseguramiento | 0-2 semanas | Crear red mínima de seguridad para cambios | Smoke tests + CI + checklist de regresión manual |
| F1 - Observabilidad y confiabilidad | 2-4 semanas | Visibilidad operativa y manejo robusto de fallos | Logs/métricas básicas, healthchecks ampliados, manejo de auditoría |
| F2 - Rendimiento y UX/accesibilidad | 4-8 semanas | Validar desempeño y experiencia de usuario | Métricas de latencia, pruebas de carga acotadas, backlog UX/WCAG priorizado |
| F3 - Consolidación | 8+ semanas | Mejora continua sin regresiones | Cobertura ampliada, SLOs, hardening operativo |

## 2. Mejoras priorizadas

| ID | Mejora | Objetivo | Justificación (brecha) | Prioridad | Riesgo | Dependencias | Estrategia de validación | Estrategia de rollback |
|---|---|---|---|---|---|---|---|---|
| M-01 | Suite smoke automatizada de endpoints críticos | Detectar regresiones básicas | F-FUN-04, F-REL-04 | Crítica | Bajo | Entorno de pruebas/BD de test, fixtures | Ejecutar smoke en PR/local: `/health`, login, consulta, listado trámites, CRUD docs mínimo; comparar contratos existentes | Mantener tests aditivos; deshabilitar job CI nuevo sin revertir app si falla infraestructura de CI |
| M-02 | Pipeline CI mínimo | Ejecutar validaciones en cada cambio | F-SUP-04 | Crítica | Bajo | M-01, `npm run typecheck` | Workflow que ejecute lint/typecheck/tests disponibles; gate de merge | Revertir archivo de workflow; no afecta runtime |
| M-03 | Matriz de regresión manual documentada | Cubrir flujos de negocio mientras madura automatización | F-FUN-04 | Alta | Bajo | Acceso a entorno funcional | Checklist firmado por release: login, roles, consulta RAG, upload/procesar, auditoría, reportes | Documento versionado; rollback = volver a checklist anterior |
| M-04 | Logging estructurado y correlación de solicitudes | Mejorar diagnóstico de fallos | F-REL-03, brecha observabilidad | Alta | Bajo-Medio | Librería logging/config | Verificar logs JSON/estructurados con request-id en endpoints clave; no cambiar respuestas API | Feature flag/config para nivel/formato; rollback a configuración previa |
| M-05 | Robustecer registro de eventos de seguridad | Evitar pérdida silenciosa de auditoría | F-REL-02 | Alta | Bajo-Medio | BD `eventos_seguridad` | Simular fallo de inserción controlado: asegurar log de warning y métrica; confirmar que flujos críticos siguen según política definida | Cambios acotados en `registrar_evento_seguridad`; rollback por revert de función |
| M-06 | Healthchecks dependientes (readiness/liveness) | Detectar degradación de BD/Redis/Ollama | F-REL-03 | Alta | Medio | Endpoints/infra | Probar `/health` actual intacto + nuevo `/ready` opcional; validar en staging | Endpoint nuevo aditivo; rollback eliminando ruta nueva |
| M-07 | Instrumentación de métricas técnicas | Medir latencia/errores reales | F-PER-03 | Media | Medio | M-04, stack métricas | Exponer/registrar p50/p95 de consulta y procesado, tasa 4xx/5xx; validar sin impacto funcional | Desactivar exportador por config |
| M-08 | Pruebas de carga acotadas y SLOs iniciales | Definir capacidad objetivo | F-PER-01..03 | Media | Medio | Entorno representativo | Escenarios: consultas concurrentes y upload/procesado; comparar con baseline; no ejecutar en prod | Scripts/herramientas fuera de runtime; rollback N/A |
| M-09 | Backlog UX/accesibilidad con correcciones incrementales | Mejorar usabilidad y acceso | F-USA-03 | Media | Bajo-Medio | Revisión UI, guías WCAG | Auditoría WCAG AA focalizada + fixes pequeños (labels, contraste, foco, mensajes); validar navegación teclado | Cambios UI atómicos y reversibles por componente |
| M-10 | Documentación operativa (runbooks) | Reducir riesgo operativo | Brecha operación | Media | Bajo | Conocimiento de despliegue | Simulacros: caída Ollama/Redis, rotación secretos, restauración BD | Solo documentación |

## 3. Orden recomendado de implementación

1. **M-01, M-02, M-03** (red de seguridad antes de tocar lógica).
2. **M-04, M-05, M-06** (confiabilidad/observabilidad).
3. **M-07, M-08** (rendimiento basado en evidencia).
4. **M-09, M-10** (experiencia y operación).

## 4. Riesgos de ejecución

| Riesgo | Mitigación |
|---|---|
| Tests inestables por dependencias externas (Ollama/Redis/BD) | Usar dobles/mocks en unitarias y entorno dockerizado controlado para integración; separar suites smoke. |
| Cambios de observabilidad afectan rendimiento/ruido | Niveles de log configurables, muestreo, despliegue gradual. |
| Healthchecks/readiness mal configurados tumban despliegue | Mantener `/health` existente; agregar readiness como endpoint nuevo y opt-in en orquestador. |
| Correcciones UI introducen regresiones visuales | Cambios pequeños, revisión manual de pantallas clave y snapshots si se incorpora tooling. |
| Falta de tiempo/entorno para carga | Priorizar escenarios críticos y baseline relativo, no metas absolutas prematuras. |

## 5. Estrategia de preservación de funcionalidad

- **Compatibilidad:** no cambiar contratos de endpoints existentes; toda adición debe ser aditiva (nuevas rutas/campos opcionales).
- **Incrementalidad:** PRs pequeños por mejora, uno a la vez, con validación antes de fusionar.
- **Validación obligatoria por cambio:** smoke manual de flujos críticos (auth, consulta, catálogo, gestión documental, auditoría) + checks automatizados cuando existan.
- **Datos:** migraciones solo hacia adelante y reversibles cuando sea posible; respaldos antes de aplicar en entornos compartidos.
- **Rollback:** revert de commits/configuración por feature; flags para observabilidad; mantener imágenes/versiones anteriores desplegables.
- **Criterio de parada:** si se detecta regresión en proceso de negocio, detener rollout y revertir antes de continuar.
