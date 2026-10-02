# PMV1 — Demostración

**Trámites Municipales · Municipalidad Provincial de Huancayo (MPH)**

## Levantar el sistema

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1   # una sola vez

.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000

cd frontend-tramites; npm run dev
```

App → <http://localhost:3000> · API → <http://localhost:8000/docs>

---

## HU-09 · Generación de respuestas con SLM

**Demo:** en <http://localhost:3000>, escribir *¿Qué necesito para el permiso de funcionamiento de una cafetería?*

```
Intención: consultar_requisitos   Confianza: media   Fuentes: 5
```

> - Formulario de solicitud
> - DNI del titular
> - Título de propiedad o contrato de alquiler
> - Plano de ubicación
> - Plano de diseño (si aplica)

Fuente: `munijunin.gob.pe/tupa/licencia-funcionamiento`

**Y cuando no tiene respaldo, lo avisa** — *¿Cuánto cuesta la licencia?* → confianza **baja**:

> No se especifica un costo fijo en el contexto proporcionado.
> ⚠️ La información recuperada no sustenta completamente esta respuesta.

---

## HU-06 · Clasificación de intención

**Demo:** el sistema detecta solo qué tipo de pregunta es, sin gastar IA:

| Se escribe | Detecta |
|---|---|
| hola, buenos días | `saludo` |
| ¿qué requisitos necesito para el permiso? | `consultar_requisitos` |
| ¿cuánto cuesta la licencia? | `consultar_costo` |
| ¿dónde se tramita el permiso? | `consultar_ubicacion` |
| ¿cómo va el estado de mi trámite? | `consultar_estado` |
| ¿quién es el presidente del Perú? | `otro` |

---

## HU-07 · Orientación de requisitos

**Demo:** *¿Cómo solicito un certificado de residencia?*

```
Fuentes: 5
```

> Presenta tu DNI, un recibo de servicios básicos (luz, agua o teléfono) y la solicitud en
> formato establecido. El plazo de atención es de 1 a 3 días hábiles.

Fuentes: `tupa/certificado-residencia`, `tupa/certificado-posesion`, `tupa/union-de-hecho`

---

## HU-05 · Consulta ciudadana

**Demo:** el flujo completo está montado — pregunta → intención → búsqueda → respuesta → auditoría.

```
GET /api/tramites   →  22 trámites del TUPA 2023
```

**Velocidad:** pregunta repetida → **5 ms** (caché). Pregunta nueva → **4–14 s** (IA en CPU).

---

## Resumen

| HU | Qué demuestra | Estado |
|---|---|:-:|
| **HU-05** | Flujo completo de consulta funcionando | **100 %** |
| **HU-06** | Detecta el tipo de pregunta | **100 %** |
| **HU-07** | Entrega los requisitos con su fuente | **80 %** |
| **HU-09** | Responde con fuentes y avisa cuando no sabe | **60 %** |

**PMV1: 88 %** (21 de 24 puntos) → detalle en
[`05-trazabilidad-por-pmv.md`](documentacion/00-documentos-rectores/05-trazabilidad-por-pmv.md) y en
[`06-estado-actual-implementado.md`](documentacion/00-documentos-rectores/06-estado-actual-implementado.md) §10