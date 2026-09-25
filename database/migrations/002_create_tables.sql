-- =============================================================
-- 002_create_tables.sql
-- Tablas del dominio: municipalidades, usuarios, tramites,
-- documentos, consultas y auditoria.
-- Ejecutar conectado a la BD: psql -d tramites_municipales -f database/migrations/002_create_tables.sql
-- =============================================================

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS municipalidades (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre       VARCHAR(200) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    provincia    VARCHAR(100) NOT NULL,
    distrito     VARCHAR(100) NOT NULL,
    sitio_web    VARCHAR(500),
    creado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS usuarios (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre    VARCHAR(150) NOT NULL,
    correo    VARCHAR(150) NOT NULL UNIQUE,
    rol       VARCHAR(30) NOT NULL CHECK (rol IN ('ciudadano', 'administrador')),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tramites (
    id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    municipalidad_id       UUID NOT NULL REFERENCES municipalidades (id) ON DELETE CASCADE,
    nombre                 VARCHAR(200) NOT NULL,
    descripcion            TEXT NOT NULL,
    tipo                   VARCHAR(60) NOT NULL,
    requisitos             TEXT[] NOT NULL DEFAULT '{}',
    costo                  NUMERIC(10, 2) NOT NULL DEFAULT 0,
    duracion_estimada_dias INT NOT NULL DEFAULT 0,
    creado_en              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documentos (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tramite_id     UUID NOT NULL REFERENCES tramites (id) ON DELETE CASCADE,
    titulo         VARCHAR(300) NOT NULL,
    contenido      TEXT NOT NULL,
    url_origen     VARCHAR(500) NOT NULL,
    estado         VARCHAR(20) NOT NULL DEFAULT 'vigente'
                   CHECK (estado IN ('vigente', 'obsoleto', 'en_revision')),
    embedding      vector(1024),
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consultas (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID REFERENCES usuarios (id) ON DELETE SET NULL,
    pregunta   TEXT NOT NULL,
    intencion  VARCHAR(50),
    creada_en  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS auditoria_consultas (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    consulta_id    UUID NOT NULL REFERENCES consultas (id) ON DELETE CASCADE,
    respuesta      TEXT,
    confianza      VARCHAR(20) CHECK (confianza IN ('alta', 'media', 'baja')),
    fuentes        TEXT,
    registrado_en  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices de apoyo para las consultas frecuentes.
CREATE INDEX IF NOT EXISTS idx_tramites_municipalidad ON tramites (municipalidad_id);
CREATE INDEX IF NOT EXISTS idx_documentos_tramite     ON documentos (tramite_id);
CREATE INDEX IF NOT EXISTS idx_documentos_estado      ON documentos (estado);
CREATE INDEX IF NOT EXISTS idx_consultas_usuario      ON consultas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_consultas_creada_en    ON consultas (creada_en DESC);