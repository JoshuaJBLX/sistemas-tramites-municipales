# 05.4 — Herramientas de Desarrollo y DevOps

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

| Herramienta | Rol | Estado real |
|---|---|---|
| Git + GitHub | Control de versiones, colaboración | ✅ Repositorio (commits/estructura) |
| Visual Studio Code | IDE de desarrollo | ✅ (config en repo: `.vscode/` si existe) |
| Docker / Docker Compose | Orquestación de servicios | ✅ 3 servicios: PostgreSQL, Redis, Ollama |
| Python/pip | Entorno backend | ✅ `requirements.txt` |
| Node/npm | Frontend | ✅ `frontend-tramites/package.json` |
| Git clone/instalación | Reproducibilidad | ✅ README con pasos |
| GitHub Actions (CI/CD) | Pipeline | ❌ (G-17) |
| Nexo archivamiento | Backup del repositorio | ❌ (G-17) |

## Evidencia clave
- `docker-compose.yml`: postgres (pgvector/pgvector:pg16), redis (redis:7-alpine), ollama (ollama/ollama:latest).
- `requirements.txt`: fastapi, uvicorn, asyncpg, pgvector, redis, httpx, pydantic[email],
  python-dotenv, sentence-transformers (sin pytest — G-18).