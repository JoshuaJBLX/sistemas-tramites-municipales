# Migraciones para Supabase

Este directorio contiene las migraciones de base de datos adaptadas para Supabase.

## 📋 Archivos disponibles

### Para despliegue en Supabase (Render/Vercel)

1. **`supabase_complete_setup.sql`** ⭐ (RECOMENDADO)
   - Contiene TODAS las migraciones en un solo archivo
   - Ejecutar una sola vez en el SQL Editor de Supabase
   - Crea: extensiones, tablas, índices, columnas, embeddings
   - Idempotente: puedes ejecutarlo varias veces sin errores

2. **`001_supabase_setup.sql`**
   - Solo habilita la extensión `vector`
   - Para uso con migraciones individuales (002-006)

### Migraciones individuales (para desarrollo local PostgreSQL)

- `001_create_database.sql` - Para PostgreSQL local (NO usar en Supabase)
- `002_create_tables.sql` - Tablas base
- `003_create_vectors.sql` - Índices vectoriales
- `004_documentos_pmv2.sql` - Metadatos de documentos y fragmentos
- `005_area_responsable.sql` - Área responsable de trámites
- `006_auditoria_trazabilidad.sql` - Auditoría y trazabilidad

## 🚀 Cómo usar en Supabase

### Opción A: Migración completa (recomendada)

1. Ve al dashboard de Supabase
2. Abre el **SQL Editor**
3. Copia el contenido de `supabase_complete_setup.sql`
4. Pega en el editor
5. Haz clic en **Run**
6. Verifica que veas: "Migración completada exitosamente"

### Opción B: Migraciones individuales

1. Ejecuta `001_supabase_setup.sql` primero
2. Luego ejecuta `002_create_tables.sql`
3. Continúa con `003`, `004`, `005`, `006` en orden

## ⚠️ Diferencias con PostgreSQL local

| Aspecto | PostgreSQL local | Supabase |
|---------|------------------|----------|
| Crear base de datos | ✅ Sí (001) | ❌ No (ya existe) |
| Comandos psql (\gexec, \c) | ✅ Sí | ❌ No |
| Extensión vector | Manual | Manual (001) |
| Tablas y columnas | Igual | Igual |
| Índices vectoriales | Igual | Igual |

## 🔍 Verificación

Después de ejecutar las migraciones, verifica:

```sql
-- Verificar extensión vector
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Verificar tablas creadas
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Verificar columnas de embedding
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('documentos', 'fragmentos_documento')
AND column_name = 'embedding';
```

## 🛠️ Solución de problemas

### Error: "extension vector already exists"
- Ya ejecutaste `001_supabase_setup.sql` antes
- Ejecuta `supabase_complete_setup.sql` (tiene `IF NOT EXISTS`)

### Error: "column already exists"
- Las migraciones usan `IF NOT EXISTS` para ser idempotentes
- Si persiste, verifica qué columnas ya existen

### Error: "relation already exists"
- Las tablas usan `IF NOT EXISTS`
- Puedes ejecutar `supabase_complete_setup.sql` varias veces

## 📝 Notas técnicas

- Todas las migraciones usan `IF NOT EXISTS` para ser idempotentes
- Los índices vectoriales HNSW requieren pgvector >= 0.5.0
- Supabase usa pgvector por defecto en todos los proyectos
- Los embeddings se guardan como `vector(1024)` con pgvector, o `double precision[]` sin él
