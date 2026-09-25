# DOCUMENTACIÓN DEL SISTEMA — Orientación de Trámites Municipales

Documentación derivada de `a.md`, corregida y contrastada contra el código real, organizada en
**1 carpeta de documentos rectores** (00) y **6 carpetas temáticas** (una por documento académico
del proyecto). Cada carpeta incluye su propio `indice.md` de resumen y contenido breve.

**Entidad del sistema:** Municipalidad Provincial de **Junín (MPJ)** — TUPA 2023, 252
procedimientos. `a.md` estaba redactado para Huancayo (MPH); todas las referencias se corrigen.

## Estructura de la documentación

```
documentacion/
├── 00-documentos-rectores/         # Documentos transversales de raíz
│   ├── indice.md                   # Resumen + índice de contenido breve
│   ├── 01-historias-de-usuario.md  # 18 HU (Given/When/Then) — antes HU.md
│   ├── 02-implementacion-de-historias.md  # Estado por HU — antes IMPLEMENTACION-HU.md
│   └── 03-ejecucion.md             # Guía de ejecución resumida — antes EJECUCION.md
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

Los documentos transversales (HU, implementación por HU y guía de ejecución) viven ahora en
`documentacion/00-documentos-rectores/`. `a.md` (documento original del proyecto) era la base a
corregir y ya no se mantiene en el repositorio.

## Código de leyenda usado en los documentos

- ✅ implementado · ⚠️ parcial/maqueta · ❌ no implementado (vacíos `G-XX`).

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
| G-12 | Carga de documentos conectada al backend (maqueta) |
| G-13 | Chunking documental, campos `version`/`fecha_publicacion`/página |
| G-14 | Consistencia campos trámite `tipo`/`duracion_estimada_dias` vs frontend `categoria`/`plazo` |
| G-15 | Fine-tuning QLoRA del SLM |
| G-17 | Contenerización frontend/backend, balanceador, HTTPS, monitoreo |
| G-18 | Suite de pruebas automatizadas (pytest) |
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
| Tablas `fragmentos_documentales`, `respuestas`, `evaluaciones_calidad` | ❌ No existen |
| 7 contenedores + monitoreo | ⚠️ 3 servicios (postgres, redis, ollama) |
| Clasificador Random Forest + TF-IDF | ❌ Regex (`ServicioNLP.py`) |
| 16 rutas frontend | ⚠️ 4 rutas (`/`, `/chat`, `/tramites`, `/admin`) |
| Paleta azul institucional | ⚠️ Rediseñada: estilo cálido/orgánico |
| SLM `qwen2.5:3b-instruct-q4_K_M` | ⚠️ `qwen2.5:3b` (Ollama) |
| Groundedness coseno > 0.82 con rechazo | ⚠️ Confianza cualitativa sin rechazo |
| Pruebas con pytest | ❌ Sin suite (pytest ausente) |