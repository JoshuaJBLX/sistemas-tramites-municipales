# 05.8 — Aplicación Integrada de Herramientas (Flujo de Trabajo)

> Parte de **05 — Uso de herramientas modernas** (AG-I11). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Flujo de trabajo de desarrollo e integración
```
CI 🙂 (GitHub + VS Code + Python/Node)
 │
 ├─ Días educativos: SLM/QA (Qwen, Ollama) + embeddings (BGE-M3)
 │
 ├─ Dev: FastAPI (backend) + Next.js (frontend) — Hot reload local
 │
 ├─ BD: PostgreSQL + pgvector (migraciones) + seeds TUPA 2023
 │
 ├─ Prueba: Endpoints HTTP (manual) + validación Pydantic
 │
 ├─ Distribución: Docker Compose (postgres | redis | ollama)
 │
 └─ Documentación viva: docs/, README, EJECUCION
```
- ❌ Falta la rama CI/CD automatizada (GitHub Actions — G-17).

## Integración en el repositorio (evidencia)
| Paso | Evidencia |
|---|---|
| Código fuente | `backend/`, `frontend-tramites/`, `database/` |
| Dependencias | `requirements.txt`, `package.json` |
| Infra | `docker-compose.yml` |
| Datos | `database/migrations/001-003`, `database/seeds/` |
| Documentación | `README.md`, `00/03-ejecucion.md`, `00/01-historias-de-usuario.md`, `00/02-implementacion-de-historias.md`, `DOCUMENTACION.md` |