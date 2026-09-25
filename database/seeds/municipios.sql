-- =============================================================
-- seeds/municipios.sql
-- Municipalidad Provincial de Junín (Código Gob.pe: 12088).
-- Fuente: https://www.gob.pe/munijunin
-- =============================================================

INSERT INTO municipalidades (id, nombre, departamento, provincia, distrito, sitio_web)
VALUES
    ('11111111-1111-1111-1111-111111111111',
     'Municipalidad Provincial de Junín',
     'Junín', 'Junín', 'Junín', 'http://www.munijunin.gob.pe/')
ON CONFLICT (id) DO NOTHING;