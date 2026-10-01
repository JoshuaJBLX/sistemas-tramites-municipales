# EJECUCIÓN LOCAL

> Verificado en Windows 11 (octubre 2026) con servicios nativos, sin Docker.

## 1. Instalar (una sola vez)

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```

El script es **idempotente**: se puede repetir sin romper nada. Hace todo lo necesario:

| # | Paso | Resultado |
|---|------|-----------|
| 1 | Verifica herramientas | Python, PostgreSQL, Node.js, Ollama (Redis opcional) |
| 2 | Crea `.env` | A partir de `.env.example` |
| 3 | Prepara la base de datos | Rol, base, migraciones y seeds |
| 4 | Instala Python | Entorno `.venv` + `requirements.txt` |
| 5 | Instala el front-end | `npm install` |
| 6 | Levanta Redis y Ollama | Descarga `qwen2.5:3b` |
| 7 | Genera embeddings | BGE-M3 sobre los 20 documentos |

Parametros útiles:

```powershell
.\instalar.ps1 -PostgresPassword 'mi_clave'   # superusuario de PostgreSQL
.\instalar.ps1 -SinIndexar                   # omite el paso 7 (el RAG quedará sin documentos)
```

## 2. Ejecutar (cada vez)

```powershell
# API
.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000
```

```powershell
# Front-end, en otra terminal
cd frontend-tramites; npm run dev
```

- API <http://localhost:8000> · Swagger <http://localhost:8000/docs> · App <http://localhost:3000>
- Comprobar: `curl http://localhost:8000/health` → `{"status":"ok"}`
- Una consulta RAG tarda ~5-9 s; las repetidas salen de la caché en ~30 ms.