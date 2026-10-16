# 04 — Base de Datos

> **Actualizado el 16 de octubre de 2026 (HEAD `ea06c9a`).** Cifras y estado verificados contra el código en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md) y [PMV2_DOCUMENTOS.md](../PMV2_DOCUMENTOS.md): global **59 %**, PMV1 **88 %**, PMV2 **56 %**, PMV3 **52 %**; la API aún no arranca (D-14).

> PostgreSQL 16 + pgvector · base `tramites_municipales`

## 1. Migraciones (`database/migrations/`)

| Migración | Función |
|---|---|
| `001_create_database.sql` | Crea la BD `tramites_municipales` (si no existe) y habilita `CREATE EXTENSION vector` |
| `002_create_tables.sql` | Crea las 6 tablas del dominio + índices B-tree de apoyo |
| `003_create_vectors.sql` | Índice **HNSW** por similitud de coseno sobre `documentos.embedding` |
| `004_documentos_pmv2.sql` | **Nuevo (PMV2), 29 líneas — ⚠️ NO APLICADA (D-15):** añade 7 columnas a `documentos`, crea la tabla `fragmentos_documento` y amplía el `CHECK` de `estado` con `derogado` |

Las migraciones `001`-`003` se ejecutan **automáticamente al primer arranque** del contenedor
postgres en `docker-compose.yml` (montadas en `/docker-entrypoint-initdb.d`).

> ⚠️ **La `004` no está aplicada en ninguna BD y hoy ni siquiera es ejecutable:** su **línea 1 es
> un docstring de Python (`"""…"""`)** en lugar de un comentario `--`, así que `psql` la rechaza
> (**D-15**). `instalar.ps1` tampoco la incluye en su paso de migraciones (**D-16**). Verificado el
> 16-oct-2026 contra la BD local: `documentos` sigue con **8 columnas**, `fragmentos_documento`
> **no existe** y el `CHECK` de `estado` sigue en `(vigente, obsoleto, en_revision)`.

`database/schema.sql` es la **referencia consolidada** del esquema (mismo modelo; no se ejecuta).

## 2. Modelo entidad-relación

```
municipalidades (1) ────< (N) tramites (1) ────< (N) documentos (1) ────< (N) fragmentos_documento
                              │                                              (PMV2, 004 sin aplicar)
usuarios (1) ────< (N) consultas ────< (1) auditoria_consultas
                           (1)        (N-1)
```

## 3. Tablas, columnas y relaciones (6 base + 1 del PMV2)

### municipalidades
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | `gen_random_uuid()` |
| nombre · departamento · provincia · distrito | VARCHAR | — |
| sitio_web | VARCHAR(500) | — |
| creado_en | TIMESTAMPTZ | default NOW() |

### usuarios
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| nombre | VARCHAR(150) | — |
| correo | VARCHAR(150) UNIQUE | — |
| rol | VARCHAR(30) | CHECK IN ('ciudadano','administrador') |
| creado_en | TIMESTAMPTZ | — |

### tramites (catálogo TUPA)
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| municipalidad_id | UUID FK → municipalidades | ON DELETE CASCADE |
| nombre · descripcion | VARCHAR / TEXT | — |
| tipo | VARCHAR(60) | 6 tipos (value object) |
| requisitos | TEXT[] | ARRAY de requisitos |
| costo | NUMERIC(10,2) | default 0 |
| duracion_estimada_dias | INT | default 0 |
| creado_en | TIMESTAMPTZ | — |

### documentos (base documental indexada)
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| tramite_id | UUID FK → tramites | ON DELETE CASCADE |
| titulo | VARCHAR(300) | — |
| contenido | TEXT | Texto que alimenta al RAG |
| url_origen | VARCHAR(500) | Fuente oficial citada |
| estado | VARCHAR(20) | CHECK IN ('vigente','obsoleto','en_revision') → **PMV2 añade `derogado`** |
| **embedding** | **vector(1024)**¹ | Embedding BGE-M3; NULL si no indexado |
| actualizado_en | TIMESTAMPTZ | default NOW() |
| **PMV2 (+7)** ↓ | — | ⚠️ **solo en la migración 004, sin aplicar (D-15)** |
| version | VARCHAR(20) | Versión del documento |
| fecha_publicacion | DATE | Fecha de publicación (opcional) |
| archivo_nombre | VARCHAR(300) | Nombre original del archivo subido |
| mime_type | VARCHAR(100) | Tipo MIME detectado |
| hash_contenido | VARCHAR(64) | SHA-256 del contenido |
| fragmentado | BOOLEAN | ¿Tiene fragmentos en `fragmentos_documento`? |
| eliminado_en | TIMESTAMPTZ | Marca de **baja lógica**; NULL = activo |

### consultas
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| usuario_id | UUID FK → usuarios | ON DELETE SET NULL |
| pregunta | TEXT | — |
| intencion | VARCHAR(50) | 9 intenciones del dominio |
| creada_en | TIMESTAMPTZ | — |

### auditoria_consultas (trazabilidad)
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| consulta_id | UUID FK → consultas | ON DELETE CASCADE |
| respuesta | TEXT | Texto final entregado |
| confianza | VARCHAR(20) | CHECK IN ('alta','media','baja') |
| fuentes | TEXT | URLs separadas por comas |
| registrado_en | TIMESTAMPTZ | — |

### fragmentos_documento (PMV2 — ⚠️ tabla aún inexistente en la BD, D-15)
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| documento_id | UUID FK → documentos | ON DELETE CASCADE |
| orden | INT | Posición del fragmento en el documento |
| contenido | TEXT | Bloque de ~800 caracteres con 120 de solape (`ServicioChunking`) |
| **embedding** | **vector(1024)** | Embedding del fragmento (BGE-M3) |
| creado_en | TIMESTAMPTZ | default NOW() |

## 4. Índices

**B-tree** (`002`): `idx_tramites_municipalidad`, `idx_documentos_tramite`, `idx_documentos_estado`,
`idx_consultas_usuario`, `idx_consultas_creada_en`, `idx_tramites_tipo` (en `003`).
`idx_fragmentos_documento` se crea en la migración `004` (**sin aplicar**).

**Vectorial HNSW** (`003`):
```sql
CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw
    ON documentos USING hnsw (embedding vector_cosine_ops);
```
- Requiere pgvector ≥ 0.5.0 (la imagen `pgvector/pgvector:pg16` lo incluye).
- Alternativa IVFFlat comentada para versiones viejas.
- Permite búsqueda por **similitud de coseno** (operador `<=>`).

¹ **pgvector es opcional en desarrollo local.** La migración `002` crea la extensión
`vector` solo si el servidor la tiene disponible; si no, la columna `embedding` se crea
como `double precision[]` y `BusquedaVectorialAdapter` calcula el coseno en Python
(`Connection.es_pgvector()` decide la ruta en el arranque). El índice HNSW se crea solo
con pgvector. En producción (Docker) se mantiene el camino vectorial nativo.

## 5. Búsqueda vectorial (RAG) — query real

```sql
SELECT id, tramite_id, titulo, contenido, url_origen, estado, actualizado_en,
       1 - (embedding <=> $1::vector) AS similitud
FROM documentos
WHERE embedding IS NOT NULL
  AND estado = 'vigente'
ORDER BY embedding <=> $1::vector
LIMIT $2
```
- `$1` = embedding de la pregunta (BGE-M3, formato `[0.1,0.2,…]`, 1024 valores).
- `$2` = `top_k` (por defecto 5, configurable con `RAG_TOP_K`).
- El adaptador descarta resultados con similitud < **0.3** (`BusquedaVectorialAdapter.py:56`).

## 6. Datos semilla (`database/seeds/`)

| Seed | Contenido real | Muestra |
|---|---|---|
| `municipios.sql` | 1 municipalidad | Junín (MPJ) |
| `tramites.sql` | **22 trámites** TUPA 2023 | Registro civil (nacimiento, matrimonio, defunción, separación, unión de hecho, partida) · certificados (residencia, posesión, no adeudo) · licencias (funcionamiento, edificación, anuncios, comercio) · urbanismo (zonificación, parámetros, habilitación, fábrica, numeración) · tributos (predial, empadronamiento) · otros (eventos, vía pública) |
| `documentos.sql` | **20 documentos** vigentes | Nacimiento (N.º 188), residencia (N.º 232), licencia funcionamiento (N.º 9), licencia edificación (N.º 30), no adeudo (N.º 109), defunción (N.º 220) + matrimonio (N.º 201), predial, numeración (N.º 42), posesión (N.º 233), zonificación (N.º 34), parámetros (N.º 36), habilitación (N.º 27), fábrica (N.º 47), anuncios (N.º 52), comercio (N.º 118), eventos (N.º 130), unión de hecho (N.º 205), empadronamiento (N.º 240), vía pública (N.º 57) — con `url_origen` de `munijunin.gob.pe`, `embedding NULL` (se indexa al registrar) |

Los seeds referencian la base de conocimiento oficial de la MPJ (TUPA 2023, 252 procedimientos
según a.md) y citan el portal <https://www.gob.pe/munijunin>.

## 7. Conexión desde el backend

- DSN construida en `Connection._construir_dsn_desde_entorno()` con variables `POSTGRES_*`
  (usuario/password `tramites`, host `localhost`, puerto `5432`, BD `tramites_municipales`).
- `asyncpg.create_pool(dsn, min_size=1, max_size=10)` — pool de conexiones asíncrono.
- Todo el SQL usa parámetros posicionales `$1…` (seguro contra inyección).

## 8. Persistencia y volumen

- Datos persistentes en el volumen `pgdata` de Docker Compose.
- `docker compose down -v` borra la BD (full reset); las migraciones y seeds se re-aplican desde cero.
- ⚠️ **Para habilitar el PMV2** hay que corregir la línea 1 de `004_documentos_pmv2.sql` (docstring
  Python → comentario `--`) y aplicarla con `psql -f`: ni el montaje de `/docker-entrypoint-initdb.d`
  (solo corre en volumen nuevo) ni `instalar.ps1` la ejecutan hoy (**D-15/D-16**). Sin ella, las
  consultas que filtran `eliminado_en IS NULL` fallan con `UndefinedColumn`.