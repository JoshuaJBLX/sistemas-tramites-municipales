-- =============================================================
-- seeds/tramites.sql
-- Trámites de la Municipalidad Provincial de Huancayo (MPH).
-- Basados en el TUPA 2023 (252 procedimientos) y la base de
-- conocimiento oficial (H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN).
-- Los costos se citan como arancel TUPA vigente; el monto exacto
-- se publica en el TUPA 2023 (https://www.gob.pe/munihuancayo).
-- =============================================================

INSERT INTO tramites (id, municipalidad_id, nombre, descripcion, tipo, requisitos, costo, duracion_estimada_dias)
VALUES
    -- Registro Civil (TUPA 2023, N.º 188)
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
     '11111111-1111-1111-1111-111111111111',
     'Inscripción de Nacimiento',
     'Registro oficial del nacimiento de una persona ante la Oficina de Registro Civil de la MPH. Trámite inmediato, se realiza el mismo día.',
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
     'Documento que acredita el domicilio de una persona en un sector específico de la provincia de Huancayo.',
     'certificado_domicilio',
     ARRAY['DNI del solicitante', 'Recibo de servicios básicos (luz, agua o teléfono)', 'Solicitud en formato establecido'],
     0.00, 3),

    -- Tributarios (TUPA 2023, N.º 109)
    ('12345678-1234-1234-1234-123456789012',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de No Adeudo',
     'Documento que declara que una persona no tiene deudas pendientes con la Municipalidad Provincial de Huancayo.',
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
     'Autorización para ejecutar obras de construcción, edificación o remodelación en la provincia de Huancayo.',
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
     0.00, 1),

    -- Urbanismo (TUPA 2023, N.º 42)
    ('11111111-aaaa-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Asignación de Numeración Municipal',
     'Asignación de la numeración oficial del predio (puerta u acceso principal) en calles de la provincia de Huancayo.',
     'otro',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante', 'Croquis de ubicación del predio'],
     0.00, 7),

    -- Certificados (TUPA 2023, N.º 233)
    ('11111111-bbbb-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de Posesión',
     'Acredita la posesión de un terreno o inmueble a favor del solicitante, previa verificación en campo.',
     'certificado_domicilio',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante', 'Croquis o acta de verificación de posesión'],
     0.00, 5),

    -- Urbanismo (TUPA 2023, N.º 34)
    ('11111111-cccc-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de Zonificación y Compatibilidad de Uso',
     'Documento que certifica la zonificación del predio y la compatibilidad de la actividad o giro con el uso de suelo permitido.',
     'licencia_construccion',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante', 'Plano de ubicación del predio', 'Descripción de la actividad o giro'],
     0.00, 5),

    -- Urbanismo (TUPA 2023, N.º 36)
    ('11111111-dddd-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Certificado de Parámetros Urbanísticos y Edificatorios',
     'Fija los parámetros urbanísticos y edificatorios aplicables a un predio (retiros, altura, coeficiente, área libre).',
     'licencia_construccion',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante', 'Título de propiedad', 'Plano de ubicación'],
     0.00, 8),

    -- Urbanismo (TUPA 2023, N.º 27)
    ('11111111-eeee-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Aprobación de Habilitación Urbana',
     'Autorización para habilitar terrenos (lotes con servicios) en habilitaciones de tipo residencial, comercial o industrial.',
     'licencia_construccion',
     ARRAY['Solicitud en formato establecido', 'Título de propiedad', 'Planos de habilitación', 'Estudios técnicos y ambientales (según el caso)'],
     0.00, 30),

    -- Urbanismo (TUPA 2023, N.º 47)
    ('11111111-ffff-2222-3333-444444444444',
     '11111111-1111-1111-1111-111111111111',
     'Declaratoria de Fábrica',
     'Registro formal de las edificaciones existentes y sus áreas construidas para regularizar el predio ante SUNARP.',
     'licencia_construccion',
     ARRAY['Solicitud en formato establecido', 'Título de propiedad', 'Planos y memoria descriptiva', 'DNI del propietario'],
     0.00, 15),

    -- Licencias (TUPA 2023, N.º 52)
    ('11111111-1111-aaaa-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Autorización de Anuncios y Publicidad Exterior',
     'Permiso para instalar paneles, carteles y anuncios publicitarios en fachadas o vía pública.',
     'licencia_funcionamiento',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante o empresa', 'Croquis de ubicación', 'Diseño o dimensiones del anuncio'],
     0.00, 7),

    -- Licencias (TUPA 2023, N.º 118)
    ('11111111-1111-bbbb-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Autorización de Comercio en Mercados de Abasto y Ambulatorio',
     'Permiso para comerciar en mercados municipales o como ambulante en zonas autorizadas.',
     'licencia_funcionamiento',
     ARRAY['Solicitud en formato establecido', 'DNI del comerciante', 'Croquis de ubicación', 'Carné de sanidad vigente'],
     0.00, 5),

    -- Otros servicios (TUPA 2023, N.º 130)
    ('11111111-1111-cccc-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Autorización de Eventos Públicos y Actividades Recreativas',
     'Permiso para organizar eventos, ferias, espectáculos y actividades recreativas en espacios públicos.',
     'otro',
     ARRAY['Solicitud en formato establecido', 'DNI del organizador', 'Plan de seguridad del evento', 'Seguro contra accidentes (según el evento)'],
     0.00, 10),

    -- Registro Civil (TUPA 2023, N.º 205)
    ('11111111-1111-dddd-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Inscripción de Unión de Hecho',
     'Reconocimiento legal de la convivencia de dos personas, inscribiendo la unión de hecho ante la Oficina de Registro Civil.',
     'otro',
     ARRAY['DNI de ambos convivientes', 'Acta notarial de reconocimiento', 'Partida de nacimiento de ambos', 'Certificado de domicilio de ambos'],
     0.00, 15),

    -- Tributarios (TUPA 2023, N.º 240)
    ('11111111-1111-eeee-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Empadronamiento Municipal de Predios y Contribuyentes',
     'Registro actualizado del contribuyente y sus predios para el cobro de tributos municipales (predial y arbitrios).',
     'pago_tributos',
     ARRAY['Solicitud en formato establecido', 'DNI del contribuyente', 'Título de propiedad o contrato', 'Última declaración jurada del predio'],
     0.00, 10),

    -- Otros servicios (TUPA 2023, N.º 57)
    ('11111111-1111-ffff-2222-333333333333',
     '11111111-1111-1111-1111-111111111111',
     'Autorización de Ocupación de Vía Pública',
     'Permiso temporal para ocupar vía pública con materiales, andamios, canaletas u otras instalaciones durante una obra.',
     'otro',
     ARRAY['Solicitud en formato establecido', 'DNI del solicitante', 'Plano del área a ocupar', 'Cronograma de la ocupación'],
     0.00, 5)
ON CONFLICT (id) DO NOTHING;