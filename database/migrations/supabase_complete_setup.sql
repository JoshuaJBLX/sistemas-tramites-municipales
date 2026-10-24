-- =============================================================
-- supabase_complete_setup.sql
-- MIGRACIÓN COMPLETA PARA SUPABASE
-- Ejecutar este único archivo en el SQL Editor de Supabase
-- Crea todas las tablas, índices y columnas necesarias
-- =============================================================

-- Paso 1: Habilitar extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- =============================================================
-- Paso 2: Crear tablas base
-- =============================================================

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
    area_responsable       VARCHAR(120),
    creado_en              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documentos (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tramite_id          UUID NOT NULL REFERENCES tramites (id) ON DELETE CASCADE,
    titulo              VARCHAR(300) NOT NULL,
    contenido           TEXT NOT NULL,
    url_origen          VARCHAR(500) NOT NULL,
    estado              VARCHAR(20) NOT NULL DEFAULT 'vigente'
                        CHECK (estado IN ('vigente', 'obsoleto', 'en_revision', 'derogado')),
    version             VARCHAR(20) NOT NULL DEFAULT '1.0',
    fecha_publicacion   DATE,
    archivo_nombre      VARCHAR(255),
    mime_type           VARCHAR(100),
    hash_contenido      VARCHAR(128),
    fragmentado         BOOLEAN NOT NULL DEFAULT false,
    eliminado_en        TIMESTAMPTZ,
    actualizado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fragmentos_documento (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    documento_id   UUID NOT NULL REFERENCES documentos (id) ON DELETE CASCADE,
    orden          INT NOT NULL,
    contenido      TEXT NOT NULL,
    creado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consultas (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios (id) ON DELETE SET NULL,
    pregunta   TEXT NOT NULL,
    intencion  VARCHAR(50),
    creada_en  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auditoria_consultas (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id          UUID NOT NULL REFERENCES consultas (id) ON DELETE CASCADE,
    respuesta            TEXT,
    confianza            VARCHAR(20) CHECK (confianza IN ('alta', 'media', 'baja')),
    fuentes              TEXT,
    groundedness         NUMERIC(5, 3),
    fuentes_detalle      JSONB,
    fuera_dominio        BOOLEAN NOT NULL DEFAULT FALSE,
    afirmaciones_bloqueadas BOOLEAN NOT NULL DEFAULT FALSE,
    entidad_sugerida     TEXT,
    registrado_en       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =============================================================
-- Paso 3: Crear índices
-- =============================================================

CREATE INDEX IF NOT EXISTS idx_tramites_municipalidad ON tramites (municipalidad_id);
CREATE INDEX IF NOT EXISTS idx_tramites_tipo ON tramites (tipo);
CREATE INDEX IF NOT EXISTS idx_documentos_tramite ON documentos (tramite_id);
CREATE INDEX IF NOT EXISTS idx_documentos_estado ON documentos (estado);
CREATE INDEX IF NOT EXISTS idx_fragmentos_documento ON fragmentos_documento (documento_id);
CREATE INDEX IF NOT EXISTS idx_consultas_usuario ON consultas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_consultas_creada_en ON consultas (creada_en DESC);
CREATE INDEX IF NOT EXISTS idx_auditoria_consulta_id ON auditoria_consultas (consulta_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_registrado ON auditoria_consultas (registrado_en DESC);

-- =============================================================
-- Paso 4: Agregar columnas de embedding (vector o array)
-- =============================================================

-- Columna embedding en documentos
DO $$
DECLARE existe_pgvector BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') INTO existe_pgvector;

    IF existe_pgvector THEN
        EXECUTE 'ALTER TABLE documentos ADD COLUMN IF NOT EXISTS embedding vector(1024)';
    ELSE
        EXECUTE 'ALTER TABLE documentos ADD COLUMN IF NOT EXISTS embedding double precision[]';
    END IF;
END $$;

-- Columna embedding en fragmentos_documento
DO $$
DECLARE existe_pgvector BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') INTO existe_pgvector;

    IF existe_pgvector THEN
        EXECUTE 'ALTER TABLE fragmentos_documento ADD COLUMN IF NOT EXISTS embedding vector(1024)';
    ELSE
        EXECUTE 'ALTER TABLE fragmentos_documento ADD COLUMN IF NOT EXISTS embedding double precision[]';
    END IF;
END $$;

-- =============================================================
-- Paso 5: Crear índice vectorial HNSW (si pgvector está disponible)
-- =============================================================

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        EXECUTE 'CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw ' ||
                'ON documentos USING hnsw (embedding vector_cosine_ops)';
    END IF;
END $$;

-- =============================================================
-- Paso 6: Comentarios
-- =============================================================

COMMENT ON COLUMN tramites.area_responsable IS
    'Oficina o área municipal que tramita el procedimiento (HU-07).';

-- =============================================================
-- Verificación final
-- =============================================================

SELECT 'Migración completada exitosamente' AS status;
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;
