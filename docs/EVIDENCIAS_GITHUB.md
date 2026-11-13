# Guía de evidencias en GitHub (mejorada)

**Proyecto:** MUN AI – Sistema de Trámites Municipales  
**Repositorio:** https://github.com/JoshuaJBLX/sistemas-tramites-municipales  
**Rama:** `main`  
**Commit actual (referencia local):** `146436cf4b59d35997a6536c5fc92b21e17ac671` (`146436c`)  
**Fuente canónica de estado/cifras:** `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` (estado vigente **101/101 = 100 %**, 18/18 HU, 40 rutas servibles)

> Objetivo: definir **qué capturar en GitHub**, **dónde (URL/ruta exacta)**, **qué debe verse** y **cómo organizarlo** para sustentar los entregables `docs/01`–`docs/07` con evidencias trazables y verificables.

---

## 1. Reglas para evidencias de calidad (antes de capturar)

| Regla | Detalle |
|---|---|
| **Fijar versión** | Capturar sobre la misma rama/commit. Para evidencia inmutable, usar permalink: en GitHub presiona `y` en la vista del archivo o copia la URL con hash (`/blob/<commit>/...`). Evita que un cambio posterior invalide la captura. |
| **URL visible** | La barra de direcciones debe verse en la captura (o anotar la URL en el índice). |
| **Legibilidad** | Zoom 100 %, resolución suficiente, sin recortes que oculten nombre del repo, rama, ruta del archivo o líneas clave. |
| **Contexto en código** | En `blob`, mostrar el bloque relevante (ideal: enlace por líneas `#Lx-Ly`). No basta con la portada del archivo si el hallazgo depende de una función específica. |
| **Evidencia positiva y negativa** | Capturar tanto lo que existe (controles, arquitectura, docs) como lo que no (p. ej. ausencia de workflows en `Actions`, sin `.github/workflows`, resultados de búsqueda `pytest/workflow`). |
| **Trazabilidad** | Cada captura debe mapearse a: entregable (01–07), hallazgo/control (ID), URL y observación breve. |
| **Consistencia** | Mismo commit/tag para todo el paquete; si se usan commits distintos, indicarlo explícitamente en el índice. |

---

## 2. Estructura del paquete de evidencias

```text
evidencias-github/
├── 00_general/
│   ├── indice_capturas.csv|md        # matriz de trazabilidad (ver plantilla §8)
│   └── capturas...
├── 01_auditoria_furps/
├── 02_plan_furps/
├── 03_auditoria_implementacion_furps/
├── 04_auditoria_owasp/
├── 05_plan_owasp/
├── 06_auditoria_implementacion_owasp/
└── 07_auditoria_final/
```

**Nomenclatura recomendada:** `NN_<area>_<evidencia>_<detalle>.png`  
Ejemplos:
- `00_general/01_repo_portada_main.png`
- `00_general/02_commits_historial.png`
- `04_auditoria_owasp/03_auth_dependencias_rbac.png`
- `03_auditoria_implementacion_furps/02_actions_sin_workflows.png`

---

## 3. Paquete mínimo recomendado (rápido y defendible)

Si el tiempo es limitado, prioriza estas capturas:

1. **Repo + rama + árbol raíz** (`/tree/main`)
2. **Historial de commits** (`/commits/main`) + 2-3 commits relevantes (detalle/diff)
3. **Carpeta `docs/`** con los 7 entregables (`/tree/main/docs`)
4. **Documento rector 06** (`/blob/main/documentacion/00-documentos-rectores/06-estado-actual-implementado.md`)
5. **Arquitectura backend** (`/tree/main/backend/domain`, `/application`, `/infrastructure`)
6. **Seguridad/auth** (`main.py`, `controllers/dependencias.py`, `auth_controller.py`, `JWTAdapter.py`, `PasswordHasher.py`)
7. **Configuración/dependencias** (`docker-compose.yml`, `.env.example`, `backend/requirements.txt`, `frontend-tramites/package.json`)
8. **Evidencia negativa de aseguramiento**: `Actions` sin workflows y/o búsqueda `workflow`, búsqueda `pytest`
9. **Migraciones** (`/tree/main/database/migrations`)
10. **Frontend API client** (`frontend-tramites/lib/api.ts`)

---

## 4. Evidencias generales (obligatorias)

| ID | Evidencia | URL/ruta en GitHub | Qué debe verse | Útil para |
|---|---|---|---|---|
| G-01 | Portada del repositorio | `https://github.com/JoshuaJBLX/sistemas-tramites-municipales` | Nombre, rama `main`, README renderizado, estructura principal, actividad reciente | Contexto general |
| G-02 | Historial de commits | `https://github.com/JoshuaJBLX/sistemas-tramites-municipales/commits/main` | Secuencia de cambios, mensajes, autores y fechas | Trazabilidad / 03,06,07 |
| G-03 | Commits clave (detalle) | `.../commit/146436c`, `.../commit/7fbcc16`, `.../commit/dd19944`, `.../commit/6f985a7`, `.../commit/5a9f069` (y otros relevantes) | Diff/archivos tocados y propósito del cambio | Trazabilidad de cierres/docs/fixes |
| G-04 | Ramas | `https://github.com/JoshuaJBLX/sistemas-tramites-municipales/branches` | Rama principal y remotas | Gestión de cambios |
| G-05 | Árbol de proyecto | `.../tree/main`, `.../tree/main/backend`, `.../tree/main/frontend-tramites`, `.../tree/main/database`, `.../tree/main/documentacion` | Organización real de módulos y artefactos | FURPS S/F |
| G-06 | README | `.../blob/main/README.md` | Guía de uso/estado y referencia al rector | Contexto / consistencia documental |
| G-07 | Documento rector (fuente canónica) | `.../blob/main/documentacion/00-documentos-rectores/06-estado-actual-implementado.md` | Estado vigente 100 %, inventario, flujos, defectos/G-XX, HU/PMV | 01–07 (línea base) |
| G-08 | Entregables de auditoría | `.../tree/main/docs` | Archivos `01`–`07` y guía de evidencias | Consolidado |
| G-09 | Actions / CI (evidencia negativa o positiva) | `https://github.com/JoshuaJBLX/sistemas-tramites-municipales/actions` | Workflows, ejecuciones o ausencia de automatización | 01,03,06,07 (brecha CI) |
| G-10 | Security (si disponible) | `https://github.com/JoshuaJBLX/sistemas-tramites-municipales/security` | Alertas/dependabot/code scanning o configuración ausente | 04,05,06 (A06/A08) |
| G-11 | Búsquedas en código | `.../search?q=pytest&type=code`, `.../search?q=workflow&type=code`, `.../search?q=rate+limit&type=code`, `.../search?q=JWT_SECRET&type=code` | Presencia/ausencia de controles o prácticas | Hallazgos verificables |
| G-12 | Releases/Tags (si aplica) | `.../releases`, `.../tags` | Versionado formal o ausencia | Soporte/Suministro |

---

## 5. Evidencias por entregable (01–07)

### 5.1 `01_auditoria_furps.md` → `01_auditoria_furps/`

**Objetivo:** sustentar hallazgos FURPS+ (Functionality, Usability, Reliability, Performance, Supportability) con evidencia observable.

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | FURPS / Hallazgo |
|---|---|---|---|---|
| F-01 | Arquitectura hexagonal | `.../tree/main/backend/domain`, `.../tree/main/backend/application`, `.../tree/main/backend/infrastructure` | Carpetas y archivos representativos (entities, use_cases/services, controllers/adapters/repositories) | S, F |
| F-02 | Entrada de la API | `.../blob/main/backend/main.py` | `lifespan`, CORS, registro de routers, endpoint `/health` | F, R |
| F-03 | Flujo de consulta RAG | `.../blob/main/backend/infrastructure/controllers/consulta_controller.py` | Validación, clasificación, caché, generación, auditoría, manejo de excepciones (p. ej. SLM no disponible) | F, R, U |
| F-04 | Gestión documental | `.../blob/main/backend/infrastructure/controllers/documento_controller.py` | Registro/upload/listado/estado/reproceso/baja lógica y física, permisos | F, R |
| F-05 | Auth y sesión | `.../blob/main/backend/infrastructure/controllers/auth_controller.py`, `.../blob/main/backend/infrastructure/controllers/dependencias.py` | Login, JWT Bearer, roles, eventos de seguridad | F, R |
| F-06 | Cliente frontend | `.../blob/main/frontend-tramites/lib/api.ts` | `API_URL`, timeouts, manejo de token/sesión, errores, consumo de endpoints | U, R |
| F-07 | UI y rutas frontend | `.../tree/main/frontend-tramites/app`, `.../tree/main/frontend-tramites/components` | Estructura de páginas/componentes (chat, admin, trámites) | U, F |
| F-08 | Persistencia y evolución | `.../tree/main/database/migrations` (abrir `002_create_tables.sql`, `007_usuarios_seguridad.sql`, `008_retroalimentacion_metricas.sql`, `009_revisor_auditoria_derivacion.sql` si aplica) | Tablas, índices/cambios funcionales y de auditoría/seguridad | F, S |
| F-09 | Operación/despliegue | `.../blob/main/docker-compose.yml`, `.../blob/main/.env.example`, `.../blob/main/instalar.ps1`, `.../blob/main/DESPLEGUE_RENDER.md` | Servicios, variables, pasos de instalación/despliegue | R, P, S |
| F-10 | Verificabilidad (brecha) | `.../actions`, búsquedas `pytest`/`workflow` | Ausencia de CI y suites formales (contrastar con scripts en `backend/scripts`) | S, R (F-FUN-04/G-18) |

### 5.2 `02_plan_furps.md` → `02_plan_furps/`

**Objetivo:** evidenciar la base y trazabilidad del plan de mejora (M-01..M-10).

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | Relación |
|---|---|---|---|---|
| P-F-01 | Documento del plan | `.../blob/main/docs/02_plan_furps.md` | Roadmap, tabla de mejoras M-01..M-10, validación y rollback | Plan completo |
| P-F-02 | Insumo: auditoría FURPS | `.../blob/main/docs/01_auditoria_furps.md` | Brechas/riesgos que originan el plan | Trazabilidad 01→02 |
| P-F-03 | Evidencia de brecha CI/tests | `.../actions` y búsquedas `pytest`/`workflow` | Estado que justifica M-01/M-02 | M-01, M-02 |
| P-F-04 | Capacidades actuales de monitoreo/auditoría | `.../blob/main/backend/infrastructure/controllers/metrica_controller.py` (si existe), `consulta_controller.py` | Puntos de partida para mejoras de observabilidad/rendimiento | M-04, M-07, M-08 |
| P-F-05 | Estado rector | `.../blob/main/documentacion/00-documentos-rectores/06-estado-actual-implementado.md` | Contexto del 100 % funcional y backlog transversal | Priorización incremental |

### 5.3 `03_auditoria_implementacion_furps.md` → `03_auditoria_implementacion_furps/`

**Objetivo:** sustentar el estado de implementación de M-01..M-10 (sin asumir cumplimiento).

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | Relación |
|---|---|---|---|---|
| I-F-01 | Documento de auditoría de implementación | `.../blob/main/docs/03_auditoria_implementacion_furps.md` | Tabla de estado por mejora y conclusión | Resultado 03 |
| I-F-02 | Ausencia/presencia de CI | `.../tree/main` (buscar `.github/`), `.../actions` | No workflows / workflows existentes | M-02 |
| I-F-03 | Ausencia/presencia de suites formales | Búsquedas `pytest`, `tests`, `unittest` (`.../search?...`) y `.../tree/main/backend` | Evidencia de scripts vs suites/runner/CI | M-01 |
| I-F-04 | Scripts de verificación disponibles | `.../tree/main/backend/scripts` y archivos `probar_hu13.py`, `probar_hu151618.py` (si versionados) | Cobertura manual/verificación dirigida existente | Parcialidad / contexto |
| I-F-05 | Trazabilidad temporal | `.../commits/main` | Commits antes/después del plan (o ausencia de commits asociados a M-01..M-10) | Evidencia de no implementación |

### 5.4 `04_auditoria_owasp.md` → `04_auditoria_owasp/`

**Objetivo:** evidenciar controles y hallazgos OWASP Top 10 con base en código/configuración.

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | OWASP / Hallazgo |
|---|---|---|---|---|
| O-01 | Protección de rutas y routers | `.../blob/main/backend/main.py` | Inclusión de routers y `Depends(requiere_administrador)` en routers admin | A01 |
| O-02 | Dependencias de autenticación/RBAC | `.../blob/main/backend/infrastructure/controllers/dependencias.py` | `HTTPBearer`, validación token, carga de usuario activo, `requiere_administrador/revisor`, eventos | A01, A07, A09 |
| O-03 | Login y emisión de sesión | `.../blob/main/backend/infrastructure/controllers/auth_controller.py` | Validación de credenciales, respuesta de error genérica, registro de eventos, token | A07, A09 |
| O-04 | Hashing de contraseñas | `.../blob/main/backend/infrastructure/adapters/auth/PasswordHasher.py` | PBKDF2-HMAC-SHA256, salt, iteraciones, `compare_digest` | A02, A07 |
| O-05 | Manejo de JWT/secreto | `.../blob/main/backend/infrastructure/adapters/auth/JWTAdapter.py` | Algoritmo, expiración, obtención/derivación de secreto | A02 |
| O-06 | Consultas parametrizadas (inyección) | `.../blob/main/backend/infrastructure/controllers/usuario_controller.py`, `.../blob/main/backend/infrastructure/controllers/consulta_controller.py`, `.../blob/main/backend/infrastructure/controllers/dependencias.py` | Ejemplos de SQL con placeholders `$1..$n` | A03 |
| O-07 | CORS y configuración app | `.../blob/main/backend/main.py`, `.../blob/main/.env.example` | `CORSMiddleware`, orígenes, métodos/headers, variables sensibles no hardcodeadas en repo | A05, A02 |
| O-08 | Infra local y exposición | `.../blob/main/docker-compose.yml` | Puertos, credenciales de entorno local, imágenes/tags | A05, A08 |
| O-09 | Dependencias de software | `.../blob/main/backend/requirements.txt`, `.../blob/main/frontend-tramites/package.json` | Versiones fijadas/rangos (base para SCA) | A06, A08 |
| O-10 | Carga/procesamiento documental | `.../blob/main/backend/infrastructure/controllers/documento_controller.py` | Validaciones, manejo de errores de formato/ilegibilidad, control de acceso | A04, A01 |
| O-11 | Registro de eventos y auditoría | `.../blob/main/backend/infrastructure/controllers/dependencias.py` (función `registrar_evento_seguridad`), `consulta_controller.py` | Inserción de eventos/auditoría y comportamiento ante fallos | A09 |
| O-12 | Postura de seguridad del repo | Pestaña `Security` y `Actions` | Alertas/SCA/escaneo o ausencia visible | A06, A08, proceso |

### 5.5 `05_plan_owasp.md` → `05_plan_owasp/`

**Objetivo:** mostrar trazabilidad desde hallazgos OWASP a remediaciones R-01..R-10.

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | Relación |
|---|---|---|---|---|
| P-O-01 | Documento del plan OWASP | `.../blob/main/docs/05_plan_owasp.md` | Roadmap R-01..R-10, mitigación, validación, rollback | Plan completo |
| P-O-02 | Insumo: auditoría OWASP | `.../blob/main/docs/04_auditoria_owasp.md` | Hallazgos/score que justifican el plan | Trazabilidad 04→05 |
| P-O-03 | Evidencia base A01/A02/A07 | `auth_controller.py`, `dependencias.py`, `JWTAdapter.py`, `PasswordHasher.py` | Controles existentes y puntos a endurecer | R-01, R-02, R-03 |
| P-O-04 | Evidencia base A05/A09 | `main.py` (CORS), `dependencias.py` (eventos), `.env.example` | Configuración/logging actual | R-04, R-05 |
| P-O-05 | Evidencia base A06/A08 | `backend/requirements.txt`, `frontend-tramites/package.json`, `docker-compose.yml`, `Security` tab | Superficie de dependencias/suministro | R-06, R-07, R-08, R-10 |

### 5.6 `06_auditoria_implementacion_owasp.md` → `06_auditoria_implementacion_owasp/`

**Objetivo:** evidenciar verificación de R-01..R-10 contra el estado real del repositorio.

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | Relación |
|---|---|---|---|---|
| I-O-01 | Documento de implementación OWASP | `.../blob/main/docs/06_auditoria_implementacion_owasp.md` | Estado por remediación, riesgos residuales, score actualizado | Resultado 06 |
| I-O-02 | Estado actual de controles auth/JWT | `dependencias.py`, `auth_controller.py`, `JWTAdapter.py`, `PasswordHasher.py` | Evidencia observada para R-01/R-02/R-03 | A01/A02/A07 |
| I-O-03 | Estado actual CORS/config/logging | `main.py`, `.env.example`, `docker-compose.yml` | Evidencia observada para R-04/R-05/R-10 | A05/A09 |
| I-O-04 | Estado dependencias/suministro | `requirements.txt`, `package.json`, `docker-compose.yml`, `Security/Actions` | Evidencia observada para R-06/R-07/R-08 | A06/A08 |
| I-O-05 | Trazabilidad de cambios de seguridad | `.../commits/main` (+ búsqueda por mensajes: `security`, `auth`, `jwt`, `rate`, `cors`) | Presencia o ausencia de commits asociados a remediaciones | Soporte del veredicto |

### 5.7 `07_auditoria_final.md` → `07_auditoria_final/`

**Objetivo:** consolidar evidencia de calidad, seguridad, funcionalidad y dictamen final.

| ID | Evidencia | URL/ruta en GitHub | Qué capturar | Relación |
|---|---|---|---|---|
| F-01 | Dictamen final | `.../blob/main/docs/07_auditoria_final.md` | Resumen ejecutivo, estados, riesgo operativo, recomendación | Resultado final |
| F-02 | Paquete completo 01–07 | `.../tree/main/docs` | Los 7 informes + guía de evidencias | Completitud |
| F-03 | Fuente canónica | `.../blob/main/documentacion/00-documentos-rectores/06-estado-actual-implementado.md` | Estado 100 % (101/101), HU/PMV, inventario y backlog transversal | Línea base verificable |
| F-04 | Evidencia de evolución reciente | `.../commits/main` | Commits de cierre/sincronización documental y técnica | Trazabilidad |
| F-05 | Evidencias de brechas residuales | `.../actions`, búsquedas `pytest`/`workflow`/`rate limit` | Sustento de condiciones y riesgos pendientes | Recomendación condicionada |

---

## 6. Búsquedas en GitHub recomendadas (capturas de apoyo)

Usa la búsqueda del repositorio (`https://github.com/JoshuaJBLX/sistemas-tramites-municipales/search`) y captura resultados (incluyendo “No results” si aplica):

| Consulta | Tipo | Propósito |
|---|---|---|
| `pytest` | Code | Evidencia de pruebas/suites o ausencia |
| `workflow` / `.github/workflows` | Code | Evidencia de CI/CD |
| `rate limit` / `slowapi` / `limiter` | Code | Evidencia de anti-abuso |
| `JWT_SECRET` | Code | Manejo/referencias de secreto JWT |
| `CORS` / `CORSMiddleware` | Code | Configuración de CORS |
| `TODO` / `FIXME` (opcional) | Code | Deuda técnica visible |

---

## 7. Checklist de entrega

- [ ] Todas las capturas tomadas sobre la **misma rama/commit** (indicado en índice)
- [ ] URL visible o registrada para cada captura
- [ ] Cobertura mínima completa (§3) y mapeo a 01–07
- [ ] Evidencias negativas incluidas (Actions/CI, pruebas formales, controles ausentes si aplica)
- [ ] Capturas de código con líneas relevantes visibles (`#Lx-Ly` cuando aplique)
- [ ] Índice de trazabilidad completado (§8)
- [ ] Nombres de archivo consistentes y ordenados por carpeta
- [ ] Revisión final: cada hallazgo crítico del informe tiene al menos una evidencia en GitHub

---

## 8. Plantilla de índice de trazabilidad (recomendada)

Crear `evidencias-github/00_general/indice_capturas.csv` (o `.md`) con estas columnas:

| archivo | carpeta | entregable | id_hallazgo/control | descripcion_evidencia | url_github | commit | observacion |
|---|---|---|---|---|---|---|---|
| `00_general/01_repo_portada_main.png` | `00_general` | General | G-01 | Portada del repositorio en rama main | https://github.com/JoshuaJBLX/sistemas-tramites-municipales | 146436c | Contexto y estructura visible |
| `04_auditoria_owasp/03_dependencias_rbac.png` | `04_auditoria_owasp` | 04 | A01/A07 | Validación JWT y control de roles | https://github.com/JoshuaJBLX/sistemas-tramites-municipales/blob/main/backend/infrastructure/controllers/dependencias.py | 146436c | Evidencia de RBAC/eventos |

> Sugerencia: al finalizar, exporta también una versión PDF del índice si la entrega lo requiere.
