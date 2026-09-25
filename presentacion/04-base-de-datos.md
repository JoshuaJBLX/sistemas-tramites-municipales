# 04 — Base de Datos

> PostgreSQL 16 + pgvector · base `tramites_municipales`

## 1. Migraciones (`database/migrations/`)

| Migración | Función |
|---|---|
| `001_create_database.sql` | Crea la BD `tramites_municipales` (si no existe) y habilita `CREATE EXTENSION vector` |
| `002_create_tables.sql` | Crea las 6 tablas del dominio + índices B-tree de apoyo |
| `003_create_vectors.sql` | Índice **HNSW** por similitud de coseno sobre `documentos.embedding` |

Las migraciones se ejecutan **automáticamente al primer arranque** del contenedor postgres en
`docker-compose.yml` (montadas en `/docker-entrypoint-initdb.d`).

`database/schema.sql` es la **referencia consolidada** del esquema (mismo modelo).

## 2. Modelo entidad-relación

```
municipalidades (1) ────< (N) tramites (1) ────< (N) documentos
                              │
usuarios (1) ────< (N) consultas ────< (1) auditoria_consultas
                           (1)        (N-1)
```

## 3. Tablas, columnas y relaciones

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
| estado | VARCHAR(20) | CHECK IN ('vigente','obsoleto','en_revision') |
| **embedding** | **vector(1024)** | Embedding BGE-M3; NULL si no indexado |
| actualizado_en | TIMESTAMPTZ | default NOW() |

### consultas
| Columna | Tipo | Notas |
|---|---|---|
| id | UUID PK | — |
| usuario_id | UUID FK → usuarios | ON DELETE SET NULL |
| pregunta | TEXT | — |
| intencion | VARCHAR(50) | 6 intenciones del dominio |
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

## 4. Índices

**B-tree** (`002`): `idx_tramites_municipalidad`, `idx_documentos_tramite`, `idx_documentos_estado`,
`idx_consultas_usuario`, `idx_consultas_creada_en`, `idx_tramites_tipo` (en `003`).

**Vectorial HNSW** (`003`):
```sql
CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw
    ON documentos USING hnsw (embedding vector_cosine_ops);
```
- Requiere pgvector ≥ 0.5.0 (la imagen `pgvector/pgvector:pg16` lo incluye).
- Alternativa IVFFlat comentada para versiones viejas.
- Permite búsqueda por **similitud de coseno** (operador `<=>`).

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
| `tramites.sql` | **10 trámites** TUPA 2023 | Inscripción de nacimiento, matrimonio, defunción, separación, certificado de residencia, no adeudo, licencia de funcionamiento, licencia de edificación, impuesto predial, partida de nacimiento |
| `documentos.sql` | **6 documentos** vigentes | Nacimiento (N.º 188), residencia (N.º 232), licencia funcionamiento, licencia edificación (N.º 30), no adeudo (N.º 109), defunción (N.º 220) — con `url_origen` de `munijunin.gob.pe`, `embedding NULL` (se indexa al registrar) |

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