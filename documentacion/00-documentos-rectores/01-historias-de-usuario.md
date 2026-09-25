# Historias de Usuario — Sistema de Trámites Municipales

---

## HU-01 — Gestión documental

**Historia de Usuario:**

Como administrador municipal necesito cargar documentos oficiales, como TUPA, ordenanzas, reglamentos y procedimientos, para construir la base de conocimiento del sistema.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Carga exitosa**
- **Given** que selecciono un archivo PDF válido de un documento municipal.
- **When** lo cargo al sistema e ingreso sus metadatos.
- **Then** el sistema valida el archivo, almacena el documento y confirma la carga.

**Escenario 2: Formato inválido**
- **Given** que selecciono un archivo no compatible.
- **When** intento cargarlo.
- **Then** el sistema rechaza el archivo e indica los formatos permitidos.

---

## HU-02 — Gestión documental

**Historia de Usuario:**

Como administrador municipal necesito registrar la vigencia, versión y fuente de cada documento para evitar que el sistema utilice información desactualizada.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Documento vigente**
- **Given** que ingreso la fecha, versión y URL oficial del documento.
- **When** guardo la información.
- **Then** el sistema registra el documento como vigente y lo habilita para indexación.

**Escenario 2: Datos incompletos**
- **Given** que el documento no tiene fecha, versión o fuente oficial.
- **When** intento publicarlo.
- **Then** el sistema impide su publicación y solicita completar los metadatos obligatorios.

---

## HU-03 — Gestión documental

**Historia de Usuario:**

Como revisor municipal necesito aprobar, modificar, derogar o desactivar documentos para mantener actualizada la base de conocimiento.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Validación aprobada**
- **Given** que reviso un documento cargado y confirmo su vigencia.
- **When** lo apruebo.
- **Then** el documento cambia a estado "vigente" y puede ser utilizado por el sistema.

**Escenario 2: Documento derogado**
- **Given** que un documento ya no se encuentra vigente.
- **When** lo marco como "derogado".
- **Then** el sistema lo conserva para auditoría, pero evita utilizarlo en nuevas respuestas.

---

## HU-04 — Procesamiento documental y RAG

**Historia de Usuario:**

Como administrador necesito que el sistema extraiga y procese automáticamente el contenido de los documentos para permitir la búsqueda semántica.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Procesamiento exitoso**
- **Given** que existe un documento vigente aprobado.
- **When** ejecuto el procesamiento documental.
- **Then** el sistema extrae el texto, lo divide en fragmentos, genera embeddings y actualiza el índice vectorial.

**Escenario 2: Documento ilegible**
- **Given** que el archivo contiene páginas escaneadas sin texto reconocible.
- **When** intento procesarlo.
- **Then** el sistema informa que requiere OCR o revisión manual.

---

## HU-05 — Consulta ciudadana

**Historia de Usuario:**

Como ciudadano necesito realizar preguntas en lenguaje natural para conocer qué trámite municipal necesito.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Consulta válida**
- **Given** que ingreso "Quiero abrir una bodega, ¿qué trámite necesito?".
- **When** envío la consulta.
- **Then** el sistema identifica el trámite probable y muestra su nivel de confianza.

**Escenario 2: Consulta ambigua**
- **Given** que ingreso "Necesito un permiso".
- **When** envío la consulta.
- **Then** el sistema solicita información adicional sobre el tipo de actividad o trámite.

---

## HU-06 — Clasificación de intención

**Historia de Usuario:**

Como ciudadano necesito que el sistema identifique si mi consulta corresponde a requisitos, costos, plazos, pasos o área responsable.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Intención identificada**
- **Given** que pregunto "¿Cuánto cuesta la licencia de funcionamiento?".
- **When** el sistema analiza la consulta.
- **Then** la clasifica como "consulta de costos".

**Escenario 2: Baja confianza**
- **Given** que ninguna categoría supera el umbral de confianza definido.
- **When** termina la clasificación.
- **Then** el sistema solicita aclaración y no genera una respuesta concluyente.

---

## HU-07 — Orientación de requisitos

**Historia de Usuario:**

Como ciudadano necesito conocer los documentos que debo presentar para realizar un trámite municipal.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Requisitos encontrados**
- **Given** que existe un TUPA vigente relacionado con el trámite.
- **When** consulto los requisitos.
- **Then** el sistema muestra una lista ordenada de requisitos y la fuente correspondiente.

**Escenario 2: Requisitos no confirmados**
- **Given** que los documentos recuperados no contienen requisitos suficientes.
- **When** solicito la orientación.
- **Then** el sistema indica que no puede confirmar la información y deriva al área responsable.

---

## HU-08 — Orientación de costos y plazos

**Historia de Usuario:**

Como ciudadano necesito conocer el costo y el plazo de atención de un trámite para planificar mi solicitud.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Información disponible**
- **Given** que el TUPA vigente contiene costo y plazo.
- **When** consulto el trámite.
- **Then** el sistema muestra ambos datos con la fuente documental.

**Escenario 2: Información no disponible**
- **Given** que no se encuentra un costo o plazo vigente.
- **When** realizo la consulta.
- **Then** el sistema no inventa el dato y comunica que debe verificarse con la municipalidad.

---

## HU-09 — Generación de respuestas con SLM

**Historia de Usuario:**

Como ciudadano necesito recibir una explicación clara y ordenada del procedimiento que debo seguir.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Respuesta fundamentada**
- **Given** que el sistema recupera fragmentos relevantes y vigentes.
- **When** el SLM genera la respuesta.
- **Then** presenta el trámite, requisitos, pasos, costo o plazo disponible y fuentes consultadas.

**Escenario 2: Contexto insuficiente**
- **Given** que no existen fragmentos relevantes suficientes.
- **When** el SLM intenta generar una respuesta.
- **Then** el sistema se abstiene de responder específicamente y solicita aclaración o deriva al funcionario.

---

## HU-10 — Trazabilidad y control de alucinaciones

**Historia de Usuario:**

Como ciudadano necesito saber cuándo una consulta no corresponde a trámites municipales para recibir orientación adecuada.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Trazabilidad disponible**
- **Given** que el sistema genera una respuesta sobre requisitos o costos.
- **When** el ciudadano visualiza la respuesta.
- **Then** se muestran el documento, número, fecha, versión, artículo, página o URL disponible.

**Escenario 2: Respuesta no fundamentada**
- **Given** que una afirmación no aparece en los documentos recuperados.
- **When** el evaluador analiza la respuesta.
- **Then** el sistema bloquea la afirmación, muestra una advertencia o deriva la consulta.

---

## HU-11 — Consultas fuera de dominio

**Historia de Usuario:**

Como ciudadano necesito saber cuándo una consulta no corresponde a trámites municipales para recibir orientación adecuada.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Consulta fuera del alcance**
- **Given** que pregunto sobre una devolución de impuestos de SUNAT.
- **When** el sistema clasifica la consulta.
- **Then** informa que está fuera de su alcance y sugiere acudir a la entidad correspondiente.

**Escenario 2: Consulta municipal**
- **Given** que pregunto sobre una licencia municipal.
- **When** el sistema analiza la consulta.
- **Then** continúa con la clasificación y recuperación de información.

---

## HU-12 — Recomendación de trámites relacionados

**Historia de Usuario:**

Como ciudadano necesito conocer trámites complementarios que podrían estar relacionados con mi solicitud.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Trámites relacionados**
- **Given** que consulto sobre una licencia de funcionamiento.
- **When** el sistema identifica el trámite.
- **Then** sugiere procedimientos relacionados, como compatibilidad de uso o inspección de seguridad, indicando que son recomendaciones.

**Escenario 2: Sin relación suficiente**
- **Given** que no existen trámites relacionados con confianza adecuada.
- **When** se ejecuta la recomendación.
- **Then** el sistema no muestra sugerencias especulativas.

---

## HU-13 — Gestión de usuarios y seguridad

**Historia de Usuario:**

Como administrador necesito gestionar usuarios y roles para controlar el acceso a documentos, configuraciones y métricas.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Acceso autorizado**
- **Given** que ingreso credenciales válidas de administrador.
- **When** inicio sesión.
- **Then** el sistema permite acceder a las funciones autorizadas.

**Escenario 2: Acceso no autorizado**
- **Given** que ingreso credenciales incorrectas o intento acceder a una función restringida.
- **When** solicito el acceso.
- **Then** el sistema rechaza la solicitud y registra el evento de seguridad.

---

## HU-14 — Auditoría

**Historia de Usuario:**

Como funcionario necesito consultar el historial de interacciones para revisar la calidad y trazabilidad de las respuestas.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Consulta de auditoría**
- **Given** que existe una interacción registrada.
- **When** el funcionario busca por fecha, trámite o usuario.
- **Then** el sistema muestra la consulta, intención, documentos recuperados, respuesta, nivel de confianza y fecha.

**Escenario 2: Registro incompleto**
- **Given** que una respuesta no tiene fuente o evaluación registrada.
- **When** se revisa la auditoría.
- **Then** el sistema marca la interacción como inconsistente para revisión técnica.

---

## HU-15 — Retroalimentación ciudadana

**Historia de Usuario:**

Como ciudadano necesito calificar la utilidad de la respuesta para contribuir a mejorar el sistema.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Calificación exitosa**
- **Given** que recibo una respuesta.
- **When** la marco como útil, parcialmente útil o no útil.
- **Then** el sistema registra la calificación asociada a la consulta.

**Escenario 2: Comentario opcional**
- **Given** que deseo explicar mi calificación.
- **When** ingreso un comentario y lo envío.
- **Then** el sistema almacena el comentario sin exigir datos personales innecesarios.

---

## HU-16 — Métricas y monitoreo

**Historia de Usuario:**

Como funcionario necesito visualizar indicadores del sistema para conocer su desempeño y calidad.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Métricas disponibles**
- **Given** que existen consultas registradas.
- **When** ingreso al panel de métricas.
- **Then** el sistema muestra cantidad de consultas, trámites frecuentes, tiempo de respuesta, satisfacción y groundedness.

**Escenario 2: Alerta de bajo desempeño**
- **Given** que la tasa de respuestas fundamentadas disminuye por debajo del umbral definido.
- **When** se actualizan las métricas.
- **Then** el sistema genera una alerta para revisión del modelo o de las fuentes.

---

## HU-17 — Derivación a atención municipal

**Historia de Usuario:**

Como ciudadano necesito ser derivado a un área responsable cuando el sistema no pueda responder de forma confiable.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Derivación por baja confianza**
- **Given** que la confianza de la respuesta es menor al umbral establecido.
- **When** termina la evaluación.
- **Then** el sistema informa su limitación y muestra el área o canal municipal correspondiente.

**Escenario 2: Caso que requiere decisión formal**
- **Given** que consulto sobre aprobación, denegatoria o resolución de un expediente.
- **When** el sistema identifica que se requiere decisión administrativa.
- **Then** informa que no puede resolver el caso y deriva al funcionario competente.

---

## HU-18 — Reportes y exportación

**Historia de Usuario:**

Como funcionario necesito generar reportes sobre las consultas y el desempeño del sistema para evaluar su funcionamiento.

**Criterios de Aceptación (Given / When / Then):**

**Escenario 1: Reporte generado**
- **Given** que selecciono un periodo de análisis.
- **When** solicito el reporte.
- **Then** el sistema muestra consultas, trámites más frecuentes, métricas de confianza, respuestas rechazadas y satisfacción.

**Escenario 2: Exportación exitosa**
- **Given** que el reporte ha sido generado.
- **When** selecciono exportar a PDF o Excel.
- **Then** el sistema descarga el archivo con los datos correspondientes y la fecha de generación.

---

## 📊 Resumen

| ID | Épica | Historia de Usuario |
| -- | ----- | ------------------- |
| HU-01 | Gestión documental | Como administrador municipal necesito cargar documentos oficiales, como TUPA, ordenanzas, reglamentos y procedimientos, para construir la base de conocimiento del sistema. |
| HU-02 | Gestión documental | Como administrador municipal necesito registrar la vigencia, versión y fuente de cada documento para evitar que el sistema utilice información desactualizada. |
| HU-03 | Gestión documental | Como revisor municipal necesito aprobar, modificar, derogar o desactivar documentos para mantener actualizada la base de conocimiento. |
| HU-04 | Procesamiento documental y RAG | Como administrador necesito que el sistema extraiga y procese automáticamente el contenido de los documentos para permitir la búsqueda semántica. |
| HU-05 | Consulta ciudadana | Como ciudadano necesito realizar preguntas en lenguaje natural para conocer qué trámite municipal necesito. |
| HU-06 | Clasificación de intención | Como ciudadano necesito que el sistema identifique si mi consulta corresponde a requisitos, costos, plazos, pasos o área responsable. |
| HU-07 | Orientación de requisitos | Como ciudadano necesito conocer los documentos que debo presentar para realizar un trámite municipal. |
| HU-08 | Orientación de costos y plazos | Como ciudadano necesito conocer el costo y el plazo de atención de un trámite para planificar mi solicitud. |
| HU-09 | Generación de respuestas con SLM | Como ciudadano necesito recibir una explicación clara y ordenada del procedimiento que debo seguir. |
| HU-10 | Trazabilidad y control de alucinaciones | Como ciudadano necesito saber cuándo una consulta no corresponde a trámites municipales para recibir orientación adecuada. |
| HU-11 | Consultas fuera de dominio | Como ciudadano necesito saber cuándo una consulta no corresponde a trámites municipales para recibir orientación adecuada. |
| HU-12 | Recomendación de trámites relacionados | Como ciudadano necesito conocer trámites complementarios que podrían estar relacionados con mi solicitud. |
| HU-13 | Gestión de usuarios y seguridad | Como administrador necesito gestionar usuarios y roles para controlar el acceso a documentos, configuraciones y métricas. |
| HU-14 | Auditoría | Como funcionario necesito consultar el historial de interacciones para revisar la calidad y trazabilidad de las respuestas. |
| HU-15 | Retroalimentación ciudadana | Como ciudadano necesito calificar la utilidad de la respuesta para contribuir a mejorar el sistema. |
| HU-16 | Métricas y monitoreo | Como funcionario necesito visualizar indicadores del sistema para conocer su desempeño y calidad. |
| HU-17 | Derivación a atención municipal | Como ciudadano necesito ser derivado a un área responsable cuando el sistema no pueda responder de forma confiable. |
| HU-18 | Reportes y exportación | Como funcionario necesito generar reportes sobre las consultas y el desempeño del sistema para evaluar su funcionamiento. |