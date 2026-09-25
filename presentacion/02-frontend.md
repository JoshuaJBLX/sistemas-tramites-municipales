# 02 — Frontend

> Next.js 14 · React 18 · Tailwind CSS — "Muni", asistente de la Municipalidad Provincial de Junín

## 1. Objetivo del frontend

Ser el **canal ciudadano** del asistente: un sitio público, responsive (móvil primero), cálido y
de lenguaje claro, que da acceso al catálogo TUPA, al chat con el SLM y a un panel administrativo
de métricas. Cuando el backend no está disponible, **degrada con datos demo** para que la
presentación nunca se rompa.

## 2. Estructura de rutas (App Router de Next.js)

| Ruta | Archivo | Tipo | Contenido |
|---|---|---|---|
| `/` | `app/page.tsx` | Server | Landing "Tus trámites, guiados por Muni": hero, mockup móvil, KPIs (252/1,236/98%), catálogo destacado, chat compacto, estado de servicios y auditoría |
| `/chat` | `app/chat/page.tsx` | Client | Chat completo: `ChatBox` grande + mockup de teléfono + robot flotante |
| `/tramites` | `app/tramites/page.tsx` | Client | Catálogo con buscador y filtros por categoría |
| `/admin` | `app/admin/page.tsx` | Server | Dashboard: KPIs, gráficos, estado de servicios, logs y gestión documental |
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
  referencia?: string;   // entidad que emite la fuente (p. ej. "Municipalidad Provincial de Junín")
  url?: string;
}

// Respuesta normalizada que el chat muestra
export interface RespuestaConsulta {
  texto: string;
  fuentes?: FuenteCitada[] | string[];
  confianza?: string;          // 'alta' | 'media' | 'baja'
  groundedness?: number;       // 0..1 (porcentaje de respaldo documental)
}

// Trámite del catálogo TUPA
export interface Tramite {
  id: string | number;
  nombre: string;
  descripcion: string;
  categoria?: string;          // ⚠️ el backend entrega "tipo" (ver G-14)
  costo?: string;
  plazo?: string;              // ⚠️ el backend entrega "duracion_estimada_dias" (G-14)
  requisitos?: string[];
  estado?: 'activo' | 'actualizando' | 'nuevo';
}
```

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

**`POST /api/consultas`** — solicitud:

```json
{ "pregunta": "¿Qué necesito para la licencia de funcionamiento?", "usuario_id": null }
```

Respuesta real del backend:

```json
{
  "consulta_id": "uuid",
  "intencion": "consultar_requisitos",
  "texto": "…respuesta del SLM…",
  "confianza": "alta",
  "fuentes": [ { "url": "https://…", "fragmento": "La licencia de funcionamiento …" } ]
}
```

Mapeo en `enviarConsulta()`: `texto` → `respuesta.texto` · `fuentes` → `r.fuentes`
· `confianza` → `r.confianza` · `groundedness` → `r.groundedness ?? 0.9` (la API aún no lo expone,
G-16).

**`GET /api/tramites`** — devuelve `TRAMITE[]` del backend: `{id, municipalidad_id, nombre,
descripcion, tipo, requisitos[], costo, duracion_estimada_dias, municipalidad}`.

⚠️ **Desajuste de contrato (G-14):** el backend usa `tipo` y `duracion_estimada_dias`; la UI lee
`categoria` y `plazo`. Con backend real los chips de costo/plazo pueden quedar vacíos; con la demo
funcionan porque `TRAMITES_DEMO` usa los campos del frontend.

**`GET /api/health`** — `{status:'ok'}`; si falla, `obtenerEstadoServicios()` asume todo operativo.

### 4.4 Funciones de la capa de datos (`lib/api.ts`)

| Función | Contrato | Timeout | Fallback |
|---|---|---|---|
| `enviarConsulta(pregunta)` | `Promise<RespuestaConsulta>` | 6 s (`AbortController`) | `respuestaDemo()` |
| `obtenerTramites()` | `Promise<Tramite[]>` | 5 s | `TRAMITES_DEMO` |
| `obtenerEstadoServicios()` | `Promise<Record<string,string>>` | — | `{api, database, redis, ollama: 'operativo'}` |

`respuestaDemo()` responde a: "nacimiento/partida", "licencia/funcionamiento", y genérico TUPA —
con `confianza` y `groundedness` simulados.

### 4.5 Estado interno de componentes (unión de interfaces)

- `ChatBox`: `mensajes: ChatMsg[]` + `entrada: string` + `cargando: boolean`.
- `TramitesPage`: `todos: Tramite[]` + `q: string` + `cat: string ('Todas'|categoría)`.
- `Navbar`: `path: string` (ruta activa) + `open: boolean` (menú móvil).
- `ServiceStatus`: `state: Record<string, string>` (operativo/offline por servicio).
- `DragDropUpload`: `drag: boolean` + `files: string[]` (nombres, sin subida real).

---

## 5. Componentes en detalle (15 + utilidades)

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
- ⚠️ El health del backend solo expone `{status:'ok'}`; la BD/Redis/Ollama se **asumen** operativos.

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
- ⚠️ **Maqueta**: solo nombres en estado local; **no** llama a `/api/documentos/upload` (G-12).

### 5.13 `Loading` — indicador de proceso (`components/Loading.tsx`)
- **Tipo**: puro.
- **Props**: ninguna.
- **Comportamiento**: pill con 3 puntos animados (`typing-dot` con delays 0/.18/.36 s) + texto
  "Muni está consultando fuentes oficiales…", `role="status"` (accesible).

### 5.14 `icons.tsx` — set de iconos SVG volumétricos
- `IconProps: { className?: string }` (default `h-6 w-6`).
- **23 iconos** sin dependencias: `ShieldIcon`, `TramiteIcon`, `OrdenanzaIcon`, `DirectorioIcon`,
  `AyudaIcon`, `ChatIcon`, `SendIcon`, `SparkIcon`, `CheckIcon`, `AlertIcon`, `UploadIcon`,
  `SearchIcon`, `ChartIcon`, `DocIcon`, `ClockIcon`, `UsersIcon`, `HeartIcon`, `MenuIcon`,
  `CloseIcon`, `LinkIcon` (+ usados por utilidades SVG internas).
- Gradientes lineales/radiales propios; `aria-hidden="true"`.

### 5.15 Composición por página (quién usa a quién)

```
app/layout.tsx        ──> Navbar
app/page.tsx          ──> RobotAgent · QuickAccessCard · ChatBox(compact) · TramiteCard ·
                          KpiCard · MiniCharts · ServiceStatus · AuditLog · DragDropUpload ·
                          GroundednessBadge · icons
app/chat/page.tsx     ──> ChatBox · RobotAgent · GroundednessBadge · ShieldIcon
app/tramites/page.tsx ──> TramiteCard · SearchIcon
app/admin/page.tsx    ──> KpiCard · MiniCharts · ServiceStatus · AuditLog · DragDropUpload · icons
ChatBox               ──> Loading · ChatThread · icons
ChatThread            ──> GroundednessBadge
```

---

## 6. Trazabilidad con las Historias de Usuario (HU)

El frontend es la **cara visible de las HU ciudadanas** (HU-05 a HU-10) y el **vehículo de
visualización** de las HU de funcionario (HU-13 a HU-16), aunque varias de estas últimas están
solo a nivel de maqueta (datos demo).

### 6.1 Componente → HU(s) que satisface

| Componente / UI | HU que soporta | Cómo la soporta |
|---|---|---|
| Botón "Consultar ahora" (Navbar, hero) | HU-05 | Atajo directo al chat |
| `ChatBox` (chips de sugerencia + input + burbujas) | HU-05, HU-06, HU-09 | Envía pregunta en lenguaje natural; `enviarConsulta` devuelve la respuesta del SLM |
| `ChatThread` (burbujas usuario/asistente, saludo de Muni) | HU-05, HU-09 | Presenta la conversación y el texto de la respuesta |
| `GroundednessBadge` (% + confianza + fuentes) | HU-10, HU-16 | Muestra nivel de respaldo documental y las fuentes (trazabilidad) |
| `TramiteCard` (costo, plazo, requisitos) | HU-07, HU-08 | Lista de requisitos con check y chips de costo/plazo |
| `DragDropUpload` | HU-01 (parcial), HU-03 (parcial) | Zona de carga y "listo para indexar" — **maqueta**, no sube al backend (G-12) |
| `AuditLog` | HU-14 | Log de interacciones con hora y punto de color — **datos demo** (G-07) |
| `KpiCard` / `MiniCharts` | HU-16 | KPIs (252 trámites, 1,236 consultas, 98%) y gráficos — **datos demo** (G-06) |
| `ServiceStatus` | HU-16 | Estado de api/BD/Redis/Ollama (usa `/api/health`) |
| `/admin` (dashboard) | HU-13 (admin), HU-16 | Panel de funcionario; **acceso sin login real** (G-01/G-11) |
| `/tramites` (buscador + filtros) | HU-05, HU-07 | Descubrimiento del catálogo TUPA |
| `respuestaDemo()` (fallback) | HU-05, HU-09 | Mantiene el chat "vivo" sin backend durante la presentación |

### 6.2 HU → estado de soporte visual en el frontend

| ID | Historia | Soporte en UI | Estado |
|---|---|---|---|
| HU-01 | Cargar documentos | `DragDropUpload` (solo nombres) | ⚠️ Maqueta — G-12 |
| HU-02 | Vigencia/versión/fuente | — | ❌ No visible (G-13)* |
| HU-03 | Aprobar/derogar | — | ❌ No visible (solo estado interno) |
| HU-04 | Procesamiento RAG | — | ❌ No visible (solo backend) |
| HU-05 | Consulta ciudadana | Chat completo `/chat` + chat compacto en `/` | ✅ Implementado |
| HU-06 | Clasificación de intención | Chat (respuesta) | ⚠️ La intención no se muestra al ciudadano (G-02) |
| HU-07 | Orientación de requisitos | `TramiteCard` + respuesta del chat | ✅/⚠️ Puntual por sustento documental |
| HU-08 | Costos y plazos | `TramiteCard` chips | ⚠️ Desajuste de campo G-14 |
| HU-09 | Respuestas con SLM | Burbujas del asistente | ✅ Implementado |
| HU-10 | Trazabilidad / anti-alucinación | `GroundednessBadge` + fuentes | ✅/⚠️ La API aún no expone `groundedness` (G-16) |
| HU-11 | Fuera de dominio | — | ❌ (solo caso en demo) |
| HU-12 | Trámites relacionados | — | ❌ G-08 |
| HU-13 | Usuarios y seguridad | Ruta `/admin` | ⚠️ Sin login/roles (G-01, G-11) |
| HU-14 | Auditoría | `AuditLog` | ⚠️ Maqueta (G-07) |
| HU-15 | Retroalimentación | — | ❌ G-05 |
| HU-16 | Métricas y monitoreo | `KpiCard`, `MiniCharts`, `ServiceStatus` | ⚠️ Maqueta (G-06/G-16) |
| HU-17 | Derivación municipal | Texto de respuesta | ⚠️ Solo nota genérica (G-09) |
| HU-18 | Reportes y exportación | — | ❌ G-07 |

\* El backend sí guarda `url_origen`/`estado`, pero la UI no ofrece pantalla de metadatos.

### 6.3 Conclusión de trazabilidad

- **HU ciudadanas centrales (HU-05 → HU-10):** cubiertas visualmente de punta a punta
  (escribir → recibir → ver fuentes/confianza), con las salvedades G-14 (costos/plazos) y G-16
  (groundedness no expuesto).
- **HU de gestión/admin (HU-01 → HU-04, HU-13 → HU-18):** presentes como **maquetas** en el
  frontend (`DragDropUpload`, `AuditLog`, `KpiCard`, `MiniCharts`) o ausentes; ninguna conecta aún
  con los endpoints reales de administración (G-12, G-07).

---

## 7. Integración frontend ↔ backend

### 6.1 Único punto de acceso (`lib/api.ts`)

| Función | Endpoint | Comportamiento |
|---|---|---|
| `enviarConsulta(pregunta)` | `POST /api/consultas` | Timeout 6 s; mapea `texto`, `fuentes`, `confianza`, `groundedness` |
| `obtenerTramites()` | `GET /api/tramites` | Timeout 5 s; catálogo o `TRAMITES_DEMO` |
| `obtenerEstadoServicios()` | `GET /api/health` | Estado; si falla, todo "operativo" |

### 6.2 Base URL y CORS
- `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).
- El backend fija `allow_origins=["http://localhost:3000","http://127.0.0.1:3000"]`
  (`backend/main.py`).

### 6.3 Degradación elegante (fallback demo)
- Si el fetch falla o expira (`AbortController`), `respuestaDemo(pregunta)` devuelve respuestas
  fundamentadas en TUPA 2023 (nacimiento, licencia de funcionamiento) y `TRAMITES_DEMO` llena el
  catálogo → la presentación es robusta aunque el backend esté apagado.

## 8. Demo para la presentación

1. Backend (8000) + frontend (3000) levantados.
2. `/` → hero, KPIs y catálogo destacado **en vivo**.
3. `/chat` → "¿Qué necesito para la licencia de funcionamiento?" → burbuja + **badge de
   groundedness** + fuentes TUPA.
4. `/tramites` → buscar "impuesto predial", filtrar por categoría.
5. Apagar backend → repetir la consulta → la **demo** mantiene la experiencia (fallback).
6. `/admin` → mostrar dashboard, aunque las métricas son de demostración (G-16).