# 07 · Checklist de Implementación — PMV1, PMV2, PMV3

> **Documento de verificación** para completar los 3 PMV. Cada punto tiene archivo de referencia,
> estado (⬜ pendiente / 🔄 en curso / ✅ verificado) y método de comprobación con `grep`.
>
> **Fecha de creación:** 16 de octubre de 2026 · HEAD `619a11d`
> **Última verificación:** 17 de octubre de 2026 (PMV1 y **PMV2 cerrados** al 100 %; solo P2-17 pendiente, no fabricable)
> **Fuente de verdad:** [`06-estado-actual-implementado.md`](./06-estado-actual-implementado.md)

---

## PMV1 · Prototipo funcional — 88 % → 100 % (7 puntos) ✅

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| 1 | HU-07 | Derivación al área responsable | Añadir columna `area_responsable` a `tramites` | `database/migrations/005_area_responsable.sql` | ✅ | `grep -c area_responsable database/migrations/005_area_responsable.sql` → 4; API: 252/265 trámites con área |
| 2 | HU-07 | Exponer área en respuesta | Añadir `area` a `TramiteProbableResponse` y `consulta_controller.py` | `backend/infrastructure/controllers/consulta_controller.py` | ✅ | `GET /api/consultas` → `tramite_probable.area` poblada |
| 3 | HU-07 | Derivar al área con confianza baja | Si confianza BAJA + trám probable → añadir texto derivación al área | `backend/application/services/ServicioOrientacion.py` | ✅ | `grep -n derivar backend/application/services/ServicioOrientacion.py` |
| 4 | HU-09 | Estructura de apartados garantizada | Si el SLM no devuelve los apartados, componerlos desde BD | `backend/application/services/ServicioSLM.py` | ✅ | `grep -n estructura backend/application/services/ServicioSLM.py` |
| 5 | HU-09 | Derivación al funcionario en la respuesta | Añadir texto de derivación al funcionario cuando no hay respuesta | `backend/application/services/ServicioOrientacion.py` | ✅ | `grep -n funcionario backend/application/services/ServicioOrientacion.py` |
| 6 | HU-08 | Montos reales del TUPA 2023 | Cargar `costo` real en `tramites` | `database/seeds/tramites.sql` | ✅ | `grep -c "^('" database/seeds/tramites.sql` → 252 filas; API: **188 con costo > 0** (93 marcadas 0.00 = gratuito/tarifa variable/proporcional, según TUPA) |
| 7 | HU-08 | Confirmar 252 procedimientos del TUPA | Ampliar seeds de trámites | `database/seeds/tramites.sql` | ✅ | `grep -c "^('" database/seeds/tramites.sql` → **252**; `POST /api/tramites` → 265 (252 TUPA + 13 prototipos) |

---

## PMV2 · Modelo RAG optimizado — 100 % (HU) ✅ (18 puntos; solo P2-17 pendiente)

### Bloqueo crítico (D-14..D-21) ✅

| # | Defecto | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|
| P2-01 | D-14 | Añadir `router` vacío o eliminar import de `tramite_admin_router` | `backend/infrastructure/controllers/tramite_admin_controller.py` | ✅ | `python -c "import main"` → 30 rutas, exit 0 |
| P2-02 | D-15 | Corregir línea 1 de migración 004 (docstring → comentario SQL) | `database/migrations/004_documentos_pmv2.sql` | ✅ | `head -1` → `--` |
| P2-03 | D-15 | Aplicar migración 004 en BD local | `psql -f database/migrations/004_documentos_pmv2.sql` | ✅ | `SELECT version, fecha_publicacion FROM documentos` → 20/20 con datos |
| P2-04 | D-16 | Añadir `004_documentos_pmv2.sql` al paso 3/7 de `instalar.ps1` | `instalar.ps1` | ✅ | `grep -n "004\|005" instalar.ps1` → ambas migraciones listadas |
| P2-05 | D-17 | Añadir `pypdf` y `python-docx` a `requirements.txt` | `requirements.txt` | ✅ | `grep -E "pypdf\|python-docx\|PyMuPDF\|rapidocr" requirements.txt` → pypdf 5.1.0, PyMuPDF 1.24.14, python-docx 1.1.2, rapidocr 3.10.0 |
| P2-06 | D-18 | Capturar `ValueError` de `EstadoDocumento()` → HTTP 422 | `backend/infrastructure/controllers/documento_admin_controller.py` | ✅ | `GET /api/tramites/admin?estado=no_valido` → 422; `PUT .../estado` con estado inválido → 422 |
| P2-07 | D-19 | Invocar `AlmacenamientoDocumentosPort.eliminar` en baja física | `backend/application/use_cases/GestionarDocumentos.py` | ✅ | Baja física de prueba → 204 y sin huérfanos en `storage/documentos` |
| P2-08 | D-20 | Corregir `pedir()` para no llamar `response.json()` en 204 | `frontend-tramites/lib/api.ts` | ✅ | DELETE desde UI sin error; `npx tsc --noEmit` → 0 errores |
| P2-09 | D-21 | Eliminar llamada a `GET /api/tramites/admin` (ruta inexistente) | `frontend-tramites/lib/api.ts` + `DocumentManager.tsx` | ✅ | Panel admin carga la lista (265 trámites) |

### Funcionalidad pendiente

| # | HU | Punto pendiente | Acción | Archivo a tocar | Estado | Verificación |
|---|---|---|---|---|---|---|
| P2-10 | HU-01 | Extracción de PDF/DOCX | Instalar deps y probar carga de `.pdf` / `.docx` | `requirements.txt` + `ExtraccionTextoAdapter.py` | ✅ | `POST /api/admin/documentos/upload` con PDF real del TUPA → **201**, `indexado=true`, `fragmentado=true`, texto extraído |
| P2-11 | HU-01 | Confirmación/firma de calidad | UI para marcar documentos como revisados | `DocumentManager.tsx` + `PUT /api/admin/documentos/{id}/estado` | ✅ | Botón "Aprobar" visible; `PUT .../estado` → 200 (`en_revision`→`vigente`); 422 si faltan metadatos |
| P2-12 | HU-02 | Columnas metadatos en BD | Verificar migración aplicada y funcional | `DocumentoRepositoryImpl.py` | ✅ | `SELECT COUNT(*) FROM documentos WHERE version IS NOT NULL AND fecha_publicacion IS NOT NULL` → 20 |
| P2-13 | HU-04 | OCR para escaneados | Integrar OCR (`rapidocr`) | `ExtraccionTextoAdapter.py` | ✅ | `grep -n rapidocr backend/infrastructure/adapters/extraction/ExtraccionTextoAdapter.py`; prueba con PDF escaneado → texto |
| P2-14 | HU-04 | Recuperación RAG por fragmento | Cambiar `BusquedaVectorialAdapter` para consultar `fragmentos_documento` | `backend/infrastructure/adapters/rag/BusquedaVectorialAdapter.py` | ✅ | `SELECT COUNT(*) FROM fragmentos_documento` → **20** (los 20 documentos reprocesados con `POST /procesar`); búsqueda por fragmentos activa |
| P2-15 | HU-12 | Motor de trámites relacionados | Implementar recomendación por similitud de embedding | nuevo `backend/application/use_cases/RecomendarTramites.py` + `TramiteCatalogoAdapter.relacionados` | ✅ | `GET /api/tramites/{id}/relacionados` → 200 con `similitud` **en orden decreciente**; embedding para trámites con documentos y **fallback léxico (Jaccard)** para los 252 TUPA |
| P2-16 | HU-12 | UI de trámites relacionados | Componente de recomendación en `/tramites` | `frontend-tramites/app/tramites/page.tsx` + `TramiteCard.tsx` + `lib/api.ts` | ✅ | `npx next build` → OK; panel "Trámites relacionados con «…»" con % de afinidad |
| P2-17 | — | Validación con 50 ciudadanos | Prueba SUS y reproducibilidad | nuevo `documentacion/06-prueba-de-concepto/validacion-sus.md` | ⬜ | Requiere prueba real con ciudadanos; no fabricable |
| P2-18 | — | Dataset PoC | Generar dataset sintético de evaluación | `backend/scripts/generar_dataset_poc.py` → `documentacion/06-prueba-de-concepto/dataset-poc.csv` | ✅ | 200 consultas (50 por intención: requisitos/costo/estado/ubicación) sobre los 50 primeros trámites TUPA; regenerable con el script (semilla fija) |

---

## PMV3 · Sistema integrado — 59 % → 100 % (21 puntos)

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
| P3-06 | HU-10 | Respuesta completa en `GET /api/consultas/{id}` | Devolver respuesta, fuentes, confianza, banderas | `consulta_controller.py` (`TrazabilidadResponse`) | ✅ | `curl /api/consultas/{id}` → incluye `respuesta`, `fuentes`, `groundedness`, `fuera_dominio` (17-oct-2026) |
| P3-07 | HU-10 | Bloqueo de afirmaciones | Rechazar groundedness < umbral con aviso | `ServicioOrientacion.py` (`BLOQUEO_AFIRMACIONES`) | ✅ | `grep -n BLOQUEO_AFIRMACIONES backend/application/services/ServicioOrientacion.py`; verificado con RAG stub |
| P3-08 | HU-10 | Fuentes con número/fecha/página | Enriquecer `Fuente` con metadatos del TUPA | `domain/entities/Fuente.py` + `ServicioRAG.py` | ✅ | `grep -n numero backend/domain/entities/Fuente.py`; respuesta incluye `numero`/`fecha`/`version` |
| P3-09 | HU-14 | Búsqueda de auditoría por filtros | Endpoint `GET /api/admin/auditoria?fecha=&tramite=&usuario=` | nuevo `backend/infrastructure/controllers/auditoria_admin_controller.py` | ⬜ | `curl "?tramite=123"` |
| P3-10 | HU-14 | Panel de auditoría real | Sustituir mock de `AuditLog.tsx` | `frontend-tramites/components/AuditLog.tsx` | ✅ | Datos reales vía `GET /api/consultas`, estados cargando/error/vacío (17-oct-2026) |

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

## Resumen de progreso (17-oct-2026, verificado)

| PMV | Actual | Meta | Puntos por cerrar |
|---|---|---|---|
| **PMV1** | **100 %** (24/24; 7/7 del checklist) | 100 % | 0 |
| **PMV2** | **100 %** (28/28; 17/18 del checklist) ✅ | 100 % | solo P2-17 (validación SUS, no fabricable) |
| **PMV3** | **63 %** (31/49) | 100 % | 18 (seguridad, auditoría, métricas, reportes, pruebas) |
| **TOTAL** | **82 %** (83/101) | 100 % | 18 |

---

## Orden de ejecución sugerido

1. ~~**Desbloqueo PMV2** (P2-01 a P2-09)~~ ✅ cerrado
2. ~~**Cierre PMV1** (7 puntos)~~ ✅ cerrado
3. ~~**Cierre PMV2** (P2-10 a P2-16, P2-18)~~ ✅ cerrado
4. ~~**PMV3 bloque 2 parcial** (P3-06 a P3-08, P3-10)~~ ✅ cerrado 17-oct (HU-10 y panel de HU-14)
5. **PMV3 bloque 1** (P3-01 a P3-05): autenticación y roles
6. **PMV3 auditoría** (P3-09): búsqueda de auditoría por filtros
7. **PMV3 bloque 3** (P3-11 a P3-14): rutas faltantes
8. **PMV3 bloque 4** (P3-15 a P3-20): calidad, métricas, reportes
9. **PMV3 bloque 5** (P3-21 a P3-30): hardening, pruebas, despliegue
10. **P2-17**: validación SUS con 50 ciudadanos (actividad real, no de código)

---

*Documento generado el 16 de octubre de 2026. Actualizar el Estado (⬜/🔄/✅) al completar cada punto.*
*Verificación PMV1/PMV2: API `localhost:8000` (venv), BD `tramites_municipales`, `npx tsc --noEmit` y `npx next build` en `frontend-tramites/`.*
