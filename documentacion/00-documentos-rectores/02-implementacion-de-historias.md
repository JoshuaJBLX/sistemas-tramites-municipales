# Estado de Implementación por Historia de Usuario

Análisis detallado de las 18 HU contra el código real del repositorio.
**Método:** revisión de `backend/` (controllers, use cases, services, adapters, repositorios,
schema/migraciones), `database/` y `frontend-tramites/`. Verificado el **1 de octubre de 2026**
(37 puntos verificados contra el código, 101 en total).

**Leyenda:** ✅ Implementado · ⚠️ Parcial · ❌ No implementado

## Cómo se calcula el % de avance

Cada HU se descompone en puntos de verificación objetivos (sección **Backend**, **Frontend**, **BD**).
El avance de la HU es el porcentaje de esos puntos ya implementados:

```
% avance HU = puntos ✅ / (puntos ✅ + puntos ❌) × 100
% global    = Σ puntos ✅ / Σ puntos totales × 100
```

No es una estimación subjective: cada punto es un archivo o una comprobación concreta, y todos son
verificables con `grep` sobre el repositorio.

## Resumen con porcentaje de avance

| ID | Épica | Estado | ✅/Total | **% avance** |
| -- | ----- | ------ | :------: | :-----------: |
| HU-01 | Gestión documental | ⚠️ Parcial | 4/9 | **44 %** |
| HU-02 | Gestión documental | ⚠️ Parcial | 4/8 | **50 %** |
| HU-03 | Gestión documental | ⚠️ Parcial | 3/7 | **43 %** |
| HU-04 | Procesamiento documental y RAG | ⚠️ Parcial | 4/9 | **44 %** |
| HU-05 | Consulta ciudadana | ⚠️ Parcial | 4/9 | **44 %** |
| HU-06 | Clasificación de intención | ⚠️ Parcial | 2/5 | **40 %** |
| HU-07 | Orientación de requisitos | ⚠️ Parcial | 2/5 | **40 %** |
| HU-08 | Orientación de costos y plazos | ⚠️ Parcial | 2/5 | **40 %** |
| HU-09 | Generación de respuestas con SLM | ⚠️ Parcial | 3/5 | **60 %** |
| HU-10 | Trazabilidad y control de alucinaciones | ⚠️ Parcial | 3/8 | **38 %** |
| HU-11 | Consultas fuera de dominio | ❌ No implementada | 0/3 | **0 %** |
| HU-12 | Recomendación de trámites relacionados | ❌ No implementada | 0/3 | **0 %** |
| HU-13 | Gestión de usuarios y seguridad | ⚠️ Parcial (solo registro) | 2/5 | **40 %** |
| HU-14 | Auditoría | ⚠️ Parcial (solo persistencia) | 2/6 | **33 %** |
| HU-15 | Retroalimentación ciudadana | ❌ No implementada | 0/3 | **0 %** |
| HU-16 | Métricas y monitoreo | ❌ No implementada (solo maqueta) | 0/3 | **0 %** |
| HU-17 | Derivación a atención municipal | ⚠️ Mínima (solo nota) | 2/5 | **40 %** |
| HU-18 | Reportes y exportación | ❌ No implementada | 0/3 | **0 %** |

### Avance global

| Métrica | Valor |
|---|---|
| Puntos de verificación cumplidos | **37 / 101** |
| **Avance total del alcance de las 18 HU** | **37 %** |
| HU al 100 % | **0 de 18** |
| HU implementadas (⚠️ parcial o mejor) | **13 de 18 (72 %)** |
| HU sin implementar (❌) | **5 de 18 (28 %)** — HU-11, HU-12, HU-15, HU-16, HU-18 |
| HU más avançada | **HU-09 · 60 %** (generación de respuestas con SLM) |
| Pruebas automatizadas | **0 suites** (ningún `test_*.py`, `*.test.ts` ni `conftest.py` en el repo) |

> El 37 % mide el **alcance total contratado** de las 18 historias. El **núcleo RAG sí funciona de
> extremo a extremo** (verificado: 22 trámites, 20 documentos indexados, consulta en 5–9 s con 5
> fuentes y caché de ~30 ms). El porcentaje bajo refleja que 5 HU no se empezaron, que ninguna
> llega al 100 % y que el panel de administración es una maqueta con datos inventados.

---

## HU-01 — Carga de documentos oficiales (PDF, TUPA, ordenanzas) ⚠️ Parcial

**Backend**
- [x] Endpoint `POST /api/documentos` registra un documento con `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado` (`backend/infrastructure/controllers/documento_controller.py:44`).
- [x] Al registrar se genera el embedding automáticamente (`GestionarDocumentos.registrar`, `backend/application/use_cases/GestionarDocumentos.py:22`).
- [x] `POST /api/documentos/upload` guarda el archivo original en disco (`documento_controller.py:66`, `DocumentStorageAdapter`).
- [ ] ❌ **Validación de formato PDF/DOCX:** el `upload` acepta cualquier archivo (`.bin` incluido); no restringe extensiones ni valida MIME.
- [ ] ❌ **Extracción de texto del PDF:** el sistema espera el `contenido` como texto ya escrito en el JSON; no lee el contenido del PDF cargado.
- [ ] ❌ **Ingreso de metadatos junto al archivo:** `upload` solo guarda bytes; los metadatos se envían aparte por JSON y no se asocian al archivo.
- [ ] ❌ **Confirmación/firma de calidad:** el registro devuelve la respuesta, pero sin verificación previa del archivo.

**Frontend**
- [x] `DragDropUpload` captura archivos arrastrados/seleccionados (`components/DragDropUpload.tsx`).
- [ ] ❌ No llama a `/api/documentos/upload` ni a `/api/documentos`; solo guarda nombres en estado local (para demostración).

---

## HU-02 — Registro de vigencia, versión y fuente ⚠️ Parcial

**Backend**
- [x] `url_origen` (fuente/URL oficial) es obligatorio en entidad y BD (`Documento.py:16`, `schema.sql:56`).
- [x] Estado de vigencia persistido: `vigente | obsoleto | en_revision` (`DocumentoRepositoryImpl`, `schema.sql:57`).
- [x] `actualizado_en` se registra automáticamente (`NOW()` en upsert).
- [x] La indexación usa solo documentos `vigente` (`BusquedaVectorialAdapter.py:14`, `ServicioRAG.recuperar`).
- [ ] ❌ **Campo `versión`:** no existe columna ni campo `version` en el modelo.
- [ ] ❌ **Campo `fecha` del documento:** solo hay `actualizado_en` (timestamp de sistema); no hay fecha normativa/emisión del documento.
- [ ] ❌ **Validación de metadatos obligatorios:** `DocumentoRequest` exige `titulo`, `contenido`, `url_origen` pero **no** valida fecha/versión; no existe el concepto "publicar" con validaciones (la vigencia se asume por defecto `vigente`, `documento_controller.py:21`).

**BD**
- [ ] ❌ `documentos` carece de columnas `version` y `fecha_emision`. (`database/schema.sql`).

---

## HU-03 — Aprobar, modificar, derogar o desactivar documentos ⚠️ Parcial

**Backend**
- [x] Cambio de estado: `PUT /api/documentos/{id}/estado` (`documento_controller.py:78`).
- [x] Estados disponibles: `vigente`, `obsoleto`, `en_revision` (cubre "vigente", "derogado"≈obsoleto, "en revisión").
- [x] El buscador excluye documentos no vigentes (no se usan en respuestas nuevas) (`BusquedaVectorialAdapter.py:14`).
- [ ] ❌ **Estado "derogado":** no existe literalmente; se usa `obsoleto`.
- [ ] ❌ **Modificación:** no hay endpoint para editar `titulo`/`contenido`/`url` (solo estado); el repo tiene `ON CONFLICT ... DO UPDATE` pero sin ruta HTTP que lo aproveche.
- [ ] ❌ **Flujo de aprobación con revisor/roles:** cualquier llamada cambia el estado; no hay validación de quien actúa.
- [ ] ❌ **Conservar para auditoría:** existe `DELETE /api/documentos/{id}` que **borra físicamente** (no es baja lógica).

---

## HU-04 — Procesamiento documental y RAG ⚠️ Parcial

**Backend**
- [x] Generación de embeddings con BGE-M3 (1024 dim) (`adapters/embeddings/BGE_M3Adapter.py`).
- [x] Índice vectorial **HNSW** pgvector (`schema.sql:79`).
- [x] Búsqueda por similitud de coseno (`BusquedaVectorialAdapter.py:9`) con umbral de similitud (0.3).
- [x] Actualización del índice: upsert de `embedding` al guardar (`DocumentoRepositoryImpl.QUERY_UPSERT`).
- [ ] ❌ **Extracción automática del texto:** no hay parser de PDF/DOCX (el texto debe venir ya en el JSON).
- [ ] ❌ **División en fragmentos (chunking):** se genera **un** vector por documento completo; no existen chunks/bloques.
- [ ] ❌ **Detección de páginas escaneadas / OCR:** no hay ningún módulo OCR ni aviso "requiere revisión manual".
- [ ] ❌ **Procesamiento por lotes / "ejecutar procesamiento":** no hay job/tarea de reprocesamiento.

**Frontend**
- [ ] ❌ No hay pantalla de "procesar documento" ni indicador de estado de indexación real (el ADN admin es mock).

---

## HU-05 — Consulta ciudadana en lenguaje natural ⚠️ Parcial

**Backend**
- [x] `POST /api/consultas` clasifica intención → registra → consulta caché → genera orientación RAG → audita (`consulta_controller.py:41`).
- [x] Devuelve `texto`, `confianza` (alta/media/baja) y `fuentes` (url + fragmento).
- [x] Persistencia de la consulta en `consultas` (`RegistrarConsulta.py`).
- [ ] ❌ **Identificar el "trámite probable":** el flujo no vincula la pregunta con el catálogo `tramites`; no aparece "trámite probable" en la respuesta.
- [ ] ❌ **Consulta ambigua (p. ej. "Necesito un permiso"):** no hay manejo especial tipo "solicitar información adicional"; responde con la respuesta genérica del SLM/`OTRO`.

**Frontend**
- [x] Chat funcional con sugerencias rápidas y burbujas (`components/ChatBox.tsx`, `ChatThread.tsx`).
- [ ] ❌ **No muestra realmente las fuentes ni el groundedness:** el badge marca siempre **90 %** porque el backend nunca envía `groundedness` y el front lo invierte (`lib/api.ts:77`); además el backend devuelve `{url, fragmento}` y el componente lee `f.titulo`, que llega `undefined` (`GroundednessBadge.tsx:15`).
- [ ] ❌ **Riesgo de responder con datos falsos:** el `AbortController` corta a los **6 s** (`lib/api.ts:63`) pero el RAG real tarda **5–9 s**; al agotarse el tiempo salta el `catch` y se muestra `respuestaDemo()`, es decir una respuesta inventada sin avisar al usuario (`lib/api.ts:79-81`).
- [ ] ❌ No muestra un "trámite probable" estructurado ni pide aclaración de forma dirigida.

---

## HU-06 — Clasificación de intención ⚠️ Parcial

**Backend**
- [x] Clasificador léxico con patrones (`ServicioNLP.py`); intenciones: `consultar_requisitos`, `consultar_costo`, `consultar_estado`, `consultar_ubicacion`, `saludo`, `otro`.
- [x] La intención se persiste en `consultas.intencion` y viaja en la respuesta (`consulta_controller.py:27`).
- [ ] ❌ **Categorías "pasos" y "área responsable":** no existen en el enum (`IntencionConsulta.py`).
- [ ] ❌ **Umbral de confianza de clasificación:** el clasificador solo devuelve `OTRO` si no hay match; no calcula confianza ni exige umbral.
- [ ] ❌ **"Solicitar aclaración" ante baja confianza:** no se implementa; responde igual.

---

## HU-07 — Orientación de requisitos ⚠️ Parcial

**Backend**
- [x] El catálogo `tramites` tiene `requisitos TEXT[]` y el endpoint `GET /api/tramites/{id}` lo expone con sus documentos vigentes (`tramite_controller.py:43`).
- [x] El RAG recupera documentos relevantes y el SLM puede listar requisitos citando la fuente (`ServicioRAG.construir_fuentes`).
- [ ] ❌ **Lista ordenada garantizada:** no hay estructura de salida "requisitos" (depende del texto libre del SLM).
- [ ] ❌ **Verificación contra `tramites.requisitos`:** el chat no consulta la tabla de trámites; solo depende del contenido documental.
- [ ] ❌ **Derivación al área responsable** si no se puede confirmar (no implementada; solo nota de baja confianza).

---

## HU-08 — Orientación de costos y plazos ⚠️ Parcial

**Backend**
- [x] BD: `costo NUMERIC` y `duracion_estimada_dias` (`schema.sql:45-46`).
- [x] `GET /api/tramites` y `/{id}` devuelven `costo` y `duracion_estimada_dias` (`tramite_controller.py:12`).
- [ ] ❌ **El chat no usa esos campos:** `ServicioRAG`/`ServicioSLM` solo trabajan con el texto de `documentos`; si el TUPA carece del dato, no hay consulta a `tramites.costo`.
- [ ] ❌ **"No inventar el dato" es solo por prompt** (instrucción al SLM y nota de baja confianza), no una validación de dato.
- [ ] ❌ **Comunicación formal "verifíquese con la municipalidad":** solo existe el texto genérico cuando no hay contexto (`ServicioSLM.generar`).

---

## HU-09 — Generación de respuestas con SLM ⚠️ Parcial

**Backend**
- [x] SLM local vía Ollama (`adapters/slm/OllamaAdapter.py`), temperatura 0.2, respuesta en español, instrucción de usar solo el contexto.
- [x] Abstención si no hay contexto (`ServicioSLM.generar`: "No encontré información oficial...").
- [x] Fuentes citadas y evaluadas (`ServicioRAG`, `EvaluadorGroundedness`).
- [ ] ❌ **Estructura clara garantizada** (trámite, requisitos, pasos, costo, plazo): no hay plantilla de salida.
- [ ] ❌ **Derivar al funcionario:** no existe canal/área de derivación (solo texto genérico).

---

## HU-10 — Trazabilidad y control de alucinaciones ⚠️ Parcial

**Backend**
- [x] Tabla `auditoria_consultas` guarda `respuesta`, `confianza`, `fuentes` (URLs), fecha (`container.py:42`).
- [x] `EvaluadorGroundedness` calcula cobertura léxica con umbrales (alta ≥0.75, media ≥0.40) (`EvaluadorGroundedness.py`).
- [x] Si confianza BAJA con fuentes, se agrega advertencia visible a la respuesta (`ServicioOrientacion.orientar`, línea 28).
- [ ] ❌ **Trazabilidad incompleta en API:** `GET /api/consultas/{id}` devuelve solo `consulta` (pregunta/intención/fecha), **no respuesta, fuentes ni confianza** (`consulta_controller.py:90`).
- [ ] ❌ **Bloqueo de afirmaciones:** el sistema advierte pero no bloquea/elimina afirmaciones no fundamentadas.
- [ ] ❌ **Fuentes detalladas** (número, fecha, versión, artículo, página): la BD solo guarda una cadena de URLs, no el detalle citado.

**Frontend**
- [ ] ❌ **El badge no refleja el dato real:** el componente existe (`components/GroundednessBadge.tsx`) pero muestra un 90 % fijo (el backend no envía `groundedness`, ver HU-05) y no lista los títulos de las fuentes por el desajuste `{url, fragmento}` ↔ `{titulo}`.
- [ ] ❌ No hay vista de auditoría real: `AuditLog` es una lista de filas **hardcodeadas** (`components/AuditLog.tsx:1`).

---

## HU-11 — Consultas fuera de dominio ❌ No implementada

**Backend**
- [ ] ❌ No existe clasificador "ámbito/dominio" (municipal vs. externo).
- [ ] ❌ El enum `IntencionConsulta.OTRO` es genérico; no distingue SUNAT/RENIEC/otros.
- [ ] ❌ No hay respuesta tipo "fuera de mi alcance, acuda a la entidad correspondiente".

---

## HU-12 — Recomendación de trámites relacionados ❌ No implementada

**Backend**
- [ ] ❌ No hay endpoint ni servicio de recomendación/"trámites relacionados".
- [ ] ❌ No hay rúbrica de similitud entre trámites ni marcador "recomendación" (con/sin especulación).

**Frontend**
- [ ] ❌ No se muestran trámites complementarios (compatibilidad de uso, inspección, etc.).

---

## HU-13 — Gestión de usuarios y seguridad ⚠️ Parcial (solo registro)

**Backend**
- [x] Tabla `usuarios` con rol (`ciudadano`/`administrador`) (`schema.sql:30`).
- [x] `POST /api/usuarios` y `GET /api/usuarios/{id}` + historial de consultas (`usuario_controller.py`).
- [ ] ❌ **Inicio de sesión / contraseñas:** no existe (sin password, tokens, JWT, sesiones).
- [ ] ❌ **Roles aplicados al acceso:** ningún endpoint valida el rol; `/api/documentos`, `/api/consultas` son abiertos.
- [ ] ❌ **Registro de eventos de seguridad:** no existe tabla ni servicio de eventos.

---

## HU-14 — Auditoría ⚠️ Parcial (solo persistencia)

**Backend**
- [x] Cada interacción se persiste en `auditoria_consultas` (`AuditarConsulta` + `_AuditoriaPostgreSQL`).
- [x] `GET /api/consultas/{id}` devuelve trazabilidad básica de la consulta.
- [ ] ❌ **Búsqueda por fecha/trámite/usuario:** no hay endpoint de listado/filtro (el único GET es por id).
- [ ] ❌ **Respuesta completa en auditoría:** la API no devuelve respuesta/fuentes/confianza (ver HU-10).
- [ ] ❌ **Marcado de registros inconsistentes** (respuesta sin fuente/evaluación): no se detecta ni marca.

**Frontend**
- [ ] ❌ Panel de auditoría es **mock estático** (`AuditLog.tsx`).

---

## HU-15 — Retroalimentación ciudadana ❌ No implementada

- [ ] ❌ No hay endpoints para calificar (útil / parcialmente útil / no útil).
- [ ] ❌ No hay tabla de calificaciones ni comentarios.
- [ ] ❌ No hay UI de "thumbs/votos" en el chat ni en el panel.

---

## HU-16 — Métricas y monitoreo ❌ No implementada (solo maqueta)

**Backend**
- [ ] ❌ No hay endpoints de métricas (conteos, trámites frecuentes, tiempo de respuesta, satisfacción, groundedness agregado).
- [ ] ❌ No hay alertas por umbral de desempeño.

**Frontend**
- [ ] ❌ Dashboard `/admin`, `KpiCard`, `MiniCharts` son **datos fijos de demostración** (252/1,236/98%, gráficos estáticos) y no consumen ninguna API real (`app/admin/page.tsx:22`).

---

## HU-17 — Derivación a atención municipal ⚠️ Mínima (solo nota)

**Backend**
- [x] El SLM sugiere "acudir a la oficina de trámites" sin contexto (`ServicioSLM.py:21`).
- [x] Nota de advertencia en confianza baja (`ServicioOrientacion.py:28`).
- [ ] ❌ **Umbral de derivación y canal municipal:** no hay lógica que derive con área/telefono/canal correspondiente.
- [ ] ❌ **Casos de decisión formal** (aprobación/denegatoria): no se detectan ni se derivan.
- [ ] ❌ No existe catálogo de áreas de atención (`directorio` en el home es tarjeta mock).

---

## HU-18 — Reportes y exportación ❌ No implementada

- [ ] ❌ No hay generación de reportes por periodo.
- [ ] ❌ No hay exportación a PDF/Excel.
- [ ] ❌ No hay datos reales que reportar (ver HU-16).

---

## Resumen final

| # | HU | Estado | % | Brecha principal |
| -- | --- | ------ | :-: | ---------------- |
| HU-01 | Carga de documentos | ⚠️ | 44 % | Sin validación PDF ni extracción de texto |
| HU-02 | Vigencia/versión/fuente | ⚠️ | 50 % | Sin campos `version`/`fecha` ni validación de metadatos |
| HU-03 | Aprobar/derogar documentos | ⚠️ | 43 % | Sin flujo por roles, sin baja lógica |
| HU-04 | Procesamiento documental y RAG | ⚠️ | 44 % | Sin chunking, sin extracción ni OCR |
| HU-05 | Consulta ciudadana | ⚠️ | 44 % | No identifica "trámite probable", sin manejo de ambigüedad |
| HU-06 | Clasificación de intención | ⚠️ | 40 % | Faltan clases "pasos"/"área" y umbral de confianza |
| HU-07 | Orientación de requisitos | ⚠️ | 40 % | Sin lista estructurada ni derivación |
| HU-08 | Costos y plazos | ⚠️ | 40 % | El chat ignora `costo`/`duracion` del catálogo |
| HU-09 | Respuestas con SLM | ⚠️ | **60 %** | Sin estructura garantizada ni derivación |
| HU-10 | Trazabilidad/anti-alucinación | ⚠️ | 38 % | Trazabilidad API incompleta, sin bloqueo real |
| HU-11 | Consultas fuera de dominio | ❌ | 0 % | Sin clasificador de dominio |
| HU-12 | Trámites relacionados | ❌ | 0 % | Sin motor de recomendaciones |
| HU-13 | Usuarios y seguridad | ⚠️ | 40 % | Solo registro; sin login, roles ni seguridad |
| HU-14 | Auditoría | ⚠️ | 33 % | Solo persistencia; sin búsqueda ni UI real |
| HU-15 | Retroalimentación | ❌ | 0 % | Sin calificaciones ni comentarios |
| HU-16 | Métricas y monitoreo | ❌ | 0 % | Solo maqueta estática |
| HU-17 | Derivación municipal | ⚠️ | 40 % | Solo nota genérica, sin canal/área |
| HU-18 | Reportes y exportación | ❌ | 0 % | No existe |
| | **TOTAL** | | **37 %** | 37 de 101 puntos de verificación |

## Defectos detectados en esta revisión (1 de octubre de 2026)

Estos no estaban en la versión anterior de este documento y son los más graves porque hacen que el
front-end **mienta al usuario**:

| # | Defecto | Ubicación | Impacto |
|---|---------|-----------|---------|
| D-1 | **Tiempo de espera de 6 s menor que el tiempo real del RAG (5–9 s)** | `lib/api.ts:63` | En consultas lentas salta el `catch` y se muestra `respuestaDemo()`: **el usuario lee una respuesta inventada sin aviso** |
| D-2 | **`groundedness` siempre 90 %** | `lib/api.ts:77` | El backend nunca devuelve ese campo; el front lo fija con `?? 0.9` |
| D-3 | **Las fuentes nunca se muestran** | `consulta_controller.py` vs `GroundednessBadge.tsx:15` | El backend devuelve `{url, fragmento}` y el componente lee `f.titulo` (llega `undefined`) |
| D-4 | **El front llama `/api/health`, pero la ruta real es `/health`** | `lib/api.ts:124` vs `main.py:59` | `ServiceStatus` cae siempre en el `catch` y reporta "todo operativo" sin comprobar nada |
| D-5 | **Campos de trámites desalineados** | `tramite_controller.py` vs `lib/api.ts` | Backend `costo`(número)/`duracion_estimada_dias`; front espera `costo`(texto)/`plazo`/`categoria`/`estado` → las tarjetas salen sin chips |
| D-6 | **Datos de demostración presented como reales** | `app/admin/page.tsx:24,38`, `app/page.tsx:46` | "Satisfacción 98 %", "1.180 votos", "v3 · 97 % groundedness" son literales fijos |
| D-7 | **`POST /api/documentos/upload` acepta cualquier archivo** | `documento_controller.py:66` | No valida extensión/MIME, no extrae texto y el parámetro `tramite_id` no se usa |
| D-8 | **`es_administrador()` nunca se invoca** | `domain/entities/Usuario.py:16` | El campo `rol` existe pero no controla ningún acceso |

**Conclusión:** el backend tiene un núcleo RAG sólido y verificado (consulta, búsqueda vectorial,
SLM, groundedness, caché y auditoría en BD) que cubre HU-01 a HU-10 y HU-13/14, pero **ninguna HU
llega al 100 %** y el avance global del alcance contratado es del **37 %**. Lo más urgente no es
añadir funcionalidad nueva, sino **corregir D-1 a D-4**, porque son datos falsos mostrados al
ciudadano en la pantalla principal.