-- Migración PMV2: expande documentos y crea la tabla de fragmentos (HU-02/HU-04).

-- Agregar metadatos a documentos
ALTER TABLE documentos
    ADD COLUMN IF NOT EXISTS version VARCHAR(20) NOT NULL DEFAULT '1.0',
    ADD COLUMN IF NOT EXISTS fecha_publicacion DATE,
    ADD COLUMN IF NOT EXISTS archivo_nombre VARCHAR(255),
    ADD COLUMN IF NOT EXISTS mime_type VARCHAR(100),
    ADD COLUMN IF NOT EXISTS hash_contenido VARCHAR(128),
    ADD COLUMN IF NOT EXISTS fragmentado BOOLEAN NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS eliminado_en TIMESTAMPTZ;

-- Tabla de fragmentos para RAG con chunking (HU-04)
CREATE TABLE IF NOT EXISTS fragmentos_documento (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    documento_id   UUID NOT NULL REFERENCES documentos (id) ON DELETE CASCADE,
    orden          INT NOT NULL,
    contenido      TEXT NOT NULL,
    creado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Columna de embedding: vector(1024) con pgvector, double precision[] sin él
-- (mismo criterio que 002_create_tables.sql para la tabla documentos).
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

CREATE INDEX IF NOT EXISTS idx_fragmentos_documento ON fragmentos_documento (documento_id);

-- Permitir estado 'derogado' (HU-03) si la restricción lo impide en algunas BD
-- Primero eliminamos la restricción si existe (idempotente)
ALTER TABLE documentos DROP CONSTRAINT IF EXISTS documentos_estado_check;

-- Luego la recreamos con el valor correcto
ALTER TABLE documentos
    ADD CONSTRAINT documentos_estado_check
    CHECK (estado IN ('vigente', 'obsoleto', 'en_revision', 'derogado'));
