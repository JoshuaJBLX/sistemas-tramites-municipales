# Guía de Despliegue en Render

Esta guía explica cómo desplegar el backend del Sistema de Trámites Municipales en Render.

## Arquitectura de Despliegue

```
Frontend (Next.js)    → Vercel
Backend (FastAPI)     → Render
PostgreSQL + pgvector → Supabase
Redis                 → Upstash
Storage (documentos)  → Supabase Storage
LLM (Ollama/Groq)     → Render o API externa
```

## Paso 1: Preparar Supabase

### 1.1 Crear proyecto en Supabase
1. Ve a https://supabase.com y crea un nuevo proyecto
2. Espera a que el proyecto esté listo (~2 minutos)

### 1.2 Habilitar pgvector
1. En el dashboard de Supabase, ve a **SQL Editor**
2. Ejecuta:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 1.3 Ejecutar migraciones
**IMPORTANTE**: En Supabase, ejecuta las migraciones directamente en el SQL Editor (NO uses psql local).

**OPCIÓN A - MÁS FÁCIL (Recomendada):**
1. En el dashboard de Supabase, ve a **SQL Editor**
2. Copia y ejecuta el archivo: `database/migrations/supabase_complete_setup.sql`
3. Este archivo contiene TODAS las migraciones en uno solo
4. Verifica que al final veas: "Migración completada exitosamente"

**OPCIÓN B - Paso a paso:**
Si prefieres ejecutar las migraciones individualmente:

```
1. database/migrations/001_supabase_setup.sql  (USAR ESTA, NO la 001)
2. database/migrations/002_create_tables.sql
3. database/migrations/003_create_vectors.sql
4. database/migrations/004_documentos_pmv2.sql
5. database/migrations/005_area_responsable.sql
6. database/migrations/006_auditoria_trazabilidad.sql
```

**NOTA**: La migración `001_create_database.sql` original NO funciona en Supabase porque usa comandos de `psql` (\gexec, \c). Usa `001_supabase_setup.sql` o `supabase_complete_setup.sql` en su lugar.

### 1.4 Crear bucket de Storage
1. En Supabase, ve a **Storage**
2. Crea un bucket llamado `documentos`
3. Configura las políticas según tu necesidad (público o privado)

### 1.5 Obtener credenciales
1. Ve a **Settings → API**
2. Copia:
   - `Project URL` → `SUPABASE_URL`
   - `anon public` → `SUPABASE_ANON_KEY`
   - `service_role` → `SUPABASE_SERVICE_ROLE_KEY`
3. Ve a **Settings → Database**
4. Copia la **Connection String** (usa la de pooling) → `DATABASE_URL`

## Paso 2: Preparar Upstash Redis

### 2.1 Crear cuenta en Upstash
1. Ve a https://upstash.com
2. Crea una cuenta gratuita
3. Crea un nuevo Redis database

### 2.2 Obtener Redis URL
1. En tu database de Upstash, ve a **Details**
2. Copia la **REST API URL** → `REDIS_URL`

## Paso 3: Preparar API de LLM

**IMPORTANTE**: Ya he preparado el código para usar OpenRouter automáticamente.

### Opción A: OpenRouter (RECOMENDADO)
1. Ve a https://openrouter.ai
2. Crea cuenta y obtén API Key
3. En variables de entorno de Render:
   - `OPENROUTER_API_KEY=sk-or-...`
   - `OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct`

**Modelos recomendados para español:**
- `meta-llama/llama-3-8b-instruct` - Económico y bueno
- `mistralai/mistral-7b-instruct` - Excelente para español
- `meta-llama/llama-3-70b-instruct` - Más potente

### Opción B: Ollama local (solo desarrollo)
- NO usar en Render (recursos limitados)
- Solo para desarrollo local
- Variables: `OLLAMA_URL`, `OLLAMA_MODEL`

### Opción C: Groq (cuando esté disponible)
- Similar a OpenRouter
- Variables: `GROQ_API_KEY`, `GROQ_MODEL`

## Paso 4: Desplegar Backend en Render

### 4.1 Preparar el repositorio
1. Asegúrate de que tu código está en GitHub
2. Confirma los cambios de configuración:
```bash
git add backend/requirements.txt backend/render.yaml backend/main.py backend/.render.env
git commit -m "Preparar despliegue en Render"
git push
```

### 4.2 Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con tu cuenta de GitHub

### 4.3 Crear Web Service
1. En Render, haz clic en **New + → Web Service**
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Name**: `tramites-municipales-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Plan: **Free** (o Starter si necesitas más recursos)

### 4.4 Configurar variables de entorno
1. En la sección **Environment** del Web Service
2. Agrega las variables (usa `.render.env` como referencia):

```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
SUPABASE_URL=https://[REF].supabase.co
SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
SUPABASE_SERVICE_ROLE_KEY=[YOUR-SERVICE-ROLE-KEY]
REDIS_URL=redis://default:[PASSWORD]@[HOST].upstash.io:6379
CACHE_TTL_SEGUNDOS=3600
OPENROUTER_API_KEY=sk-or-[YOUR-OPENROUTER-KEY]
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct
EMBEDDING_MODEL=BAAI/bge-m3
EMBEDDING_DEVICE=cpu
RAG_TOP_K=5
SUPABASE_STORAGE_URL=https://[REF].supabase.co/storage/v1
SUPABASE_STORAGE_BUCKET=documentos
VERCEL_FRONTEND_URL=https://tu-proyecto.vercel.app  # Lo agregarás después
```

### 4.5 Desplegar
1. Haz clic en **Create Web Service**
2. Render construirá y desplegará tu aplicación
3. Espera a que el estado sea **Live**

### 4.6 Verificar despliegue
1. Ve a la URL de tu servicio (ej: `https://tramites-municipales-backend.onrender.com`)
2. Visita `/health` → debería retornar `{"status": "ok"}`
3. Visita `/docs` → deberías ver la documentación de FastAPI

## Paso 5: Desplegar Frontend en Vercel

### 5.1 Preparar frontend
1. En `frontend-tramites/`, actualiza `lib/api.ts`:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
```

### 5.2 Desplegar en Vercel
1. Ve a https://vercel.com
2. Importa tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `frontend-tramites`
   - **Framework Preset**: Next.js
4. Agrega variable de entorno:
   - `NEXT_PUBLIC_API_BASE_URL=https://tramites-municipales-backend.onrender.com`
5. Deploy

### 5.3 Actualizar CORS en Backend
1. Regresa a Render
2. Agrega la variable `VERCEL_FRONTEND_URL` con tu dominio de Vercel
3. Render hará redeploy automático

## Paso 6: Migrar Storage Local a Supabase Storage

**IMPORTANTE**: Render borra archivos locales en cada deploy. Ya he preparado el código para usar Supabase Storage automáticamente.

### 6.1 Cambios ya realizados
El código ya está adaptado:
- ✅ Creado `DocumentStorageAdapterSupabase.py` (adaptador para Supabase Storage)
- ✅ Actualizado `container.py` para usar Supabase Storage automáticamente cuando se configuran las variables de entorno
- ✅ Agregado `supabase==2.5.0` a `requirements.txt`

### 6.2 Cómo funciona
En `backend/infrastructure/container.py`, el contenedor detecta automáticamente:

```python
# Si configuras SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY, usa Supabase Storage
if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SERVICE_ROLE_KEY'):
    almacenamiento = DocumentStorageAdapterSupabase()
else:
    almacenamiento = DocumentStorageAdapter()  # Almacenamiento local
```

**No necesitas modificar más código**. Solo configura las variables de entorno en Render.

## Troubleshooting

### Error: "Out of memory"
- sentence-transformers + Ollama pesan mucho
- Solución: Usa Groq/OpenRouter para LLM (ya configurado en .render.env)
- Para embeddings, considera usar OpenAI API si sentence-transformers falla

### Error: "Connection refused" a PostgreSQL
- Verifica que `DATABASE_URL` tenga formato correcto
- En Supabase, usa connection string con pooling
- Asegúrate de que `sslmode=require` esté en la URL

### Error: "CORS policy"
- Verifica que `VERCEL_FRONTEND_URL` esté configurada en Render
- Revisa el log del backend para ver qué dominios se permiten
- El código ahora lee esta variable automáticamente

### Timeout en builds
- Render free plan tiene 15 min de build
- Si sentence-transformers tarda mucho, considera:
  - Usar plan paid ($7/mes)
  - Migrar a API de embeddings (OpenAI, Cohere)

### Error: "Storage bucket not found"
- Verifica que el bucket `documentos` exista en Supabase Storage
- Verifica que `SUPABASE_STORAGE_BUCKET` tenga el nombre correcto
- Revisa las políticas de acceso del bucket

## Costos Estimados

| Servicio | Plan | Costo |
|----------|------|-------|
| Render Backend | Free | $0 (spin down) |
| Render Backend | Starter | $7/mes (always on) |
| Supabase | Free | $0 (500MB) |
| Upstash Redis | Free | $0 (10K commands/day) |
| Groq | Free | $0 (hasta ciertos límites) |
| Vercel Frontend | Free | $0 |

**Total mínimo**: $0/mes (con limitaciones)
**Total recomendado**: ~$7/mes (Render Starter para backend always on)

## Recursos

- Render Docs: https://render.com/docs
- Supabase Docs: https://supabase.com/docs
- Upstash Docs: https://upstash.com/docs
- Groq Console: https://console.groq.com
