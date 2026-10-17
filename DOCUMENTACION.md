# DOCUMENTACIÓN DEL SISTEMA — Orientación de Trámites Municipales

Documentación derivada de `a.md`, corregida y contrastada contra el código real, organizada en
**1 carpeta de documentos rectores** (00) y **6 carpetas temáticas** (una por documento académico
del proyecto). Cada carpeta incluye su propio `indice.md` de resumen y contenido breve.

**Entidad del sistema:** Municipalidad Provincial de **Huancayo (MPH)** — TUPA 2023, 252
procedimientos. ⚠️ `a.md` y los documentos de la raíz (`README.md`, `PRESENTACION-PMV1.md`) aún
dicen «Municipalidad Provincial de Junín (MPJ)» y el dominio `munijunin.gob.pe`: es una
inconsistencia pendiente de corregir (ver `06-estado-actual-implementado.md` §12.1). El código,
el front-end y los seeds ya usan Huancayo/MPH.

> **★ Documento rector de entrada:** [`documentacion/00-documentos-rectores/06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md)
> consolida este índice: inventaría los `.md` del repositorio, el código archivo por archivo
> (back-end + front-end), los flujos completos de front-end, back-end y base de datos, y el estado
> verificado de las 18 HU y los 3 PMV (**82 %** global — 83/101; PMV1 **100 %**, PMV2 **100 %**,
> PMV3 **63 %**). ✅ **Actualizado el 17 de octubre de 2026:** los defectos **D-14..D-23** están
> corregidos (la API arranca con 31 rutas, migraciones 004/005/006 aplicadas, carga de PDF real →
> 201) y se cerraron HU-08, HU-10, HU-11 y 2 puntos de HU-14 (umbral "no inventar", trazabilidad
> completa y clasificador de dominio). Las cifras de los documentos temáticos deben reconciliarse
> contra su §10.

**Presentación del PMV1** (para sustentación, en la raíz): [`PRESENTACION-PMV1.md`](PRESENTACION-PMV1.md)
— contiene los ejemplos reales de consulta, el diagrama del flujo y el rendimiento medido.

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
│   └── 06-estado-actual-implementado.md  # ★ Documento maestro: consolida los 90 .md,
│                                       #   inventaría el código archivo por archivo,
│                                       #   documenta los flujos front/back/BD y fija el
│                                       #   estado real de las 18 HU y los 3 PMV
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
| `PMV2_DOCUMENTOS.md` | **Alcance y estado del PMV2 (17-oct-2026):** lo implementado (metadatos, `derogado`, chunking, endpoints admin, `DocumentManager.tsx`), los bloqueos **D-14..D-21** y la ruta de cierre; **PMV2 cerrado al 100 %** |
| `PRESENTACION-PMV1.md` | Guion de sustentación del PMV1 ⚠️ (cifras desactualizadas: ver §12.2 del doc. 06) |
| `06-estado-actual-implementado.md` | **Documento maestro** que consolida todo lo anterior |

Los documentos transversales (HU, implementación por HU y guía de ejecución) viven ahora en
`documentacion/00-documentos-rectores/`. `a.md` (documento original del proyecto) era la base a
corregir y ya no se mantiene en el repositorio.

## Código de leyenda usado en los documentos

- ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado (vacíos `G-XX`).

## Endpoints de la API (31 rutas servibles)

> ✅ **17-oct-2026 (verificación en vivo):** la API **arranca** y todas las rutas son servibles
> (defectos D-14..D-23 corregidos). Detalle archivo:línea de cada una en
> `06-estado-actual-implementado.md` §6.2. Ninguna valida autenticación ni rol (**D-8/G-01**).

| Grupo | Nº | Rutas | Estado |
|---|---|---|---|
| Públicos | **18** | `POST /api/consultas`, `GET /api/consultas`, `GET /api/consultas/{id}`, `GET /api/tramites`, `GET /api/tramites/{id}`, `GET /api/tramites/{id}/relacionados`, `POST /api/documentos`, `POST /api/documentos/upload`, `GET /api/documentos`, `GET /api/documentos/{id}`, `PUT /api/documentos/{id}/estado`, `POST /api/documentos/{id}/procesar`, `DELETE /api/documentos/{id}`, `DELETE /api/documentos/{id}/fisico`, `POST /api/usuarios`, `GET /api/usuarios/{id}`, `GET /api/usuarios/{id}/consultas`, `GET /health` | ✅ servibles |
| Administración | **9** | `GET /api/admin/documentos`, `POST /api/admin/documentos`, `POST /api/admin/documentos/upload`, `POST /api/admin/documentos/{id}/procesar`, `PUT /api/admin/documentos/{id}/estado`, `DELETE /api/admin/documentos/{id}`, `DELETE /api/admin/documentos/{id}/fisico`, `GET /api/tramites/admin`, `PUT /api/tramites/{id}/area` | ✅ servibles; **sin autenticación ni rol** (D-8) |
| **Total** | **31 rutas** | 7 controllers (27 de API + 4 de documentación) | ✅ **la API arranca** (verificado: `import main` → 31) |

## Defectos bloqueantes (D-14..D-23) — ✅ todos corregidos (16-oct-2026)

> Catálogo con ubicación exacta y evidencia de cierre en `06-estado-actual-implementado.md`
> (§13.1) y en [`PMV2_DOCUMENTOS.md`](PMV2_DOCUMENTOS.md).

| # | Defecto | Estado |
|---|---|---|
| D-14 | La API no arrancaba: `ImportError` de `router` en un stub | ✅ 31 rutas servibles |
| D-15 | Migración `004` sin aplicar y con línea 1 inválida | ✅ `004`/`005` aplicadas (20/20 con metadatos) |
| D-16 | `instalar.ps1` no aplicaba la `004` | ✅ ambas migraciones listadas |
| D-17 | `pypdf`/`python-docx` ausentes de `requirements.txt` | ✅ deps completas (incl. OCR) |
| D-18 | `estado` inválido respondía **500** | ✅ **422** |
| D-19 | La baja física no borraba el archivo en disco | ✅ sin huérfanos |
| D-20 | `response.json()` incondicional en **204** | ✅ manejo del 204 |
| D-21 | Front llamaba a `/api/tramites/admin` inexistente | ✅ panel carga |
| D-22/D-23 | `fragmentado` BOOLEAN / publicar sin metadatos → 500 | ✅ `bool(...)` / 422 |

## Catalogo global de vacíos de código (G-XX)

| Código | Vacío |
|---|---|
| G-01 | Autenticación, contraseñas, JWT, roles y control de acceso |
| G-02 | Clasificador de intención por ML (Random Forest/TF-IDF) y métricas F1 |
| G-03 | Enmascaramiento de PII (regex/NLU) en la entrada |
| G-04 | ✅ **Cerrado:** umbral de rechazo por groundedness + clasificador de dominio (HU-08/HU-11, 17-oct-2026) |
| G-05 | Retroalimentación ciudadana (útil/no útil) y tabla `evaluaciones_calidad` |
| G-06/G-16 | Métricas reales (endpoint de métricas, agregaciones) — hoy maqueta |
| G-07 | Reportes y exportación |
| G-08 | ✅ **Cerrado:** recomendación de trámites relacionados (embedding + fallback léxico + UI, 16-oct-2026) |
| G-09 | Derivación a atención municipal (backend) |
| G-10 | UI de historial ciudadano `/mis-consultas` (solo API) |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas `/admin/*` |
| G-12 | ✅ **Cerrado:** carga de documentos conectada al backend (`DocumentManager.tsx` sube, lista, aprueba y da de baja de verdad); siguen ficticios los KPIs y gráficos de `/admin` (D-6) |
| G-13 | ✅ **Cerrado:** *chunking* + tabla `fragmentos_documento` con `004` aplicada, OCR y recuperación RAG por fragmento (20/20 documentos, 16-oct-2026) |
| G-14 | Consistencia campos trámite `tipo`/`duracion_estimada_dias` vs frontend `categoria`/`plazo` |
| G-15 | Fine-tuning QLoRA del SLM |
| G-17 | Contenerización frontend/backend, balanceador, HTTPS, monitoreo |
| G-18 | Suite de pruebas automatizadas (pytest) — **0 suites hoy** |
| G-20 | Guardrails anti prompt-injection |
| G-21 | Artefactos de PoC (dataset sintético, resultados de experimentos) |
| G-23 | Rate limiting / protección contra saturación |
| G-24 | Auditoría de manipulación de documentos |
| G-25 | Aviso legal como política de API (solo en UI) |
| G-26 | Auditoría WCAG, pruebas de carga (k6/JMeter), SonarQube, ZAP |

## Mapa de consistencia a.md ↔ código (resumen)

| Afirmación en a.md | Estado real |
|---|---|
| Entidad: MPH (Huancayo) | ⚠️ Corregido: MPJ – Junín, TUPA 2023 (252 procedimientos) |
| API `POST /api/v1/consulta` | ✅ Real: `POST /api/consultas` con `{pregunta}` |
| Respuesta con `abstencion`/`groundedness`/`latencia_ms`/`pii_filtrado` | ⚠️ Solo `confianza` (alta/media/baja) |
| Tablas `fragmentos_documentales`, `respuestas`, `evaluaciones_calidad` | ✅ `fragmentos_documento` existe y está poblada (20/20, `004` aplicada); `evaluaciones_calidad` sigue sin existir |
| 7 contenedores + monitoreo | ⚠️ 3 servicios (postgres, redis, ollama) |
| Clasificador Random Forest + TF-IDF | ❌ Regex (`ServicioNLP.py`) |
| 16 rutas frontend | ⚠️ 4 rutas (`/`, `/chat`, `/tramites`, `/admin`) |
| Paleta azul institucional | ⚠️ Rediseñada: estilo cálido/orgánico |
| SLM `qwen2.5:3b-instruct-q4_K_M` | ⚠️ `qwen2.5:3b` (Ollama) |
| Groundedness coseno > 0.82 con rechazo | ⚠️ Confianza cualitativa sin rechazo |
| Pruebas con pytest | ❌ Sin suite: **0 suites de pruebas** (G-18) |
