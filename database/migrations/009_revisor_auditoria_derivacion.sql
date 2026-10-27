-- =============================================================
-- Migración 009 — Rol revisor (HU-03), auditoría con marcado
-- (HU-14) y directorio de oficinas para derivación (HU-17)
-- =============================================================

-- HU-03: el revisor municipal aprueba, modifica, deroga o desactiva
-- documentos. Se amplía el CHECK de roles de usuarios.
ALTER TABLE usuarios DROP CONSTRAINT IF EXISTS usuarios_rol_check;
ALTER TABLE usuarios ADD CONSTRAINT usuarios_rol_check
    CHECK (rol IN ('ciudadano', 'revisor', 'administrador'));

-- HU-14: marcado manual de registros inconsistentes para revisión técnica
-- (el marcado automático —sin fuente o sin evaluación— se calcula en el query).
ALTER TABLE auditoria_consultas
    ADD COLUMN IF NOT EXISTS marcado_inconsistente BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS nota_revision         TEXT,
    ADD COLUMN IF NOT EXISTS marcado_en            TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS marcado_por           VARCHAR(200);

-- HU-17: directorio de oficinas municipales para derivar al ciudadano cuando
-- el sistema no puede responder de forma confiable. Los datos de contacto son
-- de referencia y se actualizan desde este mismo archivo.
CREATE TABLE IF NOT EXISTS oficinas (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre      VARCHAR(200) NOT NULL UNIQUE,
    area        VARCHAR(200) NOT NULL,
    telefono    VARCHAR(60),
    correo      VARCHAR(200),
    horario     VARCHAR(120) NOT NULL DEFAULT 'Lun–Vie 8:00–17:30',
    direccion   VARCHAR(300) NOT NULL DEFAULT 'Jr. Puno s/n, Huancayo',
    responsable VARCHAR(200),
    activa      BOOLEAN NOT NULL DEFAULT TRUE,
    creada_en   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO oficinas (nombre, area, telefono, correo, horario, direccion, responsable)
VALUES (
        'Mesa de Partes Central',
        'Atención y recepción de expedientes',
        '(064) 211-800',
        'mesadepartes@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Jefe de Mesa de Partes'
    ), (
        'Gerencia de Administración Tributaria',
        'Tributos, tasas y aranceles municipales',
        '(064) 211-820',
        'tributos@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Gerente de Administración Tributaria'
    ), (
        'Gerencia de Desarrollo Urbano e Infraestructura',
        'Licencias, obras, zonificación y declaratorias de fábrica',
        '(064) 211-830',
        'desarrollourbano@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Gerente de Desarrollo Urbano'
    ), (
        'Sub Gerencia de Registro Civil',
        'Partidas, certificados y actos de estado civil',
        '(064) 211-840',
        'registrocivil@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Sub Gerente de Registro Civil'
    ), (
        'Gerencia de Servicios Sociales',
        'Programas sociales, alimentación y apoyo comunal',
        '(064) 211-850',
        'servicossociales@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Gerente de Servicios Sociales'
    ), (
        'Oficina de Atención al Ciudadano',
        'Orientación, quejas, sugerencias y derivaciones',
        '(064) 211-810',
        'atencionalciudadano@munihuancayo.gob.pe',
        'Lun–Vie 8:00–17:30',
        'Jr. Puno s/n, Huancayo',
        'Jefe de Atención al Ciudadano'
    )
ON CONFLICT (nombre) DO NOTHING;
