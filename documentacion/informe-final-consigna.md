# Informe Final — Borrador según Consigna de Evaluación

> **Propósito:** este documento sigue la estructura de la consigna de la evaluación final
> (semanas 14–15). Lo que ya existe en el proyecto está **rellenado con datos verificados
> (20-oct-2026)**; lo que aún no existe queda **en blanco con [PENDIENTE]** para que el
> equipo lo complete. Al final se incluye un **resumen general detallado del estado actual
> del sistema**.
>
> Competencias evaluadas: Conocimientos de Ingeniería · El Ingeniero y la Sociedad ·
> Gestión de Proyectos · Análisis de Problemas · Uso de Herramientas Modernas.

---

## Portada

**"MUN AI — Sistema de orientación a trámites municipales empleando RAG y un SLM local
(Qwen 2.5 vía Ollama) sobre el TUPA 2023 de la Municipalidad Provincial de Huancayo"**

[Nombre del autor 1]; [Nombre del autor 2]; [Nombre del autor 3]; [Nombre del autor 4];
[Nombre del autor 5] & [Nombre del autor 6]

1 Escuela Académica Profesional de Ingeniería de Sistemas e Informática, Universidad
Continental, Junín, Perú.

> *Nota: el equipo es de 6 integrantes (roles y responsables por HU en
> `documentacion/00-documentos-rectores/08-tablero-scrum.md`). Completar nombres reales.*

---

## RESUMEN EJECUTIVO (máx. 250 palabras)

El proyecto **"MUN AI"** tuvo como objetivo reducir la desorientación ciudadana y el tiempo
de atención de las consultas sobre trámites municipales de la Municipalidad Provincial de
Huancayo (TUPA 2023, Ordenanza 790-MPH/CM, 252 procedimientos), mediante un asistente
conversacional accesible en lenguaje natural.

Finalmente se logró desarrollar la aplicación web **MUN AI**, compuesta por un back-end
Python (FastAPI, arquitectura hexagonal) y un front-end React 19 + TypeScript (Vite), con
una base de conocimiento de **45 documentos oficiales** fragmentados en **56 segmentos
vectorizados** (embeddings BGE-M3) y un catálogo de **272 trámites** (252 TUPA + 20 de
otros orígenes). La consulta ciudadana usa RAG (búsqueda semántica con similitud coseno,
umbral 0.3) más un modelo de lenguaje pequeño **Qwen 2.5 3B servido localmente con Ollama**,
con trazabilidad de fuentes (HU-10), clasificador de intención (HU-06), identificación de
trámite probable y control de consultas fuera de dominio (HU-11). La API expone **31 rutas**
(18 públicas + 9 de administración + 4 de documentación); el catálogo cubre **259 de 272
trámites con área responsable** para derivación (HU-17, en desarrollo).

El avance global verificado es **83/101 puntos = 82 %** (PMV1 100 %, PMV2 100 %, PMV3 63 %).
Quedan pendientes de PMV3 la autenticación y roles, auditoría por filtros, métricas,
reportes y las suites automatizadas de pruebas (0 suites); la validación SUS con 50
ciudadanos (P2-17) no pudo fabricarse en el entorno académico.

*(~245 palabras)*

---

## 1. ANÁLISIS DE PROBLEMAS

### 1.1 Identificación y formulación del problema

**Problema general:** la desorientación ciudadana y el elevado tiempo de atención de
consultas sobre trámites municipales en la Municipalidad Provincial de Huancayo (MPH).

**Estadísticas de sustento** (detalladas en `documentacion/01-analisis-del-problema/07-analisis-cuantitativo.md`):

| Dimensión | Indicador | Valor | Fuente |
|---|---|---|---|
| Tiempo | Atención promedio de licencia de funcionamiento | 7.9 días hábiles | COMEXPERÚ (2025) |
| Calidad | Expedientes con falta de documentación | 100 % (muestra MPH) | Reyna OC (2024) |
| Productividad | Quejas contra la MPH por demoras (2024) | 54 | Defensoría del Pueblo (2025) |
| Reclamos | Quejas contra municipalidades de Junín | 214 | Defensoría del Pueblo (2025) |
| Gestión | Municipalidades con gestión documental | 2 % | PCM (2025) |
| Accesibilidad | Con Mesa de Partes Digital | 31 % | PCM (2025) |
| Conectividad | Uso de internet móvil en la región | 91 % | PCM (2025) |
| Normativa | TUPA vigente | Ord. 790-MPH/CM (2025) | MPH |

**Problemas específicos (PE1–PE8):** sin canal único y accesible (PE1); documentos con
lenguaje técnico complejo (PE2); sin mecanismo de verificación de respuestas (PE3); el
personal dedica tiempo a consultas básicas (PE4); expedientes incompletos (PE5); sin
trazabilidad de consultas (PE6); sin herramientas de actualización para el funcionario
(PE7); información sin verificación de fuentes (PE8). Correspondencia PE→OE→solución en
`documentacion/01-analisis-del-problema/06-formulacion-del-problema.md`.

### 1.2 OBJETIVOS DEL PROYECTO

**OBJETIVO GENERAL:**
Desarrollar una aplicación web (MUN AI) que permita a los ciudadanos de la provincia de
Huancayo consultar en lenguaje natural los requisitos, costos, plazos y áreas responsables
de los trámites del TUPA 2023, con respuestas trazables a documentos oficiales.

**OBJETIVOS ESPECÍFICOS** (mapeados a problemas PE1–PE8):

| OE | Descripción | Indicador de éxito | Estado (20-oct-2026) |
|---|---|---|---|
| OE1 | Canal web único y accesible en lenguaje natural | Chat respondiendo consultas desde móvil/escritorio | ✅ Implementado (`/chat`) |
| OE2 | Traducir el lenguaje técnico del TUPA a lenguaje ciudadano | % de respuestas con lenguaje comprensible | ✅ Parcial (SLM+RAG; abstención G-04) |
| OE3 | Mecanismo de verificación de respuestas (groundedness) | % de respuestas con fuente citada y puntaje de confianza | ✅ Parcial (HU-10 con fuentes y bloqueo; sin métrica automatizada G-16) |
| OE4 | Automatizar consultas básicas de ventanilla | Reducción de consultas presenciales informativas | ✅ RAG+SLM funcional |
| OE5 | Guía de requisitos completos por trámite | 100 % de trámites del catálogo con requisitos consultables | ✅ Parcial (272 en catálogo; cobertura documental variable) |
| OE6 | Trazabilidad de consultas | Historial consultable por funcionario | ⚠️ Parcial (tabla de auditoría; búsqueda por filtros pendiente HU-14) |
| OE7 | Panel administrativo de actualización | Funcionario carga/baja documentos sin código | ✅ Parcial (gestión documental PMV2; métricas/reportes pendientes) |

> **¿Qué mediría para determinar que el proyecto fue exitoso?** (completar tras las pruebas):
> latencia de respuesta, % de respuestas con fuente correcta, % de abstenciones correctas,
> SUS ≥ 68 con 50 usuarios (P2-17), y reducción de consultas presenciales (requiere
> indicadores municipales, aún no instrumentados — G-16).

---

## 2. CONOCIMIENTOS DE INGENIERÍA APLICADOS / RELACIONADOS

### 2.1 Conocimiento en Matemáticas y computación

| Recurso matemático/computacional | Dónde se aplica |
|---|---|
| **Similitud coseno** entre vectores (espacios de 1024 dimensiones, BGE-M3) | Recuperación RAG: `BusquedaVectorialAdapter` (operador `<=>` de pgvector; fallback Python sin pgvector) |
| **Índice HNSW** (grafo de vecindad aproximado) | Búsqueda eficiente de los 5 fragmentos más similares (migración `003_create_vectors.sql`) |
| **Umbral de similitud 0.3** y márgenes de identificación de trámite (`MARGEN_MINIMO=1.15`, `SOLO_VARIANTE=0.5`, `VOTO_MINIMO_DOC=0.45`) | `IdentificarTramiteProbable` y `ServicioRAG` |
| **Normalización Unicode, tokenización y stopwords en español** | Clasificador de intención y consulta general (`ServicioNLP`) |
| **Atención (attention) de transformers** | Modelo Qwen 2.5 3B vía Ollama (sin entrenamiento local) |
| Conteo/distribución estadística del corpus y del dataset de consultas | Diseño del corpus (45 documentos) y dataset sintético (PoC, §6) |

*Módulo donde se aplica:* back-end `application/services` + `infrastructure/adapters/rag`.

### 2.2 Conocimiento en ciencias naturales

[PENDIENTE — el equipo debe sustentar el principio científico aplicable (p. ej., consumo
energético de cómputo local vs. nube y su huella de carbono, citado como beneficio
ambiental en §3). Redactar con la referencia correspondiente.]

### 2.3 Conocimiento en Ingeniería

| Principio/concepto de ingeniería | Aplicación y módulo |
|---|---|
| **Arquitectura hexagonal (puertos y adaptadores)** | `backend/domain/ports` define interfaces; `infrastructure/adapters` las implementa (SLM, embeddings, RAG, caché, catálogo). Cambiar Ollama/Redis/pgvector no toca el dominio. |
| **APIs REST y diseño de contratos (OpenAPI)** | 31 rutas FastAPI con schemas Pydantic v2; CORS restringido a localhost:3000 |
| **Diseño de BD relacional + extensión vectorial** | PostgreSQL con `text[]`, `numeric`, uuid; columna `embedding` (pgvector o `double precision[]` degradado) |
| **Chunking documental y metadatos de vigencia** | Fragmentación por documento, estado vigente/derogado (migración 004), baja lógica |
| **Control de calidad de IA (groundedness, abstención)** | `EvaluadorGroundedness`, umbral "no inventar" (G-04), bloqueo de afirmaciones sin fuente |
| **Seguridad por diseño (parámetros, minimización de datos)** | Consultas parametrizadas SQLAlchemy, sin PII en el alcance actual |

---

## 3. INGENIERO Y LA SOCIEDAD

### 3.1 Justificación social

El proyecto MUN AI busca mejorar el acceso de los ciudadanos de la provincia de Huancayo a
información sobre trámites municipales mediante un asistente conversacional basado en
inteligencia artificial. La solución permite realizar consultas en lenguaje natural sobre
requisitos, costos, plazos y procedimientos, reduciendo la desorientación, las consultas
repetitivas y la necesidad de acudir presencialmente solo para solicitar información.

Desde el aspecto ético y social, el sistema utiliza RAG, fuentes documentales y evaluación
de groundedness para reducir el riesgo de respuestas incorrectas. Además, las respuestas son
de carácter orientativo y no reemplazan la decisión de un funcionario municipal. El
proyecto debe respetar la Ley N.° 29733 de Protección de Datos Personales y su Reglamento,
así como la Ley N.° 31814 y su Reglamento sobre el uso responsable de la inteligencia
artificial en el Perú. En salud y seguridad, se busca disminuir el estrés y tiempo
asociado a desplazamientos innecesarios. Asimismo, se consideran riesgos como exposición de
datos personales, ataques de prompt injection, respuestas incorrectas e indisponibilidad
del servicio. Actualmente existen medidas como validación de entradas, consultas
parametrizadas y minimización de datos, mientras que mecanismos como enmascaramiento
completo de PII, autenticación avanzada y guardrails aún requieren mayor implementación y
validación (G-01, G-20).

### 3.2 Justificación económica

La solución puede generar beneficios económicos tanto para los ciudadanos como para la
municipalidad. Los usuarios pueden reducir gastos asociados a transporte y tiempo perdido
al realizar consultas informativas de manera remota, mientras que la municipalidad puede
disminuir la carga de atención en ventanilla y aprovechar mejor el tiempo de su personal.

Además, MUN AI utiliza tecnologías de código abierto y servicios locales como Qwen 2.5,
Ollama, BGE-M3, PostgreSQL, pgvector y Redis, reduciendo la dependencia de APIs comerciales
de inteligencia artificial y sus costos por consulta.

Sin embargo, actualmente no se cuenta con una medición formal del ahorro económico
obtenido, por lo que estos beneficios deben considerarse como impactos esperados que
deberán ser evaluados posteriormente mediante indicadores (G-16).

### 3.3 Justificación ambiental

MUN AI contribuye a la sostenibilidad mediante la digitalización de la orientación
ciudadana. El acceso remoto a información puede reducir desplazamientos presenciales
innecesarios y disminuir el uso de documentos impresos durante la etapa de consulta.

La solución también emplea un modelo de lenguaje pequeño ejecutado localmente y embeddings
locales, lo que permite un uso más controlado de los recursos computacionales frente a
soluciones basadas exclusivamente en modelos de gran escala alojados en la nube.

El proyecto se relaciona principalmente con los ODS 11, 12 y 13, vinculados con ciudades
sostenibles, consumo responsable y acción por el clima. No obstante, aún no se dispone de
mediciones formales de reducción de papel, consumo energético o emisiones de CO2, por lo
que estos resultados se plantean como beneficios esperados.

### 3.4 Acontecimientos tecnológicos y científicos que influenciaron la propuesta

El desarrollo de MUN AI fue influenciado principalmente por los avances recientes en
inteligencia artificial generativa y procesamiento de lenguaje natural. La aparición de
modelos de lenguaje pequeños (SLM) capaces de ejecutarse localmente permitió plantear una
solución que no dependa completamente de servicios comerciales en la nube. Por ello, el
proyecto utiliza Qwen 2.5 3B mediante Ollama, permitiendo generar respuestas en lenguaje
natural con mayor control sobre la infraestructura y los datos procesados.

Otro avance determinante fue la consolidación de la técnica Retrieval-Augmented Generation
(RAG). Este enfoque permite complementar al modelo de lenguaje con información recuperada
desde una base documental antes de generar la respuesta. Para MUN AI resulta especialmente
importante porque la información sobre requisitos, costos y plazos debe estar respaldada
por documentos municipales y no únicamente por el conocimiento general del modelo. De esta
manera, RAG influyó directamente en la propuesta como mecanismo para mejorar la
trazabilidad y reducir el riesgo de alucinaciones.

También influyeron los avances en embeddings semánticos y búsqueda vectorial. El modelo
BGE-M3 permite representar consultas y documentos mediante vectores, haciendo posible
encontrar información relacionada por su significado aunque el ciudadano utilice palabras
diferentes a las presentes en los documentos. Estas representaciones se almacenan y
comparan mediante PostgreSQL y pgvector, formando la base de la recuperación semántica del
sistema.

Finalmente, la evolución de herramientas de código abierto para inteligencia artificial,
como Ollama, modelos SLM y bases de datos vectoriales, hizo viable implementar una
arquitectura local, modular y de menor dependencia externa. Estos acontecimientos
tecnológicos y científicos permitieron definir la propuesta actual de MUN AI como una
combinación de SLM + RAG + embeddings + búsqueda vectorial + documentos oficiales,
orientada a proporcionar respuestas municipales más relevantes, verificables y
responsables.

---

## 4. METODOLOGÍA EMPLEADA

Se empleó una metodología **Ágil con tailoring de Scrum**, combinada con elementos de
**gestión de proyectos del PMI (PMBOK)**. A diferencia del ejemplo de la consigna, **sí se
planificaron sprints**: el tablero Scrum completo (4 sprints, 18 HU, roles y ceremonias)
está documentado en `documentacion/00-documentos-rectores/08-tablero-scrum.md`. La
planificación previa se ancló a **hitos H1–H5** (ago–oct 2026) del Project Charter
(`documentacion/04-gestion-de-proyecto/01-project-charter.md`).

El trabajo se realizó mediante:
1. Análisis de requerimientos → entregable: `documentacion/01-*` y `02-*` (RF-01..RF-10, 18 HU, 5 épicas).
2. Elaboración de prototipos → entregable: PMV1 (prototipo funcional, cerrado al 100 %).
3. Implementación de la solución → entregable: PMV2 (RAG optimizado, cerrado al 100 %) y PMV3 (en curso, 63 %).
4. Pruebas de calidad de software → ver §6 (pendiente formalizar suites automatizadas, G-18).

### 4.1 Aportes / Descubrimientos (mínimo 2)

1. **Descubrimiento: el contenido RAG pesa más que el modelo.** La base original (20
   documentos) era insuficiente; al incorporar 25 documentos oficiales adicionales de
   gob.pe (19 MPH + 6 institucionales) y 6 servicios, la cobertura de consultas aumentó de
   forma medible sin cambiar el modelo. Aprendimos que con SLM pequeños, la calidad de la
   respuesta la define la recuperación, no el parámetro de temperatura.
2. **Descubrimiento: un SLM de 3 B ignora instrucciones de formato complejas.** La
   instrucción de "pasos numerados + apartados HU-09" se cumplía de forma irregular; se
   adaptó el pipeline con una etapa determinista de condensado/reordenamiento
   (`ServicioSLM.condensar`) que garantiza límites de longitud y estructura aunque el
   modelo se desvíe, reduciendo la respuesta de ~4156 a ~1400 caracteres sin perder
   apartados.
3. **Descubrimiento (adaptación): enlaces oficiales "fantasma".** Las 20 URLs sembradas
   del dominio `munihuancayo.gob.pe/tupa/*` devolvían 404; se repuntaron a la página
   oficial del TUPA en gob.pe y se añadió verificación HTTP de fuentes como práctica
   obligatoria de carga de contenidos.
4. **Adaptación: pgvector es opcional por diseño.** La arquitectura degrada asimismo a
   similitud coseno en Python, lo que permitió desarrollar y demostrar el RAG completo en
   un entorno sin extensión vectorial, documentando la diferencia de rendimiento.

---

## 5. USO DE HERRAMIENTAS MODERNAS

### 5.1 Diseño de Ingeniería

**Requerimientos funcionales:** RF-01 a RF-10 (búsqueda, ficha, chat RAG, clasificación,
trazabilidad, fuentes, administración de documentos, derivación a área, auditoría,
retroalimentación) — `documentacion/02-conocimientos-de-ingenieria/04-requerimientos-funcionales.md`.

**Requerimientos no funcionales:** [PENDIENTE — no existe listado formal RNF-xx en la
documentación; redactar rendimiento, seguridad, disponibilidad y accesibilidad.]

**Historias de usuario por épicas** (5 épicas, 18 HU — `08-tablero-scrum.md`):
- Épica A — Gestión documental (HU-01, HU-02, HU-03)
- Épica B — Procesamiento documental y RAG (HU-04, HU-08, HU-12)
- Épica C — Consulta ciudadana (HU-05, HU-06, HU-07, HU-09)
- Épica D — Generación de respuestas y control de calidad (HU-10, HU-11, HU-17)
- Épica E — Seguridad, auditoría y monitoreo (HU-13, HU-14, HU-15, HU-16, HU-18)

**Historias de usuario por PMV:**
- PMV1 (100 %): HU-05, HU-06, HU-07, HU-09
- PMV2 (100 %): HU-04, HU-08, HU-10, HU-11, HU-12
- PMV3 (63 %): HU-01, HU-02, HU-03, HU-13, HU-14, HU-15, HU-16, HU-17, HU-18

**Diseño de flujo de navegación:** 4 páginas — `/` (inicio con acceso rápido y estado de
servicios), `/chat` (asistente con hilo de conversación, tarjeta de trámite probable,
groundedness y fuentes), `/tramites` (catálogo con búsqueda), `/admin` (gestión de
documentos con carga drag&drop, procesamiento y panel de auditoría).

**Interfaces implementadas** (16 componentes React: `ChatBox`, `ChatThread`,
`TramiteProbableCard`, `GroundednessBadge`, `TramiteCard`, `DocumentManager`,
`DragDropUpload`, `AuditLog`, `KpiCard`, `MiniCharts`, `Navbar`, `QuickAccessCard`,
`RobotAgent`, `ServiceStatus`, `Loading`, `icons`).

### 5.2 Diseño de base de datos

**Selección:** PostgreSQL (relacional + opcional pgvector); justificación en
`documentacion/05-uso-de-herramientas-modernas/02-seleccion-y-justificacion-de-herramientas.md`.

**Estado actual (verificado 20-oct-2026):** 5 tablas (`municipalidades`, `tramites`,
`documentos`, `fragmentos_documento`, `usuarios`, `consultas` + tablas de migración):
- `tramites`: 272 filas (252 TUPA con costo y área reales + 13 prototipos + 6 servicios MPH + 1 institucional); 259 con `area_responsable`.
- `documentos`: 45 (45/45 con metadatos y embedding; 45/45 fragmentados).
- `fragmentos_documento`: 56 (56/56 con embedding).
- `consultas`: 209 registradas.
- Diseño lógico/físico: `database/schema.sql`, migraciones Alembic `001`–`006`.

### 5.3 Arquitectura de la solución

**Identificación y selección:** arquitectura hexagonal (puertos y adaptadores) sobre
FastAPI; justificación en `documentacion/02-conocimientos-de-ingenieria/08-seleccion-y-justificacion-de-tecnologias.md`.

**Vista de paquetes UML:** [PENDIENTE — elaborar diagrama: `domain` → `application` →
`infrastructure` (adapters: slm, embeddings, rag, cache, documents, extraction, catalog;
controllers FastAPI) + `frontend-tramites`.]

**Vista de despliegue UML:** [PENDIENTE — elaborar diagrama: navegador → frontend Vite
(localhost:3000) → API FastAPI (localhost:8000) → PostgreSQL+pgvector / Redis / Ollama
(qwen2.5:3b + bge-m3) en la misma máquina o docker-compose.]

### 5.4 Gestión del proyecto

**Acta de Constitución (resumen):** existe y está completa en
`documentacion/04-gestion-de-proyecto/01-project-charter.md`: contexto (MPH, TUPA 2023),
entregables (front-end + back-end + BD + IA), fuera de alcance (producción municipal, mesa
de partes, WhatsApp, PII), recursos (6 integrantes, hardware propio, software open source),
hitos H1–H5, 10 riesgos de alto nivel y criterios de aceptación. Tailoring de la
metodología en `03-tailoring-de-scrum.md`; modelo de 3 PMV en `04-modelo-de-tres-pmv.md`;
Product Backlog en `06-product-backlog.md`; Definition of Done en `07-definition-of-done.md`;
registro de decisiones y cambios en `08-cambios-y-decisiones-por-pmv.md`; indicadores de
desempeño en `09-medicion-del-desempeno.md`; retrospectiva en `10-retrospectiva-y-mejora-continua.md`.

**EDT (Estructura de Desglose de Trabajo):** [PENDIENTE — no existe artefacto de EDT;
elaborar WBS por PMV/apartado.]

**Plan de comunicaciones:** [PENDIENTE — no existe artefacto; elaborar matriz de
comunicación (quién, qué, cuándo, canal).]

**Diagrama de Gantt (Línea Base):** [PENDIENTE — elaborar a partir de los hitos H1–H5
del charter y los 4 sprints del tablero Scrum.]

**Diagrama de Gantt (Ejecutado):** [PENDIENTE — elaborar con fechas reales de cierre de
PMV1 (17-oct) y PMV2 (17-oct) y avance de PMV3.]

---

## 6. PRUEBAS Y RESULTADOS y DISCUSIÓN

### 6.1 Prueba de Concepto (PoC)

Documentada en `documentacion/06-prueba-de-concepto/` (14 documentos: identificación,
hipótesis, corpus documental, dataset de consultas sintéticas, selección de modelos,
experimentos, resultados esperados, validación vs. criterios de éxito, limitaciones,
decisión go/no-go, integración PoC→PMV, fórmula práctica y conclusiones).

**Estado de reproducibilidad de la fórmula práctica** (`12-formula-practica.md`):
- ✅ Paso 1 (despliegue del SLM con Ollama), paso 5 (RAG con pgvector/HNSW, top_k=5, umbral 0.3) y paso 6 (SLM + groundedness) son plenamente reproducibles desde el repositorio.
- ⚠️ Paso 3 (extracción/limpieza de PDF): upload funcional (201 con texto extraído), sin pipeline OCR completo (G-12).
- ⚠️ Paso 4 (chunking): embeddings OK; chunking aún manual (G-13).
- ❌ Pasos 2 (dataset sintético versionado) y 7 (evaluación formal): pendientes de artefactos (G-21/G-16).

**Decisión go/no-go:** continuar (el núcleo SLM+RAG+groundedness funciona en local).

### 6.2 Pruebas por PMV

| PMV | Pruebas realizadas | Resultado |
|---|---|---|
| **PMV1** | Arranque de API (31 rutas servibles), CRUD, consulta ciudadana de extremo a extremo, `tsc --noEmit`, `next build`/`vite build` | ✅ Cerrado 100 % (24/24) |
| **PMV2** | Carga de PDF real del TUPA → 201 con texto extraído; panel admin; humo NLP/RAG (10 casos: sentido/sin sentido/consultas generales); identificador de trámite probable (licencia/carnet/habilitación → tarjeta; certificado/horarios → abstención) | ✅ Cerrado 100 % (28/28; solo P2-17 SUS no fabricable) |
| **PMV3** | Parcial: HU-01 y HU-02 al 100 %; verificación de formato de respuesta y enlaces de fuentes (HTTP 200) el 20-oct | ⚠️ 63 % (31/49) |

### 6.3 Resultados estadísticos

- **Latencia:** [PENDIENTE — medir percentiles p50/p95 de `POST /api/consultas`.]
- **Ejecutar en SO/máquina diferente:** [PENDIENTE — el entorno de desarrollo es Windows
  con Python 3.13 y Node 20; falta probar en Linux/contenedor de bajos recursos.]
- **Dataset de evaluación:** 209 consultas reales registradas en la tabla `consultas`
  hasta la fecha; dataset sintético de 200 consultas planificado en la PoC, sin
  versionar aún (G-21).
- **Suites automatizadas:** 0 (pytest ausente — G-18). Las verificaciones actuales son
  humo manuales + typecheck del front-end.

---

## 7. LECCIONES APRENDIDAS (mínimo 3)

1. **Verificar las fuentes con HTTP real antes de sembrar.** 20 URLs oficiales sembradas
   devolvían 404 silenciosamente; el usuario las detectó al hacer clic en "Fuente oficial".
   Lección: la trazabilidad incluye comprobar que el enlace abre, no solo que exista en la BD.
2. **No confiar en el formato libre de un SLM pequeño.** qwen2.5:3b a veces ignora
   instrucciones estructurales; se necesitó un condensador determinista en el backend.
   Lección: en IA aplicada, respaldar la presentación con lógica programática.
3. **La documentación es parte del entregable y se desalinea rápido.** Los conteos de
   trámites/documentos cambiaron en cada iteración (265→272, 20→45); se requirió una
   sincronización manual de ~15 archivos `.md`. Lección: centralizar cifras canónicas y
   verificarlas con scripts antes de cada cierre de PMV.
4. **Un entorno sin las piezas opcionales (Redis, pgvector) no debe bloquear el demo.**
   Diseñar degradación elegante (sin caché, coseno en Python) permitió seguir avanzando.
   Lección: la resiliencia del entorno es un requisito no funcional desde el día 1.

---

## 8. CONCLUSIONES

**Conclusión del objetivo general:** se desarrolló MUN AI como aplicación web funcional
con RAG + SLM local sobre el TUPA 2023 de la MPH; el núcleo consulta→recuperación→
respuesta trazable está operativo en entorno local (82 % del alcance total planificado).

**Conclusión OE1 (canal accesible):** ✅ el chat web funciona con lenguaje natural en
escritorio; falta validación de accesibilidad móvil (G-26).

**Conclusión OE2 (traducción del lenguaje técnico):** ✅ parcial — el SLM traduce
requisitos del TUPA a lenguaje ciudadano, pero la abstención ante consultas ambiguas aún
es conservadora (mejoras recientes del clasificador reducen falsos positivos).

**Conclusión OE3 (verificación):** ✅ parcial — toda respuesta estructurada cita fuentes
con título, fecha y versión, y el usuario puede verificar el enlace; falta la métrica
automatizada de groundedness (G-16).

**Conclusión OE4 (automatización de consultas):** ✅ el sistema responde consultas
informativas de extremo a extremo sin intervención humana (209 consultas registradas).

**Conclusión OE5 (guía de requisitos):** ✅ parcial — 272 trámites en catálogo con
requisitos/costo/plazo; la profundidad documental depende de la cobertura de fuentes.

**Conclusión OE6 (trazabilidad):** ⚠️ existe registro de consultas, pero la búsqueda de
auditoría por filtros y el panel de monitoreo están pendientes (HU-14/HU-16).

**Conclusión OE7 (panel administrativo):** ✅ parcial — el funcionario puede cargar,
procesar y dar de baja documentos con metadatos de vigencia; faltan métricas y reportes
(HU-16/HU-18).

**Aportes:** ver §4.1 (calidad de contenidos RAG, adaptación del SLM, verificación de
enlaces, degradación sin pgvector).

**Limitaciones:** sin autenticación/roles (G-01), sin guardrails avanzados (G-20), sin
suites de pruebas (G-18), sin métricas (G-16), sin despliegue público, sin validación SUS
con usuarios reales (P2-17).

**Trabajo futuro:** cerrar PMV3 (seguridad, auditoría, métricas, reportes), pipeline CI
con pytest, despliegue en contenedor con Ollama, enmascaramiento de PII, integración con
mesa de partes digital y evaluación con 50 ciudadanos.

---

## 9. REFERENCIAS BIBLIOGRÁFICAS (ISO 690-2 numérico)

[PENDIENTE — redactar según ISO 690. Fuentes mínimas a citar: TUPA 2023 (Ord.
790-MPH/CM), Defensoría del Pueblo (2025), COMEXPERÚ (2025), PCM (2025), Ley 29733,
Ley 31814, documentación de Qwen/Ollama, BGE-M3, pgvector, guía PMBOK 7.ª ed., Scrum
Guide 2020. Ver también citas en `documentacion/01-analisis-del-problema/` y
`03-el-ingeniero-y-la-sociedad/`.]

---

## 10. ANEXOS

| Anexo | Estado | Evidencia |
|---|---|---|
| Evidencias de revisión con el experto temático de Ingeniería | [PENDIENTE] | — |
| Evidencias de revisión de usuario | [PENDIENTE] | — |
| Enlace de la presentación (PDF) | [PENDIENTE] | `presentacion/` tiene los guiones por apartado (02-frontend, 04-base-de-datos, 05-implementaciones, etc.) |
| Video demostrativo por PMV (URL + QR, ≤ 20 min) | [PENDIENTE] | PMV1 y PMV2 funcionan en local para grabar |
| **Enlace GitHub del código** | ✅ | https://github.com/JoshuaJBLX/sistemas-tramites-municipales |
| Enlace del chatbot (evidencia tecnologías emergentes) | ⚠️ Local | `http://localhost:3000/chat` (sin despliegue público) |
| Enlace de Machine Learning / IA | ⚠️ Local | Ollama local: `qwen2.5:3b` + embeddings `bge-m3` (sin endpoint público) |
| Otro enlace de evidencias | [PENDIENTE] | — |

---

## ANEXO A — RESUMEN GENERAL DEL ESTADO ACTUAL DEL SISTEMA (20-oct-2026)

> Cifras verificadas en vivo (BD `tramites_municipales`, API en `localhost:8000`,
> repositorio en rama `main`, último commit `5b990ae`).

### A.1 Identidad y alcance

| Concepto | Valor |
|---|---|
| Nombre | MUN AI — Sistema de Trámites Municipales |
| Municipalidad | Municipalidad Provincial de Huancayo (MPH) |
| Norma fuente | TUPA 2023, Ordenanza 790-MPH/CM — 252 procedimientos |
| Alcance | Orientación informativa; NO resolución de trámites, NO PII, NO mesa de partes |
| Repositorio | `github.com/JoshuaJBLX/sistemas-tramites-municipales` — 40 commits, rama `main` |

### A.2 Inventario de código (disco, sin `.venv`/`node_modules`)

| Extensión | Cantidad |
|---|---|
| `.py` (back-end, arquitectura hexagonal) | 91 |
| `.ts`/`.tsx` (front-end) | 25 |
| `.sql` (migraciones + seeds) | 14 |
| `.md` (documentación) | 92 |
| Módulos back-end | 7 controllers, 11 puertos, servicios RAG/SLM/NLP/orientación/groundedness |
| Componentes front-end | 16 |
| Páginas front-end | `/`, `/chat`, `/tramites`, `/admin` |

**Estado Git:** 26 archivos modificados + 3 seeds sin trackear (pendiente de commit:
sincronización de cifras, formato de respuesta del chat, identificador de trámite
probable, semillas de contenidos y corrección de enlaces 404).

### A.3 Base de datos

| Tabla | Filas | Notas |
|---|---|---|
| `municipalidades` | 1 | MPH |
| `tramites` | **272** | 252 TUPA + 13 prototipos + 6 servicios MPH + 1 institucional; **259 con `area_responsable`** (HU-17) |
| `documentos` | **45** | **45/45 con embedding y fragmentados** |
| `fragmentos_documento` | **56** | 56/56 vectorizados (BGE-M3) |
| `consultas` | 209 | historial de consultas ciudadanas |
| `usuarios` | 1 | sin auth/roles aún (G-01) |

### A.4 Motor de IA (RAG + SLM)

| Componente | Estado |
|---|---|
| Embeddings | BGE-M3 local; pgvector con degradación a coseno en Python |
| Recuperación | top_k=5, umbral de similitud 0.3, índice HNSW |
| SLM | Qwen 2.5 3B vía Ollama (local); `num_predict=320` con instrucciones de estructura |
| Clasificador de intención | ServicioNLP: dominio/consulta general/sin sentido |
| Trámite probable | `IdentificarTramiteProbable` (variantes y votos de documento filtrados) |
| Groundedness | Evaluador con fuentes citadas (título, fecha, versión) y bloqueo de afirmaciones sin soporte (HU-10) |
| Formato de respuesta | Pasos numerados + apartados HU-09 compactos, con truncado y "Fuente oficial" (C-06) |
| Contenidos | 45 docs oficiales (20 TUPA + 19 MPH gob.pe + 6 institucionales); enlaces verificados HTTP 200 (C-07) |

### A.5 API (31 rutas: 18 públicas + 9 admin + 4 docs)

`POST /api/consultas` (chat RAG) · `GET /api/tramites` · `GET /api/documentos` ·
`POST /api/documentos/upload` y `/procesar` (PDF→texto→fragmentos→embeddings) ·
`GET /api/admin/documentos` · `PUT /api/documentos/{id}/estado` (baja lógica) ·
auth/usuarios (endpoints CRUD existen; sin validación de rol) · Swagger en `/docs`.

### A.6 Avance por PMV y HU (checklist verificado 17-oct, actualizado 20-oct)

| PMV | Avance | HU | Pendientes |
|---|---|---|---|
| **PMV1 — Prototipo funcional** | **100 %** (24/24) | HU-05, HU-06, HU-07, HU-09 | — |
| **PMV2 — Modelo RAG optimizado** | **100 %** (28/28) | HU-04, HU-08, HU-10, HU-11, HU-12 | Solo P2-17 (validación SUS, no fabricable) |
| **PMV3 — Sistema integrado** | **63 %** (31/49) | HU-01, HU-02, HU-03, HU-13..HU-18 | Auth/roles, auditoría por filtros, métricas, reportes, pruebas, hardening |
| **Global** | **82 %** (83/101) | 18 HU en 5 épicas | 0 suites de pruebas (G-18) |

### A.7 Riesgos/defectos abiertos (principales)

G-01 autenticación y roles · G-16 métricas/monitoreo · G-18 pytest/CI · G-20 guardrails
(prompt injection) · G-21 dataset de evaluación sin versionar · G-23 rate limit ·
G-26 accesibilidad/carga móvil · G-05 retroalimentación 👍/👎 · G-07 reportes ·
G-09 derivación a área (HU-17, parcial con 259 áreas cargadas).

### A.8 Entorno de ejecución

- Windows, Python 3.13 (`.venv`), Node 20, PostgreSQL 16 (pgvector no disponible), Redis no activo, Ollama con `qwen2.5:3b`.
- API: `uvicorn main:app --reload --port 8000` · Front-end: `npm run dev` → `http://localhost:3000`.
- Instalador idempotente: `instalar.ps1` (verifica, migra, siembra, indexa).

---

*Documento generado el 20-oct-2026 a partir del estado verificado del repositorio y la
base de datos. Completar los bloques [PENDIENTE] antes de la sustentación.*
