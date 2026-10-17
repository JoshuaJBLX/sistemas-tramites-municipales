# 02 — Frontend

> **Actualizado el 17 de octubre de 2026 (verificación en vivo).** Cifras verificadas contra la API y la BD local en [06-estado-actual-implementado.md](../documentacion/00-documentos-rectores/06-estado-actual-implementado.md): global **82 %** (83/101), PMV1 **100 %** ✅, PMV2 **100 %** ✅, PMV3 **63 %**; la API arranca (31 rutas) y los defectos D-14..D-23 están corregidos.

> Next.js 14 · React 18 · Tailwind CSS — "Muni", asistente de la Municipalidad Provincial de Junín

## 1. Objetivo del frontend

Ser el **canal ciudadano** del asistente: un sitio público, responsive (móvil primero), cálido y
de lenguaje claro, que da acceso al catálogo TUPA, al chat con el SLM y a un panel administrativo
de métricas y **gestión documental**. El backend real es la única fuente de datos: si una petición
falla o expira, la interfaz **muestra el error** en lugar de sustituirlo por datos inventados
(`respuestaDemo()`/`TRAMITES_DEMO` se eliminaron en la revisión de octubre).

## 2. Estructura de rutas (App Router de Next.js)

| Ruta | Archivo | Tipo | Contenido |
|---|---|---|---|
| `/` | `app/page.tsx` | Server | Landing "Tus trámites, guiados por Muni": hero, mockup móvil, KPIs reales (nº de trámites del catálogo; consultas y satisfacción informadas como "—"), catálogo destacado, chat compacto, estado de servicios y auditoría |
| `/chat` | `app/chat/page.tsx` | Client | Chat completo: `ChatBox` grande + mockup de teléfono + robot flotante |
| `/tramites` | `app/tramites/page.tsx` | Client | Catálogo con buscador y filtros por categoría |
| `/admin` | `app/admin/page.tsx` | Server | Dashboard: KPIs (252/1,236/98 %, **ficticios**, D-6), gráficos, estado de servicios, logs y **`DocumentManager`** (gestión documental real) |
| layout | `app/layout.tsx` | — | `Navbar`, `<main>` y footer institucional; metadata SEO |

- `app/page.tsx` y `app/admin/page.tsx` usan `export const dynamic = 'force-dynamic'` (render
  en servidor en cada petición, sin caché de página).
- `app/chat/page.tsx` y `app/tramites/page.tsx` son clientes (`'use client'`): necesitan estado
  (conversación / filtros).

## 3. Sistema de diseño (UI/UX) — `app/globals.css`

- **Paleta cálida institucional**: navy institucional (#0F2A4A NW), fondo papel, esmeralda
  (éxito/confianza) y ámbar (calidez/branding). Es un **rediseño** frente a la paleta azul fría
  original de a.md.
- **Estilos utilitarios**: `glass`, `glass-strong`, `card-3d`, `btn-primary-3d`, `btn-emerald-3d`,
  `btn-neu`, `badge-emerald|blue|amber`, `chip`, `bubble-user`, `bubble-bot`, `eyebrow`,
  `h-display`, `text-gradient-warm`, `skeleton`, `avatar-muni`, `scroll-thin`.
- **Animaciones CSS**: `animate-rise-in`, `float-y`, `blink-eye`, `typing-dot`, `pulse-ring`,
  `shadow-lift`, `shadow-glow-emerald|amber`.
- **Principios**: alto contraste, tarjetas suaves con sombras, redondeos grandes (2-3rem),
  tipografía legible — orientado a usuarios con baja alfabetización digital.

---

## 4. Interfaz de datos y contratos (Interfaces)

### 4.1 Modelos TypeScript del dominio (`lib/api.ts`)

```ts
// Fuente citada que acompaña a una respuesta (se muestra como badge en el chat)
export interface FuenteCitada {
  titulo: string;
  fragmento?: string;   // extracto del documento citado
  url?: string;
}

// Trámite probable identificado por el backend (HU-07)
export interface TramiteProbable {
  id: string;
  nombre: string;
  requisitos: string[];
  costo: number;
  duracion_estimada_dias: number;
  fuente_url?: string | null;
}

// Respuesta normalizada que el chat muestra
export interface RespuestaConsulta {
  texto: string;
  fuentes: FuenteCitada[];
  confianza: string;            // 'alta' | 'media' | 'baja' | 'desconocida'
  groundedness: number;         // 0..1 — valor real, ya no fijo (D-2 corregido)
  confianza_intencion: number;  // 0..1 — confianza del clasificador
  pide_aclaracion: boolean;
  intencion: string;
  tramite_probable: TramiteProbable | null;
}

// Trámite del catálogo TUPA (forma ya traducida por mapearTramite)
export interface Tramite {
  id: string;
  nombre: string;
  descripcion: string;
  categoria: string;   // el backend entrega "tipo"; lo traduce mapearTramite (D-5)
  costo: string;       // "S/ 150.00" o "Gratuito / según TUPA"
  plazo: string;       // "5 días hábiles" (desde duracion_estimada_dias)
  requisitos: string[];
  municipalidad?: string;
}
```

`mapearTramite()` (`lib/api.ts:125`) traduce `tipo → categoria` y
`duracion_estimada_dias → plazo`: **el desajuste de campos G-14 quedó cerrado (D-5)** y la UI ya
no lee campos inexistentes.

### 4.2 Modelos internos de componentes

```ts
// Mensaje de la conversación: usuario o asistente (components/ChatThread.tsx)
export interface ChatMsg {
  autor: 'usuario' | 'asistente';
  texto: string;
  fuentes?: (FuenteCitada | string)[];
  groundedness?: number;
  confianza?: string;
}

// Iconos volumétricos SVG (components/icons.tsx)
interface IconProps { className?: string; }

// Tarjeta KPI (components/KpiCard.tsx)
interface KpiProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  delta: string;
  tone: 'blue' | 'emerald' | 'amber';
}
```

### 4.3 Contratos HTTP con el backend (solicitudes y respuestas)

**`POST /api/consultas`** — solicitud (la UI envía solo `pregunta`):

```json
{ "pregunta": "¿Qué necesito para la licencia de funcionamiento?" }
```

Respuesta real del backend:

```json
{
  "consulta_id": "uuid",
  "intencion": "consultar_requisitos",
  "texto": "…respuesta del SLM…",
  "confianza": "alta",
  "groundedness": 0.87,
  "confianza_intencion": 0.85,
  "pide_aclaracion": false,
  "tramite_probable": { "id": "…", "nombre": "…", "requisitos": ["…"], "costo": 0, "duracion_estimada_dias": 10 },
  "fuentes": [ { "titulo": "TUPA 2023 · Licencias", "url": "https://…", "fragmento": "La licencia de funcionamiento …" } ]
}
```

Mapeo en `enviarConsulta()`: `texto`, `fuentes`, `confianza`, `groundedness` (valor real, ya no
fijo en 0.9 — **D-2 corregido**), `confianza_intencion`, `pide_aclaracion`, `intencion` y
`tramite_probable`; los ausentes caen en valores por defecto seguros.

**`GET /api/tramites`** — devuelve `TramiteCrudo[]` del backend: `{id, municipalidad_id, nombre,
descripcion, tipo, requisitos[], costo, duracion_estimada_dias, municipalidad}`, que
`mapearTramite()` traduce a `categoria`/`plazo` (**D-5/G-14 cerrados**).

**`GET /health`** — `{status:'ok'}`; comprueba únicamente el proceso (**D-11**). Si falla,
`obtenerEstadoServicios()` devuelve `sin verificar` para api/BD/Redis/Ollama y `no disponible`
para la api, **nunca "operativo" inventado**.

**`/api/admin/documentos*`** — 6 endpoints de administración (listado, alta, upload, reprocesar,
baja lógica y baja física) consumidos por `DocumentManager`. ⚠️ Hoy **ninguno responde**: la API no
arranca (**D-14**), y los `DELETE` devuelven `204` sin cuerpo que `pedir()` no sabe leer
(**D-20**).

### 4.4 Funciones de la capa de datos (`lib/api.ts` — 225 líneas, 9 funciones)

| Función | Endpoint | Timeout | Comportamiento en error |
|---|---|---|---|
| `enviarConsulta(pregunta)` | `POST /api/consultas` | 45 s | lanza `Error`; `ChatBox` lo muestra en la burbuja |
| `obtenerTramites()` | `GET /api/tramites` | 10 s | lanza `Error`; `page.tsx` hace `.catch(() => [])` |
| `obtenerEstadoServicios()` | `GET /health` | 10 s | devuelve `sin verificar` / `no disponible` |
| `listarDocumentosAdmin(params)` | `GET /api/admin/documentos` | 10 s | lanza `Error` (PMV2) |
| `subirDocumento(formData)` | `POST /api/admin/documentos/upload` | 120 s | lanza `Error` (PMV2) |
| `reprocesarDocumento(id)` | `POST /api/admin/documentos/{id}/procesar` | 10 s | lanza `Error` (PMV2) |
| `eliminarDocumentoLogico(id)` | `DELETE /api/admin/documentos/{id}` | 10 s | ⚠️ rompe con `204` sin cuerpo (**D-20**) |
| `eliminarDocumentoFisico(id)` | `DELETE /api/admin/documentos/{id}/fisico` | 10 s | ⚠️ ídem (**D-20**) |
| `listarTramitesAdmin()` | `GET /api/tramites/admin` | 10 s | ⚠️ ruta inexistente (**D-21**) |

Todas comparten `pedir()` (`lib/api.ts:60-78`), que envuelve `fetch` con `AbortController`,
traduce el `AbortError` a un mensaje en castellano y extrae el `detail` del backend. **No hay
respuestas de demostración**: los timeouts eran de 6 s/5 s y `respuestaDemo()`/`TRAMITES_DEMO` se
eliminaron (D-1); hoy el error se muestra tal cual.

### 4.5 Estado interno de componentes (unión de interfaces)

- `ChatBox`: `mensajes: ChatMsg[]` + `entrada: string` + `cargando: boolean`.
- `TramitesPage`: `todos: Tramite[]` + `q: string` + `cat: string ('Todas'|categoría)`.
- `Navbar`: `path: string` (ruta activa) + `open: boolean` (menú móvil).
- `ServiceStatus`: `state: {api, database, redis, ollama}` con valores `operativo`/`sin verificar`/
  `no disponible`.
- `DragDropUpload`: `drag: boolean` + `files: string[]` (nombres, sin subida real).
- `DocumentManager`: `tramites` + `docs: DocumentoAdmin[]` + `loading` + `msg` + `form`
  (`tramite_id`, `titulo`, `url_origen`, `version`, `fecha_publicacion`, `estado`, `archivo`).

---

## 5. Componentes en detalle (16 + utilidades)

### 5.1 `Navbar` — navegación principal (`components/Navbar.tsx`)
- **Tipo**: Client (`'use client'`), usa `usePathname` y `useState`.
- **Props**: ninguna.
- **Comportamiento**: header `sticky top-0 z-50`; nav con `glass-strong`. Enlaces: Inicio (`/`),
  Trámites (`/tramites`), Asistente (`/chat`), Admin (`/admin`) + botón destacado "Consultar ahora".
  El link activo (`path === href`) recibe fondo degradado `primary-600→800` y `shadow-lift`.
  En móvil (`md:hidden`) colapsa a menú hamburguesa con panel desplegable.
- **Marcas**: logo `ShieldIcon` en contenedor degradado; título "Municipalidad Provincial de Junín" ·
  "Trámites Digitales".

### 5.2 `ChatBox` — cerebro del chat (`components/ChatBox.tsx`)
- **Tipo**: Client.
- **Props**: `{ compact?: boolean }` (altura 380px compact / 420px normal; muestra 2 o 4 sugerencias).
- **Estado**: `mensajes: ChatMsg[]`, `entrada`, `cargando`.
- **Comportamiento**:
  1. `handleEnviar(texto?)` — usa el texto recibido (sugerencia) o el input; omite si vacío o si ya carga.
  2. Agrega burbuja del usuario, setea `cargando`, llama `enviarConsulta(pregunta)`.
  3. Al responder agrega burbuja del asistente con `fuentes`, `groundedness`, `confianza`.
  4. En `catch` muestra burbuja de error.
  5. El input envía con `Enter`; botón "Enviar" con `SendIcon`.
- **UI**: caja `glass rounded-3xl` con `ChatThread` + `Loading` mientras carga; si no hay mensajes,
  muestra chips `SUGERENCIAS_RAPIDAS` (✨).

### 5.3 `ChatThread` — conversación (`components/ChatThread.tsx`)
- **Tipo**: Client.
- **Props**: `{ mensajes: ChatMsg[]; cargando: boolean }`.
- **Comportamiento**: auto-scroll suave al final en cada cambio (`scrollTo({behavior:'smooth'})`);
  si `mensajes.length === 0` muestra saludo inicial de "Muni" (avatar + burbuja).
  - Burbuja de **usuario**: `bubble-user` a la derecha.
  - Burbuja de **asistente**: avatar `MuniAvatar` + `bubble-bot` + `GroundednessBadge` con fuentes.
  - `cargando && <TypingDots />`.
- **Exporta además**: `MuniAvatar` (SVG de la cara de Muni) y `TypingDots` (3 puntos animados).

### 5.4 `GroundednessBadge` — confianza de la respuesta (`components/GroundednessBadge.tsx`)
- **Tipo**: componente presentacional puro (sin hooks → usable en Server y Client).
- **Props**: `{ score?: number; fuentes?: (FuenteCitada | string)[]; compact?: boolean }`.
- **Comportamiento**: `nivelColor(score)` → `>=0.9` `badge-emerald`, `>=0.75` `badge-amber`,
  si no `badge-blue`. Muestra "Groundedness NN%" (icono check) y hasta **2** fuentes como badges
  con icono link; si hay más de 2, "+N fuentes".

### 5.5 `RobotAgent` — mascota "Muni" (`components/RobotAgent.tsx`)
- **Tipo**: puro (sin hooks).
- **Props**: `{ compact?: boolean }` (56/64 ↔ 36 😀).
- **Comportamiento**: SVG 200×220 dibujado a mano con: brote-antenna, orejas, cabeza, ojos grandes
  con parpadeo (`blink-eye`), mejillas y sonrisa, cuerpo con corazón, brazos. Animaciones
  `float-y` y halo ámbar. Debajo: plataforma ondulada y pill "En línea · responde con fuentes
  oficiales" con `pulse-ring`.
- **Uso**: hero de `/`, complemento de `/chat` (flotante fixed, `pointer-events-none`, solo xl).

### 5.6 `TramiteCard` — tarjeta de trámite (`components/TramiteCard.tsx`)
- **Tipo**: Client.
- **Props**: `{ tramite: Tramite; index?: number }`.
- **Comportamiento**: `animationDelay = min(index,8)*60ms` (entrada escalonada). Muestra
  `categoria` (eyebrow), nombre, descripción, chips `costo` (💰) y `plazo` (ClockIcon), y hasta 3
  requisitos con check esmeralda. `badgeByEstado` → `activo|nuevo|actualizando` con badges
  emerald/blue/amber. Fondo con blobs de color que escalan al hover (`group-hover:scale-150`).

### 5.7 `QuickAccessCard` — acceso rápido (`components/QuickAccessCard.tsx`)
- **Tipo**: Client.
- **Props**: `{ href; title; subtitle; icon: React.ReactNode; accent: string }`.
- **Comportamiento**: `<Link>` con `card-3d`; icono en contenedor degradado con
  `group-hover:scale-105 group-hover:-rotate-3`; flecha "→" animada al hover. Acciones del home:
  Trámites, Ordenanzas, Directorio, Ayuda.

### 5.8 `KpiCard` — indicador (`components/KpiCard.tsx`)
- **Tipo**: puro.
- **Props**: `{ icon; label; value; delta; tone: 'blue'|'emerald'|'amber' }`.
- **Comportamiento**: card-3d, label en mayúsculas espaciado, `value` grande extrabold, `delta` en
  esmeralda, icono en caja degradada según `tones[token]`.

### 5.9 `MiniCharts` — gráficos de métricas (`components/MiniCharts.tsx`)
- **Tipo**: puro.
- **Props**: ninguna.
- **Comportamiento**: **SVG sin librerías** — barras semanales (Lun..Dom, hoy "Jue" resaltada en
  ámbar), 2 donuts (`Donut(98, Satisfacción, #10b981)` y `Donut(87, Resueltas 1er contacto,
  #3569a5)`) con `strokeDasharray`, y una línea de tendencia con relleno degradado.
- ⚠️ Datos **fijos de demostración** (G-16).

### 5.10 `ServiceStatus` — monitoreo (`components/ServiceStatus.tsx`)
- **Tipo**: Client.
- **Props**: ninguna.
- **Estado**: `state: {api, database, redis, ollama}` (inicial "operativo").
- **Comportamiento**: en `useEffect` llama `obtenerEstadoServicios()`. Lista 4 servicios con
  `StatusDot` (verde con `pulse-ring` on / ámbar off) y etiqueta monospace `99.9% · {estado}`.
- ⚠️ El health del backend solo expone `{status:'ok'}` (**D-11**): BD/Redis/Ollama se informan
  como **"sin verificar"**, nunca como "operativo"; si la ruta falla, la api aparece "no disponible".

### 5.11 `AuditLog` — auditoría/logs (`components/AuditLog.tsx`)
- **Tipo**: puro.
- **Props**: ninguna.
- **Comportamiento**: lista de 5 filas tipo consola (`font-mono`) con hora, punto de color y mensaje,
  entrada escalonada (`animationDelay = i*70ms`), scroll máximo 56.
- ⚠️ Filas **hardcodeadas** de demostración (G-07/G-16).

### 5.12 `DragDropUpload` — carga de documentos (`components/DragDropUpload.tsx`)
- **Tipo**: Client.
- **Props**: ninguna.
- **Comportamiento**: zona `dropzone` con borde dashed; al `onDragOver` activa estado visual
  (`border-emerald`, escala 1.01); en `onDrop` agrega nombres de archivo a `files`. Opción
  "Seleccionar archivos" con `<input type=file multiple hidden>`. Los archivos aparecen como
  "listo para indexar".
- ⚠️ **Maqueta**: solo nombres en estado local; **no** llama a la API de documentos (G-12). El
  componente que sí la consume es `DocumentManager` (5.15).

### 5.13 `Loading` — indicador de proceso (`components/Loading.tsx`)
- **Tipo**: puro.
- **Props**: ninguna.
- **Comportamiento**: pill con 3 puntos animados (`typing-dot` con delays 0/.18/.36 s) + texto
  "Muni está consultando fuentes oficiales…", `role="status"` (accesible).

### 5.14 `icons.tsx` — set de iconos SVG volumétricos
- `IconProps: { className?: string }` (default `h-6 w-6`).
- **20 iconos** sin dependencias: `ShieldIcon`, `TramiteIcon`, `OrdenanzaIcon`, `DirectorioIcon`,
  `AyudaIcon`, `ChatIcon`, `SendIcon`, `SparkIcon`, `CheckIcon`, `AlertIcon`, `UploadIcon`,
  `SearchIcon`, `ChartIcon`, `DocIcon`, `ClockIcon`, `UsersIcon`, `HeartIcon`, `MenuIcon`,
  `CloseIcon`, `LinkIcon`.
- Gradientes lineales/radiales propios; `aria-hidden="true"`.

### 5.15 `DocumentManager` — panel de gestión documental (`components/DocumentManager.tsx`)
- **Tipo**: Client (`'use client'`); **135 líneas**; componente **nuevo del PMV2** (`ea06c9a`).
- **Props**: ninguna. Se monta en `/admin` (`app/admin/page.tsx:32`).
- **Estado**: `tramites`, `docs: DocumentoAdmin[]`, `loading`, `msg` y `form` con los metadatos
  (`tramite_id`, `titulo`, `url_origen`, `version`, `fecha_publicacion`, `estado`, `archivo`).
- **Comportamiento**:
  1. Al montar, `Promise.all([listarTramitesAdmin(), listarDocumentosAdmin({incluir_eliminados, limite:100})])`
     para poblar el `<select>` de trámites y la tabla.
  2. Formulario `FormData` → `subirDocumento()` (`POST /api/admin/documentos/upload`, acepta
     `.pdf/.docx/.txt/.md`), mensaje de éxito/error y recarga de la tabla.
  3. Fila con título, estado (incluye `derogado`), versión, fecha, `indexado`, `fragmentado` y
     tres acciones: **Reprocesar** (`POST …/procesar`), **Dar de baja** (`DELETE` lógico) y
     **Eliminar** (`DELETE` físico, con `confirm()`).
- **Estado real**: es el **único panel que consume endpoints de administración de verdad**
  (**G-12 ✅**). ✅ **Funciona (16-oct-2026):** carga la lista (265 trámites), sube archivos con
  metadatos, reprocesa, aprueba (`PUT …/estado`) y borra (D-14..D-23 corregidos).

### 5.16 Composición por página (quién usa a quién)

```
app/layout.tsx        ──> Navbar
app/page.tsx          ──> RobotAgent · QuickAccessCard · ChatBox(compact) · TramiteCard ·
                          KpiCard · MiniCharts · ServiceStatus · AuditLog · DragDropUpload ·
                          GroundednessBadge · icons
app/chat/page.tsx     ──> ChatBox · RobotAgent · GroundednessBadge · ShieldIcon
app/tramites/page.tsx ──> TramiteCard · SearchIcon
app/admin/page.tsx    ──> KpiCard · MiniCharts · ServiceStatus · AuditLog · DocumentManager · icons
ChatBox               ──> Loading · ChatThread · icons
ChatThread            ──> GroundednessBadge
```

---

## 6. Trazabilidad con las Historias de Usuario (HU)

El frontend es la **cara visible de las HU ciudadanas** (HU-05 a HU-10) y el **vehículo de
visualización** de las HU de gestión (HU-01 a HU-04, HU-13 a HU-16): `DocumentManager` ya habla con
los endpoints reales, mientras que métricas, gráficos y logs siguen siendo maquetas (G-06/G-07).

### 6.1 Componente → HU(s) que satisface

| Componente / UI | HU que soporta | Cómo la soporta |
|---|---|---|
| Botón "Consultar ahora" (Navbar, hero) | HU-05 | Atajo directo al chat |
| `ChatBox` (chips de sugerencia + input + burbujas) | HU-05, HU-06, HU-09 | Envía pregunta en lenguaje natural; `enviarConsulta` devuelve la respuesta del SLM |
| `ChatThread` (burbujas usuario/asistente, saludo de Muni) | HU-05, HU-09 | Presenta la conversación y el texto de la respuesta |
| `GroundednessBadge` (% + confianza + fuentes) | HU-10, HU-16 | Muestra nivel de respaldo documental y las fuentes (trazabilidad) |
| `TramiteCard` (costo, plazo, requisitos) | HU-07, HU-08 | Lista de requisitos con check y chips de costo/plazo |
| `DragDropUpload` | HU-01 (parcial) | Zona de carga y "listo para indexar" — **maqueta**, no sube al backend (G-12) |
| `DocumentManager` | HU-01, HU-02, HU-03, HU-04 | Carga con metadatos + tabla + reprocesar/bajas reales sobre `/api/admin/documentos` — ✅ operativo (17-oct-2026) |
| `AuditLog` | HU-14 | Log de interacciones reales vía `GET /api/consultas` — ✅ operativo (17-oct-2026) |
| `KpiCard` / `MiniCharts` | HU-16 | KPIs (252 trámites, 1,236 consultas, 98%) y gráficos — **datos demo** (G-06) |
| `ServiceStatus` | HU-16 | Estado de api/BD/Redis/Ollama (usa `/health`; lo no verificado, "sin verificar") |
| `/admin` (dashboard) | HU-13 (admin), HU-16 | Panel de funcionario; **acceso sin login real** (G-01/G-11) |
| `/tramites` (buscador + filtros) | HU-05, HU-07 | Descubrimiento del catálogo TUPA |

### 6.2 HU → estado de soporte visual en el frontend

| ID | Historia | Soporte en UI | Estado |
|---|---|---|---|
| HU-01 | Cargar documentos | `DocumentManager` (carga con metadatos) | ✅ G-12 |
| HU-02 | Vigencia/versión/fuente | `DocumentManager` (muestra versión/fecha/estado) | ✅ Columnas creadas y pobladas (004 aplicada, 16-oct-2026) |
| HU-03 | Aprobar/derogar | `DocumentManager` (baja lógica y física con `confirm()`) | ⚠️ Parcial — sin roles ni flujo de revisión (D-8) |
| HU-04 | Procesamiento RAG | `DocumentManager` (índice `indexado`/`fragmentado` + *Reprocesar*) | ✅ 004 aplicada: 20/20 fragmentos |
| HU-05 | Consulta ciudadana | Chat completo `/chat` + chat compacto en `/` | ✅ Implementado |
| HU-06 | Clasificación de intención | Chat (respuesta) | ⚠️ La intención no se muestra al ciudadano (G-02) |
| HU-07 | Orientación de requisitos | `TramiteCard` + respuesta del chat | ✅/⚠️ Puntual por sustento documental |
| HU-08 | Costos y plazos | `TramiteCard` chips | ✅ Montos reales del TUPA + umbral "no inventar" (G-04) |
| HU-09 | Respuestas con SLM | Burbujas del asistente | ✅ Implementado |
| HU-10 | Trazabilidad / anti-alucinación | `GroundednessBadge` + fuentes | ✅ Trazabilidad completa (D-9 cerrado) + bloqueo de afirmaciones |
| HU-11 | Fuera de dominio | Aviso en el chat (entidad sugerida) | ✅ Clasificador de dominio (G-04 cerrado) |
| HU-12 | Trámites relacionados | Panel "Trámites relacionados" | ✅ G-08 |
| HU-13 | Usuarios y seguridad | Ruta `/admin` | ⚠️ Sin login/roles (G-01, G-11) |
| HU-14 | Auditoría | `AuditLog` (datos reales) | ✅ Panel real; falta búsqueda por filtros |
| HU-15 | Retroalimentación | — | ❌ G-05 |
| HU-16 | Métricas y monitoreo | `KpiCard`, `MiniCharts`, `ServiceStatus` | ⚠️ Maqueta (G-06/G-16) |
| HU-17 | Derivación municipal | Texto de respuesta | ⚠️ Solo nota genérica (G-09) |
| HU-18 | Reportes y exportación | — | ❌ G-07 |

Esta tabla describe el **soporte visual** en el frontend; el estado global de cada HU con su %
de puntos de verificación está en [05-implementaciones.md](05-implementaciones.md) (global **82 %**,
83/101).

### 6.3 Conclusión de trazabilidad

- **HU ciudadanas centrales (HU-05 → HU-10):** cubiertas visualmente de punta a punta
  (escribir → recibir → ver fuentes/confianza); G-14 quedó cerrado con `mapearTramite` y el
  `groundedness` real sí viaja en la respuesta (D-2/D-5 corregidos). Queda pendiente la
  trazabilidad completa por `GET /api/consultas/{id}` (D-9 ✅).
- **HU de gestión/admin (HU-01 → HU-04, HU-13 → HU-18):** ✅ **`DocumentManager` conecta y
  funciona** con los endpoints reales de administración (G-12 ✅; upload → 201, aprobar → 200,
  bajas → 204) desde la corrección de D-14/D-20/D-21 (16-oct-2026). El resto
  (`DragDropUpload`, `AuditLog`, `KpiCard`, `MiniCharts`) sigue siendo maqueta (G-06/G-07).

---

## 7. Integración frontend ↔ backend

### 7.1 Único punto de acceso (`lib/api.ts`)

| Función | Endpoint | Comportamiento |
|---|---|---|
| `enviarConsulta(pregunta)` | `POST /api/consultas` | Timeout 45 s; mapea `texto`, `fuentes`, `confianza`, `groundedness`, `tramite_probable` |
| `obtenerTramites()` | `GET /api/tramites` | Timeout 10 s; `mapearTramite()` traduce `tipo`→`categoria` y `duracion_estimada_dias`→`plazo` |
| `obtenerEstadoServicios()` | `GET /health` | Estado; lo no comprobado se informa "sin verificar" |
| funciones admin + `obtenerAuditoria()` (PMV2) | `/api/admin/documentos*`, `GET /api/consultas` | Listado, upload, reprocesado, aprobación (`PUT …/estado`), bajas y auditoría; ✅ operativas (17-oct-2026) |

### 7.2 Base URL y CORS
- `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).
- El backend fija `allow_origins=["http://localhost:3000","http://127.0.0.1:3000"]`
  (`backend/main.py`).

### 7.3 Manejo de fallos (sin respuestas ficticias)
- Si el fetch falla o expira (`AbortController`), `pedir()` lanza un `Error` con mensaje en
  castellano: el chat muestra la burbuja de error y la portada muestra un catálogo vacío
  (`.catch(() => [])`). **No hay `respuestaDemo()` ni `TRAMITES_DEMO`** (eliminados, D-1) → la
  interfaz nunca presenta datos inventados como reales.

## 8. Demo para la presentación

1. Backend (8000) + frontend (3000) levantados.
2. `/` → hero, catálogo real de la BD y estado de servicios.
3. `/chat` → "¿Qué necesito para la licencia de funcionamiento?" → burbuja + **badge de
   groundedness** + fuentes TUPA + trámite probable.
4. `/tramites` → buscar "impuesto predial", filtrar por categoría.
5. ✅ **El paso 1 funciona (17-oct-2026):** la API arranca (31 rutas) y el frontend consume
   datos reales de la BD (catálogo de 265 trámites).
6. `/admin` → el dashboard muestra los KPIs **ficticios** (252 / 1,236 / 98 %, D-6) y
   `DocumentManager`, que **sí carga la tabla** (D-20/D-21 corregidos).