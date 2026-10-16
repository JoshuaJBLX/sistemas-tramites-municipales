# PMV2 — Extensión de documentos

> **Estado verificado: 16 de octubre de 2026 · HEAD `ea06c9a`**
> (`feat(documents): PMV2 - carga con metadatos, extracción, chunking, baja lógica y panel admin`).
> Verificación por lectura de código + consulta directa a PostgreSQL local.
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

### 2.3 ❌ Bloqueos detectados (hay que resolverlos antes de declarar PMV2)

| # | Bloqueo | Evidencia |
|---|---|---|
| B1 | **La API no arranca.** `main.py:21` y `:56` importan `router` de `tramite_admin_controller`, que es un stub de 91 bytes sin `router` → `ImportError`. Verificado ejecutando `import main`. **Ningún endpoint es servible.** | `backend/main.py`, `backend/infrastructure/controllers/tramite_admin_controller.py` |
| B2 | **La migración 004 no está aplicada en la BD local.** `documentos` solo tiene las 8 columnas originales, `fragmentos_documento` **no existe** y el `CHECK estado` no admite `derogado` (consultado a PostgreSQL el 16-oct). Todo el upsert PMV2 fallaría por columnas inexistentes. | `database/migrations/004_documentos_pmv2.sql` vs BD real |
| B3 | **La migración 004 no es SQL válido.** La línea 1 es un docstring de Python (`"""Migrations..."""`), no un comentario `--`; `psql` daría error de sintaxis y Docker montaría el fichero en `docker-entrypoint-initdb.d`. | `004_documentos_pmv2.sql:1` |
| B4 | **El booleano se envía como entero.** `DocumentoRepositoryImpl.py:122` pasa `1 if documento.fragmentado else 0` a una columna `BOOLEAN`. Verificado contra asyncpg: `DataError: invalid input for query argument $1: 1 (a boolean is required (got type int))`. Rompe **todo** insert/update de documentos (también el flujo anterior, no solo PMV2). | `backend/infrastructure/repositories/DocumentoRepositoryImpl.py:122` |
| B5 | **El front falla al borrar.** `pedir()` (`lib/api.ts:69`) hace `await response.json()` sin condición, pero los `DELETE` devuelven **204 sin cuerpo** → `SyntaxError`. Los botones "Dar de baja"/"Eliminar" de `DocumentManager` no tienen `try/catch`: la promesa se rechaza y **la tabla no se refresca**. | `lib/api.ts:69`, `DocumentManager.tsx:125-126` |
| B6 | **Frontend llama a un endpoint inexistente.** `GET /api/tramites/admin` (`lib/api.ts:224`, `DocumentManager.tsx:35` dentro de un `Promise.all`) — `tramite_admin_controller` está vacío, la ruta cae en `GET /api/tramites/{tramite_id}` con `id='admin'` → error de asyncpg → **500**, y como está en `Promise.all` **tampoco carga la lista de documentos**. | `frontend-tramites/lib/api.ts`, `backend/infrastructure/controllers/tramite_admin_controller.py` |
| B7 | **Nada ejecuta la 004.** `instalar.ps1` solo aplica 002, 003 y seeds; ningún README documenta `psql -f ...004...`. | `instalar.ps1:123-127` |
| B8 | **0 suites de pruebas.** No existe ningún `test_*.py`, `conftest.py`, `*.test.ts` ni script `test` en `package.json` (G-18). | repositorio completo |

---

## 3. Avance medido del PMV2

Método: puntos de verificación de [`02-implementacion-de-historias.md`](documentacion/00-documentos-rectores/02-implementacion-de-historias.md)
(✅ cuenta, ⚠️ y ❌ no cuentan).

| Métrica | Antes (`ff7a589`) | Ahora (`ea06c9a`) |
|---|---|---|
| HU-01 Carga de documentos | 4/9 · 44 % | **7/9 · 78 %** |
| HU-02 Vigencia/versión/fuente | 4/8 · 50 % | **7/8 · 88 %** |
| HU-03 Aprobar/derogar | 3/7 · 43 % | **5/7 · 71 %** |
| HU-04 Procesamiento y RAG | 4/9 · 44 % | **7/9 · 78 %** |
| **PMV2 (HU-04+08+10+12)** | 11/25 · **44 %** | **14/25 · 56 %** |
| **PMV3 (HU-01+02+03+13+14+15+16+18)** | 15/44 · **34 %** | **23/44 · 52 %** |
| **Global 18 HU** | 49/101 · **49 %** | **60/101 · 59 %** |

Qué ganó el PMV2 en esta iteración: validación de formato, metadatos obligatorios, `version`,
`fecha_publicacion`, estado `derogado`, baja lógica, chunking + tabla de fragmentos, reproceso,
listado con filtros y panel de administración real de documentos (`G-12` ⬆️ parcial, `G-13` ⬆️ parcial).

---

## 4. Qué falta para cerrar el PMV2

1. **Arreglar los bloqueos B1–B7** (el orden importa): `tramite_admin_controller` → `004` en SQL válido + ejecutada → `bool` en el upsert → `pypdf`/`python-docx` en `requirements.txt` → manejo del 204 y de `/api/tramites/admin` en el front.
2. **HU-04:** OCR para escaneados, recuperación **por fragmento** (hoy los chunks no se consultan), baja lógica aplicada también en `BusquedaVectorialAdapter`.
3. **HU-08:** cargar los montos reales del TUPA en `tramites.costo` (sigue en 0.00).
4. **HU-10:** `GET /api/consultas/{id}` sin respuesta/fuentes/confianza (D-9).
5. **HU-12:** motor de trámites relacionados — sigue en **0 %** (G-08).
6. **G-18:** suite `pytest` del flujo RAG completo; hoy nada está verificado de forma automatizada.

## Notas (corregidas respecto de la versión anterior de este documento)

- ~~"Upload ahora valida extensiones (.pdf,.docx,.txt,.md) y extrae texto (D-7 mitigado)"~~ →
  valida extensiones ✅, pero **solo extrae `.txt`/`.md`**; PDF/DOCX requieren `pypdf` y `python-docx`
  (ver B/§2.2).
- Baja lógica con `eliminado_en` ✅ en repositorio y casos de uso, **pero** la búsqueda vectorial
  todavía no la respeta (§2.2) y la 004 no está aplicada (B2).
- `derogado` añadido al enum ✅, pero **no es persistible** hasta aplicar 004 (el `CHECK` actual lo rechaza).
- Fragmentos guardados con embedding ✅, **aún sin consumidor** en el RAG (HU-04 pendiente).
