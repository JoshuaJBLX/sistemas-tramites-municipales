# 07. Auditoría Final Integral

**Fecha:** 2026-11-13  
**Rol ejecutado:** Auditor Principal de Calidad y Seguridad.  
**Entradas:** `docs/01_auditoria_furps.md`, `docs/02_plan_furps.md`, `docs/03_auditoria_implementacion_furps.md`, `docs/04_auditoria_owasp.md`, `docs/05_plan_owasp.md`, `docs/06_auditoria_implementacion_owasp.md`, estado actual del proyecto.  
**Fuente canónica revisada:** `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (estado vigente **100 % = 101/101**, 18/18 HU, PMV1/PMV2/PMV3 al 100 %, 40 rutas servibles; cierres HU-13/14/15/16/17/18 y G-01/G-05/G-06/G-07/D-8).

## 1. Resumen ejecutivo

El proyecto **MUN AI (Sistema de Trámites Municipales)** presenta una base funcional y arquitectónica sólida (FastAPI hexagonal, frontend Next.js, RAG con groundedness/trazabilidad/derivación, autenticación JWT con RBAC, auditoría, evaluación ciudadana, métricas y reportes). El rector 06 confirma el proyecto al **100 % (101/101 puntos, 18/18 HU, PMV1/PMV2/PMV3 al 100 %)**, aunque `README.md` conserva inconsistencias documentales (p. ej. entidad/cifras históricas) frente a dicha fuente única de verdad.

Sin embargo, los planes específicos **M-01..M-10** (FURPS+) y **R-01..R-10** (OWASP) definidos en esta intervención **no se evidencian implementados** como tales en el repositorio al momento de la verificación (ver auditorías 03 y 06). Esto es distinto del avance propio del proyecto documentado en rector 06 (que sí cerró HU/G-XX fuera de estos planes). Persisten brechas relevantes de aseguramiento: ausencia de pytest formal/CI (G-18), falta de rate limiting y guardrails anti prompt-injection (G-20), hardening/gestión explícita de secretos en configuración de ejemplo, SCA no evidenciado, observabilidad de fallos de auditoría best-effort y validaciones no funcionales pendientes (SUS, carga, PII).

**Conclusión global:** el sistema es funcional y maduro en varios frentes, pero **no acredita cumplimiento integral** de los objetivos de mejora/remediación de esta intervención ni el cierre de todos los controles de producción recomendados.

## 2. Estado de calidad (FURPS+)

| Dimensión | Resultado | Evidencia de soporte |
|---|---|---|
| Cumplimiento FURPS+ | **Cumple parcialmente** | Auditoría 01 (revisada): puntaje global 3.5/5.0; alta cobertura funcional y soporte, con brechas en verificación automatizada formal, observabilidad y validación no funcional. Auditoría 03: plan M-01..M-10 de esta intervención no implementado. |
| Mejoras críticas del plan de intervención | **No implementadas** | M-01 (smoke tests formales), M-02 (CI), entre otras, sin evidencia asociada al plan. |
| Hallazgos críticos pendientes (calidad) | **Sí** | G-18 (0 suites pytest) y ausencia de CI; validación SUS/carga pendiente. |

## 3. Estado de seguridad (OWASP Top 10)

| Dimensión | Resultado | Evidencia de soporte |
|---|---|---|
| Cumplimiento OWASP Top 10 | **Cumple parcialmente** | Auditoría 04 (revisada): score 66/100; controles positivos reforzados por HU-13 (auth/RBAC/eventos) y PBKDF2/SQL parametrizado, con brechas residuales en hardening, anti-abuso, gestión explícita de secretos, SCA y garantía de monitoreo. Auditoría 06: plan R-01..R-10 de esta intervención no implementado. |
| Riesgos críticos del plan de intervención mitigados | **No acreditado** | R-01, R-02, R-03, R-05 siguen pendientes como acciones explícitas del plan (aunque existan controles base en el sistema). |
| Riesgos residuales documentados | **Sí** | Incluye A01/A02 residuales, falta de rate limiting/G-20, CORS/hardening, SCA, eventos best-effort y PII pendiente. |

## 4. Estado de funcionalidad y estabilidad

| Dimensión | Resultado | Evidencia / observación |
|---|---|---|
| Preservación de funcionalidad existente | **Preservada (sin evidencia de regresión por este ciclo)** | No se aplicaron cambios de código de los planes; auditorías 03 y 06 no identifican regresiones introducidas en esta intervención. |
| Existencia de regresiones actuales conocidas | **No evidenciadas en revisión estática** | No se ejecutaron pruebas automatizadas (inexistentes) ni validación funcional en entorno vivo dentro de esta auditoría. |
| Procesos de negocio principales | **Implementados según código/documentación** | Flujos de consulta RAG, catálogo, gestión documental, auth/RBAC, auditoría y reportes presentes en controladores y README; operación real depende de BD/Redis/Ollama/configuración. |
| Compila / despliega / pruebas críticas | **No verificado en ejecución en esta sesión** | Revisión estática: estructura y scripts presentes (`instalar.ps1`, `docker-compose.yml`, Dockerfiles, configs). No se ejecutaron builds, despliegue ni suites (0 suites declaradas). |

## 5. Riesgo operativo

**Clasificación: MEDIO-ALTO (condicionado).**

**Justificación:** el sistema cuenta con controles y capacidades importantes (auth/RBAC, auditoría, métricas, arquitectura modular), pero persisten (a) ausencia de pruebas automatizadas formales y CI (G-18), (b) brechas de seguridad operativa (anti-abuso/rate limiting, guardrails G-20, hardening y SCA), y (c) dependencia de servicios externos (PostgreSQL, Redis, SLM/embeddings, OCR) que exige monitoreo y validación no funcional. El riesgo puede reducirse a medio con implementación priorizada de R-01/R-02/R-03/R-05 y M-01/M-02.

## 6. Riesgos pendientes (priorizados)

1. **Seguridad - Identidad y acceso:** formalizar `JWT_SECRET` fuerte por entorno (rotación documentada) y revisar cobertura/exposición de endpoints sensibles (p. ej. trazabilidad por ID) según política.
2. **Seguridad - Abuso:** implementar rate limiting en login y endpoints de alto costo (consultas/uploads) y guardrails anti prompt-injection (G-20).
3. **Seguridad - Configuración y visibilidad:** endurecer CORS/headers por entorno y garantizar alerta/fallback cuando falle el registro de eventos de seguridad.
4. **Seguridad - Suministro y datos:** establecer SCA periódico, política de actualización y tratamiento de PII (G-03).
5. **Calidad - Verificabilidad:** crear smoke tests formales y CI mínimo antes de nuevos cambios funcionales (G-18).
6. **Operación - Validación no funcional:** logging/healthchecks de dependencias, SLOs, pruebas de carga y validación UX/accesibilidad/SUS.

## 7. Observaciones

- La documentación del proyecto es abundante y útil (`documentacion/`, README, guías de despliegue), pero debe complementarse con evidencia operativa continua (tests, reportes SCA, monitoreo).
- La trazabilidad y controles RAG (groundedness, derivación, auditoría) son un diferenciador positivo de diseño; requieren protección de acceso y robustez operativa acordes a su sensibilidad.
- Los artefactos generados en `docs/01`–`06` constituyen la línea base para ejecutar remediaciones y mejoras de forma incremental y verificable.

## 8. Recomendación final

**Recomendación: Apto para producción con observaciones (condicionado a un plan de remediación y aseguramiento inmediato).**

**Condiciones mínimas recomendadas antes de promover cambios adicionales o sostener operación con mayor exposición:**
1. Implementar y validar **R-01** (gestión explícita/robusta de `JWT_SECRET`) y **R-02** (revisión de autorizaciones/exposición según política).
2. Implementar **R-03** (rate limiting básico) y **R-05** (garantía de alerta/fallback para eventos de seguridad), abordando **G-20**.
3. Establecer **M-01/M-02** (smoke tests formales + CI mínimo) para proteger estabilidad (G-18).
4. Ejecutar verificación funcional y no funcional prioritaria (flujos críticos, SCA, y carga/accesibilidad según alcance) en entorno integrado y documentar resultados.

Mientras estas condiciones no se cumplan y acrediten, el nivel de riesgo se mantiene **medio-alto** para entornos de producción expuestos o con requisitos formales de seguridad y calidad.
