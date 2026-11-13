# 05. Plan de Remediación OWASP Top 10

**Fecha:** 2026-11-13  
**Entrada:** `docs/04_auditoria_owasp.md`  
**Rol ejecutado:** Arquitecto de Seguridad.

## Restricción principal

**NO romper funcionalidad existente, NO afectar procesos de negocio y mantener compatibilidad hacia atrás.** Toda remediación debe ser incremental, validada y con rollback.

## 1. Roadmap de remediación

| Fase | Horizonte | Foco | Objetivo |
|---|---|---|---|
| R0 - Controles críticos de acceso y secreto | 0-2 semanas | A01, A02, A07 | Asegurar autenticación robusta y cobertura RBAC verificable |
| R1 - Hardening y visibilidad | 2-4 semanas | A05, A09 | Endurecer configuración y garantizar trazabilidad de seguridad |
| R2 - Cadena de suministro y abuso | 4-6 semanas | A06, A08, A04 | Reducir riesgo de componentes y ataques automatizados |
| R3 - Verificación continua | 6+ semanas | Todas | SCA/DAST periódico y revisión de diseño |

## 2. Plan por vulnerabilidad/riesgo

| ID | Riesgo (OWASP) | Prioridad | Impacto | Componentes afectados | Estrategia de mitigación | Estrategia de validación | Estrategia de rollback |
|---|---|---|---|---|---|---|---|
| R-01 | Secreto JWT débil/derivado o ausente (A02) | Crítica | Compromiso de sesiones/tokens | `JWTAdapter.py`, configuración despliegue, `.env.example`, docs | Exigir `JWT_SECRET` fuerte en producción (mín. entropía), eliminar fallback a secreto vacío, mantener derivación solo como compatibilidad transitoria documentada o detrás de flag; actualizar `.env.example` y runbook de rotación | Pruebas: arranque falla o alerta si falta secreto en modo prod; tokens emitidos/validados correctamente; rotación controlada invalida sesiones esperadas | Config rollback a secreto anterior; mantener ventana de doble secreto solo si se implementa explícitamente |
| R-02 | Cobertura RBAC y exposición de datos sensibles (A01) | Crítica | Acceso no autorizado/fuga de información | `consulta_controller.py` (GET trazabilidad por id), routers métricas/evaluaciones/reportes/oficinas/admin, frontend | Revisar matriz endpoint-rol; proteger o anonimizar `GET /api/consultas/{id}` si contiene datos sensibles, o exigir token del solicitante/admin según política; asegurar que todos los endpoints administrativos y de datos personales exijan rol adecuado; mantener endpoints públicos necesarios | Pruebas de autorización (401/403/200 esperados) por rol para cada endpoint; regresión de flujos ciudadano/admin | Cambios de dependencia por ruta reversibles; feature flag para endurecimiento progresivo si aplica |
| R-03 | Controles de autenticación insuficientes (A07) | Alta | Fuerza bruta/abuso de cuentas | `auth_controller.py`, `dependencias.py`, gateway/proxy | Añadir rate limiting e incremento de retardo/bloqueo temporal por IP/usuario en login; opcional captcha tras umbral; mantener mensajes genéricos; política de expiración/revocación de sesión documentada | Simular intentos fallidos: verificar limitación sin bloquear usuarios legítimos; login válido sigue funcionando | Desactivar limitador por config; rollback de middleware |
| R-04 | Configuración permisiva CORS y hardening (A05) | Alta | Riesgo de uso indebido desde orígenes/config errónea | `backend/main.py`, proxy/CDN, variables entorno | Restringir `allow_methods/allow_headers` a lo necesario, limitar orígenes por entorno, revisar necesidad de `allow_credentials`; añadir headers de seguridad en borde (HSTS, CSP según front, X-Content-Type-Options) sin romper app | Verificar preflight, llamadas legítimas desde frontend oficial y rechazo de orígenes no permitidos; smoke UI | Revertir configuración CORS/headers a valores previos por entorno |
| R-05 | Monitoreo y pérdida de eventos de seguridad (A09) | Alta | Incidentes no detectados / falta de evidencia | `dependencias.py`, logging app, almacenamiento auditoría | No silenciar fallos críticos: registrar warning/error estructurado si falla `eventos_seguridad`, considerar cola/reintento o fallback a log; centralizar alertas en eventos críticos (login masivo fallido, accesos denegados) | Inyectar fallo de BD/auditoría: confirmar traza operativa y comportamiento definido; eventos normales persisten | Mantener best-effort configurable; rollback a implementación anterior |
| R-06 | Componentes potencialmente vulnerables (A06) | Alta | Explotación de CVEs conocidos | `backend/requirements.txt`, `frontend-tramites/package.json`, imágenes Docker | Ejecutar SCA (`pip-audit`/ecosistema Python, `npm audit`) en CI; actualizar dependencias con cambios menores/patch compatibles; priorizar CVEs explotables en superficie expuesta | Tests de regresión + smoke tras actualizaciones; comparar baseline funcional | Fijar versiones anteriores (pin/lock) y revertir commit de upgrade |
| R-07 | Integridad de cadena de suministro (A08) | Media | Paquetes/imágenes comprometidos | Dependencias, `docker-compose.yml`, pipeline | Evitar `latest` en imágenes críticas, usar tags/digests; generar lockfiles/SBOM cuando sea viable; validar fuentes en CI | Build reproducible, verificación de versiones desplegadas | Volver a tags previos conocidos |
| R-08 | Abuso y diseño resiliente (A04) | Media | DoS lógico, scraping, degradación | Endpoints de consulta/upload, caché, colas | Rate limiting por usuario/IP en creación de consultas y uploads; límites de tamaño ya validados deben mantenerse/reforzarse; timeouts consistentes | Pruebas de umbrales y mensajes 429; carga normal no afectada | Ajustar límites por configuración |
| R-09 | Revisión SSRF/uso de URLs (A10) | Media | Acceso a recursos internos (si aparece vector) | Adapters HTTP, procesamiento de documentos, `url_origen` | Inventariar todo fetch server-side; si se incorporan descargas por URL, aplicar allowlist de dominios/esquemas, bloqueo de rangos internos y validación estricta | Casos de prueba con URLs internas/metadata bloqueadas | Deshabilitar funcionalidad de fetch remoto por config |
| R-10 | Endurecimiento de datos/configuración en entornos (A05) | Media | Exposición por defaults | `.env.example`, `docker-compose.yml`, despliegue | Documentar separación dev/prod, rotación de credenciales, no exponer puertos innecesarios en prod, secretos vía gestor/vars seguras | Checklist de despliegue y revisión de configuración por entorno | Revertir cambios de compose solo en dev; prod según runbook |

## 3. Orden recomendado

1. **R-01, R-02** (inmediato: identidad, secreto y control de acceso).
2. **R-03, R-04, R-05** (hardening y detección).
3. **R-06, R-07, R-08** (suministro y abuso).
4. **R-09, R-10** (verificación focalizada y gobernanza).

## 4. Riesgos de implementación

| Riesgo | Mitigación |
|---|---|
| Cambio de secreto JWT invalida sesiones activas | Planificar ventana de mantenimiento/rotación, comunicar a administradores, rotar en horario de bajo uso. |
| Endurecer RBAC bloquea consumidores legítimos | Inventariar clientes (frontend/admin), pruebas por rol antes de desplegar, rollout gradual. |
| Rate limiting afecta usuarios detrás de NAT/oficina | Umbrales calibrados, listas de exclusión controladas, métricas de 429. |
| Actualización de dependencias rompe compatibilidad | Actualizaciones incrementales, pruebas smoke y fijación de versiones. |
| Cambios CORS/headers rompen frontend | Validar en staging con dominio real de Vercel/frontend. |

## 5. Estrategia para preservar funcionalidad

- **Compatibilidad hacia atrás:** mantener rutas y payloads existentes; añadir controles de forma transparente cuando sea posible.
- **Cambios mínimos y reversibles:** una remediación por PR, con pruebas asociadas.
- **Validación obligatoria:** smoke de login, consulta ciudadana, gestión documental, auditoría y reportes tras cada cambio.
- **Configuración por entorno:** hardening estricto en prod, parámetros relajados solo en dev cuando sea necesario y documentado.
- **Rollback:** revert de código/configuración, restauración de secretos previos desde gestor seguro, redeploy de versión anterior.
- **Registro:** documentar cada remediación aplicada y evidencia de validación para auditoría posterior.
