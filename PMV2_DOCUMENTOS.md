# PMV2 — Extensión de documentos

> **Estado verificado: 17 de octubre de 2026 (verificación en vivo)**
> — la API arranca con **31 rutas**, migraciones `004`/`005`/`006` aplicadas y los defectos
> **D-14..D-23** corregidos (carga de PDF real → **201**). **PMV2 cerrado al 100 % (28/28).**
> Las cifras de avance se reconcilian contra
> [`documentacion/00-documentos-rectores/06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md) §10.

## 1. Alcance original (commit `ea06c9a`)

### Nuevos campos en documentos
- `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`
- `fragmentado`, `eliminado_en`

### Tabla fragmentos_documento
Para chunking con embeddings (HU-04).

### Migración
Aplicar: `database/migrations/004_documentos_pmv2.sql`

### Backend
- Nuevos puertos/adaptadores: `ExtraccionTextoPort`, `AlmacenamientoDocumentosPort`, `FragmentoRepository`
- Caso de uso `CargarDocumento` (orquesta carga + extracción + almacenamiento + fragmentación)
- Caso de uso `ProcesarDocumento` (chunking + embeddings por fragmento)
- `GestionarDocumentos` ampliado (baja lógica, filtros, metadatos)
- `DocumentoRepository` ampliado (listar, marcar_eliminado, eliminar_fisico)
- `FragmentoRepositoryImpl`, `ExtraccionTextoAdapter`
- Nuevos endpoints admin: `POST/GET /api/admin/documentos/*`, `POST /api/admin/documentos/{id}/procesar`, `DELETE /api/admin/documentos/{id}` (lógica), `DELETE /api/admin/documentos/{id}/fisico`
- Endpoints públicos de documentos mantenidos (compatibles)

### Frontend
- `DocumentManager` en admin: carga con metadatos, reprocesado, baja lógica/física
- `lib/api.ts` ampliado con funciones admin de documentos
- Reemplaza el listado estático por gestión real (G-12 en parte)

---

## 2. Estado real verificado contra el código

### 2.1 ✅ Implementado

| Elemento | Archivo |
|---|---|
| Entidad `Documento` con metadatos (`version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`, `fragmentado`, `eliminado_en`) y `requiere_metadatos()` | `backend/domain/entities/Documento.py` |
| Entidad `FragmentoDocumento` | `backend/domain/entities/FragmentoDocumento.py` |
| Errores de dominio (`FormatoNoSoportadoError`, `DocumentoIlegibleError`, `DocumentoInvalidoError`) | `backend/domain/errors.py` |
| Value object de formatos (`.pdf/.docx/.txt/.md` → MIME) | `backend/domain/value_objects/FormatoDocumento.py` |
| Enum `EstadoDocumento` con `derogado` | `backend/domain/value_objects/EstadoDocumento.py` |
| Puertos `AlmacenamientoDocumentosPort`, `ExtraccionTextoPort`, `FragmentoRepository` y `DocumentoRepository` ampliado | `backend/domain/ports/*` |
| Caso de uso `CargarDocumento` (valida extensión → extrae texto → almacena → registra metadatos → indexa → fragmenta) | `backend/application/use_cases/CargarDocumento.py` |
| Caso de uso `ProcesarDocumento` (chunking + embedding por fragmento, idempotente, marca `fragmentado`) | `backend/application/use_cases/ProcesarDocumento.py` |
| `GestionarDocumentos` ampliado (registrar con metadatos, `listar` con filtros, `actualizar`, baja lógica, baja física) | `backend/application/use_cases/GestionarDocumentos.py` |
| `ServicioChunking` real: párrafos → oraciones → grupos con solape 800/120 (sin NLTK) | `backend/application/services/ServicioChunking.py` |
| Adaptador de extracción PDF/DOCX/TXT/MD con fallback a `DocumentoIlegibleError` | `backend/infrastructure/adapters/extraction/ExtraccionTextoAdapter.py` |
| Repositorio de fragmentos (`guardar_lote`, `listar_por_documento`, `eliminar_por_documento`) | `backend/infrastructure/repositories/FragmentoRepositoryImpl.py` |
| Endpoints admin (`GET/POST /api/admin/documentos`, `POST /upload`, `POST /{id}/procesar`, `DELETE /{id}` lógico, `DELETE /{id}/fisico`) | `backend/infrastructure/controllers/documento_admin_controller.py` |
| Endpoints públicos ampliados: `GET /api/documentos` (filtros `estado`, `incluir_eliminados`), `POST /{id}/procesar`, `DELETE` **lógico** + `DELETE /fisico` | `backend/infrastructure/controllers/documento_controller.py` |
| Router admin registrado en la app | `backend/main.py:59-66` |
| Frontend `DocumentManager` (form con metadatos, tabla con indexado/fragmentado, reprocesar, dar de baja, eliminar) | `frontend-tramites/components/DocumentManager.tsx` |
| Funciones API admin (`listarDocumentosAdmin`, `subirDocumento`, `reprocesarDocumento`, `eliminarDocumentoLogico/Fisico`) | `frontend-tramites/lib/api.ts:166-224` |
| Inyección de dependencias de los 3 casos de uso nuevos/ampliados | `backend/infrastructure/container.py:111-145` |

### 2.2 ⚠️ Parcial

| Aspecto | Estado real |
|---|---|
| **Extracción de PDF/DOCX** | El código existe, pero `pypdf` y `python-docx` **no están en `requirements.txt` ni instalados** (verificado con `importlib.util.find_spec`). Solo `.txt` y `.md` se procesan; un `.pdf`/`.docx` devuelve `DocumentoIlegibleError` → **422**. |
| **Baja lógica en la búsqueda vectorial** | `BusquedaVectorialAdapter` filtra `estado='vigente'` pero **no** `eliminado_en IS NULL`: un documento dado de baja sigue compitiendo por el `top_k` y solo se descarta después en Python (`ServicioRAG`/`BuscarDocumentos`/`ConsultarTramite`). |
| **Recuperación por fragmento (HU-04)** | Los fragmentos se guardan con embedding, pero `FragmentoRepository.listar_por_documento` **no tiene consumidor**: el RAG sigue usando el embedding del documento completo. |
| **Baja física** | Borra las filas de `documentos` y `fragmentos_documento`, pero **no** el archivo en `storage/documentos` (`AlmacenamientoDocumentosPort.eliminar` nunca se invoca) → huérfanos en disco. |
| **Campos sin uso** | `Documento.fragmento_destacado` (nunca se lee/escribe), `hash_contenido` (calculado, no se usa para deduplicar). |
| **Panel admin (G-12)** | `DocumentManager` es real, pero los KPIs/gráficos de `/admin` siguen siendo estáticos (`admin/page.tsx:22-24`: 252 / 1,236 / 98 %). |
| **Autorización** | Los 6 endpoints admin **no validan autenticación ni rol**: cualquiera puede subir/borrar (D-8 / G-01 abiertos). |
| **Validación de `estado` en listado admin** | `EstadoDocumento(estado)` puede lanzar `ValueError` no capturado → **500** en vez de **422** (`documento_admin_controller.py:48`). |

### 2.3 ❌ Bloqueos detectados el 16-oct-2026 — ✅ resueltos todos (excepto B8)

| # | Bloqueo | Estado |
|---|---|---|
| B1 | **La API no arrancaba** (`ImportError` de `router` en un stub) | ✅ Corregido (D-14): `import main` → **31 rutas**, ningún endpoint cae |
| B2 | **La migración 004 no estaba aplicada** | ✅ Aplicada (`004` + `005`): 45/45 documentos con metadatos; `derogado` en el `CHECK` |
| B3 | **La 004 no era SQL válido** (línea 1 con docstring) | ✅ Corregido (línea 1 con `--`) |
| B4 | **El booleano se enviaba como entero** (`1 if … else 0` → `DataError`) | ✅ Corregido (D-22): `bool(fragmentado)` |
| B5 | **El front fallaba al borrar** (204 sin cuerpo → `SyntaxError`) | ✅ Corregido (D-20): 204 manejado, sin errores en `tsc` |
| B6 | **Front llamaba a `/api/tramites/admin` inexistente** | ✅ Corregido (D-21): panel carga (272 trámites) |
| B7 | **Nada ejecutaba la 004** | ✅ Corregido (D-16): `instalar.ps1` lista `004` y `005` |
| B8 | **0 suites de pruebas.** No existe ningún `test_*.py`, `conftest.py`, `*.test.ts` ni script `test` en `package.json` (G-18). | ⬜ **Abierto** (G-18) |

---

## 3. Avance medido del PMV2

Método: puntos de verificación de [`02-implementacion-de-historias.md`](documentacion/00-documentos-rectores/02-implementacion-de-historias.md)
(✅ cuenta, ⚠️ y ❌ no cuentan).

| Métrica | Antes (`ff7a589`) | Ahora (`ea06c9a`) | **Verificado 16-oct (en vivo)** | **Verificado 17-oct (en vivo)** |
|---|---|---|---|---|
| HU-01 Carga de documentos | 4/9 · 44 % | 7/9 · 78 % | **9/9 · 100 %** ✅ | **9/9 · 100 %** ✅ |
| HU-02 Vigencia/versión/fuente | 4/8 · 50 % | 7/8 · 88 % | **8/8 · 100 %** ✅ | **8/8 · 100 %** ✅ |
| HU-03 Aprobar/derogar | 3/7 · 43 % | 5/7 · 71 % | **6/7 · 86 %** | **6/7 · 86 %** |
| HU-04 Procesamiento y RAG | 4/9 · 44 % | 7/9 · 78 % | **9/9 · 100 %** ✅ | **9/9 · 100 %** ✅ |
| HU-08 Costos y plazos | 3/5 · 60 % | 4/5 · 80 % | 4/5 · 80 % | **5/5 · 100 %** ✅ |
| HU-10 Trazabilidad/anti-alucinación | 4/8 · 50 % | 4/8 · 50 % | 4/8 · 50 % | **8/8 · 100 %** ✅ |
| HU-11 Consultas fuera de dominio | 0/3 · 0 % | 0/3 · 0 % | **0/3 · 0 %** | **3/3 · 100 %** ✅ |
| HU-12 Trámites relacionados | 0/3 · 0 % | 0/3 · 0 % | **3/3 · 100 %** ✅ | **3/3 · 100 %** ✅ |
| **PMV2 (HU-04+08+10+11+12)** | 11/25 · 44 % | 14/25 · 56 % | 20/28 · 71 % | **28/28 · 100 %** ✅ |
| **PMV3 (HU-01+02+03+13..18)** | 15/44 · 34 % | 23/44 · 52 % | 29/49 · 59 % | **31/49 · 63 %** |
| **Global 18 HU** | 49/101 · 49 % | 60/101 · 59 % | 73/101 · 72 % | **83/101 · 82 %** |

Qué ganó el PMV2: validación de formato, metadatos obligatorios, `version`, `fecha_publicacion`,
estado `derogado`, baja lógica, chunking + tabla de fragmentos, reproceso, listado con filtros y
panel de administración real de documentos (`G-12` ✅, `G-13` ✅). En la verificación del
**17-oct-2026** se sumaron el umbral "no inventar" (G-04/HU-08), la trazabilidad completa con
bloqueo y fuentes con metadatos (HU-10) y el clasificador de dominio (HU-11), cerrando **PMV2 al
100 %**.

---

## 4. Qué falta para cerrar el PMV2

1. ~~**Arreglar los bloqueos B1–B7**~~ → ✅ **hecho** (D-14..D-23, verificados en vivo: 31 rutas,
   `004`/`005`/`006` aplicadas, deps en `requirements.txt`, 204 y panel admin OK).
2. ~~**HU-04:** OCR y recuperación **por fragmento**~~ → ✅ **hecho** (rapidocr + 45/45 documentos
   fragmentados con `fragmentos_documento`).
3. ~~**HU-08:** cargar los montos reales del TUPA + umbral "no inventar"~~ → ✅ **hecho** (252
   sembrados; 188 con costo > 0; `BLOQUEO_AFIRMACIONES` con umbral de groundedness).
4. ~~**HU-10:** `GET /api/consultas/{id}` sin respuesta/fuentes/confianza (D-9)~~ → ✅ **hecho**
   (17-oct-2026: `TrazabilidadResponse`, bloqueo de afirmaciones, fuentes con número/fecha/versión,
   `GET /api/consultas` y panel `AuditLog` real).
5. ~~**HU-12:** motor de trámites relacionados~~ → ✅ **hecho** (embedding + fallback léxico + UI).
6. **G-18:** suite `pytest` del flujo RAG completo; hoy nada está verificado de forma automatizada.
7. ~~**G-04 + HU-11:** umbral de abstención y clasificador de dominio (fuera de dominio)~~ → ✅
   **hecho** (17-oct-2026: `ServicioDominio` + `BLOQUEO_AFIRMACIONES`).
8. **P2-17:** validación SUS con 50 ciudadanos (no fabricable; pendiente honesto).

> ✅ **PMV2 cerrado el 17-oct-2026.** Queda únicamente P2-17 (actividad real, no de código) y,
> fuera del alcance de este PMV, G-18 (suite de pruebas) y el resto de PMV3.

## Notas (corregidas respecto de la versión anterior de este documento)

- ~~"Upload solo extrae `.txt`/`.md`"~~ → ✅ PDF/DOCX verificados con `pypdf`/`python-docx`
  (upload con PDF real → 201, texto extraído).
- ~~Baja lógica: la búsqueda vectorial no la respeta y la 004 no está aplicada~~ → ✅ 004/005
  aplicadas (45/45 con metadatos).
- ~~`derogado` no es persistible~~ → ✅ persistible tras aplicar `004`.
- ~~Fragmentos "aún sin consumidor" en el RAG~~ → ✅ recuperación por fragmento activa (G-13).
