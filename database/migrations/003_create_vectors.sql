-- =============================================================
-- 003_create_vectors.sql
-- Índices vectoriales (pgvector) para la búsqueda semántica RAG.
-- Requiere pgvector >= 0.5.0 para HNSW.
-- =============================================================

-- Índice HNSW por similitud de coseno (recomendado).
CREATE INDEX IF NOT EXISTS idx_documentos_embedding_hnsw
    ON documentos USING hnsw (embedding vector_cosine_ops);

-- Alternativa (pgvector < 0.5.0): índice IVFFlat.
-- CREATE INDEX IF NOT EXISTS idx_documentos_embedding_ivfflat
--     ON documentos USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Índice GIN para filtrar por tipo de trámite si se usan etiquetas.
CREATE INDEX IF NOT EXISTS idx_tramites_tipo ON tramites (tipo);