# 06. Auditoría de Implementación OWASP

**Fecha:** 2026-11-13  
**Rol ejecutado:** Auditor Independiente de Seguridad (Implementación).  
**Entradas:** `docs/04_auditoria_owasp.md`, `docs/05_plan_owasp.md`, estado actual del repositorio.  
**Fuente canónica contrastada:** `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (HU-13/G-01 cerrados en el proyecto; pendiente distinguir de las remediaciones R-01..R-10 de esta intervención).  
**Método:** revisión estática del código y configuración para contrastar remediaciones R-01..R-10. No se ejecutaron pruebas dinámicas, escaneos SCA en vivo ni explotación.

## 1. Estado por remediación planificada

| Remediación | Riesgo OWASP | Estado | Evidencia actual | Riesgo residual |
|---|---|---|---|---|
| R-01 Secreto JWT robusto y gestión | A02 | **No corregida** | `backend/infrastructure/adapters/auth/JWTAdapter.py` mantiene `_secreto()` con lectura de `JWT_SECRET` o derivación desde `OPENAI_API_KEY`/`OPENROUTER_API_KEY`/`POSTGRES_PASSWORD` y posible hash de cadena vacía si no hay base. `.env.example` no define `JWT_SECRET`. | Alto: seguridad de tokens depende del entorno; material derivado puede ser predecible en despliegues mal configurados. |
| R-02 Cobertura RBAC / exposición trazabilidad | A01 | **Parcialmente corregida** (preexistente, sin cambios del plan) | `main.py` aplica `Depends(requiere_administrador)` a routers admin/trámite-admin/documento-admin; `consulta_controller.py` exige admin en `listar_consultas` y en marcar inconsistente, pero `GET /api/consultas/{consulta_id}` (trazabilidad) no exige autenticación. `documento_controller.py` protege mutaciones; `listar_documentos` público. `usuario_controller.py` controla perfil/historial por identidad/rol. | Alto-Medio: posible exposición de información de auditoría por identificador y necesidad de verificación integral de todos los endpoints. |
| R-03 Controles anti-fuerza bruta/rate limiting | A07 | **No corregida** | No se observan middlewares/limitadores (slowapi u otros) ni contadores de intentos en `auth_controller.py`/`dependencias.py`; búsquedas de `rate/limiter/throttle` sin resultados relevantes. | Alto: login y APIs susceptibles a abuso automatizado. |
| R-04 Hardening CORS/headers | A05 | **No corregida** | `main.py`: `allow_origins` lista localhost y `VERCEL_FRONTEND_URL`, `allow_credentials=True`, `allow_methods=['*']`, `allow_headers=['*']`. No se evidencian headers de seguridad en app. | Medio-Alto: configuración permisiva según entorno. |
| R-05 Monitoreo garantizado de eventos de seguridad | A09 | **No corregida** | `dependencias.py` `registrar_evento_seguridad` captura excepciones y hace `pass`. No se evidencia fallback a logging/alerta en fallo de inserción. | Medio: pérdida silenciosa posible de eventos. |
| R-06 Gestión de componentes vulnerables (SCA) | A06 | **No corregida** | `backend/requirements.txt` y `frontend-tramites/package.json` mantienen versiones pinneadas/rangos sin evidencia de ejecución de `pip-audit`/`npm audit` ni actualizaciones asociadas al plan. No hay CI de seguridad. | Alto (potencial): CVEs no evaluados. |
| R-07 Integridad de cadena de suministro | A08 | **No corregida** | `docker-compose.yml` usa `ollama/ollama:latest`; no se evidencian digests, SBOM ni políticas de integridad en repo. | Medio: reproducibilidad/integridad limitada. |
| R-08 Controles anti-abuso en endpoints sensibles | A04 | **No corregida** | Sin rate limiting en consultas/uploads; existen límites funcionales parciales (p. ej. tamaño/formatos en procesamiento documental, límites de paginación), pero no protección de tasa. | Medio: riesgo de abuso/DoS lógico. |
| R-09 Revisión/controles SSRF | A10 | **No corregida / no aplicable comprobado** | No se identificaron nuevos controles explícitos de allowlist SSRF; tampoco vectores claros de fetch arbitrario en controladores revisados. `url_origen` sigue siendo metadato. | Bajo-Medio: riesgo latente si se amplía funcionalidad. |
| R-10 Endurecimiento documental/config por entorno | A05 | **Parcialmente corregida** | Existen `.env.example`, `docker-compose.yml`, `DESPLEGUE_RENDER.md`, `README.md` con guías de despliegue; no se añadió guía específica de hardening/rotación de secretos/JWT en este ciclo ni separación explícita dev/prod en configuración de app. | Medio: operación depende de disciplina manual. |

### Resumen cuantitativo

- **Corregidas:** 0
- **Parcialmente corregidas:** 2 (R-02, R-10, por controles/documentación preexistentes)
- **No corregidas:** 8 (R-01, R-03, R-04, R-05, R-06, R-07, R-08, R-09)

## 2. Nuevas vulnerabilidades o controles mal implementados

- **No se identificaron nuevas vulnerabilidades introducidas por remediaciones**, debido a que no hay evidencia de cambios de remediación aplicados en el repositorio respecto al plan `05_plan_owasp.md`.
- **Controles existentes observados (no nuevos, con limitaciones ya conocidas):** hashing PBKDF2 correcto, uso de consultas parametrizadas, RBAC en múltiples rutas administrativas y registro de eventos/auditoría.

## 3. Regresiones funcionales derivadas de cambios de seguridad

- **Ninguna observada.** No se aplicaron cambios de seguridad que alteren comportamiento; por tanto no se detectaron regresiones funcionales atribuibles a remediaciones.

## 4. Riesgos residuales principales

1. **A02:** secreto/gestión de JWT no endurecida de forma explícita en código/configuración de ejemplo.
2. **A01:** exposición potencial de trazabilidad por ID y necesidad de verificación exhaustiva de autorizaciones.
3. **A07/A04:** ausencia de rate limiting y protecciones anti-abuso.
4. **A05/A09:** configuración permisiva y auditoría de eventos best-effort sin garantía ante fallos.
5. **A06/A08:** postura de suministro de software no verificada ni endurecida.

## 5. Score de seguridad actualizado

**Score estimado: 66 / 100 (alineado con la auditoría 04 revisada; sin evidencia de implementación de las remediaciones R-01..R-10 de esta intervención).**

No se evidencian remediaciones implementadas que modifiquen sustancialmente la postura de seguridad evaluada estáticamente.

## 6. Conclusión

**Cumplimiento del plan OWASP: NO CUMPLIDO.**

Las remediaciones definidas en `docs/05_plan_owasp.md` no se encuentran implementadas en el estado actual del repositorio, salvo elementos parciales preexistentes que no alcanzan los criterios de mitigación propuestos. Se recomienda ejecutar prioritariamente R-01 y R-02, seguidos de R-03/R-04/R-05, con validación de no regresión en flujos de autenticación, consulta ciudadana, administración documental y auditoría.
