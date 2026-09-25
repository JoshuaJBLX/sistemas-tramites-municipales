-- =============================================================
-- seeds/documentos.sql
-- Documentos oficiales de la Municipalidad Provincial de Junín.
-- Contenido basado en el TUPA 2023 y la base de conocimiento
-- oficial (H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN).
-- El embedding se genera al indexar (BGE-M3 + pgvector).
-- =============================================================

INSERT INTO documentos (id, tramite_id, titulo, contenido, url_origen, estado, embedding)
VALUES
    -- Inscripción de Nacimiento (TUPA 2023, pág. 399)
    ('ffffffff-ffff-ffff-ffff-ffffffffffff',
     'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
     'Inscripción de Nacimiento - Requisitos y plazos',
     'La inscripción de nacimiento se realiza en la Oficina de Registro Civil de la '
     'Municipalidad Provincial de Junín. Requiere el certificado de nacimiento del '
     'establecimiento de salud, DNI de la madre y DNI del padre (si está disponible). '
     'El trámite es inmediato y la partida se entrega el mismo día. Arancel según TUPA '
     'vigente (ver TUPA 2023, N.º 188).',
     'https://www.munijunin.gob.pe/tupa/inscripcion-nacimiento',
     'vigente',
     NULL),

    -- Certificado de Residencia (TUPA 2023, pág. 487)
    ('11111111-2222-3333-4444-555555555555',
     'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
     'Certificado de Residencia - Requisitos',
     'El Certificado de Residencia acredita el domicilio del solicitante. Se presenta '
     'DNI, recibo de servicios básicos (luz, agua o teléfono) y solicitud en formato '
     'establecido. Plazo de atención: 1 a 3 días hábiles. Arancel según TUPA 2023 '
     '(N.º 232).',
     'https://www.munijunin.gob.pe/tupa/certificado-residencia',
     'vigente',
     NULL),

    -- Licencia de Funcionamiento (TUPA 2023)
    ('11111111-3333-4444-5555-666666666666',
     'aaaaaaaa-1111-2222-3333-aaaaaaaaaaaa',
     'Licencia de Funcionamiento - Requisitos y plazo',
     'La licencia de funcionamiento autoriza a operar un negocio o establecimiento. '
     'Se presenta formulario de solicitud, DNI del titular, título de propiedad o '
     'contrato de alquiler, plano de ubicación y plano de diseño (si aplica). '
     'Plazo de 5 a 15 días hábiles según el tipo de actividad. Incluye la '
     'Inspección Técnica de Seguridad en Edificaciones (ITSE) según el nivel de '
     'riesgo del giro. Arancel según TUPA 2023.',
     'https://www.munijunin.gob.pe/tupa/licencia-funcionamiento',
     'vigente',
     NULL),

    -- Licencia de Edificación (TUPA 2023, pág. 58)
    ('11111111-4444-5555-6666-777777777777',
     'bbbbbbbb-1111-2222-3333-bbbbbbbbbbbb',
     'Licencia de Edificación - Modalidades',
     'Para ejecutar obras de construcción se presenta solicitud formal, título de '
     'propiedad, planos arquitectónicos y memoria descriptiva. Se evalúa mediante '
     'las modalidades A (aprobación automática), B, C o D (comisión técnica) según '
     'las características de la obra. Plazo de 10 a 20 días hábiles. Arancel según '
     'TUPA 2023 (N.º 30).',
     'https://www.munijunin.gob.pe/tupa/licencia-edificacion',
     'vigente',
     NULL),

    -- Certificado de No Adeudo (TUPA 2023, pág. 397)
    ('11111111-5555-6666-7777-888888888888',
     '12345678-1234-1234-1234-123456789012',
     'Certificado de No Adeudo - Requisitos',
     'El certificado declara que el solicitante no tiene deudas pendientes con la '
     'municipalidad. Se presenta DNI y solicitud escrita; la Gerencia de '
     'Administración Tributaria verifica en el sistema de tributos. Plazo de 1 a 2 '
     'días hábiles. Arancel según TUPA 2023 (N.º 109).',
     'https://www.munijunin.gob.pe/tupa/certificado-no-adeudo',
     'vigente',
     NULL),

    -- Inscripción de Defunción (TUPA 2023, pág. 463)
    ('11111111-6666-7777-8888-999999999999',
     'cccccccc-cccc-cccc-cccc-cccccccccccc',
     'Inscripción de Defunción - Requisitos',
     'La inscripción de defunción se realiza presentando el certificado de defunción '
     'del establecimiento de salud, el DNI del fallecido y el DNI del declarante. '
     'El trámite es inmediato y se realiza en el mismo día en la Oficina de Registro '
     'Civil. Arancel según TUPA 2023 (N.º 220).',
     'https://www.munijunin.gob.pe/tupa/inscripcion-defuncion',
     'vigente',
     NULL)
ON CONFLICT (id) DO NOTHING;