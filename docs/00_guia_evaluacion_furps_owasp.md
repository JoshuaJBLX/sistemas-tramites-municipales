# Guía para la Evaluación, Mejora y Validación de la Calidad y Seguridad de Software mediante FURPS+ y OWASP Top 10 utilizando Agentes de IA

**Aplicación real sobre el proyecto `sistemas-tramites-municipales` — informe de ejecución**

| Campo | Valor |
|---|---|
| **Proyecto** | MUN AI — Sistema de Trámites Municipales |
| **Repositorio** | <https://github.com/JoshuaJBLX/sistemas-tramites-municipales> |
| **Rama / commit de referencia** | `main` / `146436c` |
| **Fecha de ejecución** | 2026-11-13 |
| **Agente ejecutor** | OpenCode (agente de IA con acceso a código, shell y edición de archivos) |
| **Marcos aplicados** | FURPS+ (calidad) · OWASP Top 10 2021 (seguridad) |
| **Fuente canónica del estado** | `documentacion/00-documentos-rectores/06-estado-actual-implementado.md` |
| **Estado del proyecto (funcional)** | **100 % = 101/101**, 18/18 HU, PMV1/PMV2/PMV3 al 100 %, 40 rutas servibles |
| **Estado de los planes de esta intervención** | **No aplicados** (0/10 mejoras FURPS+, 0/10 remediaciones OWASP) |
| **Dictamen final** | **Apto para producción con observaciones** — riesgo operativo **MEDIO-ALTO** |

---

## 0. Resumen ejecutivo

Se ejecutó el proceso completo de la guía en sus tres fases (calidad, seguridad y validación global) sobre un proyecto **ya funcional y documentado como cerrado al 100 %**. La intervención fue **no invasiva**: se diagnosticó con evidencia, se planificaron mejoras incrementales y se verificó de forma independiente qué se implementó realmente.

### 0.1 Resultados clave

| Dimensión | Resultado | Escala / referencia |
|---|---|---|
| **Calidad FURPS+** | **3.5 / 5.0** — cumple parcialmente | Promedio simple de 5 categorías (§7.1) |
| **Seguridad OWASP Top 10** | **66 / 100** — cumple parcialmente | Rúbrica 10 categorías × 10 puntos (§8.1) |
| **Madurez de calidad** | **3 / 5** — “Definido” | Procesos y documentación definidos; medición/automatización débil |
| **Madurez de seguridad** | **2.5 / 5** — “Repetible” | Controles base presentes; hardening y verificación continua en consolidación |
| **Funcionalidad** | **Preservada** | Sin cambios de código; sin regresiones atribuibles |
| **Estabilidad** | **No acreditada en ejecución** | Sin build/despliegue/suites en esta sesión |
| **Riesgo operativo** | **MEDIO-ALTO** | Matriz probabilidad × impacto (§9.2) |
| **Recomendación** | **Apto con observaciones** | Condicionado a R-01/R-02/R-03/R-05 + M-01/M-02 |

### 0.2 Cifras del proceso

| Métrica | Valor |
|---|---|
| Agentes ejecutados | **7 / 7** |
| Entregables producidos | **7 / 7** (`docs/01`–`docs/07`) + guía de evidencias |
| Hallazgos de calidad documentados | **18** (F-FUN, F-USA, F-REL, F-PER, F-SUP) |
| Categorías OWASP evaluadas | **10 / 10** |
| Acciones planificadas | **20** (M-01..M-10 + R-01..R-10) |
| Acciones aplicadas en esta intervención | **0** |
| Acciones con capacidades parciales preexistentes | **5** (M-03, M-07, M-10, R-02, R-10) |
| Pruebas dinámicas / SCA ejecutados | **0** |

### 0.3 Aclaración clave: dos métricas que no deben confundirse

| Métrica | Valor | Significado |
|---|---|---|
| **Avance funcional del proyecto** | **100 % (101/101)** | Estado de las 18 HU según el rector 06 (trabajo previo del equipo). |
| **Aplicación de los planes de esta auditoría** | **0 %** | Ninguna mejora M-01..M-10 ni remediación R-01..R-10 fue implementada en esta intervención. |

> Ambas afirmaciones son compatibles: el sistema está funcionalmente completo, pero **no acredita** las mejoras de aseguramiento y hardening propuestas por esta auditoría.

### 0.4 Índice

1. [Introducción](#1-introducción) · 2. [Objetivos](#2-objetivos) · 3. [Alcance y método](#3-alcance-y-método) · 4. [Principios](#4-principios-fundamentales-y-cómo-se-cumplieron) · 5. [Entregables](#5-organización-de-entregables) · 6. [Flujo](#6-flujo-general-del-proceso-ejecutado) · 7. [Fase 1 — Calidad](#7-fase-1--evaluación-y-mejora-de-calidad) · 8. [Fase 2 — Seguridad](#8-fase-2--evaluación-y-mejora-de-seguridad) · 9. [Fase 3 — Validación](#9-fase-3--validación-integral) · 10. [Criterios de aprobación](#10-criterios-de-aprobación-evaluación-real) · 11. [Resultados esperados](#11-resultados-esperados-verificación-de-entrega) · 12. [Backlog](#12-backlog-priorizado-con-esfuerzo-y-criterios-de-aceptación) · 13. [Verificación reproducible](#13-verificación-reproducible-comandos) · 14. [Evidencias](#14-evidencias-y-trazabilidad) · 15. [Limitaciones](#15-limitaciones-supuestos-y-observaciones) · 16. [Conclusión](#16-conclusión) · [Anexos](#anexo-a-prompts-completos-de-los-7-agentes)

---

## 1. Introducción

La presente guía establece el procedimiento estandarizado aplicado para **evaluar, mejorar y validar** el proyecto `sistemas-tramites-municipales` utilizando dos marcos reconocidos de la industria:

- **FURPS+** para la evaluación de la **calidad del software** (Functionality, Usability, Reliability, Performance, Supportability y los “+” de restricciones de diseño, implementación, interfaz y física).
- **OWASP Top 10 (2021)** para la evaluación de la **seguridad de aplicaciones**.

El proyecto ya se encontraba **funcional y documentado como cerrado al 100 %** según su documento rector (`06-estado-actual-implementado.md`). Por ello, la intervención se ejecutó bajo un criterio **no invasivo**:

1. **Diagnosticar** con evidencia verificable.
2. **Planificar** mejoras incrementales, compatibles y reversibles.
3. **Verificar** de forma independiente qué se implementó realmente.
4. **Dictaminar** el estado final sin comprometer la funcionalidad existente.

Los agentes utilizados fueron los definidos en los siete archivos de instrucciones de la raíz del repositorio:

| # | Agente | Archivo de definición | Entregable |
|---|---|---|---|
| 1 | Auditor FURPS+ | `Auditor FURPS+.txt` | `01_auditoria_furps.md` |
| 2 | Planificador FURPS+ | `Planificador FURPS+.txt` | `02_plan_furps.md` |
| 3 | Auditor de Implementación FURPS+ | `Auditor de Implementación FURPS+.txt` | `03_auditoria_implementacion_furps.md` |
| 4 | Auditor OWASP Top 10 | `Auditor OWASP Top 10.txt` | `04_auditoria_owasp.md` |
| 5 | Planificador OWASP Top 10 | `Planificador OWASP Top 10.txt` | `05_plan_owasp.md` |
| 6 | Auditor de Implementación OWASP | `Auditor de Implementación OWASP.txt` | `06_auditoria_implementacion_owasp.md` |
| 7 | Auditor Final Integral | `Auditor Final Integral.txt` | `07_auditoria_final.md` |

> **Nota de alcance:** el agente trabajó en modo **análisis estático** del repositorio (código, configuración, migraciones, documentación y scripts). No se dispuso de un entorno vivo con PostgreSQL/Redis/Ollama ni de suites automatizadas para ejecutar pruebas dinámicas. Los prompts completos se reproducen en el [Anexo A](#anexo-a-prompts-completos-de-los-7-agentes).

---

## 2. Objetivos

### 2.1 Objetivo general

Evaluar, mejorar y validar la calidad y seguridad del proyecto `sistemas-tramites-municipales` utilizando agentes de IA, **preservando la funcionalidad existente**.

### 2.2 Objetivos específicos y resultado obtenido

| # | Objetivo específico | Resultado | Evidencia |
|---:|---|---|---|
| 1 | Evaluar la calidad mediante FURPS+ | ✅ **Cumplido** — 3.5/5.0 | `docs/01` §2 |
| 2 | Identificar oportunidades de mejora | ✅ **Cumplido** — 10 mejoras | `docs/02` §2 |
| 3 | Implementar mejoras de forma controlada | ⏸️ **No ejecutado** — decisión justificada | §7.3 |
| 4 | Evaluar la seguridad mediante OWASP Top 10 | ✅ **Cumplido** — 66/100 | `docs/04` §2–5 |
| 5 | Remediar vulnerabilidades identificadas | ⏸️ **No ejecutado** — plan definido | §8.3 |
| 6 | Verificar que las mejoras no generen regresiones | ⚠️ **Parcial** — sin regresiones por ausencia de cambios; sin pruebas dinámicas | `docs/03`, `docs/06` |
| 7 | Emitir una validación final del estado del proyecto | ✅ **Cumplido** | `docs/07` |

### 2.3 Criterios de éxito del proceso (no del sistema)

| Criterio | Estado |
|---|---|
| Todos los entregables existen y son trazables | ✅ |
| Cada hallazgo cita evidencia observable | ✅ |
| Los planes indican validación y rollback | ✅ |
| La verificación no asume implementación | ✅ |
| Se documentan limitaciones y riesgos residuales | ✅ |

---

## 3. Alcance y método

### 3.1 Incluido en la evaluación

| Área | Elementos revisados |
|---|---|
| **Backend** | `backend/main.py`, controladores (`consulta`, `documento`, `usuario`, `auth`, `métrica`, `evaluación`, `reporte`, `oficina`), `dependencias.py`, adaptadores (`JWTAdapter`, `PasswordHasher`, `RedisAdapter`), puertos y casos de uso. |
| **Frontend** | `frontend-tramites/lib/api.ts`, `package.json`, rutas y componentes principales (`app/`, `components/`). |
| **Base de datos** | Migraciones `001`–`009`, seeds y esquema (18 archivos `.sql`). |
| **Configuración e infraestructura** | `docker-compose.yml`, `.env.example`, `requirements.txt`, `instalar.ps1`, `DESPLEGUE_RENDER.md`, Dockerfiles. |
| **Pruebas y aseguramiento** | Scripts de verificación (`scripts/probar_hu13.py`, `scripts/probar_hu151618.py`), ausencia/presencia de `pytest` y CI (`.github/workflows`). |
| **Documentación** | Rector `06`, `README.md`, `DOCUMENTACION.md`, `documentacion/` y `presentacion/`. |

**Volumen analizado (según rector 06):** 104 archivos `.py`, 27 `.ts/.tsx` de fuente, 18 `.sql`, 94 `.md`, 40 rutas servibles.

### 3.2 Excluido o no verificable en esta sesión

| Exclusión | Motivo | Impacto en las conclusiones |
|---|---|---|
| Pruebas dinámicas (DAST), pentest autenticado, explotación | Sin entorno vivo desplegado en la sesión | Hallazgos de seguridad son **potenciales**, no explotados |
| SCA en línea (`pip-audit`, `npm audit`) | Sin base de vulnerabilidades actualizada en línea | A06 se reporta como **no evaluado / potencial** |
| Ejecución integrada (PostgreSQL, Redis, Ollama) | Sin infraestructura levantada | No se acredita estabilidad en ejecución |
| Pruebas de carga, p95, benchmarks | Sin entorno representativo | Performance evaluada solo por diseño/código |
| WCAG/SUS con usuarios | Sin sesión de usabilidad | Usabilidad evaluada de forma heurística |
| Revisión exhaustiva de todos los adaptadores/repositorios | Tiempo/alcance | Revisión focalizada en flujos críticos |

### 3.3 Método y fuentes de evidencia

1. **Lectura dirigida del código** de los flujos críticos (consulta RAG, documentos, auth/RBAC, auditoría, métricas/reportes).
2. **Revisión de configuración** (CORS, secretos, dependencias, compose).
3. **Contraste documental** con el rector 06 como fuente única de verdad.
4. **Búsquedas de evidencia negativa** (ausencia de CI, suites, rate limiting, headers, SBOM).
5. **Trazabilidad explícita**: cada hallazgo → archivo/función → plan → verificación.

**Regla de evidencia aplicada:** ninguna afirmación se emite como “implementada/corregida” sin evidencia observable en el repositorio. Lo no verificable se marca como **“no verificado”**, no como ausente.

### 3.4 Reproducibilidad

| Elemento | Valor |
|---|---|
| Rama | `main` |
| Commit local de referencia | `146436c` (`docs(limpieza): eliminar PMV2_DOCUMENTOS.md y PRESENTACION-PMV1.md...`) |
| Fecha de revisión | 2026-11-13 |
| Comandos de verificación | §13 |
| Capturas de evidencia | `docs/EVIDENCIAS_GITHUB.md` |

---

## 4. Principios fundamentales (y cómo se cumplieron)

| Principio | Aplicación concreta | ¿Verificado? |
|---|---|---|
| **Preservación de funcionalidad** | No se modificó código de aplicación, configuración ni migraciones. Solo se creó/actualizó documentación en `docs/` y se corrigieron cifras documentales inconsistentes. | ✅ `git diff` acotado a `.md` |
| **Compatibilidad** | No se alteraron contratos de API, esquemas de BD, integraciones ni variables de entorno. Los planes se diseñaron como cambios aditivos y reversibles. | ✅ Sin cambios de código |
| **Evidencia** | Cada hallazgo de `docs/01`/`docs/04` cita archivo, función o configuración. Las auditorías 03/06 verifican estado real. Lo no verificable se declara. | ✅ §14 |
| **Implementación incremental** | Planes en fases (F0–F3, R0–R3) con una acción por cambio, validación y rollback. **No se aplicó ninguna** por ausencia de red de pruebas y entorno. | ✅ §7.3, §8.3 |
| **Riesgo mínimo** | Se priorizó no introducir cambios no validados sobre un sistema en producción. | ✅ Decisión documentada |
| **Rollback** | Cada M/R incluye estrategia de reversión (revert de commit, flag de config, versión anterior de imagen). | ✅ `docs/02`, `docs/05` |

---

## 5. Organización de entregables

```text
docs/
├── 00_guia_evaluacion_furps_owasp.md      # este documento (registro de aplicación)
├── 01_auditoria_furps.md                  # Fase 1 - Paso 1
├── 02_plan_furps.md                       # Fase 1 - Paso 2
├── 03_auditoria_implementacion_furps.md   # Fase 1 - Paso 4
├── 04_auditoria_owasp.md                  # Fase 2 - Paso 5
├── 05_plan_owasp.md                       # Fase 2 - Paso 6
├── 06_auditoria_implementacion_owasp.md   # Fase 2 - Paso 8
├── 07_auditoria_final.md                  # Fase 3 - Paso 9
└── EVIDENCIAS_GITHUB.md                   # guía de capturas para sustentar evidencias
```

| Entregable | Estado | Contenido principal | Control de calidad aplicado |
|---|---|---|---|
| `01_auditoria_furps.md` | ✅ | Puntaje por categoría, 18 hallazgos, brechas y riesgos | Fecha, rol, alcance, restricción y evidencia por hallazgo |
| `02_plan_furps.md` | ✅ | Roadmap F0–F3 + M-01..M-10 con validación/rollback | Prioridad, riesgo, dependencias y estrategia de preservación |
| `03_auditoria_implementacion_furps.md` | ✅ | Estado real de M-01..M-10 (0/3/7) | Comparación antes/después + riesgos residuales |
| `04_auditoria_owasp.md` | ✅ | A01–A10 con severidad/probabilidad/impacto + score 66/100 | Evidencia por categoría + límites del análisis |
| `05_plan_owasp.md` | ✅ | Roadmap R0–R3 + R-01..R-10 con validación/rollback | Componentes afectados y mitigación por riesgo |
| `06_auditoria_implementacion_owasp.md` | ✅ | Estado real de R-01..R-10 (0/2/8) + score actualizado | Sin asumir correcciones + nuevas vulnerabilidades |
| `07_auditoria_final.md` | ✅ | Dictamen, riesgo operativo y recomendación | Consolida 03+06 y estado actual |
| `EVIDENCIAS_GITHUB.md` | ✅ | URLs, qué capturar, checklist e índice | Permalinks, evidencia positiva/negativa y trazabilidad |

---

## 6. Flujo general del proceso (ejecutado)

```text
FASE 1 - CALIDAD
┌─────────────────────────────┐
│ 1. Auditor FURPS+           │──► docs/01_auditoria_furps.md
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 2. Planificador FURPS+      │──► docs/02_plan_furps.md
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 3. Aplicación del plan      │──► NO APLICADO (§7.3)
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 4. Auditor de Implementación│──► docs/03_auditoria_implementacion_furps.md
└─────────────────────────────┘

FASE 2 - SEGURIDAD
┌─────────────────────────────┐
│ 5. Auditor OWASP Top 10     │──► docs/04_auditoria_owasp.md
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 6. Planificador OWASP       │──► docs/05_plan_owasp.md
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 7. Aplicación del plan      │──► NO APLICADO (§8.3)
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 8. Auditor de Implementación│──► docs/06_auditoria_implementacion_owasp.md
└─────────────────────────────┘

FASE 3 - VALIDACIÓN GLOBAL
┌─────────────────────────────┐
│ 9. Auditor Final Integral   │──► docs/07_auditoria_final.md
└─────────────────────────────┘
```

| Paso | Agente | Entrada | Salida | Resultado |
|---:|---|---|---|---|
| 1 | Auditor FURPS+ | Repositorio completo | `01_auditoria_furps.md` | 3.5/5.0 |
| 2 | Planificador FURPS+ | `01` | `02_plan_furps.md` | 10 mejoras priorizadas |
| 3 | Aplicación del plan | `02` | Cambios en repositorio | **No ejecutado** |
| 4 | Auditor de Implementación FURPS+ | `01`, `02`, estado actual | `03_...furps.md` | Plan no cumplido (0/3/7) |
| 5 | Auditor OWASP Top 10 | Repositorio completo | `04_auditoria_owasp.md` | 66/100 |
| 6 | Planificador OWASP Top 10 | `04` | `05_plan_owasp.md` | 10 remediaciones priorizadas |
| 7 | Aplicación del plan | `05` | Cambios en repositorio | **No ejecutado** |
| 8 | Auditor de Implementación OWASP | `04`, `05`, estado actual | `06_...owasp.md` | Plan no cumplido (0/2/8) |
| 9 | Auditor Final Integral | `03`, `06`, estado actual | `07_auditoria_final.md` | Apto con observaciones |

### 6.1 Puntos de decisión (gates)

| Gate | Momento | Pregunta | Resultado |
|---|---|---|---|
| **G1** | Tras auditoría FURPS+ | ¿Los hallazgos están respaldados por evidencia? | ✅ Aprobado |
| **G2** | Tras plan FURPS+ | ¿Las mejoras son incrementales y reversibles? | ✅ Aprobado |
| **G3** | Tras verificación FURPS+ | ¿Se aplicó el plan? | ❌ No aplicado |
| **G4** | Tras auditoría OWASP | ¿Las categorías fueron evaluadas con evidencia? | ✅ Aprobado |
| **G5** | Tras plan OWASP | ¿Las remediaciones preservan funcionalidad? | ✅ Aprobado |
| **G6** | Tras verificación OWASP | ¿Se aplicaron las remediaciones? | ❌ No aplicado |
| **G7** | Auditoría final | ¿El proyecto es apto para producción? | ⚠️ Apto con observaciones |

---

## 7. Fase 1 — Evaluación y mejora de calidad

### 7.1 Paso 1. Auditoría FURPS+

**Prompt aplicado:** Auditor Senior de Calidad de Software; analizar código, arquitectura, APIs, BD, configuración, pruebas, documentación, flujos e interfaces; **no modificar nada** ni asumir funcionalidades; evaluar F/U/R/P/S y generar resumen, puntajes, hallazgos, evidencias, brechas y riesgos (texto completo en [Anexo A.1](#a1-agente-1--auditor-furps)).

**Ejecución:** revisión estática del backend (arquitectura hexagonal), frontend, migraciones, configuración y documentación; contraste con el rector 06.

#### 7.1.1 Puntaje por categoría

| Categoría | Puntaje (0–5) | Estado | Justificación breve |
|---|---:|---|---|
| **Functionality (F)** | **4.5** | Bueno | Cobertura amplia: RAG, catálogo, documentos, auth/RBAC, auditoría, evaluación, métricas, reportes y derivación; 18/18 HU al 100 %. Brecha: regresión automatizada formal. |
| **Usability (U)** | **3.2** | Parcial | Flujos de consulta, transparencia (confianza/groundedness/fuentes/derivación), voto ciudadano y panel admin real. Sin evidencia WCAG/SUS. |
| **Reliability (R)** | **3.3** | Parcial | Manejo de errores, caché degradable, auditoría y eventos. Dependencias externas críticas; sin CI/monitoreo integral. |
| **Performance (P)** | **2.7** | Parcial | Caché, pgvector/HNSW, fragmentación y `duracion_ms`. Sin SLOs por percentil, benchmarks ni pruebas de carga. |
| **Supportability (S)** | **3.7** | Parcial-bueno | Arquitectura hexagonal, DI, migraciones 001–009, documentación extensa y scripts. Débil en CI/pytest/observabilidad. |

**Cálculo:** `(4.5 + 3.2 + 3.3 + 2.7 + 3.7) / 5 = 17.4 / 5 = 3.48 ≈ 3.5`.

**Interpretación:** 3.5/5 corresponde a un sistema **funcionalmente sólido con aseguramiento intermedio**; no es un aprobado pleno de calidad de producción porque las dimensiones de verificación (P, R, S) dependen de prácticas que no están institucionalizadas.

#### 7.1.2 Hallazgos por categoría

**Functionality**

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-FUN-01 | Cobertura funcional amplia de dominio municipal y RAG | `main.py` incluye routers de consulta/trámite/documento/usuario/auth/oficina/métrica/evaluación/reporte/admin; `consulta_controller.py` | Alto positivo |
| F-FUN-02 | Gestión documental y ciclo de vida implementados | `documento_controller.py`: registro, upload, listado, estado, reproceso, baja lógica/física; 422 en formato/ilegibilidad | Alto positivo |
| F-FUN-03 | Autenticación y RBAC presentes | `auth_controller.py` (`/api/auth/login`, `/api/auth/me`); `dependencias.py` (`requiere_administrador`, `requiere_revisor`); routers admin protegidos | Alto positivo |
| F-FUN-04 | Verificación funcional automatizada insuficiente | 0 suites pytest (G-18); solo scripts manuales (`probar_hu13.py`, `probar_hu151618.py`); sin CI | Alto negativo |

**Usability**

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-USA-01 | Cliente frontend centraliza API y sesión | `lib/api.ts`: timeouts, Bearer token, parseo defensivo, mensajes de error, descarga CSV, tipos TS | Medio positivo |
| F-USA-02 | Feedback de negocio en flujo conversacional | Campos `confianza`, `groundedness`, `pide_aclaracion`, `afirmaciones_bloqueadas`, `fuera_dominio`, `derivacion` | Medio positivo |
| F-USA-03 | Evidencia limitada de accesibilidad/UX validada | Sin reportes WCAG/SUS; P2-17 pendiente | Medio |

**Reliability**

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-REL-01 | Manejo de fallos comunes en consultas | `consulta_controller.py`: `ValueError`→400, timeout/conexión SLM→503, descarte de caché inválida, auditoría de cache-hit | Medio positivo |
| F-REL-02 | Eventos de seguridad sin bloquear flujo | `registrar_evento_seguridad` con `try/except: pass`; registra token inválido, acceso denegado, login fallido/exitoso | Medio (riesgo de pérdida silenciosa) |
| F-REL-03 | Dependencias externas críticas | `docker-compose.yml` (postgres/redis/ollama); pool en arranque; RAG depende de SLM/embeddings | Medio-alto |
| F-REL-04 | Sin evidencia de pruebas de regresión/estabilidad | Ausencia de suites y CI | Alto |

**Performance**

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-PER-01 | Mecanismos de eficiencia presentes | Caché Redis (`RedisAdapter`), pgvector/HNSW, paginación y topes en listados | Medio positivo |
| F-PER-02 | Operaciones potencialmente costosas | Upload/procesamiento (pypdf/PyMuPDF/python-docx, OCR `rapidocr`/`onnxruntime`), embeddings y generación SLM; reproceso síncrono | Medio |
| F-PER-03 | Falta de evidencia de desempeño | Sin benchmarks, p95 ni pruebas de carga; `duracion_ms` existe como base | Medio-alto |

**Supportability**

| ID | Hallazgo | Evidencia | Impacto |
|---|---|---|---|
| F-SUP-01 | Arquitectura modular y mantenible | `domain/application/infrastructure`, contenedor DI, routers separados, puertos/adapters | Alto positivo |
| F-SUP-02 | Evolución de datos controlada | Migraciones `001`–`009` y scripts Supabase | Alto positivo |
| F-SUP-03 | Documentación funcional extensa | `documentacion/` (análisis, ingeniería, gestión, PMV), README operativo | Medio-alto positivo |
| F-SUP-04 | Débil aseguramiento automatizado | Sin `.github/workflows`; `package.json` solo dev/build/start/typecheck | Alto negativo |

#### 7.1.3 Brechas y riesgos

| # | Brecha | Consecuencia |
|---:|---|---|
| 1 | Sin pruebas unitarias/integración/E2E ni CI | Regresiones no detectadas; cambios de alto riesgo |
| 2 | Sin logging estructurado/trazas/alertas transversales | Diagnóstico operativo lento |
| 3 | Sin evidencia WCAG/SUS | Posibles barreras de accesibilidad |
| 4 | Sin SLOs ni pruebas de carga | Capacidad desconocida ante picos |
| 5 | Runbooks operativos por consolidar | Respuesta a incidentes dependiente de conocimiento tácito |

| Riesgo | Severidad | Probabilidad | Descripción |
|---|---|---|---|
| Regresiones en cambios futuros | Alta | Alta | Sin pruebas automatizadas/CI |
| Degradación por dependencias externas | Media-Alta | Media | BD, Redis, Ollama, OCR |
| Pérdida de trazabilidad de seguridad | Media | Media | `except: pass` en auditoría |
| Deuda de rendimiento | Media | Media | OCR/embeddings/SLM sin benchmarks |
| Barreras de accesibilidad | Media | Media | SUS/WCAG no evidenciados |

**Dictamen parcial:** cumplimiento **parcial-alto** para el alcance implementado, con brechas de aseguramiento verificable. Apto para operación controlada y mejora continua; **no acredita** calidad de producción completa.

---

### 7.2 Paso 2. Planificación de mejoras FURPS+

**Prompt aplicado:** Arquitecto de Software Senior; el sistema ya funciona; ninguna propuesta debe arriesgar funcionalidad; compatibilidad, cambios incrementales, riesgo mínimo, validación y rollback; priorizar y generar roadmap (texto completo en [Anexo A.2](#a2-agente-2--planificador-furps)).

**Roadmap:**

| Fase | Horizonte | Objetivo | Resultado esperado |
|---|---|---|---|
| **F0** — Estabilización de aseguramiento | 0–2 semanas | Crear red mínima de seguridad para cambios | Smoke tests + CI + checklist de regresión |
| **F1** — Observabilidad y confiabilidad | 2–4 semanas | Visibilidad operativa y manejo robusto de fallos | Logs/métricas, healthchecks, auditoría robusta |
| **F2** — Rendimiento y UX/accesibilidad | 4–8 semanas | Validar desempeño y experiencia | p95, carga acotada, backlog WCAG |
| **F3** — Consolidación | 8+ semanas | Mejora continua sin regresiones | Cobertura ampliada, SLOs, hardening |

**Mejoras priorizadas:**

| ID | Mejora | Prioridad | Riesgo | Esfuerzo* | Criterio de aceptación (resumen) |
|---|---|---|---:|---:|---|
| M-01 | Suite smoke de endpoints críticos | Crítica | Bajo | 4–5 d | Smoke verde: `/health`, login, consulta, listado de trámites, CRUD documental mínimo |
| M-02 | Pipeline CI mínimo | Crítica | Bajo | 2 d | Workflow en push/PR con typecheck + tests disponibles; check requerido |
| M-03 | Matriz de regresión manual | Alta | Bajo | 2 d | Checklist por release con casos, resultado y responsable |
| M-04 | Logging estructurado + request-id | Alta | Bajo-Medio | 4 d | Logs JSON con correlación en endpoints clave; respuestas API intactas |
| M-05 | Auditoría de seguridad robusta | Alta | Bajo-Medio | 2 d | Fallo de inserción produce warning/métrica; flujo no se bloquea según política |
| M-06 | Readiness/liveness de dependencias | Alta | Medio | 3 d | `/health` intacto + `/ready` verifica BD/Redis/Ollama |
| M-07 | Métricas técnicas (p50/p95, 4xx/5xx) | Media | Medio | 4 d | Métricas expuestas sin impacto funcional |
| M-08 | Pruebas de carga + SLOs | Media | Medio | 5 d | Escenarios concurrentes con baseline documentado |
| M-09 | Backlog UX/accesibilidad | Media | Bajo-Medio | 5 d | Auditoría WCAG AA focalizada + fixes atómicos |
| M-10 | Runbooks operativos | Media | Bajo | 2 d | Procedimientos: caída Ollama/Redis, rotación, restauración BD |

\* Esfuerzo estimado en días-persona; no comprometido, solo orientativo para priorización.

**Estrategia de preservación:** contratos de API sin cambios; adiciones solo aditivas; una mejora por PR; validación antes de fusionar; migraciones hacia adelante; rollback por revert/flag/versión anterior; criterio de parada ante regresión.

---

### 7.3 Paso 3. Aplicación del plan — decisión y justificación

**Decisión: NO APLICAR el plan en esta intervención.**

| Alternativa evaluada | Ventajas | Riesgos | Resultado |
|---|---|---|---|
| **A. Aplicar M-01..M-10 completo** | Cierra brechas de aseguramiento | Alto: sin entorno ni suites, cambios no validados sobre sistema en producción | ❌ Descartada |
| **B. Aplicar solo documentación (M-03, M-10)** | Bajo riesgo | No genera evidencia de ejecución; M-03/M-10 ya tienen base parcial | ⏸️ No aporta valor suficiente |
| **C. Aplicar M-01 en rama aislada** | Primer paso de aseguramiento | Requiere BD de test/fixtures y tiempo; no ejecutable en la sesión | ⏸️ Recomendada como siguiente paso |
| **D. No aplicar y documentar** | Preserva funcionalidad; entrega diagnóstico y plan verificable | No cierra brechas | ✅ **Elegida** |

**Fundamento:**

1. El proyecto ya está **funcional y cerrado al 100 %**; el objetivo es mejorar sin romper.
2. No existen **suites automatizadas ni CI** (G-18) para detectar regresiones.
3. No se dispone de **entorno integrado** (PostgreSQL + Redis + Ollama) para validar flujos.
4. Las mejoras son mayoritariamente **infraestructura de aseguramiento**; aplicarlas a ciegas contradice el principio de evidencia y validación.

**Definición de “listo para reanudar” (Definition of Ready):**

- [ ] Entorno de test reproducible (contenedores + BD semilla).
- [ ] Suite smoke mínima definida (M-01) y ejecutable localmente.
- [ ] CI configurado en rama de trabajo (M-02).
- [ ] Ventana de cambio y plan de rollback acordados.
- [ ] Responsable de validación funcional designado.

---

### 7.4 Paso 4. Auditoría de implementación FURPS+

**Método:** verificación estática de cada mejora contra el repositorio, sin asumir cumplimiento.

| Mejora | Estado | Evidencia actual | Observación |
|---|---|---|---|
| M-01 | **No implementada** | 0 suites formales; `backend/scripts/test_nuevos_endpoints.py` es script manual; sin `tests/`, `pytest.ini`, `tox.ini` | Brecha persiste |
| M-02 | **No implementada** | Sin `.github/workflows/` ni pipeline | Sin validación por commit/PR |
| M-03 | **Parcial** | Documentación operativa/estado en README y rector; sin matriz FURPS con casos/criterios/responsable | Falta el artefacto puntual |
| M-04 | **No implementada** | Sin logging estructurado ni middleware de request-id | Diagnóstico limitado |
| M-05 | **No implementada** | `registrar_evento_seguridad` con `try/except Exception: pass`, sin logging/métrica de fallo | Pérdida silenciosa posible |
| M-06 | **No implementada** | `/health` retorna `{'status':'ok'}` fijo; no verifica dependencias | Healthcheck superficial |
| M-07 | **Parcial** | `duracion_ms` persistido; módulos de métricas/reportes; sin Prometheus/OTel ni SLOs | Métricas de negocio parciales |
| M-08 | **No implementada** | Sin scripts k6/locust/JMeter ni SLO/benchmark | Capacidad no acreditada |
| M-09 | **No implementada** | Sin cambios trazables ni reportes WCAG nuevos | Requiere ciclo UX |
| M-10 | **Parcial** | README, `DESPLEGUE_RENDER.md`, `instalar.ps1`, compose; sin runbooks de incidentes | Documentación de despliegue sí; runbooks de operación por consolidar |

**Resumen cuantitativo:**

| Estado | Mejoras | Total |
|---|---|---:|
| Implementadas | — | **0** |
| Parcialmente implementadas | M-03, M-07, M-10 | **3** |
| No implementadas | M-01, M-02, M-04, M-05, M-06, M-08, M-09 | **7** |

**Regresiones:** no se detectaron regresiones atribuibles a esta intervención (no hubo cambios). No se ejecutaron suites (inexistentes), por lo que no se puede afirmar “pruebas exitosas”.

**Riesgos residuales:**

| Riesgo | Estado | Comentario |
|---|---|---|
| Regresiones no detectadas | Alto | Persiste ausencia de smoke/CI |
| Observabilidad insuficiente | Medio-Alto | Sin logging estructurado ni healthchecks profundos |
| Capacidad no acreditada | Medio | Sin carga ni SLOs |
| Accesibilidad no validada | Medio | Pendiente WCAG/SUS |
| Pérdida de eventos de seguridad | Medio | `except: pass` |

**Conclusión:** cumplimiento del plan FURPS+ **NO CUMPLIDO**. Se recomienda iniciar por **M-01/M-02/M-03** para habilitar un ciclo de mejora seguro.

---

## 8. Fase 2 — Evaluación y mejora de seguridad

### 8.1 Paso 5. Auditoría OWASP Top 10

**Prompt aplicado:** Auditor de Seguridad; analizar frontend, backend, APIs, autenticación, autorización, configuración, dependencias e infraestructura; **no corregir ni modificar**; evaluar A01–A10 con estado, evidencia, impacto, probabilidad, severidad y score global (texto completo en [Anexo A.4](#a4-agente-4--auditor-owasp-top-10)).

#### 8.1.1 Rúbrica de puntuación

Se usó una rúbrica orientativa de **10 puntos por categoría, peso equitativo (10 %)**. El score global es la suma de los puntajes por categoría:

| # | Categoría | Puntaje | Fundamento |
|---|---|---:|---|
| A01 | Broken Access Control | **7/10** | RBAC amplio, pero exposición de trazabilidad por ID y verificación integral pendiente |
| A02 | Cryptographic Failures | **6/10** | PBKDF2 correcto; JWT con fallback de secreto y configuración de ejemplo sin `JWT_SECRET` |
| A03 | Injection | **9/10** | Consultas parametrizadas (`$1..$n`) de forma consistente |
| A04 | Insecure Design | **6/10** | Controles RAG/derivación; sin anti-abuso ni threat modeling |
| A05 | Security Misconfiguration | **5/10** | CORS permisivo, defaults de compose, sin headers de seguridad en app |
| A06 | Vulnerable Components | **5/10** | Versiones pinneadas sin SCA/advisories verificados |
| A07 | Authentication Failures | **7/10** | Login JWT + eventos; sin rate limiting/MFA/revocación formal |
| A08 | Software/Data Integrity | **6/10** | Sin pinning por hash/SBOM; `ollama:latest` |
| A09 | Logging/Monitoring Failures | **7/10** | Auditoría/eventos y métricas; fallo silencioso en registro |
| A10 | SSRF | **8/10** | Sin vector claro de fetch arbitrario; revisión de adapters pendiente |
| | **TOTAL** | **66/100** | `7+6+9+6+5+5+7+6+7+8 = 66` |

> La rúbrica es **cualitativa y orientativa**; no sustituye un SCA/DAST. Se documenta para hacer explícita la relación entre hallazgos y score.

#### 8.1.2 Resultado por categoría

| # | Categoría | Estado | Severidad | Probabilidad | Impacto | Evidencia principal |
|---|---|---|---|---|---|---|
| A01 | Broken Access Control | Parcialmente controlado | Alta | Media | Alto | `main.py` protege routers admin con `Depends(requiere_administrador)`; `dependencias.py` implementa RBAC y eventos. `GET /api/consultas/{id}` es público. |
| A02 | Cryptographic Failures | Parcialmente controlado | Media-Alta | Media | Alto | `PasswordHasher.py`: PBKDF2-HMAC-SHA256, salt, 310k iteraciones, `compare_digest`. `JWTAdapter.py`: HS256, 8 h, secreto o derivación determinista. |
| A03 | Injection | **Controlado** | Media | Baja | Alto | SQL con placeholders asyncpg en `dependencias.py`, `auth_controller.py`, `consulta_controller.py`, `usuario_controller.py`, `documento_controller.py`. |
| A04 | Insecure Design | Parcialmente controlado | Media | Media | Medio | Groundedness/bloqueo, clasificación de dominio y derivación; validación de formatos; topes de listado. Sin rate limiting. |
| A05 | Security Misconfiguration | **Riesgo presente** | Alta | Media | Medio-Alto | CORS: localhost + `VERCEL_FRONTEND_URL`, `allow_credentials=True`, `allow_methods/headers=['*']`; compose expone 5432/6379/11434 con credenciales simples. |
| A06 | Vulnerable Components | No evaluado completamente | Alta (potencial) | Media | Alto | `requirements.txt` pinneado; `next@14.2.5`, `react@^18.3.1`; sin SCA. |
| A07 | Authentication Failures | Parcialmente controlado | Media-Alta | Media | Alto | Login JWT, PBKDF2, usuario activo, eventos; sin rate limiting/MFA/revocación. |
| A08 | Software/Data Integrity | Parcialmente controlado | Media | Baja-Media | Alto | Sin SBOM/firma/pinning por hash; `ollama/ollama:latest`. |
| A09 | Logging/Monitoring Failures | Parcialmente controlado | Media | Media | Medio | `eventos_seguridad`, auditoría y métricas; `registrar_evento_seguridad` silencia fallos. |
| A10 | SSRF | Riesgo bajo / evidencia limitada | Media | Baja | Medio | Integraciones por configuración (`OLLAMA_URL`); sin endpoint de fetch arbitrario identificado; `url_origen` es metadato. |

#### 8.1.3 Hallazgos transversales

1. **Gestión de secretos JWT (A02):** soporta `JWT_SECRET` pero permite derivación/fallback operativo; `.env.example` no lo guía.
2. **Sin anti-abuso visible (A04/A07):** no hay rate limiting en login, consultas o cargas; G-20 pendiente.
3. **CORS amplio (A05):** métodos/cabeceras `*` con credenciales, acotado a orígenes listados.
4. **Componentes sin SCA (A06):** riesgo potencial no cuantificado.
5. **Eventos best-effort (A09):** inserción puede fallar en silencio.
6. **PII (G-03):** manejo pendiente según rector.

**Clasificación:** sin hallazgos **críticos** confirmados por explotación (no hubo pruebas dinámicas); **altos** A01/A02/A05/A06/A07; **medios** A03/A04/A08/A09/A10.

**Score global: 66/100 — cumplimiento parcial.**

---

### 8.2 Paso 6. Planificación de remediación OWASP

**Prompt aplicado:** Arquitecto de Seguridad; no romper funcionalidad ni procesos; compatibilidad hacia atrás; por vulnerabilidad indicar riesgo, prioridad, impacto, componentes, mitigación, validación y rollback; generar roadmap (texto completo en [Anexo A.5](#a5-agente-5--planificador-owasp-top-10)).

**Roadmap:**

| Fase | Horizonte | Foco | Objetivo |
|---|---|---|---|
| **R0** — Acceso y secreto | 0–2 semanas | A01, A02, A07 | Autenticación robusta y RBAC verificable |
| **R1** — Hardening y visibilidad | 2–4 semanas | A05, A09 | Configuración endurecida y trazabilidad garantizada |
| **R2** — Suministro y abuso | 4–6 semanas | A06, A08, A04 | Reducir riesgo de componentes y ataques automatizados |
| **R3** — Verificación continua | 6+ semanas | Todas | SCA/DAST periódico y revisión de diseño |

**Remediaciones priorizadas:**

| ID | Riesgo (OWASP) | Prioridad | Esfuerzo* | Criterio de aceptación (resumen) |
|---|---|---|---:|---|
| R-01 | Secreto JWT débil/derivado (A02) | Crítica | 2 d | Producción exige `JWT_SECRET` fuerte; sin fallback silencioso; `.env.example` y runbook actualizados |
| R-02 | Cobertura RBAC/exposición (A01) | Crítica | 3 d | Matriz endpoint-rol verificada; trazabilidad protegida/anonimizada según política |
| R-03 | Rate limiting / anti-fuerza bruta (A07) | Alta | 3 d | Umbral en login; 429 sin bloquear usuarios legítimos |
| R-04 | Hardening CORS/headers (A05) | Alta | 2 d | Orígenes/métodos/headers mínimos; headers de seguridad en borde |
| R-05 | Monitoreo de eventos (A09) | Alta | 2 d | Fallo de inserción genera warning/métrica/alerta; sin pérdida silenciosa |
| R-06 | SCA de componentes (A06) | Alta | 3 d | `pip-audit`/`npm audit` en CI con política de CVEs |
| R-07 | Integridad de suministro (A08) | Media | 2 d | Tags/digests fijos y SBOM cuando sea viable |
| R-08 | Anti-abuso en endpoints sensibles (A04) | Media | 3 d | Límites por IP/usuario en consultas/uploads; 429 |
| R-09 | Revisión SSRF (A10) | Media | 2 d | Inventario de fetch server-side; allowlist si aplica |
| R-10 | Hardening por entorno (A05) | Media | 2 d | Guía dev/prod, rotación de credenciales y puertos mínimos |

\* Esfuerzo estimado en días-persona; orientativo.

**Estrategia de preservación:** mantener rutas/payloads; controles transparentes; una remediación por PR; smoke de login, consulta, gestión documental, auditoría y reportes; configuración por entorno; rollback documentado.

---

### 8.3 Paso 7. Aplicación del plan — decisión y justificación

**Decisión: NO APLICAR el plan en esta intervención.**

| Factor | Implicación |
|---|---|
| Cambiar `JWT_SECRET`/RBAC/CORS | Puede invalidar sesiones o romper el frontend sin staging |
| Rate limiting | Requiere calibración con tráfico real para no bloquear usuarios |
| Actualización de dependencias | Sin suites de regresión es fuente conocida de rupturas |
| Auditoría/logging | Cambios en flujo crítico sin observabilidad previa |

**Alternativas:** (A) aplicar todo → descartada; (B) solo configuración/documentación → insuficiente; (C) R-01/R-02 en rama aislada con pruebas → **recomendada como siguiente paso**; (D) no aplicar y documentar → **elegida**.

**Definition of Ready para seguridad:** entorno de staging con frontend real, matriz endpoint-rol, smoke de auth/consulta, ventana de rotación y plan de rollback.

---

### 8.4 Paso 8. Auditoría de implementación OWASP

**Método:** contraste estático de R-01..R-10 con código/configuración actual.

| Remediación | Estado | Evidencia actual | Riesgo residual |
|---|---|---|---|
| R-01 | **No corregida** | `JWTAdapter._secreto()` mantiene `JWT_SECRET` o derivación desde claves de entorno; `.env.example` sin `JWT_SECRET` | Alto |
| R-02 | **Parcial** (preexistente) | RBAC en routers admin; `GET /api/consultas/{id}` sin auth; `listar_documentos` público | Alto-Medio |
| R-03 | **No corregida** | Sin middleware/limitador ni contadores de intentos | Alto |
| R-04 | **No corregida** | CORS con `allow_methods/headers=['*']`, credentials; sin headers de seguridad | Medio-Alto |
| R-05 | **No corregida** | `registrar_evento_seguridad` con `except: pass`, sin fallback/alerta | Medio |
| R-06 | **No corregida** | Sin evidencia de `pip-audit`/`npm audit` ni CI de seguridad | Alto (potencial) |
| R-07 | **No corregida** | `ollama:latest`; sin digests/SBOM | Medio |
| R-08 | **No corregida** | Sin rate limiting en consultas/uploads; límites funcionales parciales | Medio |
| R-09 | **No corregida / no aplicable comprobado** | Sin allowlist SSRF; sin vector claro en controladores | Bajo-Medio |
| R-10 | **Parcial** | Guías de despliegue y `.env.example`; sin hardening/rotación específica dev/prod | Medio |

**Resumen cuantitativo:**

| Estado | Remediaciones | Total |
|---|---|---:|
| Corregidas | — | **0** |
| Parcialmente corregidas | R-02, R-10 (por controles/documentación preexistentes) | **2** |
| No corregidas | R-01, R-03, R-04, R-05, R-06, R-07, R-08, R-09 | **8** |

**Nuevas vulnerabilidades/regresiones:** no se identificaron, porque no se aplicaron remediaciones.

**Score actualizado: 66/100** (sin cambios respecto a la auditoría 04).

**Conclusión:** cumplimiento del plan OWASP **NO CUMPLIDO**. Prioridad recomendada: **R-01 y R-02**, seguidos de **R-03/R-04/R-05**.

---

## 9. Fase 3 — Validación integral

**Prompt aplicado:** Auditor Principal de Calidad y Seguridad; evaluar calidad, seguridad, funcionalidad y riesgo operativo; emitir dictamen y recomendación (texto completo en [Anexo A.7](#a7-agente-7--auditor-final-integral)).

### 9.1 Dictamen consolidado

| Dimensión | Resultado | Sustento |
|---|---|---|
| **Calidad (FURPS+)** | **Cumple parcialmente** | 3.5/5.0; fortalezas en F y S; brechas en P, R y verificación automatizada. Plan M-01..M-10 no implementado. |
| **Seguridad (OWASP Top 10)** | **Cumple parcialmente** | 66/100; controles base sólidos; brechas en hardening, anti-abuso, secretos, SCA y monitoreo. Plan R-01..R-10 no implementado. |
| **Funcionalidad** | **Preservada** | Sin cambios de código; sin regresiones atribuibles. |
| **Estabilidad** | **No acreditada en ejecución** | Sin build/despliegue/suites en esta sesión. |
| **Riesgo operativo** | **MEDIO-ALTO (condicionado)** | Brechas de aseguramiento + dependencias externas + hardening pendiente. |

### 9.2 Matriz de riesgos

| Riesgo | Probabilidad | Impacto | Nivel | Mitigación prioritaria |
|---|---|---|---|---|
| Regresiones no detectadas | Alta | Alto | **Crítico (calidad)** | M-01/M-02 |
| Compromiso de sesión por secreto JWT | Media | Alto | **Alto** | R-01 |
| Abuso de login/endpoints (sin rate limit) | Media-Alta | Medio-Alto | **Alto** | R-03/R-08 |
| Exposición de trazabilidad por ID | Media | Medio | **Medio-Alto** | R-02 |
| Pérdida de eventos de seguridad | Media | Medio | **Medio** | R-05 |
| CVE en dependencias | Media | Alto | **Alto (potencial)** | R-06 |
| Degradación por dependencias externas | Media | Medio-Alto | **Medio-Alto** | M-06/M-08 |
| Barreras de accesibilidad | Media | Medio | **Medio** | M-09 |

**Escala:** Probabilidad {Baja, Media, Media-Alta, Alta} × Impacto {Bajo, Medio, Medio-Alto, Alto} → Nivel {Bajo, Medio, Medio-Alto, Alto, Crítico}.

### 9.3 Recomendación final

> **Apto para producción con observaciones** (condicionado a un plan de remediación y aseguramiento inmediato).

**Condiciones mínimas antes de promover cambios o sostener mayor exposición:**

1. **R-01** (gestión explícita y robusta de `JWT_SECRET`) y **R-02** (revisión de autorizaciones/exposición).
2. **R-03** (rate limiting básico) y **R-05** (garantía de alerta/fallback), abordando **G-20**.
3. **M-01/M-02** (smoke tests formales + CI mínimo) para proteger estabilidad (**G-18**).
4. Verificación funcional y no funcional en entorno integrado (flujos críticos, SCA, carga/accesibilidad) con resultados documentados.

**Qué cambiaría el dictamen:**

| Para pasar a “Apto para producción” | Para caer a “No apto” |
|---|---|
| R-01/R-02/R-03/R-05 implementados y verificados + M-01/M-02 verdes + SCA sin CVEs críticos | Aparición de CVE crítico explotable, regresión funcional en flujo crítico o brecha de acceso confirmada |

---

## 10. Criterios de aprobación (evaluación real)

| Criterio | ¿Se cumple? | Evidencia | Qué falta |
|---|---|---|---|
| **Calidad** — mejoras críticas implementadas | ❌ **No** | M-01/M-02 no implementadas; 0/10 mejoras | Ejecutar F0 (M-01..M-03) |
| **Calidad** — sin hallazgos críticos pendientes | ❌ **No** | G-18: 0 suites pytest/CI | Suite + pipeline |
| **Seguridad** — vulnerabilidades críticas mitigadas | ❌ **No acreditado** | R-01/R-02/R-03 pendientes | Aplicar R0 y verificar |
| **Seguridad** — riesgos residuales documentados | ✅ **Sí** | `docs/04` §3–4; `docs/06` §4 | — |
| **Funcionalidad** — sin regresiones | ✅ **Sí (por esta intervención)** | Sin cambios de código; `docs/03`/`docs/06` | Pruebas dinámicas |
| **Funcionalidad** — procesos de negocio funcionan | ✅ **Según código/documentación** | Flujos RAG, catálogo, documentos, auth, auditoría, reportes | Validación en vivo |
| **Estabilidad** — compila | ⚠️ **No verificado** | Sin build en la sesión | Ejecutar build/typecheck |
| **Estabilidad** — despliega | ⚠️ **No verificado** | `docker-compose.yml`/`DESPLEGUE_RENDER.md` presentes | Despliegue en staging |
| **Estabilidad** — pruebas críticas satisfactorias | ❌ **No acreditado** | 0 suites; solo scripts manuales | M-01 + ejecución |

**Resultado de la compuerta de aprobación:** ❌ **NO APROBADA PLENAMENTE** — 4 criterios no cumplidos o no acreditados, 2 no verificados y 3 cumplidos (uno de ellos condicionado a revisión estática).

---

## 11. Resultados esperados (verificación de entrega)

| Resultado esperado | Estado | Archivo |
|---|---|---|
| Diagnóstico de calidad FURPS+ | ✅ | `docs/01_auditoria_furps.md` |
| Plan de mejora de calidad | ✅ | `docs/02_plan_furps.md` |
| Validación de mejoras implementadas | ✅ (verificación: no implementadas) | `docs/03_auditoria_implementacion_furps.md` |
| Diagnóstico de seguridad OWASP Top 10 | ✅ | `docs/04_auditoria_owasp.md` |
| Plan de remediación de vulnerabilidades | ✅ | `docs/05_plan_owasp.md` |
| Validación de remediaciones implementadas | ✅ (verificación: no implementadas) | `docs/06_auditoria_implementacion_owasp.md` |
| Informe final de calidad y seguridad | ✅ | `docs/07_auditoria_final.md` |
| Evidencias verificables para la entrega | ✅ | `docs/EVIDENCIAS_GITHUB.md` |

**Nivel de madurez estimado:**

| Dimensión | Nivel | Justificación |
|---|---:|---|
| Calidad | **3/5 — Definido** | Procesos, arquitectura y documentación definidos; medición y automatización débiles |
| Seguridad | **2.5/5 — Repetible** | Controles base implementados; hardening, SCA y verificación continua en consolidación |

---

## 12. Backlog priorizado con esfuerzo y criterios de aceptación

### 12.1 Calidad (FURPS+)

| Orden | Mejora | Prioridad | Esfuerzo | Dependencias | Criterio de aceptación |
|---:|---|---|---:|---|---|
| 1 | M-01 Smoke tests | Crítica | 4–5 d | BD de test/fixtures | Suite verde en endpoints críticos |
| 2 | M-02 CI mínimo | Crítica | 2 d | M-01, typecheck | Workflow en PR con checks requeridos |
| 3 | M-03 Matriz de regresión | Alta | 2 d | Acceso funcional | Checklist por release firmado |
| 4 | M-04 Logging estructurado | Alta | 4 d | Config logging | Logs JSON + request-id sin cambiar API |
| 5 | M-05 Auditoría robusta | Alta | 2 d | BD `eventos_seguridad` | Fallo registra warning/métrica |
| 6 | M-06 Readiness/liveness | Alta | 3 d | Infra | `/ready` verifica dependencias |
| 7 | M-07 Métricas técnicas | Media | 4 d | M-04 | p50/p95 y tasa 4xx/5xx |
| 8 | M-08 Carga + SLOs | Media | 5 d | Entorno representativo | Baseline documentado |
| 9 | M-09 UX/accesibilidad | Media | 5 d | Revisión UI | WCAG AA focalizada + fixes |
| 10 | M-10 Runbooks | Media | 2 d | Despliegue | Procedimientos de contingencia |

### 12.2 Seguridad (OWASP)

| Orden | Remediación | Prioridad | Esfuerzo | Dependencias | Criterio de aceptación |
|---:|---|---|---:|---|---|
| 1 | R-01 Secreto JWT | Crítica | 2 d | Config prod | Sin fallback silencioso; rotación documentada |
| 2 | R-02 RBAC/exposición | Crítica | 3 d | Matriz endpoint-rol | 401/403/200 esperados por rol |
| 3 | R-03 Rate limiting | Alta | 3 d | Proxy/gateway | 429 calibrado sin bloquear legítimos |
| 4 | R-04 CORS/headers | Alta | 2 d | Dominio frontend | Preflight correcto y orígenes mínimos |
| 5 | R-05 Monitoreo de eventos | Alta | 2 d | Logging | Alerta/fallback ante fallo |
| 6 | R-06 SCA | Alta | 3 d | CI | Política de CVEs aplicada |
| 7 | R-07 Suministro | Media | 2 d | Pipeline | Tags/digests fijos + SBOM |
| 8 | R-08 Anti-abuso | Media | 3 d | R-03 | Límites en consultas/uploads |
| 9 | R-09 SSRF | Media | 2 d | Inventario fetch | Allowlist si aplica |
| 10 | R-10 Hardening por entorno | Media | 2 d | Despliegue | Guía dev/prod y puertos mínimos |

---

## 13. Verificación reproducible (comandos)

Ejecutar desde la raíz del repositorio (PowerShell):

```powershell
# 1) Contexto de versión
git rev-parse --short HEAD
git status --short

# 2) Inventario
(git ls-files '*.py'   | Measure-Object).Count
(git ls-files '*.ts'   | Measure-Object).Count
(git ls-files '*.tsx'  | Measure-Object).Count
(git ls-files '*.sql'  | Measure-Object).Count
(git ls-files '*.md'   | Measure-Object).Count

# 3) Evidencia negativa de CI
Test-Path .github/workflows

# 4) Evidencia de suites formales
Get-ChildItem -Recurse -Include pytest.ini,tox.ini,test_*.py,*_test.py -ErrorAction SilentlyContinue

# 5) SQL parametrizado (esperado: múltiples coincidencias)
Get-ChildItem backend -Recurse -Include *.py | Select-String -Pattern '\$\d'

# 6) Auditoría best-effort (esperado: except/pass en registrar_evento_seguridad)
Get-ChildItem backend -Recurse -Include *.py | Select-String -Pattern 'registrar_evento_seguridad|except Exception'

# 7) CORS (esperado: allow_credentials=True y allow_methods/headers '*')
Select-String -Path backend\main.py -Pattern 'CORSMiddleware|allow_origins|allow_methods|allow_headers|allow_credentials'

# 8) Secreto JWT (esperado: lectura de JWT_SECRET y derivación)
Get-Content backend\infrastructure\adapters\auth\JWTAdapter.py

# 9) Dependencias (esperado: versiones pinneadas)
Get-Content backend\requirements.txt
Get-Content frontend-tramites\package.json

# 10) Migraciones
Get-ChildItem database\migrations -Filter *.sql | Select-Object -ExpandProperty Name
```

**Lectura esperada:** inventario ~104 `.py`, 27 `.ts/.tsx`, 18 `.sql`, 94 `.md`; sin `.github/workflows`; sin suites; SQL parametrizado presente; `except` en auditoría; CORS permisivo; JWT con fallback; dependencias pinneadas; migraciones 001–009.

---

## 14. Evidencias y trazabilidad

### 14.1 Mapa hallazgo → plan → verificación

| Hallazgo / brecha | Plan | Verificación | Resultado |
|---|---|---|---|
| F-FUN-04 / G-18 (sin pruebas/CI) | M-01, M-02, M-03 | `docs/03` | No implementado (M-03 parcial) |
| F-REL-02/03, F-PER-03 (observabilidad/confiabilidad) | M-04, M-05, M-06, M-07, M-08 | `docs/03` | No implementado (M-07 parcial) |
| F-USA-03, operación | M-09, M-10 | `docs/03` | No implementado (M-10 parcial) |
| A02 (secreto JWT) | R-01 | `docs/06` | No corregida |
| A01 (RBAC/exposición) | R-02 | `docs/06` | Parcial (preexistente) |
| A07/A04 (abuso) | R-03, R-08 | `docs/06` | No corregida |
| A05/A09 (config/logging) | R-04, R-05, R-10 | `docs/06` | No corregida (R-10 parcial) |
| A06/A08 (suministro) | R-06, R-07 | `docs/06` | No corregida |
| A10 (SSRF) | R-09 | `docs/06` | No corregida / no aplicable comprobado |

### 14.2 Evidencia primaria por afirmación

| Afirmación | Fuente de evidencia |
|---|---|
| Arquitectura hexagonal | `backend/domain`, `backend/application`, `backend/infrastructure` |
| Auth/RBAC | `backend/infrastructure/controllers/auth_controller.py`, `dependencias.py` |
| Hashing/JWT | `PasswordHasher.py`, `JWTAdapter.py` |
| SQL parametrizado | Controladores con `$1..$n` |
| CORS | `backend/main.py` (`CORSMiddleware`) |
| Dependencias | `backend/requirements.txt`, `frontend-tramites/package.json` |
| Infraestructura | `docker-compose.yml`, `.env.example` |
| Migraciones | `database/migrations/001`–`009` |
| Estado funcional | Rector `06-estado-actual-implementado.md` |
| Ausencia de CI/suites | `.github/`, búsqueda `pytest`/`workflow` |

### 14.3 Evidencias para la entrega

- Guía de capturas: **`docs/EVIDENCIAS_GITHUB.md`** (URLs, qué debe verse, checklist e índice de trazabilidad).
- Repositorio: <https://github.com/JoshuaJBLX/sistemas-tramites-municipales> (`main`, commit `146436c`).
- Para capturas inmutables: usar permalink `/blob/<commit>/...` y registrar el commit en el índice.

---

## 15. Limitaciones, supuestos y observaciones

1. **Sin ejecución dinámica:** no se validó compilación, despliegue, latencia ni comportamiento en vivo; las conclusiones son de revisión estática.
2. **Sin SCA actualizado:** el riesgo de componentes (A06) es potencial y requiere `pip-audit`/`npm audit`.
3. **Doble métrica:** el proyecto está **100 % (101/101)** en avance funcional, mientras que **los planes de esta intervención están 0 % aplicados**. Ambas afirmaciones se documentan por separado.
4. **Inconsistencia documental preexistente:** `README.md` conserva referencias históricas a Junín/MPJ frente a Huancayo/MPH del código; se actualizaron las cifras de estado, no el branding (decisión pendiente del proyecto).
5. **Hallazgos de seguridad potenciales:** la severidad asignada es cualitativa; no sustituye un pentest ni un SCA.
6. **Los documentos 01–07 no son una certificación:** son una línea base de auditoría con evidencia y backlog priorizado.
7. **Reconciliación documental:** el rector 06 presentaba cifras internas inconsistentes (resumen y §10.6 con 94 %/88 % frente a §10.3 con 101/101); se alineó el estado vigente a **100 % (101/101)** y se conservaron las cifras intermedias como historial.

---

## 16. Conclusión

La aplicación de la guía permitió obtener, con evidencia verificable:

- un **diagnóstico de calidad FURPS+ (3.5/5.0)**,
- un **diagnóstico de seguridad OWASP (66/100)**,
- dos **planes incrementales y reversibles** (M-01..M-10 y R-01..R-10),
- dos **verificaciones independientes** que confirman que los planes **no fueron implementados**,
- y un **dictamen final**: *Apto para producción con observaciones*, con riesgo operativo **medio-alto**.

La decisión de **no aplicar cambios** fue deliberada y alineada con los principios de la guía: sin pruebas automatizadas ni entorno de validación, modificar autenticación, CORS, dependencias u observabilidad habría comprometido la preservación de funcionalidad. El resultado es un **plan de mejora listo para ejecutarse de forma controlada**, con criterios de validación y rollback definidos para cada intervención.

**Siguiente paso recomendado:** ejecutar **M-01 + M-02 + M-03** (red de seguridad) y, en paralelo, **R-01 + R-02** (acceso y secreto), en ramas aisladas y con validación funcional antes de fusionar.

---

## Anexo A. Prompts completos de los 7 agentes

> Reproducción fiel de los archivos de instrucciones de la raíz del repositorio. Los nombres de salida originales (`01_Auditoria_FURPS.md`, etc.) se materializaron con la nomenclatura en minúsculas solicitada (`01_auditoria_furps.md`, etc.).

### A.1 Agente 1 — Auditor FURPS+

```text
# Rol
Actúa como Auditor Senior de Calidad de Software especializado en el modelo FURPS+.

# Objetivo
Realizar una auditoría completa del proyecto actual para determinar su nivel de cumplimiento
respecto al modelo FURPS+.

# Alcance
Analiza: código fuente, arquitectura, estructura del proyecto, APIs, base de datos, configuración,
pruebas, documentación, flujos de negocio e interfaces de usuario.

# Restricciones
NO modificar archivos. NO generar código. NO crear planes de implementación.
NO realizar refactorizaciones. NO asumir funcionalidades inexistentes.
Toda conclusión debe estar respaldada por evidencia encontrada en el proyecto.

# Evaluación
Functionality (F): funcionalidades implementadas, parciales, ausentes y cobertura de procesos.
Usability (U): consistencia visual, navegación, accesibilidad, retroalimentación y validaciones.
Reliability (R): manejo de errores, recuperación, robustez, disponibilidad y estabilidad.
Performance (P): tiempo de respuesta potencial, consultas ineficientes, escalabilidad y recursos.
Supportability (S): modularidad, legibilidad, documentación, pruebas y mantenibilidad.

# Formato de salida
Generar 01_Auditoria_FURPS.md con: resumen ejecutivo, puntaje por categoría, hallazgos,
evidencias, brechas identificadas, riesgos detectados y recomendaciones de alto nivel.
```

### A.2 Agente 2 — Planificador FURPS+

```text
# Rol
Actúa como Arquitecto de Software Senior.

# Entrada
01_Auditoria_FURPS.md

# Objetivo
Construir un plan de mejora para cubrir las brechas detectadas.

# Restricción principal
EL SISTEMA YA FUNCIONA. Puede encontrarse desplegado en producción.
NINGUNA propuesta debe poner en riesgo funcionalidades existentes.

# Principios obligatorios
Compatibilidad hacia atrás. Cambios incrementales. Riesgo mínimo.
Validación obligatoria. Posibilidad de rollback.

# Para cada mejora indicar
Objetivo, justificación, prioridad, riesgo, dependencias,
estrategia de validación y estrategia de rollback.

# Priorización
Crítica, Alta, Media, Baja.

# Formato de salida
Generar 02_Plan_FURPS.md con: roadmap, mejoras priorizadas, orden recomendado,
riesgos de ejecución y estrategia de preservación de funcionalidad.
```

### A.3 Agente 3 — Auditor de Implementación FURPS+

```text
# Rol
Actúa como Auditor Independiente.

# Entradas
01_Auditoria_FURPS.md, 02_Plan_FURPS.md y estado actual del proyecto.

# Objetivo
Verificar si el plan fue implementado correctamente.

# Restricciones
NO asumir que una mejora fue aplicada.
Toda afirmación debe basarse en evidencia observable.

# Validaciones
Para cada mejora del plan: Implementada / Parcialmente implementada / No implementada.

# Buscar además
Regresiones funcionales, funcionalidades rotas, errores nuevos, pruebas fallidas e incompatibilidades.

# Formato de salida
Generar 03_Auditoria_Implementacion_FURPS.md con: comparación antes/después,
estado de cada mejora, evidencias, riesgos residuales y conclusión de cumplimiento.
```

### A.4 Agente 4 — Auditor OWASP Top 10

```text
# Rol
Actúa como Auditor de Seguridad especializado en OWASP Top 10.

# Objetivo
Evaluar el proyecto exclusivamente desde la perspectiva de seguridad.

# Alcance
Frontend, backend, APIs, autenticación, autorización, configuración,
dependencias e infraestructura disponible en el repositorio.

# Restricciones
NO corregir. NO modificar. NO generar código. NO implementar controles.

# Evaluar
Broken Access Control, Cryptographic Failures, Injection, Insecure Design,
Security Misconfiguration, Vulnerable Components, Authentication Failures,
Software and Data Integrity Failures, Logging and Monitoring Failures, SSRF.

# Formato de salida
Generar 04_Auditoria_OWASP.md. Para cada categoría indicar:
estado, evidencia, impacto, probabilidad y severidad
(Crítico / Alto / Medio / Bajo). Generar score global de seguridad.
```

### A.5 Agente 5 — Planificador OWASP Top 10

```text
# Rol
Actúa como Arquitecto de Seguridad.

# Entrada
04_Auditoria_OWASP.md

# Objetivo
Construir un plan de remediación de vulnerabilidades.

# Restricción principal
NO romper funcionalidad existente. NO afectar procesos de negocio.
Mantener compatibilidad hacia atrás.

# Para cada vulnerabilidad indicar
Riesgo, prioridad, impacto, componentes afectados,
estrategia de mitigación, estrategia de validación y estrategia de rollback.

# Priorización
Crítico, Alto, Medio, Bajo.

# Formato de salida
Generar 05_Plan_OWASP.md con: roadmap de remediación, orden recomendado,
riesgos de implementación y estrategia para preservar funcionalidad.
```

### A.6 Agente 6 — Auditor de Implementación OWASP

```text
# Rol
Actúa como Auditor Independiente de Seguridad.

# Entradas
04_Auditoria_OWASP.md, 05_Plan_OWASP.md y estado actual del proyecto.

# Objetivo
Verificar si las remediaciones fueron aplicadas correctamente.

# Restricciones
NO asumir que una vulnerabilidad fue corregida.
Toda afirmación debe estar respaldada por evidencia.

# Validar
Para cada vulnerabilidad: Corregida / Parcialmente corregida / No corregida.

# Buscar además
Nuevas vulnerabilidades, controles mal implementados y
regresiones funcionales derivadas de cambios de seguridad.

# Formato de salida
Generar 06_Auditoria_Implementacion_OWASP.md con: estado de cada vulnerabilidad,
evidencias, riesgos residuales, score de seguridad actualizado y conclusión.
```

### A.7 Agente 7 — Auditor Final Integral

```text
# Rol
Actúa como Auditor Principal de Calidad y Seguridad.

# Entradas
03_Auditoria_Implementacion_FURPS.md, 06_Auditoria_Implementacion_OWASP.md
y estado actual del proyecto.

# Objetivo
Emitir el dictamen final del proyecto.

# Evaluar
Calidad: cumple FURPS+ / cumple parcialmente / no cumple.
Seguridad: cumple OWASP Top 10 / cumple parcialmente / no cumple.
Funcionalidad: se preservó la funcionalidad / existen regresiones / riesgos de regresión.
Riesgo operativo: Bajo / Medio / Alto.

# Formato de salida
Generar 07_Auditoria_Final.md con: resumen ejecutivo, estado de calidad,
estado de seguridad, riesgos pendientes, observaciones y recomendación final
(Apto para producción / Apto para producción con observaciones / No apto para producción).
```

---

## Anexo B. Glosario

| Término | Definición |
|---|---|
| **FURPS+** | Modelo de calidad: Functionality, Usability, Reliability, Performance, Supportability y extensiones (“+”). |
| **OWASP Top 10** | Lista de referencia de las diez categorías de riesgo de seguridad de aplicaciones más críticas (edición 2021). |
| **RBAC** | Control de acceso basado en roles (`administrador`, `revisor`, ciudadano). |
| **JWT** | Token firmado para autenticación/sesión (HS256 en este proyecto). |
| **PBKDF2** | Función de derivación de claves usada para almacenar contraseñas con salt e iteraciones. |
| **SCA** | Software Composition Analysis: análisis de dependencias y CVEs. |
| **DAST** | Dynamic Application Security Testing: pruebas de seguridad en ejecución. |
| **SBOM** | Software Bill of Materials: inventario de componentes y versiones. |
| **SLO** | Service Level Objective: objetivo medible de nivel de servicio (p. ej. p95 de latencia). |
| **Smoke test** | Prueba mínima que verifica que los flujos críticos funcionan. |
| **Rollback** | Reversión controlada de un cambio a un estado anterior conocido. |
| **Ground truth / groundedness** | Grado en que una respuesta RAG se sustenta en las fuentes recuperadas. |
| **G-XX / D-XX / HU-XX** | Nomenclatura del proyecto: vacíos, defectos e historias de usuario del rector 06. |
| **M-XX / R-XX** | Mejoras FURPS+ y remediaciones OWASP definidas en esta intervención. |

---

## Anexo C. Referencias

- **FURPS+:** Grady, R. B. (1992). *Practical Software Metrics for Project Management and Process Improvement*; extensión de IBM Rational.
- **OWASP Top 10 (2021):** <https://owasp.org/Top10/>
- **OWASP ASVS:** <https://owasp.org/www-project-application-security-verification-standard/>
- **ISO/IEC 25010:** modelo de calidad de producto de software.
- **Documento rector del proyecto:** `documentacion/00-documentos-rectores/06-estado-actual-implementado.md`.
- **Guía de evidencias:** `docs/EVIDENCIAS_GITHUB.md`.

---

## Anexo D. Control de versiones de este documento

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0 | 2026-11-13 | Registro inicial de la aplicación de la guía (3 fases, 7 entregables). |
| 1.1 | 2026-11-13 | Mejora integral: resumen ejecutivo, rúbricas de puntuación, matriz de riesgos, decisión de no aplicación con alternativas, comandos de verificación, prompts completos, glosario, referencias y trazabilidad ampliada. |
