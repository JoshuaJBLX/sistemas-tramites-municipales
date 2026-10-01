# PMV1 — Prototipo Funcional

**Trámites Municipales · Municipalidad Provincial de Junín**

## Qué hace

El ciudadano escribe su duda en español y recibe una respuesta de una IA que corre **en el equipo**,
**citando la fuente oficial** y **reconociendo cuando no sabe**.

## Cómo se levanta

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1   # una sola vez

.venv\Scripts\Activate.ps1
cd backend; uvicorn main:app --reload --port 8000         # API

cd frontend-tramites; npm run dev                         # App → localhost:3000
```

Swagger (para probar la API): <http://localhost:8000/docs>

## Prueba de que funciona

**`GET /api/tramites`** → **22 trámites** del TUPA 2023 cargados desde la BD.

**Consulta real** — *¿Qué necesito para el permiso de funcionamiento de una cafetería?*

```
Intención: consultar_requisitos   Confianza: media   Fuentes: 5
```

> - Formulario de solicitud
> - DNI del titular
> - Título de propiedad o contrato de alquiler
> - Plano de ubicación
> - Plano de diseño (si aplica)

Fuente: `munijunin.gob.pe/tupa/licencia-funcionamiento`

**Y cuando no sabe, lo dice** — *¿Cuánto cuesta la licencia?* → confianza **baja**:
> No se especifica un costo fijo en el contexto proporcionado. ⚠️ La información recuperada no
> sustenta completamente esta respuesta.

## Rendimiento

| | |
|---|---|
| Pregunta repetida (caché) | **5 ms** |
| Pregunta nueva (IA local en CPU) | 4–14 s |

## Historias de usuario que se implementan aquí

| HU | Qué hace | Avance |
|---|---|:-:|
| **HU-05** | Consulta ciudadana en lenguaje natural | 44 % |
| **HU-06** | Clasificación de intención | 40 % |
| **HU-07** | Orientación de requisitos | 40 % |
| **HU-09** | Generación de respuestas con SLM | 60 % |

**PMV1: 46 % · Proyecto completo: 37 %** → detalle en
[`05-trazabilidad-por-pmv.md`](documentacion/00-documentos-rectores/05-trazabilidad-por-pmv.md).

## Pendiente

- El front corta la espera a 6 s y el RAG tarda hasta 14 s → a veces muestra texto de ejemplo (**D-1**)
- El panel de administración es maqueta (98 % satisfacción y 1.180 votos están inventados en el código)
- Sin inicio de sesión, sin pruebas automáticas, costos de trámites en 0
- Falta la validación con los 15 usuarios del PMV1