-- =============================================================
-- 001_supabase_setup.sql
-- Configuración inicial para Supabase (NO crea base de datos, ya existe)
-- Ejecutar en el SQL Editor de Supabase
-- =============================================================

-- NOTA: En Supabase NO necesitas crear la base de datos.
-- Supabase ya te proporciona una base de datos llamada "postgres".
-- Este script solo habilita las extensiones necesarias.

-- Extensión de vectores para búsqueda semántica (RAG con pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar que la extensión esté instalada
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
