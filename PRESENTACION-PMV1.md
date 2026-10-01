# PMV1 — Prototipo Funcional

**Sistema de Trámites Municipales · Municipalidad Provincial de Junín**
Presentación de avance · PMV1 de 3

---

## 1. ¿Qué es el PMV1?

Es la **primera versión operable** del sistema: un ciudadano escribe su duda en español y recibe
una respuesta generada por una IA local, **citando la fuente oficial** de donde salió.

| | PMV1 | PMV2 | PMV3 |
|---|---|---|---|
| **Objetivo** | Prototipo funcional | Modelo optimizado con RAG y citas | Sistema integrado desplegable |
| **Alcance** | Chat + IA + 5 trámites | RAG con 20+ trámites y abstención | API completa + seguridad + UX |
| **Arquitectura** | Capas, en local | Hexagonal + pgvector | Hexagonal + Docker + Redis |
| **Validación** | 15 usuarios | 50 ciudadanos | 100+ / SUS / carga |

**Meta del PMV1:** comprobar que un SLM local, sin conexión a internet y sin enviar datos del
ciudadano a terceros, puede orientar trámites de forma realmente útil.

---

## 2. Qué se logró en este PMV

| Entregable del PMV1 | Meta | Estado real | % |
|---|---|---|:-:|
| Chat conversacional | ✅ | `app/chat` con `ChatBox` y `ChatThread` | 100 % |
| SLM local que orienta | ✅ | `OllamaAdapter` + `qwen2.5:3b` en CPU | 100 % |
| Clasificación de intención | ✅ heurística | `ServicioNLP` (regex, 6 intenciones) | 100 % |
| 5 trámites mínimos | ✅ 5 | **22 trámites** del TUPA 2023 | 100 % |
| Validación con 15 usuarios | ❌ 0 | Sin estudio de usuarios todavía | 0 % |

**Resultado del PMV1: las 4 metas técnicas se cumplen; la validación con usuarios queda pendiente.**

Avance global del proyecto (las 18 HU, no solo PMV1): **37 %** → ver
[`05-trazabilidad-por-pmv.md`](documentacion/00-documentos-rectores/05-trazabilidad-por-pmv.md).

---

## 3. Cómo se ejecuta (para la demo)

Un solo comando instala todo:

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1
```

Y para levantar:

```powershell
# API
.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000

# Front-end, en otra terminal
cd frontend-tramites; npm run dev
```

- **App para la demo:** <http://localhost:3000>
- **API:** <http://localhost:8000> · **Swagger:** <http://localhost:8000/docs>

> Si al levantar la API aparece `[WinError 10013]`, es que el puerto 8000 ya está ocupado: la
> instancia anterior sigue corriendo. No es un error del sistema.

---

## 4. Ejemplos reales de uso

Estos son resultados **verificados** en la máquina, no texto ilustrativo.

### Ejemplo 1 — Consulta de requisitos ✅

**Ciudadano:** *¿Qué necesito para sacar el permiso de funcionamiento de una cafetería?*

```
Intención detectada: consultar_requisitos
Confianza: media
Fuentes recuperadas: 5
```

**Respuesta del sistema:**
> Para sacar el permiso de funcionamiento de una cafetería, necesitas presentar:
> - Formulario de solicitud
> - DNI del titular
> - Título de propiedad o contrato de alquiler
> - Plano de ubicación
> - Plano de diseño (si aplica)
>
> El permiso incluye una Inspección Técnica de Seguridad en Edificaciones (ITSE)

**Fuentes citadas:**
1. `https://www.munijunin.gob.pe/tupa/licencia-funcionamiento`
2. `https://www.munijunin.gob.pe/tupa/ocupacion-via-publica`
3. `https://www.munijunin.gob.pe/tupa/comercio-mercados`

### Ejemplo 2 — Trámite simple ✅

**Ciudadano:** *¿Cómo solicito un certificado de residencia?*

```
Intención detectada: otro
Confianza: media
Fuentes recuperadas: 5
```

> Para solicitar un Certificado de Residencia, debes presentar tu DNI, un recibo de servicios
> básicos (luz, agua o teléfono) y la solicitud en formato establecido.
> El plazo de atención es de 1 a 3 días hábiles.

**Fuentes citadas:**
1. `https://www.munijunin.gob.pe/tupa/certificado-residencia`
2. `https://www.munijunin.gob.pe/tupa/certificado-posesion`
3. `https://www.munijunin.gob.pe/tupa/union-de-hecho`

> Nota honesta: la intención quedó como `otro` porque el clasificador por palabras clave no
> contempla "certificados". Es una limitación conocida (HU-06, 40 % de avance).

### Ejemplo 3 — Cuando no hay dato (control de invención) ✅

**Ciudadano:** *¿Cuánto cuesta la licencia de funcionamiento?*

```
Intención detectada: consultar_costo
Confianza: baja
Fuentes recuperadas: 5
```

> El costo de la licencia de funcionamiento se determina según el arancel establecido en el
> TUPA 2023 […] **No se especifica un costo fijo en el contexto proporcionado.**
>
> ⚠️ *Nota: la información recuperada no sustenta completamente esta respuesta.*

**Fuentes citadas:**
1. `https://www.munijunin.gob.pe/tupa/licencia-funcionamiento`
2. `https://www.munijunin.gob.pe/tupa/licencia-edificacion`
3. `https://www.munijunin.gob.pe/tupa/zonificacion-compatibilidad`

**Este es el resultado más importante de la demo:** cuando el modelo no tiene respaldo, **lo dice**
en lugar de inventar un monto. La confianza cae a `baja` y se muestra la advertencia.

---

## 5. Cómo funciona (por dentro)

```
Ciudadano escribe
      │
      ▼
┌─────────────────────┐
│ 1. Clasificar       │  ServicioNLP: regex, 6 intenciones
│    intención        │  (rápido, sin modelo)
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 2. Registrar        │  PostgreSQL: tabla consultas
│    consulta         │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 3. ¿Está en caché?  │  Redis: SHA-256 de la pregunta
└─────┬─────────┬─────┘
  SÍ   │         │ NO
      ▼         ▼
 respuesta   ┌─────────────────────┐
 guardada    │ 4. Recuperar       │  BGE-M3 convierte la pregunta
 (~5 ms)     │    documentos      │  en vector → busca los 5 más
             │    similares       │  parecidos en pgvector
             └─────────┬───────────┘
                       ▼
             ┌─────────────────────┐
             │ 5. Generar         │  qwen2.5:3b (Ollama) redacta
             │    respuesta       │  SOLO con el contexto dado
             └─────────┬───────────┘
                       ▼
             ┌─────────────────────┐
             │ 6. Evaluar         │  Groundedness: ¿la respuesta
             │    + auditar       │  está en el contexto? → confianza
             └─────────────────────┘
```

**Tecnologías:** Python · FastAPI · PostgreSQL · pgvector · Redis · Ollama · Next.js · BGE-M3

---

## 6. Rendimiento medido

| Operación | Tiempo real |
|---|---|
| **Consulta con caché** (pregunta repetida) | **0.005 s** (5 ms) |
| Consulta nueva (RAG completo: búsqueda + IA) | 4–14 s |
| Búsqueda de trámites | 5 ms |
| 1.er embedding BGE-M3 (carga del modelo en memoria) | 3.95 s |
| Embeddings siguientes | 0.18 s cada uno |

> La primera vez que se pregunta algo el sistema tarda **varios segundos** porque la IA local
> procesa la respuesta en la CPU del equipo, sin GPU. Las siguientes son casi instantáneas.
> El vector tiene **1024 dimensiones** (BGE-M3).

⚠️ **Bug conocido:** el front-end corta la espera a los 6 s, pero el RAG puede tardar hasta 14 s.
Cuando pasa, el front muestra una respuesta de demostración **sin avisar al usuario**. Es el
defecto **D-1** y es lo primero que hay que corregir.

---

## 7. Qué se puede mostrar en la demo

| # | Momento | Qué demostrar |
|---|---|---|
| 1 | `npm run dev` → abrir <http://localhost:3000> | La interfaz del chat |
| 2 | Preguntar requisitos de una licencia | Clasificación + 5 fuentes citadas |
| 3 | Repetir la misma pregunta | El caché: baja de segundos a 5 ms |
| 4 | Preguntar un costo | La IA dice "no tengo el dato" en vez de inventar |
| 5 | Preguntar algo absurdo (receta de cocina) | Ver el comportamiento fuera de dominio |
| 6 | `GET /api/tramites` en Swagger | Los 22 trámites del TUPA cargados |

---

## 8. Límites honestos de esta versión

Lo que **todavía no** hace, para no sobrevender en la sustentación:

- **No hay inicio de sesión:** todas las rutas son públicas (HU-13, 40 %).
- **El panel de administración es una maqueta:** muestra "98 % satisfacción" y "1.180 votos" fijos,
  inventados en el código (HU-16, 0 %).
- **El chat no muestra de verdad las fuentes ni el porcentaje**: el backend no manda ese dato y el
  front pone 90 % por defecto (defectos D-2 y D-3).
- **No existen pruebas automatizadas** (0 suites).
- **Los costos están en 0** en los 22 trámites: el dato real del arancel no se cargó.
- **No se validó con 15 usuarios:** es la única meta del PMV1 sin cumplir.

---

## 9. Conclusión del PMV1

**Lo que se demuestra:** una IA que corre **en el equipo del usuario**, en español, que responde
sobre trámites reales de la Municipalidad Provincial de Junín, **cita su fuente oficial** y
**reconoce cuándo no sabe**. La mejora de 5 s a 5 ms con el caché es el resultado técnico más
destacable.

**Lo que sigue:** corregir los defectos que hacen que la pantalla muestre datos falsos (D-1 a D-4)
y luego completar la validación con los 15 usuarios para cerrar formalmente el PMV1.