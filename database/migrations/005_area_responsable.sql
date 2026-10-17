-- Migración PMV1/HU-07: área responsable de cada trámite.
-- Permite derivar al ciudadano hacia la oficina competente cuando la
-- confianza de la respuesta es baja o el asistente no resuelve la consulta.

ALTER TABLE tramites
    ADD COLUMN IF NOT EXISTS area_responsable VARCHAR(120);

COMMENT ON COLUMN tramites.area_responsable IS
    'Oficina o área municipal que tramita el procedimiento (HU-07).';
