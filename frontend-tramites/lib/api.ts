const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// El RAG local (embeddings + SLM) puede tardar entre 4 y 15 segundos en la
// primera consulta, por lo que el plazo debe ser holgado. Antes se agotaba a los
// 6 s y la consulta se sustituía por una respuesta ficticia.
const TIMEOUT_CONSULTA_MS = 45000;
const TIMEOUT_CATALOGO_MS = 10000;

export interface FuenteCitada {
  titulo: string;
  fragmento?: string;
  url?: string;
}

export interface TramiteProbable {
  id: string;
  nombre: string;
  requisitos: string[];
  costo: number;
  duracion_estimada_dias: number;
  fuente_url?: string | null;
}

export interface RespuestaConsulta {
  texto: string;
  fuentes: FuenteCitada[];
  confianza: string;
  groundedness: number;
  confianza_intencion: number;
  pide_aclaracion: boolean;
  intencion: string;
  tramite_probable: TramiteProbable | null;
}

export interface Tramite {
  id: string;
  nombre: string;
  descripcion: string;
  categoria: string;
  costo: string;
  plazo: string;
  requisitos: string[];
  municipalidad?: string;
}

export const SUGERENCIAS_RAPIDAS = [
  '¿Qué necesito para la licencia de funcionamiento?',
  '¿Cuánto cuesta el certificado de zonificación?',
  '¿En qué área tramito el permiso de obra?',
  '¿Cómo sigue el estado de mi expediente?',
];

async function leerDetalle(response: Response): Promise<string | null> {
  try {
    const cuerpo = await response.json();
    return typeof cuerpo?.detail === 'string' ? cuerpo.detail : null;
  } catch {
    return null;
  }
}

async function pedir<T>(url: string, init: RequestInit, timeoutMs: number): Promise<T> {
  const controller = new AbortController();
  const temporizador = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${API_URL}${url}`, { ...init, signal: controller.signal });
    if (!response.ok) {
      // Se conserva el detalle que explica el backend (p. ej. SLM no disponible)
      // en lugar de mostrar un código HTTP sin contexto.
      const detalle = await leerDetalle(response);
      throw new Error(detalle ?? `El servidor respondió ${response.status}.`);
    }
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('La consulta está tardando demasiado. Intenta de nuevo en unos segundos.');
    }
    throw error;
  } finally {
    clearTimeout(temporizador);
  }
}

/**
 * Envía la consulta al backend RAG.
 *
 * No existe respuesta alternativa: si el servicio falla se propaga el error para
 * que el ciudadano lo vea, en lugar de mostrar información ficticia (D-1).
 */
export async function enviarConsulta(pregunta: string): Promise<RespuestaConsulta> {
  const data = await pedir<Partial<RespuestaConsulta>>(
    '/api/consultas',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta }),
    },
    TIMEOUT_CONSULTA_MS,
  );

  return {
    texto: data.texto ?? 'Sin respuesta del servidor.',
    fuentes: Array.isArray(data.fuentes) ? (data.fuentes as FuenteCitada[]) : [],
    confianza: data.confianza ?? 'desconocida',
    // El groundedness es el valor real calculado por el evaluador; si el backend
    // no lo entrega se informa 0 en vez de inventar una medición alta (D-2).
    groundedness: typeof data.groundedness === 'number' ? data.groundedness : 0,
    confianza_intencion: typeof data.confianza_intencion === 'number' ? data.confianza_intencion : 0,
    pide_aclaracion: Boolean(data.pide_aclaracion),
    intencion: data.intencion ?? 'desconocida',
    tramite_probable: data.tramite_probable ?? null,
  };
}

/** Fila cruda devuelta por `GET /api/tramites`. */
interface TramiteCrudo {
  id: string;
  nombre: string;
  descripcion: string;
  tipo: string;
  requisitos: string[] | null;
  costo: number | string | null;
  duracion_estimada_dias: number | null;
  municipalidad?: string;
}

function formatearCosto(valor: number | string | null): string {
  const monto = typeof valor === 'string' ? Number(valor) : (valor ?? 0);
  if (!monto) return 'Gratuito / según TUPA';
  return `S/ ${monto.toFixed(2)}`;
}

function formatearPlazo(dias: number | null): string {
  if (!dias) return 'No especificado';
  return dias === 1 ? '1 día hábil' : `${dias} días hábiles`;
}

/** Traduce la fila del backend al modelo que usa la interfaz (D-5). */
export function mapearTramite(fila: TramiteCrudo): Tramite {
  return {
    id: fila.id,
    nombre: fila.nombre,
    descripcion: fila.descripcion,
    categoria: fila.tipo,
    costo: formatearCosto(fila.costo),
    plazo: formatearPlazo(fila.duracion_estimada_dias),
    requisitos: fila.requisitos ?? [],
    municipalidad: fila.municipalidad,
  };
}

/** Obtiene el catálogo de trámites; propaga el error si el backend no responde. */
export async function obtenerTramites(): Promise<Tramite[]> {
  const data = await pedir<TramiteCrudo[]>('/api/tramites', {}, TIMEOUT_CATALOGO_MS);
  return Array.isArray(data) ? data.map(mapearTramite) : [];
}

export interface EstadoServicios {
  api: string;
  database: string;
  redis: string;
  ollama: string;
}

const SIN_VERIFICAR: EstadoServicios = {
  api: 'sin verificar',
  database: 'sin verificar',
  redis: 'sin verificar',
  ollama: 'sin verificar',
};

/**
 * Consulta el estado real de los servicios.
 *
 * El backend expone `GET /health` (no `/api/health`) y solo verifica su propio
 * proceso; lo que no se comprueba se informa como "sin verificar" en lugar de
 * mostrarse como operativo (D-4).
 */
export async function obtenerEstadoServicios(): Promise<EstadoServicios> {
  try {
    const data = await pedir<{ status?: string }>('/health', {}, TIMEOUT_CATALOGO_MS);
    return { ...SIN_VERIFICAR, api: data.status === 'ok' ? 'operativo' : 'degradado' };
  } catch {
    return { ...SIN_VERIFICAR, api: 'no disponible' };
  }
}