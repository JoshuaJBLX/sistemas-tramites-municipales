"""Migrations: expand documentos y agregar fragmentos (HU-02/HU-04)."""

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
    embedding      vector(1024),
    creado_en      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fragmentos_documento ON fragmentos_documento (documento_id);

-- Permitir estado 'derogado' (HU-03) si la restricción lo impide en algunas BD
ALTER TABLE documentos DROP CONSTRAINT IF EXISTS documentos_estado_check;
ALTER TABLE documentos
    ADD CONSTRAINT documentos_estado_check
    CHECK (estado IN ('vigente', 'obsoleto', 'en_revision', 'derogado'));
