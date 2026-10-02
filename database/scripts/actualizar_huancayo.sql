-- Corrige la entidad: el catálogo decía "Junín" y corresponde a Huancayo.
BEGIN;

UPDATE municipalidades
SET nombre = 'Municipalidad Provincial de Huancayo',
    departamento = 'Junín',
    provincia = 'Huancayo',
    distrito = 'Huancayo',
    sitio_web = 'http://www.munihuancayo.gob.pe/';

UPDATE tramites
SET nombre = replace(nombre, 'Junín', 'Huancayo'),
    descripcion = replace(descripcion, 'Junín', 'Huancayo')
WHERE nombre ILIKE '%Jun%' OR descripcion ILIKE '%Jun%';

UPDATE documentos
SET titulo = replace(titulo, 'Junín', 'Huancayo'),
    contenido = replace(contenido, 'Junín', 'Huancayo'),
    url_origen = replace(replace(url_origen, 'munijunin.gob.pe', 'munihuancayo.gob.pe'), 'junin.gob.pe', 'huancayo.gob.pe')
WHERE titulo ILIKE '%Jun%' OR contenido ILIKE '%Jun%' OR url_origen ILIKE '%junin%';

COMMIT;