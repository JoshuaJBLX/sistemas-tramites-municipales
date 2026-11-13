# DOCUMENTACIÓN DEL SISTEMA — Orientación de Trámites Municipales
> **Documento relacionado:** [06 · Estado actual implementado](documentacion/00-documentos-rectores/06-estado-actual-implementado.md) — documento rector y fuente única de verdad del estado y las cifras.

Documentación derivada de `a.md`, corregida y contrastada contra el código real, organizada en
**1 carpeta de documentos rectores** (00) y **6 carpetas temáticas** (una por documento académico
del proyecto). Cada carpeta incluye su propio `indice.md` de resumen y contenido breve.

**Entidad del sistema:** Municipalidad Provincial de **Huancayo (MPH)** — TUPA 2023, 252
procedimientos. ⚠️ `a.md` y `README.md` aún
dicen «Municipalidad Provincial de Junín (MPJ)» y el dominio `munijunin.gob.pe`: es una
inconsistencia pendiente de corregir (ver `06-estado-actual-implementado.md` §12.1). El código,
el front-end y los seeds ya usan Huancayo/MPH.

> **★ Documento rector de entrada:** [`documentacion/00-documentos-rectores/06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md)
> consolida este índice: inventaría los `.md` del repositorio, el código archivo por archivo
> (back-end + front-end), los flujos completos de front-end, back-end y base de datos, y el estado
> verificado de las 18 HU y los 3 PMV (**100 %** global — 101/101; PMV1 **100 %**, PMV2 **100 %**,
> PMV3 **100 %**). ✅ **Estado vigente:** los defectos **D-14..D-23** están corregidos (la API
> arranca con 40 rutas, migraciones 004–009 aplicadas, carga de PDF real → 201) y las 18 HU están
> cerradas. Las cifras de los documentos temáticos se reconcilian contra su §10.

## Estructura de la documentación

```
documentacion/
├── 00-documentos-rectores/         # Documentos transversales de raíz
│   ├── indice.md                   # Resumen + índice de contenido breve
│   ├── 01-historias-de-usuario.md  # 18 HU (Given/When/Then) — antes HU.md
│   ├── 02-implementacion-de-historias.md  # Estado por HU — antes IMPLEMENTACION-HU.md
│   ├── 03-ejecucion.md             # Ejecución local: preparación + arranque — antes EJECUCION.md
│   ├── 04-implementado-y-por-implementar.md  # Inventario real ✅/⚠️/❌ y brechas G-XX
│   ├── 05-trazabilidad-por-pmv.md  # Avance por PMV1/PMV2/PMV3
│   ├── 06-estado-actual-implementado.md  # ★ Documento maestro: consolida los 94 .md,
│   │                                   #   inventaría el código archivo por archivo,
│   │                                   #   documenta los flujos front/back/BD y fija el
│   │                                   #   estado real de las 18 HU y los 3 PMV
│   ├── 07-checklist-implementacion.md  # Checklist de verificación de los 3 PMV
│   └── 08-tablero-scrum.md         # Tablero Scrum: backlog, sprints, roles y ceremonias
├── 01-analisis-del-problema/        # Doc. 1 — Diagnóstico del problema (AG-T08)
│   ├── indice.md                    # Resumen + índice de contenido breve
│   └── 01..10                       # 10 numerales: contexto, AS-IS, causas, efectos,
│                                    #   formulación, cuantitativos, restricciones,
│                                    #   búsqueda de información, conclusiones
├── 02-conocimientos-de-ingenieria/  # Doc. 2 — Conocimientos de ingeniería (AG-107)
│   ├── indice.md
│   └── 01..09                       # 9 numerales: HU, RF, fundamentos, computación,
│                                    #   especializados, tecnologías, trazabilidad
├── 03-el-ingeniero-y-la-sociedad/   # Doc. 3 — Impacto y ética (AG-101/AG-102)
│   ├── indice.md
│   └── 01..13                       # 13 numerales: contexto, stakeholders, impactos,
│                                    #   salud/seguridad, marco legal, ética, KPIs
├── 04-gestion-de-proyecto/          # Doc. 4 — Gestión PMI/Scrum
│   ├── indice.md
│   └── 01..10                       # 10 numerales: charter, Scrum, 3 PMV, sprints,
│                                    #   backlog, DoD, desempeño, retrospectiva
├── 05-uso-de-herramientas-modernas/ # Doc. 5 — Herramientas de TI (AG-I11)
│   ├── indice.md
│   └── 01..12                       # 12 numerales: criterios, selección, dev, IA,
│                                    #   calidad, PMV, métricas, trazabilidad AG-I11
└── 06-prueba-de-concepto/           # Doc. 6 — Validación técnica (PoC)
    ├── indice.md
    └── 01..13                       # 13 numerales: hipótesis, corpus, dataset,
                                     #   modelos, experimentos, Go/No-Go, conclusión
```

> Cada carpeta subdivide el documento en un `.md` por numeral (`NN-titulo.md`), manteniendo el
> mismo formato **(A)** a.md / **(B)** implementado / **(C)** vacíos G-XX en todos los archivos.

## Documentos de referencia (raíz)

| Archivo | Contenido |
|---|---|
| `README.md` | Guía de puesta en marcha completa del repositorio |
| `DOCUMENTACION.md` | Índice maestro de toda la documentación |
| `06-estado-actual-implementado.md` | **Documento maestro** que consolida todo lo anterior |

Los documentos transversales (HU, implementación por HU y guía de ejecución) viven ahora en
`documentacion/00-documentos-rectores/`. `a.md` (documento original del proyecto) era la base a
corregir y ya no se mantiene en el repositorio.

## Código de leyenda usado en los documentos

- ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado (vacíos `G-XX`).

## Endpoints de la API (40 rutas servibles)

> ✅ **Estado vigente:** la API **arranca** y todas las rutas son servibles. **40 rutas** =
> 36 operaciones (`/openapi.json`) + 4 de documentación. Los routers de administración están
> protegidos con **JWT/RBAC** (`Depends(requiere_administrador)` / `requiere_revisor`).
> Detalle archivo:línea en `06-estado-actual-implementado.md` §6.2.

| Grupo | Nº | Estado |
|---|---|---|
| Operaciones (`/openapi.json`) | **36** | ✅ servibles; auth/RBAC en rutas admin |
| Documentación (Swagger/ReDoc/OpenAPI) | **4** | ✅ servibles |
| **Total** | **40 rutas** | ✅ **la API arranca** (verificado: `import main` → 40) |

## Defectos bloqueantes (D-14..D-23) — ✅ todos corregidos (16-oct-2026)

> Catálogo con ubicación exacta y evidencia de cierre en `06-estado-actual-implementado.md`
> (§13.1).

| # | Defecto | Estado |
|---|---|---|
| D-14 | La API no arrancaba: `ImportError` de `router` en un stub | ✅ 40 rutas servibles |
| D-15 | Migración `004` sin aplicar y con línea 1 inválida | ✅ `004`/`005` aplicadas (45/45 con metadatos) |
| D-16 | `instalar.ps1` no aplicaba la `004` | ✅ ambas migraciones listadas |
| D-17 | `pypdf`/`python-docx` ausentes de `requirements.txt` | ✅ deps completas (incl. OCR) |
| D-18 | `estado` inválido respondía **500** | ✅ **422** |
| D-19 | La baja física no borraba el archivo en disco | ✅ sin huérfanos |
| D-20 | `response.json()` incondicional en **204** | ✅ manejo del 204 |
| D-21 | Front llamaba a `/api/tramites/admin` inexistente | ✅ panel carga |
| D-22/D-23 | `fragmentado` BOOLEAN / publicar sin metadatos → 500 | ✅ `bool(...)` / 422 |

## Catálogo de vacíos históricos y mejoras de aseguramiento (G-XX)

> ✅ **Estado vigente: 100 % (101/101).** Los vacíos funcionales del alcance comprometido están
> cerrados. La tabla distingue **cerrados** de **mejoras opcionales/hardening** que no bloquean el
> 100 % funcional.

| Código | Estado |
|---|---|
| G-01 | ✅ **Cerrado:** autenticación, contraseñas (PBKDF2), JWT, roles y control de acceso |
| G-02 | 🟡 Mejora opcional: clasificador ML (Random Forest/TF-IDF); el clasificador regex + dominio es funcional |
| G-03 | 🟡 Mejora: enmascaramiento de PII (regex/NLU) en la entrada |
| G-04 | ✅ **Cerrado:** umbral de rechazo por groundedness + clasificador de dominio (HU-08/HU-11) |
| G-05 | ✅ **Cerrado:** retroalimentación ciudadana (útil/no útil) y tabla `evaluaciones_calidad` |
| G-06/G-16 | ✅ **Cerrado:** métricas reales (endpoint de métricas, agregaciones y panel) |
| G-07 | ✅ **Cerrado:** reportes y exportación CSV |
| G-08 | ✅ **Cerrado:** recomendación de trámites relacionados (embedding + fallback léxico + UI) |
| G-09 | ✅ **Cerrado:** derivación a atención municipal (canal/área/teléfono + directorio) |
| G-10 | 🟡 Mejora: UI de historial ciudadano `/mis-consultas` (la API de historial existe) |
| G-11 | ✅ **Cerrado:** rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas `/admin/*` |
| G-12 | ✅ **Cerrado:** carga de documentos conectada al backend (`DocumentManager` sube, lista, aprueba y da de baja); KPIs y gráficos reales |
| G-13 | ✅ **Cerrado:** *chunking* + tabla `fragmentos_documento` con `004` aplicada, OCR y recuperación RAG por fragmento (20/20 documentos) |
| G-14 | ✅ **Cerrado:** consistencia de campos trámite (`mapearTramite`) |
| G-15 | 🟡 Mejora opcional: fine-tuning QLoRA del SLM |
| G-17 | 🟡 Mejora: contenerización frontend/CI, balanceador, HTTPS, monitoreo |
| G-18 | 🟠 **Mejora de aseguramiento:** suite formal pytest/CI (existen scripts de verificación manual) |
| G-20 | 🟠 **Hardening:** guardrails anti prompt-injection |
| G-21 | 🟡 Mejora: resultados del dataset de evaluación (dataset ya versionado) |
| G-23 | 🟠 **Hardening:** rate limiting / protección contra saturación |
| G-24 | 🟡 Mejora: auditoría de manipulación de documentos |
| G-25 | 🟡 Mejora: aviso legal como política de API (ya presente en UI) |
| G-26 | 🟡 Mejora: auditoría WCAG, pruebas de carga (k6/JMeter), SonarQube, ZAP |

## Mapa de consistencia a.md ↔ código (resumen)

| Afirmación en a.md | Estado real |
|---|---|
| Entidad: MPH (Huancayo) | ✅ Corregido en código, frontend y seeds: **MPH – Huancayo**, TUPA 2023 (252 procedimientos); `a.md`/`README.md` conservan la mención histórica Junín/MPJ |
| API `POST /api/v1/consulta` | ✅ Real: `POST /api/consultas` con `{pregunta}` |
| Respuesta con `abstencion`/`groundedness`/`latencia_ms`/`pii_filtrado` | ✅ `confianza`, `groundedness`, fuentes y bloqueo de afirmaciones; PII queda como mejora G-03 |
| Tablas `fragmentos_documentales`, `respuestas`, `evaluaciones_calidad` | ✅ `fragmentos_documento` (45/45, `004` aplicada) y `evaluaciones_calidad` existen y están en uso (HU-15) |
| 7 contenedores + monitoreo | 🟡 3 servicios base (postgres, redis, ollama) + métricas; CI/HTTPS es mejora G-17 |
| Clasificador Random Forest + TF-IDF | ✅ Funcional con regex + clasificador de dominio; ML es mejora opcional G-02 |
| 16 rutas frontend | ✅ 4 páginas principales (`/`, `/chat`, `/tramites`, `/admin`) + subrutas admin/login |
| Paleta azul institucional | ✅ Rediseñada: estilo cálido/orgánico |
| SLM `qwen2.5:3b-instruct-q4_K_M` | ✅ `qwen2.5:3b` (Ollama) |
| Groundedness coseno > 0.82 con rechazo | ✅ Confianza cualitativa + umbral de bloqueo (G-04 cerrado) |
| Pruebas con pytest | 🟡 Scripts de verificación manual; suite formal/CI pendiente (G-18, mejora de aseguramiento) |
