-- =============================================================
-- Migración 008 — Retroalimentación y métricas (HU-15 / HU-16 / HU-18)
-- =============================================================

-- HU-15: el ciudadano califica la utilidad de la respuesta
-- (útil / parcialmente útil / no útil) con comentario opcional.
-- Una sola calificación vigente por consulta (la recalificación la actualiza).
CREATE TABLE IF NOT EXISTS evaluaciones_calidad (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id    UUID NOT NULL REFERENCES consultas (id) ON DELETE CASCADE,
    valoracion     VARCHAR(20) NOT NULL
        CHECK (valoracion IN ('util', 'parcialmente_util', 'no_util')),
    comentario     TEXT,
    creada_en      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    actualizada_en TIMESTAMPTZ
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_evaluaciones_consulta
    ON evaluaciones_calidad (consulta_id);

CREATE INDEX IF NOT EXISTS idx_evaluaciones_creada
    ON evaluaciones_calidad (creada_en DESC);

-- HU-16/HU-18: la auditoría pasa a registrar también el tiempo de
-- generación (ms) y el trámite probable, para métricas y reportes.
ALTER TABLE auditoria_consultas
    ADD COLUMN IF NOT EXISTS duracion_ms      INT,
    ADD COLUMN IF NOT EXISTS tramite_probable VARCHAR(200);
