-- =============================================================
-- seeds/documentos_mph.sql
-- Documentos de trámites y servicios de la Municipalidad Provincial
-- de Huancayo (MPH), extraídos de los clippings oficiales de gob.pe
-- (https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios).
--
-- Contenido: requisitos, costo, pasos y vigencia de cada trámite.
-- El embedding se genera al indexar (BGE-M3 + pgvector).
--
-- Fuentes:
--   * Clippings del vault H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN\Clippings
--   * https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios
--
-- Es idempotente: usa ON CONFLICT (id) DO NOTHING. No borra filas.
-- =============================================================

INSERT INTO documentos (id, tramite_id, titulo, contenido, url_origen, estado,
                        version, fecha_publicacion, embedding)
VALUES
    -- 1. Mesa de partes virtual (MPH)
    ('c1000000-0000-4000-8000-000000000001',
     'd2000000-0000-4000-8000-000000000001',
     'Mesa de Partes Virtual - Cómo enviar documentos',
     'La mesa de partes virtual de la Municipalidad Provincial de Huancayo permite enviar '
     'documentos para realizar trámites. Requisitos: tener un correo electrónico activo que '
     'permita recibir el cargo de recepción del documento presentado; contar con un número de '
     'teléfono activo; y un archivo en formato PDF no mayor a 10 MB, con un nombre sencillo '
     '(por ejemplo: documento.pdf, oficio.pdf). Se accede a través del portal de trámites '
     'virtuales (sisgedoc.munihuancayo.gob.pe).',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 2. Certificado de Habitabilidad (MPH)
    ('c1000000-0000-4000-8000-000000000002',
     '55db9fae-d137-5196-8d9a-ef168c56a448',
     'Certificado de Habitabilidad - Requisitos y pasos',
     'El Certificado de Habitabilidad acredita que una vivienda cumple con las condiciones '
     'mínimas de seguridad y salubridad para ser habitada. Requisitos: solicitud simple '
     'dirigida al alcalde; número de DNI; copia del documento que acredite la propiedad; '
     'plano de ubicación, localización y distribución con firma del profesional responsable; '
     'e informe de estabilidad de obra y de cumplimiento de normas urbanísticas suscrito por '
     'un arquitecto o ingeniero civil habilitado, si corresponde. Costo: S/ 200.00 en '
     'efectivo. Pasos: 1) dirigirse a la Oficina de Trámite Documentario (lunes a viernes de '
     '8:00 a. m. a 2:30 p. m.) y solicitar la evaluación; 2) pagar en caja; 3) entregar los '
     'documentos junto con el recibo; 4) recoger el certificado en 10 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 3. Licencia de Funcionamiento Temporal (MPH)
    ('c1000000-0000-4000-8000-000000000003',
     '3ad672fe-7bef-5bb4-81de-54f52095b278',
     'Licencia de Funcionamiento Temporal - Requisitos y costo',
     'La licencia de funcionamiento temporal tiene una vigencia de 1 año y no es renovable. '
     'Permite desarrollar cualquier actividad económica comercial, industrial o de servicios. '
     'Requisitos: solicitud de licencia de funcionamiento con carácter de declaración jurada; '
     'formato del reporte de nivel de riesgo del establecimiento; certificado ITSE (si el '
     'riesgo es bajo o medio, puede presentarse hasta 1 mes después de obtener la licencia); '
     'copia de DNI; certificado de vigencia de poder si es persona jurídica; certificado de la '
     'Dirección Regional de Salud o compromiso simple (máximo 60 días) si es giro de salud; '
     'resolución de la Dirección Regional de Salud y título profesional de químico '
     'farmacéutico si es botica, farmacia o droguería; autorización del Ministerio de Cultura '
     'si está en zona monumental. Costo: S/ 173.00. Pasos: 1) acercarse a la mesa de partes '
     'de la Gerencia de Promoción Económica y Turismo (GPET), Jr. Piura 1230, Huancayo, lunes '
     'a viernes de 8:30 a. m. a 2:30 p. m.; 2) pagar en caja; 3) presentar los requisitos con '
     'el recibo; 4) recoger la licencia en 7 días hábiles en el módulo de licencias.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 4. Licencia de Funcionamiento - Riesgo Bajo o Medio (MPH)
    ('c1000000-0000-4000-8000-000000000004',
     'bd5545cc-cdb8-5708-94e3-c98bd436135b',
     'Licencia de Funcionamiento - Riesgo Bajo o Medio (ITSE posterior)',
     'Si la municipalidad clasificó el negocio como de riesgo bajo o medio, se puede solicitar '
     'la licencia de funcionamiento antes de obtener el certificado ITSE, siempre y cuando se '
     'tramite en un plazo máximo de 1 mes; de lo contrario, la licencia será revocada. La '
     'licencia tiene vigencia indeterminada, pero puede solicitarse una temporal (1 año). Es '
     'personal e intransferible. Requisitos: solicitud con declaración jurada; formato lleno '
     'del reporte de nivel de riesgo; copia de DNI; certificado de vigencia de poder si es '
     'persona jurídica; certificado de la Dirección Regional de Salud o compromiso simple '
     '(máximo 60 días) si es giro de salud; resolución de la Dirección Regional de Salud y '
     'título profesional de químico farmacéutico si es botica, farmacia o droguería; y '
     'autorización si está en zona monumental. Costo: riesgo bajo S/ 263.20; riesgo medio '
     'S/ 420.30. Pasos: 1) mesa de partes de la GPET; 2) pagar en caja; 3) presentar '
     'requisitos con el recibo; 4) recoger la licencia en 4 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 5. Licencia de Funcionamiento - Riesgo Alto o Muy Alto (MPH)
    ('c1000000-0000-4000-8000-000000000005',
     'aedd72bd-5a16-5941-bf76-cd5f09e3b107',
     'Licencia de Funcionamiento - Riesgo Alto o Muy Alto (ITSE previa)',
     'Si la municipalidad clasificó el negocio como de riesgo alto o muy alto y ya se cuenta '
     'con el certificado ITSE, se solicita la licencia de funcionamiento. Tiene vigencia '
     'indeterminada; puede solicitarse una temporal (1 año). Es personal e intransferible. '
     'Requisitos: solicitud con declaración jurada; croquis de ubicación; plano de '
     'arquitectura de la distribución existente y detalles del cálculo de aforo; plano de '
     'distribución de tableros eléctricos, diagramas unifilares y cuadro de cargas; '
     'certificado vigente de medición de resistencia del sistema de puesta a tierra; plan de '
     'seguridad del establecimiento; memorias y protocolos de pruebas de operatividad o '
     'mantenimiento de los equipos de seguridad y protección contra incendios; declaración '
     'jurada de contar con título profesional vigente si brinda servicios de salud; '
     'declaración jurada de contar con el número de estacionamientos exigible; declaración '
     'jurada de contar con la autorización sectorial respectiva; y autorización si está en '
     'zona monumental. Costo: riesgo alto S/ 517.50; riesgo muy alto S/ 3,182.10. Pasos: 1) '
     'mesa de partes de la GPET; 2) pagar en caja; 3) presentar requisitos con el recibo; 4) '
     'recoger la licencia en 10 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 6. ITSE - Riesgo Bajo o Medio (MPH)
    ('c1000000-0000-4000-8000-000000000006',
     '6162049f-2887-58b7-9a74-e8e6098a1287',
     'Certificado ITSE - Riesgo Bajo o Medio',
     'El Certificado de Inspección Técnica de Seguridad en Edificaciones (ITSE) tiene una '
     'vigencia de 2 años. Si el negocio es de riesgo bajo o medio y ya se obtuvo la licencia '
     'de funcionamiento, debe solicitarse el ITSE en un plazo máximo de 1 mes; de lo '
     'contrario, la licencia será revocada. Requisitos: solicitud de ITSE; formato para '
     'determinar el nivel de riesgo; croquis del establecimiento; certificado de cumplimiento '
     'de condiciones de seguridad; copia de certificado de extintores; protocolo de '
     'operatividad de extintores; y plan de prevención contra la COVID-19. Se presenta en 2 '
     'juegos originales y 1 en copia. Costo: riesgo bajo S/ 60.00; riesgo medio S/ 130.20. '
     'Pasos: 1) módulo de atención al usuario de la Gerencia de Seguridad Ciudadana; 2) pagar '
     'en caja (primer piso); 3) presentar requisitos en mesa de partes; 4) recoger el '
     'certificado en 9 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 7. ITSE - Riesgo Alto o Muy Alto (MPH)
    ('c1000000-0000-4000-8000-000000000007',
     '8c7658b8-4615-5b31-8f6c-bb1fb579404a',
     'Certificado ITSE - Riesgo Alto o Muy Alto',
     'El Certificado ITSE tiene una vigencia de 2 años. Para riesgo alto o muy alto, primero '
     'debe obtenerse el ITSE antes de la licencia de funcionamiento. Requisitos: solicitud de '
     'ITSE (original y copia); formato para determinar el nivel de riesgo (original y copia); '
     'croquis del establecimiento (original y copia); y documentos técnicos en copia simple '
     'firmados por el profesional o empresa responsable: croquis de ubicación; plano de '
     'arquitectura de la distribución existente y detalles del cálculo de aforo; plano de '
     'distribución de tableros eléctricos, diagramas unifilares y cuadro de cargas; '
     'certificado vigente de medición de resistencia del sistema de puesta a tierra; y plan '
     'de seguridad del establecimiento. Sobre los equipos de seguridad y protección contra '
     'incendios: memorias del sistema de detección y alarma de incendios y de los extintores; '
     'y protocolos de pruebas de operatividad o mantenimiento de rociadores, redes enterradas, '
     'montantes y gabinetes de agua, bombas de agua, luces de emergencia, puertas cortafuego, '
     'sistema de administración de humos, presurización de escaleras, extracción de CO, '
     'teléfono de emergencia en ascensores y teléfono de bomberos. Costo: riesgo alto '
     'S/ 698.10; riesgo muy alto S/ 1,017.90. Pasos: 1) módulo de atención al usuario de la '
     'Gerencia de Seguridad Ciudadana; 2) pagar en caja; 3) presentar requisitos en mesa de '
     'partes; 4) recoger el certificado en 7 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 8. Renovación ITSE (MPH)
    ('c1000000-0000-4000-8000-000000000008',
     '05518daa-1755-56b6-913e-0f7a5f864fde',
     'Renovación de Certificado ITSE - Requisitos y costo',
     'Si se venció el certificado ITSE (riesgo bajo, medio, alto o muy alto), debe solicitarse '
     'su renovación. Si hay cambios en las condiciones de seguridad del establecimiento, debe '
     'realizarse una nueva solicitud de ITSE. El certificado tiene una duración de 2 años. '
     'Requisitos: solicitud de inspección; y declaración jurada para renovación de certificado '
     'ITSE. Se presenta en 2 juegos: 1 original y 1 copia. Costo: riesgo bajo S/ 34.20; '
     'riesgo medio S/ 82.70; riesgo alto S/ 389.50. Pasos: 1) módulo de atención al usuario '
     'de la Gerencia de Seguridad Ciudadana (Prolongación Puno y Jr. José Gálvez, Huancayo); '
     '2) pagar en caja (primer piso); 3) presentar requisitos en mesa de partes; 4) recoger la '
     'renovación en la oficina de Archivos en 5 días hábiles (riesgo alto: 9 días hábiles).',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 9. Carnet de Sanidad (MPH)
    ('c1000000-0000-4000-8000-000000000009',
     'd2000000-0000-4000-8000-000000000002',
     'Carnet de Sanidad - Requisitos y vigencia',
     'El carnet de sanidad certifica que la persona tiene buena salud y trabaja en óptimas '
     'condiciones de higiene, apta para laborar en venta o manipulación de alimentos o atención '
     'al público. Si manipula directamente los alimentos, el carnet tiene vigencia de 6 meses; '
     'si no los manipula directamente, de 1 año. Debe tramitarse uno nuevo cada vez que venza. '
     'Requisitos para personas con nacionalidad peruana: 1 fotografía tamaño carné actual; '
     'muestra del primer esputo del día en ayunas; toma de muestra de sangre; y pago por '
     'derecho S/ 20.00. Para personas con nacionalidad extranjera: copia de carnet de '
     'extranjería o pasaporte; 1 fotografía tamaño carné actual; muestra del primer esputo del '
     'día en ayunas; toma de muestra de sangre; y pago por derecho S/ 20.00.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 10. Carnet de Habilitación de Conductor (MPH)
    ('c1000000-0000-4000-8000-000000000010',
     'd2000000-0000-4000-8000-000000000003',
     'Carnet de Habilitación de Conductor - Requisitos y vigencia',
     'El carnet de habilitación de conductor es para quienes trabajan manejando buses, taxis, '
     'combis u otros vehículos de transporte público. Solo se aceptan licencias de conducir '
     'tipo A-II, A-III y B. La vigencia del carnet es de 1 año; pasado ese tiempo debe '
     'renovarse. Requisitos: solicitud simple dirigida al alcalde (persona natural o jurídica) '
     'con RUC activo e indicando nombre completo, DNI, razón social y domicilio legal; 2 '
     'fotografías a color tamaño carné; copia simple de recibo de luz o agua que acredite el '
     'domicilio actual; copia simple de la licencia de conducir de la categoría '
     'correspondiente; y declaración jurada de no tener antecedentes penales, judiciales ni '
     'policiales (formato libre). Costo: S/ 18.10. Pasos: 1) módulo de atención de la '
     'Gerencia de Tránsito y Transporte (Centro Internacional de Negocios, Jr. Piura 1230, '
     'Huancayo), lunes a viernes de 8:30 a. m. a 2:30 p. m.; 2) pagar en caja del SATH; 3) '
     'presentar requisitos en mesa de partes; 4) apelar observaciones si las hubiera '
     '(reconsideración y, de ser negativa, apelación ante la Gerencia Municipal); 5) recoger el '
     'carnet en 8 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 11. Duplicado de Carnet de Habilitación de Conductor (MPH)
    ('c1000000-0000-4000-8000-000000000011',
     'd2000000-0000-4000-8000-000000000004',
     'Duplicado de Carnet de Habilitación de Conductor',
     'Si se perdió, fue robado o se deterioró el carnet de habilitación de conductor, puede '
     'pedirse una copia o duplicado. La vigencia del documento es de 1 año. Requisitos: '
     'solicitud simple dirigida al alcalde (persona natural o jurídica) con RUC activo e '
     'indicando nombre completo, DNI, razón social y domicilio legal; 1 fotografía a color '
     'tamaño carné; y copia simple de la licencia de conducir vigente. Costo: S/ 18.10. '
     'Pasos: 1) módulo de atención de la Gerencia de Tránsito y Transporte; 2) pagar en caja '
     'del SATH; 3) presentar requisitos en mesa de partes; 4) recoger el duplicado en 3 días '
     'hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 12. Tarjeta Única de Circulación - TUC (MPH)
    ('c1000000-0000-4000-8000-000000000012',
     'd2000000-0000-4000-8000-000000000005',
     'Tarjeta Única de Circulación (TUC) - Requisitos y vigencia',
     'La Tarjeta Única de Circulación (TUC) aplica para buses, combis y otros medios de '
     'transporte de personas, a excepción de taxis. Su vigencia es de 1 año; pasado ese '
     'tiempo debe renovarse. Requisitos: solicitud simple dirigida al alcalde, bajo '
     'declaración jurada, con RUC activo e indicando nombre completo, DNI, número de teléfono '
     'fijo o celular, correo electrónico y domicilio legal. Costo: S/ 63.00. Pasos: 1) módulo '
     'de atención de la Gerencia de Tránsito y Transporte (Centro Internacional de Negocios, '
     'Jr. Piura 1230, Huancayo), lunes a viernes de 8:30 a. m. a 2:30 p. m.; 2) pagar en caja '
     'del SATH; 3) presentar requisitos en mesa de partes; 4) apelar observaciones si las '
     'hubiera; 5) recoger la TUC en 8 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 13. Registro de Nacimiento (MPH)
    ('c1000000-0000-4000-8000-000000000013',
     'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
     'Registro de Nacimiento - Requisitos y gratuidad',
     'Si se tiene un hijo recién nacido, debe registrarlo en cualquiera de las oficinas '
     'registrales del RENIEC a nivel nacional. Si no hay una cerca de la localización, puede '
     'hacerse en la municipalidad para obtener el acta o partida de nacimiento por primera vez. '
     'Este procedimiento es gratuito y permite que el hijo disfrute de todos los beneficios de '
     'ser ciudadano peruano, como obtener su DNI o acceder a programas sociales. No es '
     'necesario llevar al bebé para la inscripción. El plazo de inscripción es de 60 días '
     'para recién nacidos en establecimientos de salud públicos o privados, y de 90 días '
     'calendario para centros poblados y comunidades nativas. Requisitos para el registro de '
     'un nacimiento ordinario: certificado de nacido vivo original y copia; y presencia de '
     'ambos padres con sus DNI. Para el registro extemporáneo de un mayor de edad: formato de '
     'inscripción debidamente llenado; constancia negativa de inscripción de nacimiento de la '
     'municipalidad del lugar donde nació; declaración jurada de domicilio; y presencia de '
     'dos testigos con sus DNI.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 14. Partida de Nacimiento (MPH)
    ('c1000000-0000-4000-8000-000000000014',
     'dddddddd-1111-2222-3333-dddddddddddd',
     'Partida de Nacimiento - Copia certificada',
     'La copia certificada de un acta de nacimiento tiene validez legal, pues certifica que la '
     'copia es igual al original. Cualquier peruano mayor de edad puede pedir la partida de '
     'nacimiento de otro ciudadano, siempre que tenga la información de registro y pague el '
     'derecho de trámite, salvo que la entidad establezca otros requisitos. Si se tiene un '
     'hijo recién nacido, debe registrarse en la municipalidad para obtener su primera '
     'partida, la cual es gratuita. Requisitos: número de DNI; e información de registro: '
     'nombres y apellidos que figuran en el acta o partida, y año del nacimiento.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 15. Partida de Matrimonio (MPH)
    ('c1000000-0000-4000-8000-000000000015',
     'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
     'Partida de Matrimonio - Copia certificada',
     'La copia certificada de una partida de matrimonio tiene validez legal, pues certifica que '
     'la copia es igual al original. Cualquier peruano mayor de edad puede pedir la partida de '
     'matrimonio de otro ciudadano, siempre que tenga la información de registro y pague el '
     'derecho de trámite, salvo que la entidad establezca otros requisitos. Requisitos: DNI '
     'original; e información de registro: nombres y apellidos que figuran en el acta o '
     'partida, y año del matrimonio.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 16. Partida de Defunción (MPH)
    ('c1000000-0000-4000-8000-000000000016',
     'cccccccc-cccc-cccc-cccc-cccccccccccc',
     'Partida de Defunción - Copia certificada',
     'El acta o partida de defunción es el documento legal y oficial donde se constata el día, '
     'la hora y el lugar del deceso, así como los nombres, número de DNI, edad y lugar y fecha '
     'de nacimiento del fallecido. La copia certificada tiene validez legal. Cualquier persona '
     'peruana mayor de edad puede pedir la copia de un acta de defunción, siempre que tenga '
     'la información de registro y pague el derecho de trámite, salvo que la entidad '
     'establezca otros requisitos. Si un familiar falleció, debe obtenerse la primera '
     'partida de fallecimiento, la cual es gratuita. Requisitos: DNI original; e información '
     'de registro: nombres y apellidos que figuran en el acta o partida, y año del '
     'fallecimiento.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 17. Copia certificada de partida o acta (MPH)
    ('c1000000-0000-4000-8000-000000000017',
     'dddddddd-1111-2222-3333-dddddddddddd',
     'Copia certificada de partida o acta de nacimiento, matrimonio o defunción',
     'La copia certificada de una partida o acta de nacimiento, matrimonio o defunción tiene '
     'validez legal, pues certifica que la copia emitida es igual al original presentado. '
     'Cualquier peruano mayor de edad puede pedir la copia de un acta de otro ciudadano, '
     'siempre que tenga la información de registro y cancele el derecho de trámite. Puede '
     'solicitarse de manera presencial en la Oficina de Registro Civil de la municipalidad '
     'donde fue inscrita, u online si esta se encuentra registrada en la entidad.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 18. Copia de videos de cámaras de seguridad (MPH)
    ('c1000000-0000-4000-8000-000000000018',
     'd2000000-0000-4000-8000-000000000006',
     'Copia de videos de cámaras de seguridad',
     'Si se necesita la grabación de imágenes o videos captados por cámaras de vigilancia del '
     'distrito, para seguimiento de faltas o delitos, puede solicitarse a la municipalidad, '
     'según el Decreto Legislativo N° 1218 que regula el uso de las cámaras de videovigilancia '
     '(artículos 6 y 7). Requisitos: solicitud simple dirigida al Gerente de Seguridad '
     'Ciudadana; denuncia policial según corresponda; y portar un dispositivo de '
     'almacenamiento (DVD, memoria USB o disco duro externo).',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 19. Transferencia de Licencia de Funcionamiento (MPH)
    ('c1000000-0000-4000-8000-000000000019',
     '1aaf0f3f-9b4f-55b5-aa19-4a04e13c2afa',
     'Transferencia de Licencia de Funcionamiento o Cambio de Nombre Comercial',
     'Si se tiene una licencia de funcionamiento a nombre propio y necesita transferirla a otra '
     'persona, natural o jurídica, debe solicitarse en la municipalidad. La licencia es la '
     'autorización que otorga la municipalidad para iniciar las actividades de comercio, '
     'industria o servicios. La solicitud será aprobada siempre que el negocio mantenga el giro '
     'autorizado y la zonificación. Este procedimiento es el mismo para los casos de cambio de '
     'denominación o nombre comercial de la persona jurídica. Requisitos: solicitud con '
     'carácter de declaración jurada; y copia simple del contrato de transferencia. Costo: '
     'S/ 200.00. Pasos: 1) mesa de partes de la GPET; 2) pagar en caja; 3) presentar '
     'requisitos con el recibo; 4) recoger la licencia en 2 días hábiles.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL)
ON CONFLICT (id) DO NOTHING;
