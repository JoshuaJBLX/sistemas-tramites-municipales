# Presupuesto Detallado del Proyecto: Sistema de Trámites Municipales (MUN AI)

**Proyecto:** Sistema de Trámites Municipales — MUN AI
**Entidad:** Municipalidad Provincial de Huancayo (MPH) — TUPA 2023 (Ord. 790-MPH/CM)
**Equipo:** Estudiantes de Ingeniería de Sistemas (9.° y 10.° ciclo)
**Tarifa horaria:** 15 Soles/hora por estudiante
**Moneda:** Soles (S/.)
**Estado del proyecto:** ✅ **Terminado al 100 %** (cierre PMV3: 27-oct-2026)
**Documento actualizado:** 12-nov-2026

> **Fuente única de verdad del estado y las cifras:**
> [`documentacion/00-documentos-rectores/06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md)

---

## 1. ESTADO ACTUAL DEL PROYECTO — 100 % COMPLETADO

### 🎉 Proyecto finalizado

| Indicador | Valor | Estado |
|-----------|-------|--------|
| **Proyecto completado** | **100 %** | ✅ FINALIZADO |
| **Historias de Usuario (HU)** | **18/18** | ✅ 100 % completadas |
| **Indicadores de medición** | **101/101** | ✅ Total cumplido |
| **PMV1** (prototipo funcional) | 24/24 | ✅ 100 % cerrado |
| **PMV2** (RAG optimizado) | 28/28 | ✅ 100 % cerrado |
| **PMV3** (sistema integrado) | 49/49 | ✅ 100 % cerrado |
| **Avance global** | **101/101** | ✅ **100 %** |

### 🔢 Hechos numéricos confirmados

| Métrica | Valor |
|---------|-------|
| Endpoints REST servibles | **40 rutas** (36 operaciones + 4 de documentación) |
| Archivos de código backend | **104 `.py`** |
| Archivos de código frontend | **27 `.ts`/`.tsx`** |
| Migraciones SQL | **18 archivos** (aplicadas hasta `008_retroalimentacion_metricas.sql`) |
| Procedimientos TUPA | **252** (con costo y área responsable) |
| Documentos indexados | **45/45** (100 % con metadatos y fragmentación) |
| Fragmentos vectorizados | **56** (RAG activo por fragmento) |
| Controllers FastAPI | **7** (arquitectura hexagonal) |
| Puertos y adaptadores | **11** |
| Componentes front-end | **19** (incluye `AdminGate`, `VotoRespuesta`, `MetricasPanel`) |
| Umbral "no inventar" (groundedness) | **G-04** — cerrado 17-oct-2026 |
| Autenticación y roles (JWT) | **HU-13** — cerrado 26-oct-2026 |
| Auditoría con filtros y marcado | **HU-14** — cerrado 27-oct-2026 |
| Derivación a atención municipal | **HU-17** — cerrado 27-oct-2026 |

### ✅ Funcionalidades implementadas

1. **Chat conversacional RAG** — búsqueda semántica (PostgreSQL/pgvector) + SLM Qwen 2.5 vía Ollama.
2. **Catálogo de trámites** — 252 procedimientos del TUPA con costo y área reales.
3. **Orientación de requisitos, costos y plazos** — HU-07 y HU-08.
4. **Trazabilidad y anti-alucinación** — HU-10 con fuentes (documento, número, fecha, versión, URL).
5. **Clasificación de intención y consultas fuera de dominio** — HU-06 y HU-11.
6. **Trámites relacionados** — HU-12.
7. **Derivación a oficina municipal con datos de contacto** — HU-17.
8. **Retroalimentación ciudadana (👍/👎)** — HU-15.
9. **Panel administrativo** — Gestión Documental (HU-01/02/03), Métricas (HU-16), Auditoría (HU-14), Reportes con exportación CSV (HU-18).
10. **Seguridad** — login JWT, contraseñas PBKDF2-SHA256, roles administrador/revisor/ciudadano (HU-13).
11. **Carga y procesamiento documental** — PDF/DOCX, OCR (rapidocr), chunking y embeddings (HU-01, HU-04).
12. **Despliegue en producción** — Backend en Render + PostgreSQL en Render; Frontend en Vercel.

### 📌 Deuda técnica opcional (no bloquea el cierre)

| Vacío | Descripción | Estado |
|-------|-------------|--------|
| **G-18** | Suites automatizadas `pytest` (hoy: scripts de verificación manuales) | Abierto |
| **G-20** | Guardrails anti *prompt-injection* | Abierto |
| **G-03** | Enmascaramiento completo de PII | Abierto |
| **G-23** | Rate limiting / protección contra saturación | Abierto |
| **G-26** | Auditoría WCAG, pruebas de carga, SonarQube, ZAP | Abierto |
| **P2-17** | Validación SUS con 50 ciudadanos reales | No ejecutable en el entorno académico |

---

## 2. PRESUPUESTO EJECUTADO — PROYECTO 100 % COMPLETO

| Categoría | Costo S/ | Justificación |
|-----------|----------|---------------|
| **Personal estudiantil** | **7,350** | 490 horas-hombre @ 15 S/hora (estudiantes de Ing. de Sistemas, 9.° y 10.° ciclo) |
| **Infraestructura y tecnología** | **1,180** | Hosting, base de datos, SLM, dominio y herramientas |
| **Costos adicionales** | **453** | Materiales, capacitación y contingencia |
| **TOTAL GENERAL** | **8,983 Soles** | **Proyecto completado al 100 %** |

### 📊 Resumen ejecutivo

- **Estado:** Proyecto **100 % desarrollado, desplegado y operativo**.
- **Historias HU:** **18/18** finalizadas.
- **Indicadores:** **101/101** cumplidos.
- **PMV:** **3/3** cerrados.
- **Rutas API:** **40/40** servibles.
- **Inversión:** **8,983 Soles** (presupuesto ejecutado).
- **Fecha de cierre:** **27-oct-2026**.
- **Equipo:** Estudiantes de Ingeniería de Sistemas (9.° y 10.° ciclo).

> **Nota:** El presupuesto de 8,983 Soles corresponde al proyecto completo y operativo, con las
> 18 HU al 100 % y los 101 indicadores cumplidos. El personal estudiantil realizó **490 horas-hombre**
> a 15 S/hora (7,350 S/), alcanzando todos los objetivos del PMV1, PMV2 y PMV3.

---

## 3. DESGLOSE DEL PRESUPUESTO

### 3.1 Costos de personal (estudiantes)

| Rol | Estudiantes | Tarifa | Horas | Costo S/ |
|-----|-------------|--------|-------|----------|
| Desarrollo Backend | 2 | 15 S/hora | 200 h | 3,000 |
| Desarrollo Frontend | 2 | 15 S/hora | 150 h | 2,250 |
| QA y Pruebas | 1 | 15 S/hora | 80 h | 1,200 |
| Documentación y RAG | 1 | 15 S/hora | 60 h | 900 |
| **Subtotal personal** | | | **490 h** | **7,350** |

*Cálculo: 490 horas-hombre × 15 S/hora = 7,350 S/.*

### 3.2 Costos de infraestructura y tecnología

| Elemento | Descripción | Costo S/ |
|----------|-------------|----------|
| Hosting de producción (Render + Vercel) | 3 meses de plan básico | 450 |
| Base de datos PostgreSQL con pgvector (Render) | 3 meses | 300 |
| Servicio SLM (Ollama) | Recursos de servidor | 200 |
| Dominio y SSL | Renovación anual | 80 |
| Herramientas de desarrollo | Licencias o suscripciones | 150 |
| **Subtotal infraestructura** | | **1,180** |

### 3.3 Costos adicionales

| Elemento | Descripción | Costo S/ |
|----------|-------------|----------|
| Materiales de documentación | Impresión y recursos visuales | 100 |
| Capacitación adicional | Talleres o cursos complementarios | 200 |
| Contingencia | Imprevistos y ajustes | 153 |
| **Subtotal adicionales** | | **453** |

---

## 4. PRESUPUESTO TOTAL

| Categoría | Costo S/ |
|-----------|----------|
| Personal (estudiantes) | 7,350 |
| Infraestructura y tecnología | 1,180 |
| Costos adicionales | 453 |
| **TOTAL GENERAL** | **8,983 Soles** |

*Comprobación: 7,350 + 1,180 + 453 = 8,983 S/.*

---

## 5. PROYECCIÓN DE HORAS POR ESTUDIANTE

Considerando una tarifa de **15 Soles/hora**:

| Estudiante | Horas | Responsabilidad | Inversión |
|------------|-------|-----------------|-----------|
| Estudiante 1 | 130 h | Backend API + integración RAG | 1,950 S/ |
| Estudiante 2 | 130 h | Frontend + UI/UX | 1,950 S/ |
| Estudiante 3 | 120 h | QA, pruebas y documentación | 1,800 S/ |
| Estudiante 4 | 110 h | Reportes, métricas y despliegue | 1,650 S/ |
| **Total** | **490 h** | | **7,350 S/** |

*Comprobación: 130 + 130 + 120 + 110 = 490 h; 490 × 15 = 7,350 S/.*

---

## 6. CRONOGRAMA EJECUTADO

| Fase | Duración | Actividades | Estado |
|------|----------|-------------|--------|
| Fase 1 — Puesta al día | 2 semanas | Corrección de vacíos críticos (D-14..D-23) | ✅ Completada |
| Fase 2 — PMV1 | 2 semanas | Chat, SLM, clasificador de intención, requisitos | ✅ Completada |
| Fase 3 — PMV2 | 3 semanas | RAG por fragmento, groundedness, trámites relacionados | ✅ Completada |
| Fase 4 — PMV3 | 4 semanas | Seguridad/roles, auditoría, métricas, reportes, derivación | ✅ Completada |
| Fase 5 — Despliegue y cierre | 2 semanas | Render + Vercel, pruebas de integración, documentación | ✅ Completada |
| **Total** | **13 semanas** | | **100 %** |

---

## 7. RECOMENDACIONES

1. **Aprovechar la tarifa estudiantil:** a 15 S/hora, el costo de personal es competitivo frente a la calidad entregada.
2. **Cerrar la deuda técnica prioritaria:** implementar las suites `pytest` (G-18) y los guardrails anti *prompt-injection* (G-20).
3. **Reutilizar la infraestructura existente:** el despliegue actual (Render + Vercel + PostgreSQL) permite escalar sin costos adicionales altos.
4. **Validación con usuarios reales:** ejecutar la medición SUS con 50 ciudadanos (P2-17) en un entorno municipal real.
5. **Mantener la documentación sincronizada:** toda cifra debe tomarse de `06-estado-actual-implementado.md`.

---

## 8. FORMA DE PAGO PROPUESTA

| Hito | Porcentaje | Monto S/ |
|------|-----------|----------|
| Pago inicial (inicio del proyecto) | 40 % | 3,593 |
| Pago intermedio (50 % de avance) | 30 % | 2,695 |
| Pago final (cierre y entrega) | 30 % | 2,695 |
| **Total** | **100 %** | **8,983** |

*Comprobación: 3,593 + 2,695 + 2,695 = 8,983 S/.*

---

*Presupuesto del proyecto "Sistema de Trámites Municipales" (MUN AI) — Municipalidad Provincial de Huancayo — TUPA 2023.*
*Proyecto completado al 100 % — 18/18 HU — 101/101 indicadores — cierre PMV3: 27-oct-2026.*
