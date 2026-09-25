-- =============================================================
-- seeds/tramites.sql
-- Trámites de la Municipalidad Provincial de Junín (MPJ).
-- Basados en el TUPA 2023 (252 procedimientos) y la base de
-- conocimiento oficial (H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN).
-- Los costos se citan como arancel TUPA vigente; el monto exacto
-- se publica en el TUPA 2023 (https://www.gob.pe/munijunin).
-- =============================================================

INSERT INTO tramites (id, municipalidad_id, nombre, descripcion, tipo, requisitos, costo, duracion_estimada_dias)
VALUES
    -- Registro Civil (TUPA 2023, N.º 188)
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
     '11111111-1111-1111-1111-111111111111',
     'Inscripción de Nacimiento',
     'Registro oficial del nacimiento de una persona ante la Oficina de Registro Civil de la MPJ. Trámite inmediato, se realiza el mismo día.',
     'partida_nacimiento',
     ARRAY['Certificado de nacimiento del establecimiento de salud', 'DNI de la madre', 'DNI del padre (si está disponible)'],
     0.00, 1),

    -- Registro Civil (TUPA 2023, N.º 201)
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
     '11111111-1111-1111-1111-111111111111',
     'Inscripción de Matrimonio',
     'Registro oficial del matrimonio civil. Las ceremonias se realizan en fechas programadas por la Oficina de Registro Civil.',
     'otro',
     ARRAY['DNI de ambos contrayentes', 'Certificado de nacimiento de ambos', 'Certificado de soltería o disponibilidad', 'Certificado de domicilio', 'Dos testigos con DNI'],
     0.00, 15),

    -- Registro Civil (TUPA 2023, N.º 220)
    ('cccccccc-cccc-cccc-cccc-cccccccccccc',
     '11111111-1111-1111-1111-111111111111',
     'Inscripción de Defunción',
     'Registro oficial del fallecimiento de una persona. Trámite inmediato ante la Oficina de Registro Civil.',
     'otro',
     ARRAY['Certificado de defunción del establecimiento de salud', 'DNI del fallecido', 'DNI del declarante'],
     0.00, 1),

    -- Registro Civil (TUPA 2023, N.º 212)
    ('dddddddd-dddd-dddd-dddd-dddddddddddd',
     '11111111-1111-1111-1111-111111111111',
     'Separación Convencional',
     'Declaración de separación de cónyuges de manera consensuada, sin necesidad de juicio judicial.',
     'otro',
     ARRAY['DNI de ambos cónyuges', 'Partida de matrimonio', 'Convenio de separación'],
     0.00, 10),

    -- Certificados (TUPA 2023, N.º 232)
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de Residencia',
     'Documento que acredita el domicilio de una persona en un sector específico de la provincia de Junín.',
     'certificado_domicilio',
     ARRAY['DNI del solicitante', 'Recibo de servicios básicos (luz, agua o teléfono)', 'Solicitud en formato establecido'],
     0.00, 3),

    -- Tributarios (TUPA 2023, N.º 109)
    ('12345678-1234-1234-1234-123456789012',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de No Adeudo',
     'Documento que declara que una persona no tiene deudas pendientes con la Municipalidad Provincial de Junín.',
     'pago_tributos',
     ARRAY['DNI del solicitante', 'Solicitud escrita', 'Verificación en el sistema de tributos'],
     0.00, 2),

    -- Licencias (TUPA 2023, N.º 9/11/13/15)
    ('aaaaaaaa-1111-2222-3333-aaaaaaaaaaaa',
     '11111111-1111-1111-1111-111111111111',
     'Licencia de Funcionamiento',
     'Autorización para operar un negocio o establecimiento. Incluye ITSE según el nivel de riesgo del giro.',
     'licencia_funcionamiento',
     ARRAY['Formulario de solicitud', 'DNI del titular', 'Título de propiedad o contrato de alquiler', 'Plano de ubicación', 'Plano de diseño (si aplica)'],
     0.00, 15),

    -- Urbanismo (TUPA 2023, N.º 30)
    ('bbbbbbbb-1111-2222-3333-bbbbbbbbbbbb',
     '11111111-1111-1111-1111-111111111111',
     'Licencia de Edificación',
     'Autorización para ejecutar obras de construcción, edificación o remodelación en la provincia de Junín.',
     'licencia_construccion',
     ARRAY['Solicitud formal', 'Título de propiedad', 'Planos arquitectónicos', 'Memoria descriptiva', 'Estudio de suelos (si aplica)'],
     0.00, 20),

    -- Tributarios
    ('cccccccc-1111-2222-3333-cccccccccccc',
     '11111111-1111-1111-1111-111111111111',
     'Pago de Impuesto Predial',
     'Declaración y pago del impuesto predial. Se paga en ventanilla de la municipalidad o en bancos autorizados.',
     'pago_tributos',
     ARRAY['Código de contribuyente', 'Declaración jurada del predio', 'DNI del propietario'],
     0.00, 1),

    -- Identidad (TUPA 2023, N.º 194)
    ('dddddddd-1111-2222-3333-dddddddddddd',
     '11111111-1111-1111-1111-111111111111',
     'Expedición de Partida de Nacimiento',
     'Emisión de partida o copia certificada de nacimiento para trámites civiles y escolares.',
     'partida_nacimiento',
     ARRAY['DNI del solicitante', 'Fecha del registro de nacimiento'],
     0.00, 1)
ON CONFLICT (id) DO NOTHING;