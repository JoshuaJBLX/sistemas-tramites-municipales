# 02.6 — Conocimientos de Computación Aplicados

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 5.1 Algoritmos y estructuras de datos
- ✅ Normalización de texto, clasificación por patrones léxicos, búsqueda vectorial top-k (HNSW).

## 5.2 Bases de datos (relacional + vectorial)
- ✅ PostgreSQL 16 + pgvector (HNSW, `vector_cosine_ops`), asyncpg, migraciones 001-003.
- ✅ Seeds TUPA 2023 MPJ.

## 5.3 Ingeniería de software
- ✅ FastAPI, Pydantic v2, inyección de dependencias (`container.py`), modularidad hexagonal.
- ⚠️ Sin suite de pruebas (G-18).

## 5.4 Arquitectura de software (matriz de selección)
- ✅ Arquitectura hexagonal implementada (a.md: "mejor puntaje"; ver 02 03 / DOCUMENTACION Parte 7).

## 5.5 Inteligencia Artificial y Machine Learning
- ✅ SLM Qwen 2.5 3B (Ollama), embeddings BGE-M3, evaluador de groundedness (confianza).
- ❌ Clasificador ML (G-02), fine-tuning (G-15), dataset de entrenamiento (G-21).

## 5.6 Redes y comunicaciones
- ✅ API REST, CORS (orígenes locales), cliente HTTP a Ollama (httpx).

## 5.7 Seguridad informática
- ✅ SQL parametrizado, validación Pydantic.
- ❌ Autenticación/control de acceso (G-01), prompt-guardrails (G-20).

## 5.8 Sistemas distribuidos y Cloud
- ✅ Docker Compose (3 servicios), Redis cache-aside.
- ⚠️ Sin orquestación de frontend/backend (G-17), sin monitoreo (G-16).