-- =============================================================
-- seeds/documentos.sql
-- Documentos oficiales de la Municipalidad Provincial de Huancayo.
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
     'Municipalidad Provincial de Huancayo. Requiere el certificado de nacimiento del '
     'establecimiento de salud, DNI de la madre y DNI del padre (si está disponible). '
     'El trámite es inmediato y la partida se entrega el mismo día. Arancel según TUPA '
     'vigente (ver TUPA 2023, N.º 188).',
     'https://www.munihuancayo.gob.pe/tupa/inscripcion-nacimiento',
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
     'https://www.munihuancayo.gob.pe/tupa/certificado-residencia',
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
     'https://www.munihuancayo.gob.pe/tupa/licencia-funcionamiento',
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
     'https://www.munihuancayo.gob.pe/tupa/licencia-edificacion',
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
     'https://www.munihuancayo.gob.pe/tupa/certificado-no-adeudo',
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
'https://www.munihuancayo.gob.pe/tupa/inscripcion-defuncion',
      'vigente',
      NULL),

    -- Asignación de Numeración Municipal (TUPA 2023, N.º 42)
    ('22222222-0000-0000-0000-000000000042',
     '11111111-aaaa-2222-3333-444444444444',
     'Asignación de Numeración Municipal - Requisitos',
     'La asignación de numeración municipal ubica oficialmente el acceso principal del '
     'predio. Se presenta solicitud, DNI y croquis de ubicación; el personal técnico '
     'realiza la verificación en campo y emite su conformidad. Plazo de atención: 7 días '
     'hábiles. Arancel según TUPA 2023 (N.º 42).',
     'https://www.munihuancayo.gob.pe/tupa/numeracion-municipal',
      'vigente',
      NULL),

    -- Certificado de Posesión (TUPA 2023, N.º 233)
    ('22222222-0000-0000-0000-000000000233',
     '11111111-bbbb-2222-3333-444444444444',
     'Certificado de Posesión - Requisitos y verificación',
     'El Certificado de Posesión acredita la posesión legítima de un terreno o inmueble. '
     'Se presenta solicitud, DNI y croquis; el área técnica verifica en campo la posesión '
     'continua y pacífica. Plazo de atención: 5 días hábiles. Arancel según TUPA 2023 '
     '(N.º 233).',
     'https://www.munihuancayo.gob.pe/tupa/certificado-posesion',
      'vigente',
      NULL),

    -- Zonificación y Compatibilidad de Uso (TUPA 2023, N.º 34)
    ('22222222-0000-0000-0000-000000000034',
     '11111111-cccc-2222-3333-444444444444',
     'Certificado de Zonificación y Compatibilidad de Uso',
     'Certifica la zonificación vigente del predio y la compatibilidad del giro o actividad '
     'solicitada con el uso de suelo permitido. Se presenta solicitud, DNI, plano de '
     'ubicación y descripción de la actividad. Plazo de atención: 5 días hábiles. Arancel '
     'según TUPA 2023 (N.º 34).',
     'https://www.munihuancayo.gob.pe/tupa/zonificacion-compatibilidad',
      'vigente',
      NULL),

    -- Parámetros Urbanísticos (TUPA 2023, N.º 36)
    ('22222222-0000-0000-0000-000000000036',
     '11111111-dddd-2222-3333-444444444444',
     'Certificado de Parámetros Urbanísticos y Edificatorios',
     'Fija los parámetros urbanísticos del predio: retiros, altura máxima, coeficiente de '
     'edificación y porcentaje de área libre. Se presenta solicitud, DNI, título de '
     'propiedad y plano de ubicación. Plazo de atención: 8 días hábiles. Arancel según TUPA '
     '2023 (N.º 36).',
     'https://www.munihuancayo.gob.pe/tupa/parametros-urbanisticos',
      'vigente',
      NULL),

    -- Habilitación Urbana (TUPA 2023, N.º 27)
    ('22222222-0000-0000-0000-000000000027',
     '11111111-eeee-2222-3333-444444444444',
     'Aprobación de Habilitación Urbana - Modalidades',
     'Para habilitar terrenos se presenta solicitud, título de propiedad y planos de '
     'habilitación, evaluados en modalidades A (previos) o B-C (con aportes) según el tipo '
     'de habilitación (residencial, comercial o industrial). Plazo de 30 a 45 días hábiles '
     'según modalidad. Arancel según TUPA 2023 (N.º 27).',
     'https://www.munihuancayo.gob.pe/tupa/habilitacion-urbana',
      'vigente',
      NULL),

    -- Declaratoria de Fábrica (TUPA 2023, N.º 47)
    ('22222222-0000-0000-0000-000000000047',
     '11111111-ffff-2222-3333-444444444444',
     'Declaratoria de Fábrica - Regularización',
     'La declaratoria de fábrica registra las edificaciones existentes y sus áreas '
     'construidas ante SUNARP. Se presenta solicitud, título de propiedad, planos y memoria '
     'descriptiva firmados por el profesional responsable. Plazo de atención: 15 días '
     'hábiles. Arancel según TUPA 2023 (N.º 47).',
     'https://www.munihuancayo.gob.pe/tupa/declaratoria-fabrica',
      'vigente',
      NULL),

    -- Anuncios y Publicidad Exterior (TUPA 2023, N.º 52)
    ('22222222-0000-0000-0000-000000000052',
     '11111111-1111-aaaa-2222-333333333333',
     'Autorización de Anuncios y Publicidad Exterior',
     'Permiso para instalar paneles, carteles, letreros y anuncios publicitarios en '
     'fachadas o vía pública. Se presenta solicitud, DNI, croquis de ubicación y diseño del '
     'anuncio con dimensiones. Plazo de atención: 7 días hábiles. Arancel según TUPA 2023 '
     '(N.º 52).',
     'https://www.munihuancayo.gob.pe/tupa/anuncios-publicidad',
      'vigente',
      NULL),

    -- Comercio en Mercados y Ambulatorio (TUPA 2023, N.º 118)
    ('22222222-0000-0000-0000-000000000118',
     '11111111-1111-bbbb-2222-333333333333',
     'Autorización de Comercio en Mercados y Ambulatorio',
     'Autoriza el comercio en puestos de mercados municipales o en zonas establecidas para '
     'comercio ambulatorio. Se presenta solicitud, DNI, croquis de ubicación y carné de '
     'sanidad vigente. Plazo de atención: 5 días hábiles. Arancel según TUPA 2023 (N.º 118).',
     'https://www.munihuancayo.gob.pe/tupa/comercio-mercados',
      'vigente',
      NULL),

    -- Eventos Públicos (TUPA 2023, N.º 130)
    ('22222222-0000-0000-0000-000000000130',
     '11111111-1111-cccc-2222-333333333333',
     'Autorización de Eventos Públicos - Seguridad',
     'Para organizar eventos en espacios públicos se presenta solicitud, DNI del '
     'organizador, plan de seguridad (personal, equipos, rutas de evacuación) y seguro '
     'contra accidentes. Plazo de atención: 10 días hábiles. Arancel según TUPA 2023 '
     '(N.º 130).',
     'https://www.munihuancayo.gob.pe/tupa/eventos-publicos',
      'vigente',
      NULL),

    -- Unión de Hecho (TUPA 2023, N.º 205)
    ('22222222-0000-0000-0000-000000000205',
     '11111111-1111-dddd-2222-333333333333',
     'Inscripción de Unión de Hecho - Requisitos',
     'La inscripción de unión de hecho reconoce legalmente la convivencia ante la Oficina '
     'de Registro Civil. Se presenta DNI de ambos convivientes, acta notarial de '
     'reconocimiento, partidas de nacimiento y certificado de domicilio. Plazo de atención: '
     '15 días hábiles. Arancel según TUPA 2023 (N.º 205).',
     'https://www.munihuancayo.gob.pe/tupa/union-de-hecho',
      'vigente',
      NULL),

    -- Empadronamiento Municipal (TUPA 2023, N.º 240)
    ('22222222-0000-0000-0000-000000000240',
     '11111111-1111-eeee-2222-333333333333',
     'Empadronamiento Municipal de Predios y Contribuyentes',
     'Registro actualizado del contribuyente y sus predios para la cobranza de tributos '
     'municipales (impuesto predial y arbitrios). Se presenta solicitud, DNI, título de '
     'propiedad o contrato y última declaración jurada. Plazo de atención: 10 días hábiles. '
     'Sin costo adicional al arancel TUPA 2023 (N.º 240).',
     'https://www.munihuancayo.gob.pe/tupa/empadronamiento',
      'vigente',
      NULL),

    -- Ocupación de Vía Pública (TUPA 2023, N.º 57)
    ('22222222-0000-0000-0000-000000000057',
     '11111111-1111-ffff-2222-333333333333',
     'Autorización de Ocupación de Vía Pública',
     'Permiso temporal para ocupar vía pública con materiales, andamios, canaletas u otras '
     'instalaciones durante una obra. Se presenta solicitud, DNI, plano del área a ocupar y '
     'cronograma. Plazo de atención: 5 días hábiles. Arancel según TUPA 2023 (N.º 57).',
     'https://www.munihuancayo.gob.pe/tupa/ocupacion-via-publica',
      'vigente',
      NULL),

    -- Matrimonio Civil (TUPA 2023, pág. 423)
    ('22222222-0000-0000-0000-000000000201',
     'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
     'Inscripción de Matrimonio Civil - Ceremonia y requisitos',
     'El matrimonio civil se inscribe en la Oficina de Registro Civil; las ceremonias se '
     'programan por la municipalidad. Se presenta DNI de ambos contrayentes, certificado de '
     'nacimiento, certificado de soltería o disponibilidad, certificado de domicilio y dos '
     'testigos con DNI. Plazo de atención: 15 días hábiles desde la programación. Arancel '
     'según TUPA 2023 (N.º 201).',
     'https://www.munihuancayo.gob.pe/tupa/matrimonio-civil',
      'vigente',
      NULL),

    -- Impuesto Predial (TUPA 2023, Tributos)
    ('22222222-0000-0000-0000-000000000109',
     'cccccccc-1111-2222-3333-cccccccccccc',
     'Impuesto Predial - Pago y cronogramas',
     'El impuesto predial se declara y paga en la Gerencia de Administración Tributaria o '
     'en bancos autorizados, al contado (hasta febrero, con descuento) o en cuatro cuotas '
     'trimestrales. Se requiere el código de contribuyente, la declaración jurada del predio '
     'y el DNI del propietario. Vigencia según TUPA 2023 y ordenanza anual de tributos.',
     'https://www.munihuancayo.gob.pe/tributos/impuesto-predial',
      'vigente',
      NULL)
ON CONFLICT (id) DO NOTHING;