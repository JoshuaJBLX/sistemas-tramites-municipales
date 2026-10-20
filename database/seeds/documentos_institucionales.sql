-- =============================================================
-- seeds/documentos_institucionales.sql
-- Contenido institucional de la Municipalidad Provincial de Huancayo
-- (MPH) para la base documental de referencia (RAG).
--
-- Fuentes:
--   * https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios
--     (catálogo oficial de 19 trámites y servicios, 2 páginas)
--   * https://www.gob.pe/institucion/munihuancayo/contacto-y-numeros-de-emergencias
--   * Clippings oficiales (H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN\Clippings):
--     Portal de Transparencia Estándar, Texto Único de Procedimientos
--     Administrativos.
--
-- Nota: documentos.tramite_id es NOT NULL, por lo que este archivo crea
-- además un servicio institucional ("Información institucional y contacto")
-- al que se vinculan los documentos generales. Los documentos de canales en
-- línea y de transparencia se vinculan a servicios/trámites existentes.
--
-- Es idempotente: usa ON CONFLICT. No borra filas.
-- El embedding se genera al indexar (BGE-M3 + pgvector).
-- =============================================================

-- -------------------------------------------------------------
-- 1. Servicio institucional (vehículo para los documentos generales)
-- -------------------------------------------------------------
INSERT INTO tramites (id, municipalidad_id, nombre, descripcion, tipo, requisitos, costo, duracion_estimada_dias, area_responsable)
VALUES
    ('d2000000-0000-4000-8000-000000000007',
     '11111111-1111-1111-1111-111111111111',
     'Información institucional y contacto',
     'Consulta de información institucional de la Municipalidad Provincial de Huancayo: catálogo de trámites y servicios, sedes, horarios de atención, canales en línea, números de emergencia, transparencia y TUPA.',
     'servicio',
     '{}'::text[],
     0.00, 0, 'OFICINA DE ATENCIÓN AL CIUDADANO')
ON CONFLICT (id) DO UPDATE SET
    nombre = EXCLUDED.nombre,
    descripcion = EXCLUDED.descripcion,
    tipo = EXCLUDED.tipo,
    requisitos = EXCLUDED.requisitos,
    costo = EXCLUDED.costo,
    duracion_estimada_dias = EXCLUDED.duracion_estimada_dias,
    area_responsable = EXCLUDED.area_responsable;

-- -------------------------------------------------------------
-- 2. Documentos institucionales
-- -------------------------------------------------------------
INSERT INTO documentos (id, tramite_id, titulo, contenido, url_origen, estado,
                        version, fecha_publicacion, embedding)
VALUES
    -- 1. Catálogo oficial de trámites y servicios (gob.pe, 19 resultados)
    ('c1000000-0000-4000-8000-000000000020',
     'd2000000-0000-4000-8000-000000000007',
     'Catálogo de trámites y servicios de la Municipalidad Provincial de Huancayo',
     'Catálogo oficial de trámites y servicios publicado por la Municipalidad Provincial de '
     'Huancayo en gob.pe (19 resultados). 1) Acceder a la mesa de partes virtual: enviar '
     'documentos para realizar trámites desde el portal virtual. 2) Certificado de '
     'Habitabilidad: certificado de habitabilidad de la vivienda. 3) Obtener licencia de '
     'funcionamiento temporal en Huancayo: licencia temporal para negocios. 4) Obtener o '
     'renovar carnet de habilitación de conductor en Huancayo: para quienes conducen buses, '
     'taxis, combis u otros vehículos de transporte público. 5) Licencia de funcionamiento '
     'para establecimientos de riesgo alto o muy alto. 6) Certificado de Inspección Técnica '
     'de Seguridad en Edificaciones (ITSE) para establecimientos de riesgo alto o muy alto. '
     '7) Renovación del ITSE para establecimientos de riesgo bajo o medio. 8) Licencia de '
     'funcionamiento para establecimientos de riesgo bajo o medio. 9) Realizar el registro '
     'de nacimiento: inscribir a un hijo recién nacido en las oficinas registrales. 10) '
     'Renovar el Certificado de Inspección Técnica de Seguridad en Edificaciones: cuando se '
     'venció el ITSE de cualquier nivel de riesgo. 11) Sacar Carnet de Sanidad en el distrito '
     'de Huancayo: para quienes venden o manipulan alimentos o prestan servicios de '
     'atención. 12) Solicitar acta de nacimiento, matrimonio y/o defunción: copia certificada '
     'de partida o acta. 13) Solicitar duplicado de carnet de habilitación de conductor: por '
     'pérdida, robo o deterioro. 14) Solicitar una copia de los videos de las cámaras de '
     'seguridad de la municipalidad. 15) Solicitar una partida de defunción. 16) Solicitar '
     'una partida de matrimonio. 17) Solicitar una partida de nacimiento. 18) Transferir o '
     'modificar información en licencia de funcionamiento: transferirla a otra persona o '
     'cambiar el nombre comercial. 19) Solicitar la Tarjeta Única de Circulación (TUC) en '
     'Huancayo: para vehículos de transporte público. Para requisitos, costo, plazos y pasos '
     'de cada trámite consulta el documento específico de ese trámite en esta base de '
     'conocimiento. El listado completo y actualizado está en la página de trámites y '
     'servicios de gob.pe.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 2. Contacto, sedes y horarios
    ('c1000000-0000-4000-8000-000000000021',
     'd2000000-0000-4000-8000-000000000007',
     'Contacto, sedes y horarios de atención de la Municipalidad Provincial de Huancayo',
     'Sede Central - Palacio Municipal: Calle Real #800 (Plaza Huamanmarca), Huancayo, Junín, '
     'Perú, código postal 12001. Horario de atención de oficinas: lunes a viernes de 8:00 a. '
     'm. a 1:00 p. m. y de 3:00 p. m. a 5:45 p. m. Horario de atención de mesa de partes: de '
     'lunes a viernes de 8:00 a. m. a 5:45 p. m. Otras sedes: Biblioteca Municipal, Centro '
     'Internacional de Negocios, Centro Médico Municipal, Centro de Monitoreo de '
     'Videovigilancia y el Instituto de la Juventud y Cultura. Redes sociales oficiales: '
     'Facebook (munhuancayo), Instagram (muni_huancayo), YouTube y TikTok (@munihuancayo). '
     'Ayuda por WhatsApp: 948595958. Para reclamos formales usa el libro de reclamaciones en '
     'línea y para trámites presenciales verifica primero si el trámite puede hacerse en la '
     'mesa de partes virtual.',
     'https://www.gob.pe/institucion/munihuancayo/contacto-y-numeros-de-emergencias',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 3. Números de emergencia
    ('c1000000-0000-4000-8000-000000000022',
     'd2000000-0000-4000-8000-000000000007',
     'Números de emergencia de Huancayo',
     'Números de emergencia y atención de urgencias en Huancayo: Comisaría PNP Huancayo: '
     '064-211637. Compañía de Bomberos: 064-211020 y 064-221324. Serenazgo Huancayo: '
     '064-202050. Centro Veterinario Municipal: 940 349 958 (Prolongación Puno y Jr. José '
     'Galvez, Huancayo). Estos números corresponden a instituciones de la ciudad; para '
     'reclamos, quejas o sugerencias a la municipalidad usa el libro de reclamaciones en '
     'línea, y para denunciar actos de corrupción de funcionarios usa el portal de denuncias '
     'de gob.pe.',
     'https://www.gob.pe/institucion/munihuancayo/contacto-y-numeros-de-emergencias',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 4. Canales en línea y servicios digitales
    ('c1000000-0000-4000-8000-000000000023',
     'd2000000-0000-4000-8000-000000000001',
     'Canales en línea y servicios digitales de la Municipalidad Provincial de Huancayo',
     'Canales digitales oficiales de la MPH: Mesa de partes virtual (envío de documentos para '
     'trámites): sisgedoc.munihuancayo.gob.pe:8083/tramitevirtualHyo/. Seguimiento de '
     'trámites presentados: sisgedoc.munihuancayo.gob.pe:8080/sisgedoc_seguimiento. Libro de '
     'reclamaciones en línea: reclamos.servicios.gob.pe/?institution_id=291. Denuncia de '
     'actos de corrupción de funcionarios de la entidad: '
     'denuncias.servicios.gob.pe/?gobpe_id=2063. Acceso a la información pública (plataforma '
     'Facilita del Estado): facilita.gob.pe/t/15033. Texto Único de Procedimientos '
     'Administrativos (TUPA) y sus modificaciones: gob.pe/institucion/munihuancayo/'
     'informes-publicaciones/1050892. Convocatorias y trabajo en la municipalidad: '
     'gob.pe/institucion/munihuancayo/colecciones/4695-convocatorias-de-trabajo. Consulta de '
     'información de transparencia: gob.pe/institucion/munihuancayo/pages/60655.',
     'https://www.gob.pe/institucion/munihuancayo/tramites-y-servicios',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 5. Portal de Transparencia Estándar
    ('c1000000-0000-4000-8000-000000000024',
     '8d00d343-db53-55c8-8f51-540aa9169532',
     'Portal de Transparencia Estándar de la Municipalidad Provincial de Huancayo',
     'Portal de Transparencia de la Municipalidad Provincial de Huancayo (id de entidad 1190). '
     'Responsable del Portal de Transparencia: Ing. José Carlos Cuba Castillo (Resolución de '
     'Alcaldía N.° 023-2023-MPH/A), correo jcuba@munihuancayo.gob.pe, teléfono 064-600408. '
     'Responsable de acceso a la información: Abg. José Lutz Alvino Arge (Resolución de '
     'Alcaldía N.° 023-2023-MPH/A), correo jalvino@munihuancayo.gob.pe, teléfono 064-600408. '
     'El portal publica la información pública de compras estatales, laudos arbitrales y '
     'transparencia (Art. 25 del TUO de la Ley N.° 27806, Ley de Transparencia y Acceso a la '
     'Información Pública, D.S. N.° 021-2019-JUS). Mayor información en https://www.gob.pe/oece/. '
     'Para solicitar información pública se usa además la plataforma Facilita '
     '(facilita.gob.pe/t/15033).',
     'https://www.transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad=1190',
     'vigente', '1.0', DATE '2026-10-19', NULL),

    -- 6. TUPA de la MPH
    ('c1000000-0000-4000-8000-000000000025',
     'd2000000-0000-4000-8000-000000000007',
     'Texto Único de Procedimientos Administrativos (TUPA) de la Municipalidad Provincial de Huancayo',
     'El Texto Único de Procedimientos Administrativos (TUPA) es el documento normativo que '
     'concentra los procedimientos administrativos municipales con sus requisitos, plazos, '
     'aranceles y unidades responsables. La Municipalidad Provincial de Huancayo publica su '
     'TUPA y sus modificaciones en gob.pe (informes-publicaciones/1050892). El TUPA vigente '
     '2023 de Huancayo agrupa 252 procedimientos administrativos por área (desarrollo '
     'urbano, tributos, registro civil, transporte, entre otros). Los costos y plazos '
     'oficiales de cada trámite deben consultarse en el TUPA; los valores publicados en este '
     'sistema provienen de ese TUPA. El TUPA reemplaza a los reglamentos anteriores y debe '
     'estar disponible de forma gratuita en la sede central y en el portal de transparencia.',
     'https://www.gob.pe/institucion/munihuancayo/informes-publicaciones/1050892-texto-unico-de-procedimientos-administrativos-tupa-y-modificaciones',
     'vigente', '1.0', DATE '2026-10-19', NULL)
ON CONFLICT (id) DO NOTHING;
