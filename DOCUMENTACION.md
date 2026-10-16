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
> consolida este índice: inventaría los 90 `.md` del repositorio, el código archivo por archivo
> (back-end + front-end), los flujos completos de front-end, back-end y base de datos, y el estado
> verificado de las 18 HU y los 3 PMV (**59 %** global — 60/101; PMV1 **88 %**, PMV2 **56 %**,
> PMV3 **52 %**). ⚠️ **Actualizado el 16 de octubre de 2026 (HEAD `ea06c9a`):** el código del PMV2
> está escrito pero **la API no arranca** (defectos **D-14..D-21**, ver
> [`PMV2_DOCUMENTOS.md`](PMV2_DOCUMENTOS.md)). Las cifras de este índice y de los documentos
> temáticos deben reconciliarse contra su §10.

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
| `PMV2_DOCUMENTOS.md` | **Alcance y estado del PMV2 (16-oct-2026):** lo implementado (metadatos, `derogado`, chunking, 6 endpoints admin, `DocumentManager.tsx`), los bloqueos **D-14..D-21** y la ruta de cierre |
| `PRESENTACION-PMV1.md` | Guion de sustentación del PMV1 ⚠️ (cifras desactualizadas: ver §12.2 del doc. 06) |
| `06-estado-actual-implementado.md` | **Documento maestro** que consolida todo lo anterior |

Los documentos transversales (HU, implementación por HU y guía de ejecución) viven ahora en
`documentacion/00-documentos-rectores/`. `a.md` (documento original del proyecto) era la base a
corregir y ya no se mantiene en el repositorio.

## Código de leyenda usado en los documentos

- ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado (vacíos `G-XX`).

## Endpoints de la API (22: 16 públicos + 6 admin)

> ⚠️ **16-oct-2026:** son **22 endpoints declarados** (el recuento anterior era de 13 rutas), pero
> **hoy 0 son servibles** porque `main.py` aborta con `ImportError` (**D-14**). Detalle archivo:línea de cada
> uno en `06-estado-actual-implementado.md` §6.2.

| Grupo | Nº | Rutas | Estado |
|---|---|---|---|
| Públicos | **16** | `POST /api/consultas`, `GET /api/consultas/{id}`, `GET /api/tramites`, `GET /api/tramites/{id}`, `POST /api/documentos`, `POST /api/documentos/upload`, `GET /api/documentos`, `GET /api/documentos/{id}`, `PUT /api/documentos/{id}/estado`, `POST /api/documentos/{id}/procesar`, `DELETE /api/documentos/{id}`, `DELETE /api/documentos/{id}/fisico`, `POST /api/usuarios`, `GET /api/usuarios/{id}`, `GET /api/usuarios/{id}/consultas`, `GET /health` | ⚠️ **0 servibles** (D-14) |
| Administración | **6** | `GET /api/admin/documentos`, `POST /api/admin/documentos`, `POST /api/admin/documentos/upload`, `POST /api/admin/documentos/{id}/procesar`, `DELETE /api/admin/documentos/{id}`, `DELETE /api/admin/documentos/{id}/fisico` | ⚠️ **0 servibles** (D-14); además **sin autenticación ni rol** (D-8) |
| **Total** | **22** | 6 controllers (1 es stub: `tramite_admin_controller`) | **0 servibles** hasta cerrar D-14 |

## Defectos bloqueantes (D-14..D-21 — revisión del PMV2, 16-oct-2026)

> Catálogo ampliado, ubicación exacta y ruta de cierre en `06-estado-actual-implementado.md`
> (§13.1) y en [`PMV2_DOCUMENTOS.md`](PMV2_DOCUMENTOS.md).

| # | Defecto | Impacto |
|---|---|---|
| D-14 | La API no arranca: `main.py:21` importa `router` de `tramite_admin_controller` (stub de 91 bytes sin `router`) → `ImportError` | 🔴 **0 de los 22 endpoints son servibles** |
| D-15 | Migración `004_documentos_pmv2.sql` sin aplicar y con línea 1 inválida (docstring Python en vez de comentario SQL) | 🔴 Sin los 7 metadatos, sin `fragmentos_documento`, sin `derogado` en el `CHECK` |
| D-16 | `instalar.ps1` no aplica la migración `004` | 🟠 Instalación limpia ≠ base preparada para PMV2 |
| D-17 | `pypdf`/`python-docx` ausentes de `requirements.txt` | 🟠 Extracción de PDF/DOCX → 422 |
| D-18 | `estado` inválido en el listado admin responde **500** en vez de **422** | 🟡 Error genérico |
| D-19 | La baja física no borra el archivo en disco | 🟡 Archivos huérfanos en `storage/documentos` |
| D-20 | `pedir()` hace `response.json()` incondicional pero los `DELETE` devuelven **204 sin cuerpo** | 🔴 Baja lógica/física fallan desde la UI |
| D-21 | El front llama a `GET /api/tramites/admin` (inexistente) dentro de `Promise.all` | 🔴 El panel `DocumentManager.tsx` no carga |

## Catalogo global de vacíos de código (G-XX)

| Código | Vacío |
|---|---|
| G-01 | Autenticación, contraseñas, JWT, roles y control de acceso |
| G-02 | Clasificador de intención por ML (Random Forest/TF-IDF) y métricas F1 |
| G-03 | Enmascaramiento de PII (regex/NLU) en la entrada |
| G-04 | Abstención / umbral de groundedness con rechazo / fuera de dominio |
| G-05 | Retroalimentación ciudadana (útil/no útil) y tabla `evaluaciones_calidad` |
| G-06/G-16 | Métricas reales (endpoint de métricas, agregaciones) — hoy maqueta |
| G-07 | Reportes y exportación |
| G-08 | Recomendación de trámites relacionados |
| G-09 | Derivación a atención municipal (backend) |
| G-10 | UI de historial ciudadano `/mis-consultas` (solo API) |
| G-11 | Rutas `/login`, `/tramites/[id]`, `/404`, sub-rutas `/admin/*` |
| G-12 | ⚠️ **Parcial:** carga de documentos conectada al backend (`DocumentManager.tsx` en `/admin` sube, lista y da de baja de verdad); siguen ficticios los KPIs y gráficos de `/admin` |
| G-13 | ⚠️ **Parcial:** *chunking* (`ServicioChunking`) y tabla `fragmentos_documento` escritos (PMV2), pero **la migración 004 no está aplicada** (D-15) y faltan OCR y recuperación RAG por fragmento |
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
| Tablas `fragmentos_documentales`, `respuestas`, `evaluaciones_calidad` | ⚠️ Existe `fragmentos_documento` (PMV2) pero su migración `004` **no está aplicada** (D-15); `evaluaciones_calidad` sigue sin existir |
| 7 contenedores + monitoreo | ⚠️ 3 servicios (postgres, redis, ollama) |
| Clasificador Random Forest + TF-IDF | ❌ Regex (`ServicioNLP.py`) |
| 16 rutas frontend | ⚠️ 4 rutas (`/`, `/chat`, `/tramites`, `/admin`) |
| Paleta azul institucional | ⚠️ Rediseñada: estilo cálido/orgánico |
| SLM `qwen2.5:3b-instruct-q4_K_M` | ⚠️ `qwen2.5:3b` (Ollama) |
| Groundedness coseno > 0.82 con rechazo | ⚠️ Confianza cualitativa sin rechazo |
| Pruebas con pytest | ❌ Sin suite: **0 suites de pruebas** (G-18) |
