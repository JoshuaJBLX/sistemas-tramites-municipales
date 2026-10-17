-- 006_auditoria_trazabilidad.sql
-- HU-10 (P3-06 / D-9): trazabilidad completa de la respuesta auditada.
-- `fuentes` conserva las URLs separadas por coma (compatibilidad con lo ya
-- registrado); `fuentes_detalle` guarda el JSON con título, número, fecha,
-- versión y fragmento de cada fuente citada.

ALTER TABLE auditoria_consultas
    ADD COLUMN IF NOT EXISTS groundedness NUMERIC(5, 3),
    ADD COLUMN IF NOT EXISTS fuentes_detalle JSONB,
    ADD COLUMN IF NOT EXISTS fuera_dominio BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS afirmaciones_bloqueadas BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS entidad_sugerida TEXT;

CREATE INDEX IF NOT EXISTS idx_auditoria_consulta_id ON auditoria_consultas (consulta_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_registrado ON auditoria_consultas (registrado_en DESC);
