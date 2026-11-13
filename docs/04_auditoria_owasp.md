# 04. Auditoría de Seguridad OWASP Top 10 (2021)

**Fecha:** 2026-11-13  
**Alcance:** Frontend, backend, APIs, autenticación/autorización, configuración, dependencias e infraestructura disponible en repositorio.  
**Rol ejecutado:** Auditor de Seguridad (OWASP Top 10).  
**Restricción aplicada:** Auditoría pasiva, sin correcciones ni modificaciones. Evidencia basada en revisión estática del repositorio.  
**Revisión cruzada:** contrastado con `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (cierre HU-13/G-01, HU-15/16/18, D-8; pendientes G-18, G-20, G-03, P2-17).

## 1. Metodología y límites

- Revisión de código/configuración: `backend/` (FastAPI, controladores, auth, JWT, hashing), `frontend-tramites/` (cliente API), `.env.example`, `docker-compose.yml`, `requirements.txt`, migraciones.
- No se realizaron pruebas dinámicas (DAST), pentest autenticado en entorno vivo, escaneo SCA con base de vulnerabilidades actualizada en línea, ni revisión de infraestructura desplegada real fuera del repo.
- El documento rector 06 aporta contexto de diseño/despliegue (p. ej. derivación de `JWT_SECRET` por restricción de Render CLI, endpoints protegidos, scripts de verificación) que se incorpora como evidencia documental complementaria. Hallazgos marcados según evidencia observable.

## 2. Resultado por categoría

| # | Categoría OWASP | Estado | Severidad | Probabilidad | Impacto | Evidencia | Observación |
|---|---|---|---|---|---|---|---|
| A01 | Broken Access Control | **Parcialmente controlado** | Alta | Media | Alto | Rector 06 indica HU-13 cerrada y D-8 corregido (endpoints admin protegidos por JWT/rol). `main.py` aplica `Depends(requiere_administrador)` a routers admin; `dependencias.py` implementa auth/RBAC (`obtener_usuario_actual/opcional`, `requiere_administrador`, `requiere_revisor`) y eventos `acceso_denegado`; `usuario_controller.py` controla bootstrap/lecturas; mutaciones documentales restringidas. `GET /api/consultas/{id}` es público (trazabilidad ciudadana) y algunos listados pueden ser públicos por diseño. | RBAC implementado de forma amplia; requiere verificación integral endpoint-rol y decisión explícita sobre exposición de trazabilidad/datos sensibles por identificador. |
| A02 | Cryptographic Failures | **Parcialmente controlado** | Media-Alta | Media | Alto | `PasswordHasher.py`: PBKDF2-HMAC-SHA256 con salt aleatorio, 310k iteraciones y `compare_digest`. `JWTAdapter.py`: HS256 con `JWT_SECRET` o derivación determinista (SHA-256) desde material de entorno (documentado en rector 06 como compatibilidad por restricción de Render CLI); si no hay material base el secreto puede resultar débil. `.env.example` no guía `JWT_SECRET`. | Hashing adecuado; la postura JWT es aceptable solo si el entorno provee secreto/material robusto y rotación controlada. Recomendar `JWT_SECRET` explícito en producción. |
| A03 | Injection | **Controlado (evidencia favorable)** | Media | Baja | Alto | Uso consistente de consultas parametrizadas asyncpg (`$1`, `$2`, ...) en `dependencias.py`, `auth_controller.py`, `consulta_controller.py`, `usuario_controller.py`, `documento_controller.py` (a través de casos/repos) y script de prueba. | No se observaron concatenaciones SQL directas en patrones revisados; revisión completa de repositorios/adapters no exhaustiva en esta pasada. |
| A04 | Insecure Design | **Parcialmente controlado** | Media | Media | Medio | Controles de diseño presentes: groundedness/bloqueo de afirmaciones, clasificación de dominio y derivación (HU-10/11/17) en `consulta_controller.py`; validación de formatos/errores de documento (`FormatoNoSoportadoError`, `DocumentoIlegibleError`); límites en listados (`max(1,min(limite,100))`). | Faltan controles de abuso/rate limiting evidentes y pruebas de diseño de amenazas documentadas en repo. |
| A05 | Security Misconfiguration | **Riesgo presente** | Alta | Media | Medio-Alto | `main.py` CORS permite orígenes locales y `VERCEL_FRONTEND_URL`, con `allow_credentials=True`, `allow_methods=['*']`, `allow_headers=['*']`. `.env.example` incluye credenciales por defecto de ejemplo; `docker-compose.yml` expone puertos 5432/6379/11434 y credenciales simples. No se evidencia hardening de headers (CSP/HSTS) en app (puede delegarse a proxy). Debug/entorno productivo no determinable desde repo. | Configuración permisiva típica de dev; requiere endurecimiento por entorno en despliegue real. |
| A06 | Vulnerable and Outdated Components | **Riesgo no evaluado completamente** | Alta (potencial) | Media | Alto | `backend/requirements.txt` fija versiones (ej. `fastapi==0.111.0`, `uvicorn==0.30.1`, `python-multipart==0.0.9`, `pydantic==2.9.2`, `httpx==0.27.0`, `openai==1.109.1`, etc.). `frontend-tramites/package.json` usa `next@14.2.5`, `react@^18.3.1`. | No se ejecutó SCA/`pip-audit`/`npm audit` ni comparación con advisories actuales; versiones pinneadas requieren verificación periódica. |
| A07 | Identification and Authentication Failures | **Parcialmente controlado** | Media-Alta | Media | Alto | Rector 06/HU-13: login JWT HS256 (8 h), contraseñas PBKDF2, validación de usuario activo, eventos de seguridad (`login_exitoso/fallido`, `token_invalido`, `acceso_denegado`), bootstrap controlado de primer admin y scripts de verificación. | Controles base sólidos; faltan rate limiting/bloqueo ante intentos, MFA/políticas avanzadas y revocación/rotación formal de sesiones. |
| A08 | Software and Data Integrity Failures | **Parcialmente controlado** | Media | Baja-Media | Alto | Dependencias de registros públicos sin evidencia de pinning por hash/SBOM/firma en repo; sin CI de integridad. Docker compose usa tags (incl. `ollama:latest`). | Riesgo de cadena de suministro y reproducibilidad. |
| A09 | Security Logging and Monitoring Failures | **Parcialmente controlado** | Media | Media | Medio | Existen `eventos_seguridad`, auditoría de consultas con trazabilidad/marcado y métricas/reportes administrativos (HU-16/18). `registrar_evento_seguridad` es best-effort y silencia fallos de inserción (`except: pass`). | Buena base de auditoría; falta garantizar alerta/retención ante fallos de registro y monitoreo centralizado. |
| A10 | Server-Side Request Forgery (SSRF) | **Riesgo bajo / evidencia limitada** | Media | Baja | Medio | Backend integra Ollama/servicios vía configuración (`OLLAMA_URL` en `.env.example`) y adaptadores; no se identificó endpoint que acepte URL arbitraria del usuario para fetch server-side en controladores revisados. `url_origen` se almacena como metadato de documento. | Sin indicador claro de SSRF explotable; requiere revisión de adapters HTTP y validación de URLs si se usan para descarga/procesado. |

## 3. Hallazgos transversales relevantes

1. **Gestión de secretos JWT (A02):** soporta `JWT_SECRET` pero permite derivación/fallback por compatibilidad operativa; `.env.example` no lo documenta explícitamente.
2. **Ausencia de controles anti-abuso visibles (A04/A07):** sin rate limiting en login/consultas/cargas (G-20 guardrails anti prompt-injection también pendiente según rector 06).
3. **Exposición y configuración CORS amplia (A05):** métodos/cabeceras `*` con credenciales habilitadas (acotado a orígenes listados).
4. **Componentes sin verificación SCA reciente (A06):** riesgo potencial no cuantificado.
5. **Eventos de seguridad best-effort (A09):** inserción puede fallar silenciosamente; requiere alerta/fallback operativo.
6. **Datos sensibles/PII:** manejo de PII pendiente (G-03, rector 06).

## 4. Clasificación de riesgos (resumen)

- **Crítico:** Ninguno confirmado con evidencia directa de explotación en revisión estática.
- **Alto:** A01 (residual de exposición/cobertura), A02 (gestión de secreto JWT dependiente de entorno), A05 (configuración/hardening), A06 (potencial por falta de SCA), A07 (anti-abuso no implementado).
- **Medio:** A03 (residual), A04, A08, A09, A10.
- **Bajo:** No aplica como categoría principal.

## 5. Score global de seguridad

**Score estimado: 66 / 100 (Cumplimiento parcial).**

**Criterio:** ponderación cualitativa actualizada tras revisión con rector 06 (se reconoce implementación de HU-13/G-01 y auditoría/telemetría funcional), manteniendo brechas en hardening, anti-abuso, gestión explícita de secretos, SCA y garantía de monitoreo. Orientativo; requiere recalibración con SCA y pruebas dinámicas.
