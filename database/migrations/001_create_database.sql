-- =============================================================
-- 001_create_database.sql
-- Crea la base de datos y habilita la extensión pgvector.
-- Ejecutar con: psql -U postgres -f database/migrations/001_create_database.sql
-- =============================================================

-- Crear la base de datos (si no existe).
SELECT 'CREATE DATABASE tramites_municipales'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tramites_municipales')\gexec

-- Conectarse a la base de datos recién creada.
\c tramites_municipales

-- Extensión de vectores para búsqueda semántica (RAG).
CREATE EXTENSION IF NOT EXISTS vector;