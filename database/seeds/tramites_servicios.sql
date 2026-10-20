-- =============================================================
-- seeds/tramites_servicios.sql
-- Servicios de la Municipalidad Provincial de Huancayo (MPH) que
-- no forman parte del TUPA 2023 pero aparecen en el listado
-- oficial de trámites y servicios de gob.pe.
--
-- Fuente: https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios
--          y clippings oficiales (H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN\Clippings).
--
-- Es idempotente: usa ON CONFLICT (id) DO UPDATE. No borra filas.
-- =============================================================

INSERT INTO tramites (id, municipalidad_id, nombre, descripcion, tipo, requisitos, costo, duracion_estimada_dias, area_responsable)
VALUES
    ('d2000000-0000-4000-8000-000000000001',
     '11111111-1111-1111-1111-111111111111',
     'Mesa de Partes Virtual',
     'Servicio para enviar documentos y realizar trámites a través de la mesa de partes virtual de la Municipalidad Provincial de Huancayo.',
     'servicio',
     ARRAY['Correo electrónico activo para recibir el cargo de recepción', 'Número de teléfono activo', 'Archivo en PDF no mayor a 10 MB con nombre sencillo']::text[],
     0.00, 1, 'Mesa de Partes'),

    ('d2000000-0000-4000-8000-000000000002',
     '11111111-1111-1111-1111-111111111111',
     'Carnet de Sanidad',
     'Certificado que acredita buena salud y condiciones de higiene para laborar en venta o manipulación de alimentos o atención al público. Vigencia: 6 meses (manipula alimentos) o 1 año (no manipula).',
     'servicio',
     ARRAY['1 fotografía tamaño carné actual', 'Muestra del primer esputo del día en ayunas', 'Toma de muestra de sangre', 'Pago por derecho S/ 20.00']::text[],
     20.00, 1, 'Gerencia de Salud'),

    ('d2000000-0000-4000-8000-000000000003',
     '11111111-1111-1111-1111-111111111111',
     'Carnet de Habilitación de Conductor',
     'Habilitación para conductores de buses, taxis, combis u otros vehículos de transporte público. Solo licencias A-II, A-III y B. Vigencia: 1 año.',
     'servicio',
     ARRAY['Solicitud simple con RUC activo', '2 fotografías a color tamaño carné', 'Copia de recibo de luz o agua', 'Copia de licencia de conducir (A-II, A-III o B)', 'Declaración jurada de no tener antecedentes']::text[],
     18.10, 8, 'Gerencia de Tránsito y Transporte'),

    ('d2000000-0000-4000-8000-000000000004',
     '11111111-1111-1111-1111-111111111111',
     'Duplicado de Carnet de Habilitación de Conductor',
     'Copia o duplicado del carnet de habilitación de conductor en caso de pérdida, robo o deterioro. Vigencia: 1 año.',
     'servicio',
     ARRAY['Solicitud simple con RUC activo', '1 fotografía a color tamaño carné', 'Copia de licencia de conducir vigente']::text[],
     18.10, 3, 'Gerencia de Tránsito y Transporte'),

    ('d2000000-0000-4000-8000-000000000005',
     '11111111-1111-1111-1111-111111111111',
     'Tarjeta Única de Circulación (TUC)',
     'Tarjeta para vehículos de transporte público (buses, combis; excepto taxis). Vigencia: 1 año.',
     'servicio',
     ARRAY['Solicitud simple bajo declaración jurada con RUC activo', 'Nombre completo, DNI, teléfono, correo y domicilio legal']::text[],
     63.00, 8, 'Gerencia de Tránsito y Transporte'),

    ('d2000000-0000-4000-8000-000000000006',
     '11111111-1111-1111-1111-111111111111',
     'Copia de Videos de Cámaras de Seguridad',
     'Grabación de imágenes o videos captados por cámaras de vigilancia para seguimiento de faltas o delitos, según el Decreto Legislativo N° 1218.',
     'servicio',
     ARRAY['Solicitud simple dirigida al Gerente de Seguridad Ciudadana', 'Denuncia policial según corresponda', 'Dispositivo de almacenamiento (DVD, USB o disco duro externo)']::text[],
     0.00, 5, 'Gerencia de Seguridad Ciudadana')
ON CONFLICT (id) DO UPDATE SET
    nombre = EXCLUDED.nombre,
    descripcion = EXCLUDED.descripcion,
    tipo = EXCLUDED.tipo,
    requisitos = EXCLUDED.requisitos,
    costo = EXCLUDED.costo,
    duracion_estimada_dias = EXCLUDED.duracion_estimada_dias,
    area_responsable = EXCLUDED.area_responsable;
