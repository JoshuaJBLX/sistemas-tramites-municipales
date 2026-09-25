-- =============================================================
-- schema.sql
-- Referencia consolidada del esquema de la base de datos
-- `tramites_municipales` (PostgreSQL + pgvector).
--
-- Las migraciones ejecutables viven en ./migrations:
--   001_create_database.sql  -> crea la BD y habilita pgvector
--   002_create_tables.sql    -> crea las tablas e índices
--   003_create_vectors.sql   -> índices vectoriales (HNSW)
-- Los datos de ejemplo viven en ./seeds.
-- =============================================================

-- municipalidades: catálogo de municipalidades atendidas.
-- usuarios: ciudadanos y administradores del sistema.
-- tramites: catálogo de trámites por municipalidad.
-- documentos: base documental oficial, indexada vectorialmente.
-- consultas: preguntas formuladas por los ciudadanos.
-- auditoria_consultas: trazabilidad de cada consulta y su respuesta.

CREATE TABLE IF NOT EXISTS municipalidades (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre       VARCHAR(200) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    provincia    VARCHAR(100) NOT NULL,
    distrito     VARCHAR(100) NOT NULL,
    sitio_web    VARCHAR(500),
    creado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS usuarios (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre    VARCHAR(150) NOT NULL,
    correo    VARCHAR(150) NOT NULL UNIQUE,
    rol       VARCHAR(30) NOT NULL CHECK (rol IN ('ciudadano', 'administrador')),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tramites (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    municipalidad_id       UUID NOT NULL REFERENCES municipalidades (id) ON DELETE CASCADE,
    nombre                 VARCHAR(200) NOT NULL,
    descripcion            TEXT NOT NULL,
    tipo                   VARCHAR(60) NOT NULL,
    requisitos             TEXT[] NOT NULL DEFAULT '{}',
    costo                  NUMERIC(10, 2) NOT NULL DEFAULT 0,
    duracion_estimada_dias INT NOT NULL DEFAULT 0,
    creado_en              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documentos (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tramite_id     UUID NOT NULL REFERENCES tramites (id) ON DELETE CASCADE,
    titulo         VARCHAR(300) NOT NULL,
    contenido      TEXT NOT NULL,
    url_origen     VARCHAR(500) NOT NULL,
    estado         VARCHAR(20) NOT NULL DEFAULT 'vigente'
                   CHECK (estado IN ('vigente', 'obsoleto', 'en_revision')),
    embedding      vector(1024),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consultas (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios (id) ON DELETE SET NULL,
    pregunta   TEXT NOT NULL,
    intencion  VARCHAR(50),
    creada_en  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auditoria_consultas (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id   UUID NOT NULL REFERENCES consultas (id) ON DELETE CASCADE,
    respuesta     TEXT,
    confianza     VARCHAR(20) CHECK (confianza IN ('alta', 'media', 'baja')),
    fuentes       TEXT,
    registrado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw ON documentos USING hnsw (embedding vector_cosine_ops);