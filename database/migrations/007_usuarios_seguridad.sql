-- =============================================================
-- Migración 007 — Seguridad (HU-13 / G-01)
-- Contraseñas hasheadas, control de actividad y eventos de
-- seguridad (intentos de acceso y accesos denegados).
-- =============================================================

-- Contraseña hasheada (PBKDF2-SHA256). NULL solo para usuarios
-- heredados sin credenciales: no pueden iniciar sesión.
ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS password_hash VARCHAR(200),
    ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE,
    ADD COLUMN IF NOT EXISTS ultimo_acceso_en TIMESTAMPTZ;

-- Registro de eventos de seguridad (HU-13, escenario 2):
-- login fallido, acceso denegado, token inválido, etc.
CREATE TABLE IF NOT EXISTS eventos_seguridad (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id       UUID REFERENCES usuarios (id) ON DELETE SET NULL,
    correo           VARCHAR(150),
    evento           VARCHAR(40) NOT NULL,
    detalle          TEXT,
    ip               VARCHAR(60),
    registrado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_eventos_seguridad_evento
    ON eventos_seguridad (evento, registrado_en DESC);
