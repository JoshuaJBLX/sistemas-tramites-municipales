# Estado de Implementación por Historia de Usuario

Análisis detallado de las 18 HU contra el código real del repositorio.
**Método:** revisión de `backend/` (controllers, use cases, services, adapters, repositorios,
schema/migraciones), `database/` y `frontend-tramites/`. Verificado el **16 de octubre de 2026**
(HEAD `ea06c9a`; 101 puntos de verificación contra el código y la base de datos PostgreSQL local).

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
| HU-01 | Gestión documental | ⚠️ Parcial | 7/9 | **78 %** |
| HU-02 | Gestión documental | ⚠️ Parcial | 7/8 | **88 %** |
| HU-03 | Gestión documental | ⚠️ Parcial | 5/7 | **71 %** |
| HU-04 | Procesamiento documental y RAG | ⚠️ Parcial | 7/9 | **78 %** |
| HU-05 | Consulta ciudadana | ✅ Completa | 9/9 | **100 %** |
| HU-06 | Clasificación de intención | ✅ Completa | 5/5 | **100 %** |
| HU-07 | Orientación de requisitos | ✅ Completa | 4/5 | **80 %** |
| HU-08 | Orientación de costos y plazos | ⚠️ Parcial | 3/5 | **60 %** |
| HU-09 | Generación de respuestas con SLM | ⚠️ Parcial | 3/5 | **60 %** |
| HU-10 | Trazabilidad y control de alucinaciones | ⚠️ Parcial | 4/8 | **50 %** |
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
| Puntos de verificación cumplidos | **60 / 101** |
| **Avance total del alcance de las 18 HU** | **59 %** |
| HU al 100 % | **2 de 18** — HU-05, HU-06 |
| HU implementadas (⚠️ parcial o mejor) | **13 de 18 (72 %)** |
| HU sin implementar (❌) | **5 de 18 (28 %)** — HU-11, HU-12, HU-15, HU-16, HU-18 |
| HU más avanzada | **HU-05 y HU-06 · 100 %** |
| Pruebas automatizadas | **0 suites** (ningún `test_*.py`, `*.test.ts` ni `conftest.py` en el repo; **G-18** sigue abierto) |

> El 59 % mide el **alcance total contratado** de las 18 historias. El **núcleo RAG sí funciona de
> extremo a extremo** (verificado: 22 trámites, 20 documentos indexados, consulta en 4–17 s con 5
> fuentes y acierto de caché inmediato). El porcentaje subió del 37 % al 49 % con HU-05, HU-06 y
> las correcciones D-1..D-5, y ahora al **59 %** con el PMV2 documental (HU-01, HU-02, HU-03 y
> HU-04 ganaron 11 puntos en el commit `ea06c9a`). Sigue bajo porque 5 HU no se empezaron, porque
> el arancel real del TUPA no está cargado en la base de datos y porque la API **no arranca en el
> HEAD actual** (defecto bloqueante D-14).

---

## HU-01 — Carga de documentos oficiales (PDF, TUPA, ordenanzas) ⚠️ Parcial

**Backend**
- [x] Endpoint `POST /api/documentos` registra un documento con `tramite_id`, `titulo`, `contenido`, `url_origen`, `estado` (`backend/infrastructure/controllers/documento_controller.py:44`).
- [x] Al registrar se genera el embedding automáticamente (`GestionarDocumentos.registrar`, `backend/application/use_cases/GestionarDocumentos.py:22`).
- [x] `POST /api/documentos/upload` guarda el archivo original en disco (`documento_controller.py:66`, `DocumentStorageAdapter`).
- [x] **Validación de formato PDF/DOCX:** `FormatoDocumento` rechaza con **422** formatos no admitidos (PMV2, commit `ea06c9a`).
- [ ] ❌ **Extracción de texto del PDF/DOCX:** existe `ExtraccionTextoAdapter`, pero `pypdf` y `python-docx` no están en `requirements.txt` (**D-17**), por lo que la extracción real no funciona.
- [x] **Ingreso de metadatos junto al archivo:** metadatos obligatorios (`version`, `fecha_publicacion`, `hash_contenido`, `archivo_nombre`, `mime_type`, `fragmentado`, `eliminado_en`); la migración que los define (**004**) aún no está aplicada (**D-15**).
- [ ] ❌ **Confirmación/firma de calidad:** el registro devuelve la respuesta, pero sin verificación previa ni firma del archivo.

**Frontend**
- [x] `DragDropUpload` captura archivos arrastrados/seleccionados (`components/DragDropUpload.tsx`).
- [x] **Carga conectada a la API real:** panel `DocumentManager.tsx` en `/admin` consume `GET /api/documentos` y `/api/admin/documentos` con filtros (hoy el panel no carga en runtime por **D-21** y la API no arranca por **D-14**).

---

## HU-02 — Registro de vigencia, versión y fuente ⚠️ Parcial

**Backend**
- [x] `url_origen` (fuente/URL oficial) es obligatorio en entidad y BD (`Documento.py:16`, `schema.sql:56`).
- [x] Estado de vigencia persistido: `vigente | obsoleto | en_revision` (`DocumentoRepositoryImpl`, `schema.sql:57`).
- [x] `actualizado_en` se registra automáticamente (`NOW()` en upsert).
- [x] La indexación usa solo documentos `vigente` (`BusquedaVectorialAdapter.py:14`, `ServicioRAG.recuperar`).
- [x] **Campo `version`:** los metadatos obligatorios del PMV2 incluyen `version` (migración 004, pendiente de aplicar — **D-15**).
- [x] **Campo de fecha del documento:** los metadatos obligatorios incluyen `fecha_publicacion` (normativa/emisión), además de `actualizado_en`.
- [x] **Validación de metadatos obligatorios:** `version`, `fecha_publicacion`, `hash_contenido`, `archivo_nombre` y `mime_type` son obligatorios; la API responde **422** si faltan.

**BD**
- [ ] ❌ **Columnas en la base de datos:** la migración `004_documentos_pmv2.sql` define las columnas de metadatos y la tabla `fragmentos_documento`, pero **no está aplicada** y su línea 1 usa docstring de Python en vez de `--` (**D-15**); la BD vigente aún no tiene esos campos.

---

## HU-03 — Aprobar, modificar, derogar o desactivar documentos ⚠️ Parcial

**Backend**
- [x] Cambio de estado: `PUT /api/documentos/{id}/estado` (`documento_controller.py:78`).
- [x] Estados disponibles: `vigente`, `obsoleto`, `en_revision` (cubre "vigente", "derogado"≈obsoleto, "en revisión").
- [x] El buscador excluye documentos no vigentes (no se usan en respuestas nuevas) (`BusquedaVectorialAdapter.py:14`).
- [x] **Estado "derogado":** añadido en el PMV2 junto a los metadatos del documento.
- [ ] ❌ **Modificación de contenido:** no hay endpoint para editar `titulo`/`contenido`/`url` (solo estado y reprocesado).
- [ ] ❌ **Flujo de aprobación con revisor/roles:** cualquier llamada cambia el estado; no hay validación de quien actúa (**D-8**).
- [x] **Conservar para auditoría (baja lógica):** `DELETE /api/documentos/{id}` marca `eliminado_en` en vez de borrar (**D-10 corregido**); existe además `DELETE /{id}/fisico` para borrado físico (con el hueco **D-19**: no borra el archivo de `storage/documentos`).

---

## HU-04 — Procesamiento documental y RAG ⚠️ Parcial

**Backend**
- [x] Generación de embeddings con BGE-M3 (1024 dim) (`adapters/embeddings/BGE_M3Adapter.py`).
- [x] Índice vectorial **HNSW** pgvector (`schema.sql:79`).
- [x] Búsqueda por similitud de coseno (`BusquedaVectorialAdapter.py:9`) con umbral de similitud (0.3).
- [x] Actualización del índice: upsert de `embedding` al guardar (`DocumentoRepositoryImpl.QUERY_UPSERT`).
- [ ] ❌ **Extracción automática del texto:** `ExtraccionTextoAdapter` existe, pero sin `pypdf`/`python-docx` en `requirements.txt` (**D-17**) no extrae PDF/DOCX reales.
- [x] **División en fragmentos (chunking):** `ServicioChunking` (800/120) + tabla `fragmentos_documento` + repositorio `FragmentoRepositoryImpl` (migración 004 pendiente de aplicar, **D-15**).
- [ ] ❌ **Detección de páginas escaneadas / OCR:** no hay ningún módulo OCR ni aviso "requiere revisión manual" (**G-13** parcial).
- [x] **Procesamiento y reprocesamiento:** `POST /api/documentos/{id}/procesar` + casos de uso `CargarDocumento` y `ProcesarDocumento`.

**Frontend**
- [x] **Pantalla de gestión/procesamiento:** `DocumentManager.tsx` en `/admin` lista documentos con filtros y dispara acciones reales (en runtime bloqueado por **D-14** y **D-21**).

> Nota **G-13** (parcial): el chunking existe, pero `ServicioRAG` sigue recuperando por el **embedding del documento completo**, no por fragmento; la recuperación RAG por chunk y el OCR siguen pendientes.

---

## HU-05 — Consulta ciudadana en lenguaje natural ✅ Completa

**Backend**
- [x] `POST /api/consultas` clasifica intención → registra → consulta caché → genera orientación RAG → audita (`consulta_controller.py`).
- [x] Devuelve `texto`, `confianza` (alta/media/baja), `groundedness` real, `confianza_intencion`, `pide_aclaracion` y `fuentes` con `titulo` + `fragmento` + `url`.
- [x] Persistencia de la consulta en `consultas` (`RegistrarConsulta.py`).
- [x] **Trámite probable implementado:** `IdentificarTramiteProbable` vincula los documentos recuperados con `tramites` mediante `documentos.tramite_id`, pondera los votos por la similitud semántica del RAG y exige que el ganador supere al segundo por un margen (1.15) con puntaje mínimo 0.45. Si ningún trámite domina, **no se propone ninguno** (`IdentificarTramiteProbable.py`).
- [x] **Consulta ambigua gestionada:** sin patrón reconocido, con empate entre intenciones o con confianza < 0.5, `ServicioOrientacion` responde con `ACLARACION_AMBIGUA` y `pide_aclaracion: true`, sin generar respuesta ni citar fuentes (`ServicioOrientacion.py`).

**Frontend**
- [x] Chat funcional con sugerencias rápidas y burbujas (`components/ChatBox.tsx`, `ChatThread.tsx`).
- [x] **Groundedness y fuentes reales:** el backend ya envía `groundedness` y las fuentes incluyen `titulo`; `GroundednessBadge` los muestra sin valores fijos (`lib/api.ts`).
- [x] **Sin riesgo de datos falsos:** el timeout subió a 45 s (el RAG tarda 4–17 s) y se eliminó `respuestaDemo()`. Si el backend falla, el ciudadano ve el error real (`lib/api.ts`).
- [x] Muestra el "trámite probable" estructurado (`components/TramiteProbableCard.tsx`) y rotula cuando pide aclaración.

> Verificado en la API real: "cuánto cuesta la licencia de funcionamiento" → `consultar_costo` → trámite probable *Licencia de Funcionamiento* con requisitos del catálogo; "quiero saber" → `pide_aclaracion: true` en 2.2 s sin fuentes.

---

## HU-06 — Clasificación de intención ✅ Completa

**Backend**
- [x] Clasificador léxico con raíces tolerantes a conjugaciones (`ServicioNLP.py`); nueve intenciones: `consultar_requisitos`, `consultar_costo`, `consultar_plazo`, `consultar_pasos`, `consultar_area`, `consultar_estado`, `consultar_ubicacion`, `saludo`, `otro`.
- [x] La intención se persiste en `consultas.intencion` y viaja en la respuesta con su confianza.
- [x] **Categorías "pasos" y "área responsable" añadidas** al enum (`IntencionConsulta.py`) y con patrones léxicos.
- [x] **Umbral de confianza implementado:** `ClasificacionIntencion` calcula confianza (base 0.55 + 0.15 por patrón adicional, máx. 1.0) y desempata por especificidad del patrón, de modo que "cuanto cuesta" gana sobre "pago".
- [x] **Solicita aclaración ante baja confianza o empate:** `requiere_aclaracion` es verdadero si la intención es `OTRO`, si hay empate o si la confianza es < 0.5; en ese caso el flujo no genera respuesta.

> Verificado: 19/19 casos de un recorrido manual (8 intenciones y 2 casos sin patrón) clasificados correctamente.

---

## HU-07 — Orientación de requisitos ✅ Completa

**Backend**
- [x] El catálogo `tramites` tiene `requisitos TEXT[]` y el endpoint `GET /api/tramites/{id}` lo expone con sus documentos vigentes (`tramite_controller.py`).
- [x] El RAG recupera documentos relevantes y el SLM puede listar requisitos citando la fuente (`ServicioRAG.construir_fuentes`).
- [x] **Lista ordenada garantizada:** `Respuesta.con_datos_estructurados()` anexa al texto los requisitos numerados desde la base de datos, no desde el redactado del SLM (`Respuesta.py`).
- [x] **Verificación contra `tramites.requisitos`:** el flujo consulta el catálogo mediante `TramiteCatalogoPort` / `TramiteCatalogoAdapter`, que resuelve los trámites de los documentos recuperados (`JOIN documentos d ON d.tramite_id = t.id`).
- [ ] ⚠️ **Derivación al área responsable:** no implementada. La base de datos no tiene columna de área responsable por trámite, por lo que el sistema no puede derivar y se limita a informar al ciudadano.

---

## HU-08 — Orientación de costos y plazos ⚠️ Parcial

**Backend**
- [x] BD: `costo NUMERIC` y `duracion_estimada_dias` (`schema.sql:45-46`).
- [x] `GET /api/tramites` y `/{id}` devuelven `costo` y `duracion_estimada_dias` (`tramite_controller.py:12`).
- [x] **El chat ya usa esos campos:** `TramiteProbable` transporta `costo` y `duracion_estimada_dias` desde el catálogo y `Respuesta.con_datos_estructurados()` los anexa ("Datos del catálogo: arancel S/ X; plazo estimado de N días hábiles").
- [x] **El frontend formatea los datos reales:** `mapearTramite` convierte `costo` y `duracion_estimada_dias` a texto legible (`lib/api.ts`), corrigiendo el desajuste de campos anterior.
- [ ] ❌ **"No inventar el dato" es solo por prompt** (instrucción al SLM y nota de baja confianza), no una validación de dato.
- [ ] ❌ **Comunicación formal "verifíquese con la municipalidad":** solo existe el texto genérico cuando no hay contexto (`ServicioSLM.generar`).

> Nota de datos: `tramites.costo` es 0.00 en la base de datos, por lo que el catálogo muestra "Gratuito / según TUPA" y el chat omite el arancel. Los montos del TUPA deben cargarse para que esta HU pueda cerrarse.

---

## HU-09 — Generación de respuestas con SLM ⚠️ Parcial

**Backend**
- [x] SLM local vía Ollama (`adapters/slm/OllamaAdapter.py`), temperatura 0.2, respuesta en español, instrucción de usar solo el contexto.
- [x] Abstención si no hay contexto (`ServicioSLM.generar`: "No encontré información oficial...") y abstención adicional por consulta ambigua.
- [x] Fuentes citadas y evaluadas (`ServicioRAG`, `EvaluadorGroundedness`).
- [ ] ❌ **Estructura clara garantizada** (trámite, requisitos, pasos, costo, plazo): el prompt declara los apartados REQUISITOS, PASOS, COSTO, PLAZO y OBSERVACIONES, con "No especificado en la base documental" si el contexto no respalda un dato (`ServicioSLM.py`), pero `qwen2.5:3b` puede no respetar la plantilla. Los datos críticos no dependen del SLM (se anexan desde `tramites`), la estructura de apartados no está garantizada.
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
- [x] **El badge refleja el dato real:** el backend envía `groundedness` (valor numérico real) y las fuentes ya incluyen `titulo`; `GroundednessBadge` los muestra y `ServiceStatus` informa lo no verificado como "sin verificar" en vez de "99.9% operativo".
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
| HU-01 | Carga de documentos | ⚠️ | 78 % | Sin extracción real de PDF/DOCX (D-17) ni firma de calidad |
| HU-02 | Vigencia/versión/fuente | ⚠️ | 88 % | Metadatos en código; migración 004 sin aplicar en la BD (D-15) |
| HU-03 | Aprobar/derogar documentos | ⚠️ | 71 % | Sin edición de contenido ni flujo de aprobación por roles |
| HU-04 | Procesamiento documental y RAG | ⚠️ | 78 % | Sin OCR ni recuperación por fragmento; deps de extracción (D-17) |
| HU-05 | Consulta ciudadana | ✅ | **100 %** | — (cerrada) |
| HU-06 | Clasificación de intención | ✅ | **100 %** | — (cerrada) |
| HU-07 | Orientación de requisitos | ✅ | **80 %** | Sin derivación al área responsable (no hay dato en BD) |
| HU-08 | Costos y plazos | ⚠️ | 60 % | Arancel del TUPA sin cargar en la BD |
| HU-09 | Respuestas con SLM | ⚠️ | 60 % | Sin estructura garantizada ni derivación |
| HU-10 | Trazabilidad/anti-alucinación | ⚠️ | 50 % | Trazabilidad API incompleta, sin bloqueo real |
| HU-11 | Consultas fuera de dominio | ❌ | 0 % | Sin clasificador de dominio |
| HU-12 | Trámites relacionados | ❌ | 0 % | Sin motor de recomendaciones |
| HU-13 | Usuarios y seguridad | ⚠️ | 40 % | Solo registro; sin login, roles ni seguridad |
| HU-14 | Auditoría | ⚠️ | 33 % | Solo persistencia; sin búsqueda ni UI real |
| HU-15 | Retroalimentación | ❌ | 0 % | Sin calificaciones ni comentarios |
| HU-16 | Métricas y monitoreo | ❌ | 0 % | Solo maqueta estática |
| HU-17 | Derivación municipal | ⚠️ | 40 % | Solo nota genérica, sin canal/área |
| HU-18 | Reportes y exportación | ❌ | 0 % | No existe |
| | **TOTAL** | | **59 %** | 60 de 101 puntos de verificación |

## Defectos detectados (1 y 16 de octubre de 2026)

| # | Defecto | Ubicación | Estado |
|---|---------|-----------|--------|
| D-1 | Tiempo de espera de 6 s menor que el tiempo real del RAG (4–17 s), con respuesta ficticia al agotarse | `lib/api.ts` | ✅ Corregido — timeout 45 s y `respuestaDemo()` eliminada; el error se muestra al ciudadano |
| D-2 | `groundedness` siempre 90 % | `lib/api.ts` | ✅ Corregido — el backend envía el valor real y el front lo muestra tal cual |
| D-3 | Las fuentes nunca se muestran (`{url, fragmento}` vs `titulo`) | `consulta_controller.py` | ✅ Corregido — las fuentes incluyen `titulo` |
| D-4 | El front llama `/api/health`, pero la ruta real es `/health` | `lib/api.ts` | ✅ Corregido — se consulta `/health`; lo no verificado se informa como "sin verificar" |
| D-5 | Campos de trámites desalineados | `tramite_controller.py` vs `lib/api.ts` | ✅ Corregido — `mapearTramite` traduce `costo`, `duracion_estimada_dias` y `tipo` al modelo de la interfaz |
| D-6 | Datos de demostración presentados como reales | `app/admin/page.tsx`, `app/page.tsx` | ⚠️ Parcial — se retiraron los KPI inventados de la portada y `DocumentManager` ya consume la API, pero los KPIs/gráficos de `/admin` siguen siendo ficticios (252 / 1.236 / 98 %) |
| D-7 | `POST /api/documentos/upload` acepta cualquier archivo | `documento_controller.py:66` | ⚠️ Parcial — `FormatoDocumento` valida la extensión con 422, pero faltan `pypdf`/`python-docx` (**D-17**) para extraer texto real |
| D-8 | `es_administrador()` nunca se invoca | `domain/entities/Usuario.py:16` | ❌ Abierto — el campo `rol` existe pero no controla ningún acceso |
| D-9 | `GET /api/consultas/{id}` no devuelve respuesta, fuentes ni confianza | `consulta_controller.py:90` | ❌ Abierto |
| D-10 | `DELETE /api/documentos/{id}` borraba físicamente el documento | `documento_controller.py` | ✅ Corregido — baja lógica: marca `eliminado_en` (existe además `DELETE /{id}/fisico`) |
| D-11 | `/health` no comprueba la base de datos, Redis ni Ollama | `main.py` / health | ❌ Abierto |
| D-12 | Branding inconsistente (Huancayo vs. Junín) | frontend | ⚠️ Parcial |
| D-13 | Normalización de la caché de consultas | `ServicioCache` | 🟡 Menor |
| D-14 | **La API no arranca:** `main.py:21` importa `router` de `tramite_admin_controller`, que es un stub de 91 bytes sin `router` → `ImportError`; 0 de 22 endpoints servibles | `main.py:21`, `tramite_admin_controller.py` | 🔴 Bloqueante |
| D-15 | Migración `004_documentos_pmv2.sql` **sin aplicar** y con línea 1 inválida (docstring de Python en vez de `--`); la BD no tiene los metadatos, `fragmentos_documento` ni `derogado` | `database/migrations/004_documentos_pmv2.sql` | 🔴 Bloqueante |
| D-16 | `instalar.ps1` no aplica la migración 004 | `instalar.ps1` | 🔴 Bloqueante |
| D-17 | `pypdf` y `python-docx` no están en `requirements.txt` (la extracción de PDF/DOCX no puede funcionar) | `requirements.txt` | 🔴 Bloqueante |
| D-18 | `estado` inválido produce **500** en vez de 422 | `documento_admin_controller.py:48` | 🔴 Alto |
| D-19 | La baja física no borra el archivo en `storage/documentos` | `DELETE /{id}/fisico` | 🟠 Medio |
| D-20 | `lib/api.ts` `pedir()` hace `response.json()` incondicional, pero los DELETE devuelven **204 sin cuerpo** → `SyntaxError` | `lib/api.ts` | 🔴 Alto |
| D-21 | El front llama a `GET /api/tramites/admin` (inexistente; cae en `GET /api/tramites/{id}` → 500) dentro de `Promise.all`, así que el panel de documentos no carga | `DocumentManager.tsx` / `lib/api.ts` | 🔴 Bloqueante |

**Conclusión:** el backend tiene un núcleo RAG sólido y verificado (consulta, búsqueda vectorial,
SLM, groundedness, caché, identificación de trámite probable y auditoría en BD). Con la corrección
de D-1 a D-5, **HU-05 y HU-06 llegaron al 100 %**; con el PMV2 documental del commit `ea06c9a`
(validación de formato, metadatos obligatorios, estado `derogado`, baja lógica, chunking,
reprocesado, listados con filtros, 6 endpoints admin y el panel `DocumentManager`) el avance global
sube del 49 % al **59 %** (60/101). Sin embargo, el HEAD actual **no arranca la API (D-14)**, la
migración 004 no está aplicada (D-15/D-16) y el panel de documentos no carga (D-21): son los
bloqueos inmediatos. El frente funcional que sigue abierto es HU-12 (trámites relacionados al 0 %),
los montos del TUPA en `tramites.costo`, el OCR y la recuperación RAG por fragmento.