-- =============================================================
-- 003_create_vectors.sql
-- Índices vectoriales (pgvector) para la búsqueda semántica RAG.
-- Requiere pgvector >= 0.5.0 para HNSW.
-- =============================================================

-- Índice HNSW por similitud de coseno (recomendado).
-- Solo se crea cuando la extensión vector está disponible; en servidores sin
-- pgvector el mapeo cae a `double precision[]` y la búsqueda se resuelve en Python.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        EXECUTE 'CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw ' ||
                'ON documentos USING hnsw (embedding vector_cosine_ops)';
    END IF;
END $$;

-- Alternativa (pgvector < 0.5.0): índice IVFFlat.
-- CREATE INDEX IF NOT EXISTS idx_documentos_embedding_ivfflat
--     ON documentos USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Índice GIN para filtrar por tipo de trámite si se usan etiquetas.
CREATE INDEX IF NOT EXISTS idx_tramites_tipo ON tramites (tipo);