# 07 · Checklist de Implementación — PMV1, PMV2, PMV3

> **Documento de verificación** para completar los 3 PMV. Cada punto tiene archivo de referencia,
> estado (⬜ pendiente / 🔄 en curso / ✅ verificado) y método de comprobación con `grep`.
>
> **Fecha de creación:** 16 de octubre de 2026 · HEAD `619a11d`
> **Fuente de verdad:** [`06-estado-actual-implementado.md`](./06-estado-actual-implementado.md)

---

## PMV1 · Prototipo funcional — 88 % → 100 % (3 puntos)

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| 1 | HU-07 | Derivación al área responsable | Añadir columna `area_responsable` a `tramites` | `database/migrations/005_area_responsable.sql` (nuevo) | ⬜ | `grep -c area_responsable database/migrations/005_area_responsable.sql` |
| 2 | HU-07 | Exponer área en respuesta | Añadir `area` a `TramiteProbableResponse` y `consulta_controller.py` | `backend/infrastructure/controllers/consulta_controller.py` | ⬜ | `grep -n area consulta_controller.py` |
| 3 | HU-07 | Derivar al área con confianza baja | Si confianza BAJA + trám probable → añadir texto derivación al área | `backend/application/services/ServicioOrientacion.py` | ⬜ | `grep -n derivar ServicioOrientacion.py` |
| 4 | HU-09 | Estructura de apartados garantizada | Si el SLM no devuelve los apartados, componerlos desde BD | `backend/application/services/ServicioSLM.py` | ⬜ | `grep -n estructura ServicioSLM.py` |
| 5 | HU-09 | Derivación al funcionario en la respuesta | Añadir texto de derivación al funcionario cuando no hay respuesta | `backend/application/services/ServicioOrientacion.py` | ⬜ | `grep -n funcionario ServicioOrientacion.py` |
| 6 | HU-08 | Montos reales del TUPA 2023 | Cargar `costo` real en `tramites` | `database/seeds/tramites.sql` o migration | ⬜ | `grep -v "costo 0.00" database/seeds/tramites.sql` |
| 7 | HU-08 | Confirmar 252 procedimientos del TUPA | Ampliar seeds de trámites | `database/seeds/tramites.sql` | ⬜ | `grep -c "^('" database/seeds/tramites.sql` → 252 |

---

## PMV2 · Modelo RAG optimizado — 56 % → 100 % (11 puntas)

### Bloqueo crítico (D-14..D-21)

| # | Defecto | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|
| P2-01 | D-14 | Añadir `router` vacío o eliminar import de `tramite_admin_router` | `backend/infrastructure/controllers/tramite_admin_controller.py` | ⬜ | `python -c "import main"` → exit 0 |
| P2-02 | D-15 | Corregir línea 1 de migración 004 (docstring → comentario SQL) | `database/migrations/004_documentos_pmv2.sql` | ⬜ | `head -1 database/migrations/004_documentos_pmv2.sql` → `--` |
| P2-03 | D-15 | Aplicar migración 004 en BD local | `psql -U tramites -d tramites_municipales -f database/migrations/004_documentos_pmv2.sql` | ⬜ | `psql -c "\d documentos"` → 15 columnas |
| P2-04 | D-16 | Añadir `004_documentos_pmv2.sql` al paso 3/7 de `instalar.ps1` | `instalar.ps1` | ⬜ | `grep 004 instalar.ps1` |
| P2-05 | D-17 | Añadir `pypdf` y `python-docx` a `requirements.txt` | `requirements.txt` | ⬜ | `grep -E "pypdf|python-docx" requirements.txt` |
| P2-06 | D-18 | Capturar `ValueError` de `EstadoDocumento()` → HTTP 422 | `backend/infrastructure/controllers/documento_admin_controller.py:48` | ⬜ | `curl "?estado=no_valido"` → 422 |
| P2-07 | D-19 | Invocar `AlmacenamientoDocumentosPort.eliminar` en baja física | `backend/application/use_cases/GestionarDocumentos.py` | ⬜ | `grep -n eliminar GestionarDocumentos.py` |
| P2-08 | D-20 | Corregir `pedir()` para no llamar `response.json()` en 204 | `frontend-tramites/lib/api.ts:69` | ⬜ | DELETE desde UI funciona |
| P2-09 | D-21 | Eliminar llamada a `GET /api/tramites/admin` (ruta inexistente) | `frontend-tramites/lib/api.ts:224` + `DocumentManager.tsx:35` | ⬜ | Panel admin carga lista |

### Funcionalidad pendiente

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P2-10 | HU-01 | Extracción de PDF/DOCX | Instalar deps y probar carga de `.pdf` / `.docx` | `requirements.txt` + `ExtraccionTextoAdapter.py` | ⬜ | Subir PDF → 200 |
| P2-11 | HU-01 | Confirmación/firma de calidad | UI para marcar documentos como revisados | `DocumentManager.tsx` | ⬜ | Botón "Aprobar" visible |
| P2-12 | HU-02 | Columnas metadatos en BD | Verificar migración aplicada y funcional | `DocumentoRepositoryImpl.py` | ⬜ | `SELECT version FROM documentos` funciona |
| P2-13 | HU-04 | OCR para escaneados | Integrar `pytesseract` o similar | `ExtraccionTextoAdapter.py` | ⬜ | Subir escaneado → texto extraído |
| P2-14 | HU-04 | Recuperación RAG por fragmento | Cambiar `BusquedaVectorialAdapter` para consultar `fragmentos_documento` | `backend/infrastructure/adapters/rag/BusquedaVectorialAdapter.py` | ⬜ | Búsqueda usa fragmentos |
| P2-15 | HU-12 | Motor de trámites relacionados | Implementar recomendación por similitud de embedding | nuevo `backend/application/use_cases/RecomendarTramites.py` | ⬜ | `GET /api/tramites/{id}/relacionados` |
| P2-16 | HU-12 | UI de trámites relacionados | Componente de recomendación en `/tramites` | `frontend-tramites/app/tramites/page.tsx` | ⬜ | Cards de "Trámites relacionados" |
| P2-17 | — | Validación con 50 ciudadanos | Prueba SUS y reproducibilidad | nuevo `documentacion/06-prueba-de-concepto/validacion-sus.md` | ⬜ | Informe publicado |
| P2-18 | — | Dataset PoC | Generar dataset sintético de evaluación | nuevo `documentacion/06-prueba-de-concepto/dataset-poc.md` | ⬜ | Dataset disponible |

---

## PMV3 · Sistema integrado — 52 % → 100 % (21 puntos)

### Seguridad y autenticación

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P3-01 | HU-13 | Login de usuarios | Endpoint `POST /api/auth/login` con JWT | nuevo `backend/infrastructure/controllers/auth_controller.py` | ⬜ | `curl -X POST /api/auth/login` |
| P3-02 | HU-13 | Contraseñas hasheadas | Usar `bcrypt` o `argon2` para passwords | `domain/entities/Usuario.py` + `usuario_controller.py` | ⬜ | `grep -n bcrypt backend/` |
| P3-03 | HU-13 | JWT en endpoints protegidos | Middleware de autenticación | `backend/main.py` + `auth_controller.py` | ⬜ | `curl /api/admin/documentos` → 401 sin token |
| P3-04 | HU-13 | Roles aplicados | Invocar `es_administrador()` en endpoints admin | `documento_admin_controller.py` + `tramite_admin_controller.py` | ⬜ | `grep es_administrador backend/infrastructure/controllers/` |
| P3-05 | HU-13 | Eventos de seguridad | Registrar login fallido exitoso en auditoría | `backend/application/services/ServicioAuditoria.py` | ⬜ | `grep -n seguridad ServicioAuditoria.py` |

### API y auditoría

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P3-06 | HU-10 | Respuesta completa en `GET /api/consultas/{id}` | Devolver respuesta, fuentes confianza | `consulta_controller.py:224` | ⬜ | `curl /api/consultas/{id}` → incluye `respuesta` |
| P3-07 | HU-10 | Bloqueo de afirmaciones | Rechazar groundedness < umbral con aviso | `ServicioOrientacion.py` | ⬜ | `grep -n groundedness ServicioOrientacion.py` |
| P3-08 | HU-10 | Fuentes con número/fecha/página | Enriquecer `Fuente` con metadatos del TUPA | `domain/entities/Fuente.py` | ⬜ | `grep -n numero Fuente.py` |
| P3-09 | HU-14 | Búsqueda de auditoría por filtros | Endpoint `GET /api/admin/auditoria?fecha=&tramite=&usuario=` | nuevo `backend/infrastructure/controllers/auditoria_admin_controller.py` | ⬜ | `curl "?tramite=123"` |
| P3-10 | HU-14 | Panel de auditoría real | Sustituir mock de `AuditLog.tsx` | `frontend-tramites/components/AuditLog.tsx` | ⬜ | Datos reales visibles |

### UX y rutas faltantes

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P3-11 | — | Ruta `/login` | Página de inicio de sesión | `frontend-tramites/app/login/page.tsx` | ⬜ | `curl localhost:3000/login` → 200 |
| P3-12 | — | Ruta `/tramites/[id]` | Detalle de trámite con documentos | `frontend-tramites/app/tramites/[id]/page.tsx` | ⬜ | Navegación funciona |
| P3-13 | — | Ruta `/404` | Página de no encontrado | `frontend-tramites/app/not-found.tsx` | ⬜ | URL inválida → 404 page |
| P3-14 | HU-14 | Ruta `/mis-consultas` | Historial ciudadano | `frontend-tramites/app/mis-consultas/page.tsx` | ⬜ | Login → historial |

### Calidad y monitoreo

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P3-15 | HU-15 | Retroalimentación ciudadana | Endpoints `POST /api/consultas/{id}/feedback` + tabla | nuevo migration + `feedback_controller.py` | ⬜ | `curl -X POST .../feedback` |
| P3-16 | HU-15 | UI de voto útil/no útil | Botones en `ChatThread.tsx` | `frontend-tramites/components/ChatThread.tsx` | ⬜ | Botones visibles |
| P3-17 | HU-16 | Endpoint de métricas agregadas | `GET /api/admin/metricas` | nuevo `metricas_controller.py` | ⬜ | `curl /api/admin/metricas` |
| P3-18 | HU-16 | Dashboard con datos reales | Sustituir KPIs ficticios de `/admin` | `frontend-tramites/app/admin/page.tsx` | ⬜ | KPIs reales |
| P3-19 | HU-18 | Reportes por periodo | `GET /api/admin/reportes?desde=&hasta=` | nuevo `reportes_controller.py` | ⬜ | CSV/JSON descargable |
| P3-20 | HU-18 | Exportación PDF/Excel | Librería de exportación | `reportes_controller.py` | ⬜ | Archivo descargado |
| P3-21 | — | Guardrails anti prompt-injection | Validación de entrada contra inyección | `backend/application/use_cases/RegistrarConsulta.py` | ⬜ | `grep -n injection` |
| P3-22 | — | Clasificador ML (Random Forest) | Sustituir heurística léxica | `backend/application/services/ServicioNLP.py` | ⬜ | F1 score documentado |
| P3-23 | — | Fine-tuning QLoRA del SLM | Entrenar modelo adaptado | nuevo `backend/scripts/finetune.py` | ⬜ | Benchmark mejorado |
| P3-24 | — | Pruebas automatizadas (pytest) | Suite de tests del flujo RAG | `backend/tests/` | ⬜ | `pytest` → tests pasan |
| P3-25 | — | Pruebas de carga (k6) | Script de load testing | `backend/tests/load/k6.js` | ⬜ | Latencia < 3s |
| P3-26 | — | Auditoría WCAG + SonarQube + ZAP | Accesibilidad y seguridad | config files | ⬜ | Reporte publicado |
| P3-27 | — | Rate limiting | Middleware de rate limiting | `backend/main.py` | ⬜ | `429 Too Many Requests` |
| P3-28 | — | Enmascaramiento de PII | Detectar y anonimizar datos personales | `backend/application/use_cases/RegistrarConsulta.py` | ⬜ | `grep -n pii` |
| P3-29 | — | Contenerización front/back | Dockerfile para cada servicio | `frontend-tramites/Dockerfile` + `backend/Dockerfile` | ⬜ | `docker compose up` |
| P3-30 | — | Balanceador HTTPS + monitoreo | nginx + Prometheus + Grafana | nuevo `nginx.conf` + `docker-compose.monitoring.yml` | ⬜ | Stack completo |

---

## Resumen de progreso

| PMV | Actual | Meta | Puntos por cerrar |
|---|---|---|---|
| **PMV1** | 88 % (21/24) | 100 % | 3 |
| **PMV2** | 56 % (14/25) | 100 % | 11 |
| **PMV3** | 52 % (23/44) | 100 % | 21 |
| **Transversal** | 25 % (2/8) | 100 % | 6 |
| **TOTAL** | 59 % (60/101) | 100 % | 41 |

---

## Orden de ejecución sugerido

1. **Desbloqueo PMV2** (P2-01 a P2-09): 9 tareas que habilitan el arranque de la API y el panel admin
2. **Cierre PMV1** (3 tareas): derivación al área + estructura garantizada + derivación funcionario
3. **Cierre PMV2** (P2-10 a P2-16): OCR, fragmentos RAG, HU-12, UI admin
4. **PMV3 bloque 1** (P3-01 a P3-05): autenticación y roles
5. **PMV3 bloque 2** (P3-06 a P3-10): auditoría completa
6. **PMV3 bloque 3** (P3-11 a P3-14): rutas faltantes
7. **PMV3 bloque 4** (P3-15 a P3-20): calidad, métricas, reportes
8. **PMV3 bloque 5** (P3-21 a P3-30): hardening, pruebas, despliegue

---

*Documento generado el 16 de octubre de 2026. Actualizar el Estado (⬜/🔄/✅) al completar cada punto.*
