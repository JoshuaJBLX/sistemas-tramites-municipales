const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// El RAG local puede tardar 4–17 segundos en la primera consulta.
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
    groundedness: typeof data.groundedness === 'number' ? data.groundedness : 0,
    confianza_intencion: typeof data.confianza_intencion === 'number' ? data.confianza_intencion : 0,
    pide_aclaracion: Boolean(data.pide_aclaracion),
    intencion: data.intencion ?? 'desconocida',
    tramite_probable: data.tramite_probable ?? null,
  };
}

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

export async function obtenerEstadoServicios(): Promise<EstadoServicios> {
  try {
    const data = await pedir<{ status?: string }>('/health', {}, TIMEOUT_CATALOGO_MS);
    return { ...SIN_VERIFICAR, api: data.status === 'ok' ? 'operativo' : 'degradado' };
  } catch {
    return { ...SIN_VERIFICAR, api: 'no disponible' };
  }
}

// ---------- Administración de documentos (HU-01..HU-04, G-12) ----------
export interface DocumentoAdmin {
  id: string;
  tramite_id: string;
  titulo: string;
  url_origen: string;
  estado: 'vigente' | 'obsoleto' | 'en_revision' | 'derogado';
  indexado: boolean;
  version: string;
  fecha_publicacion?: string | null;
  fragmentado: boolean;
  archivo_nombre?: string | null;
  mime_type?: string | null;
  hash_contenido?: string | null;
  actualizado_en?: string | null;
  eliminado_en?: string | null;
}

export async function listarDocumentosAdmin(params: {
  tramite_id?: string;
  estado?: string;
  incluir_eliminados?: boolean;
  limite?: number;
  desde?: number;
} = {}): Promise<DocumentoAdmin[]> {
  const search = new URLSearchParams();
  if (params.tramite_id) search.set('tramite_id', params.tramite_id);
  if (params.estado) search.set('estado', params.estado);
  if (params.incluir_eliminados) search.set('incluir_eliminados', 'true');
  if (params.limite) search.set('limite', String(params.limite));
  if (params.desde) search.set('desde', String(params.desde));
  const qs = search.toString();
  return pedir<DocumentoAdmin[]>(`/api/admin/documentos${qs ? `?${qs}` : ''}`, {}, TIMEOUT_CATALOGO_MS);
}

export async function subirDocumento(
  form: FormData,
): Promise<DocumentoAdmin> {
  return pedir<DocumentoAdmin>(
    '/api/admin/documentos/upload',
    { method: 'POST', body: form },
    120000, // subir archivos puede tardar un poco
  );
}

export async function reprocesarDocumento(id: string): Promise<DocumentoAdmin> {
  return pedir<DocumentoAdmin>(`/api/admin/documentos/${id}/procesar`, { method: 'POST' }, TIMEOUT_CATALOGO_MS);
}

export async function eliminarDocumentoLogico(id: string): Promise<void> {
  await pedir(`/api/admin/documentos/${id}`, { method: 'DELETE' }, TIMEOUT_CATALOGO_MS);
}

export async function eliminarDocumentoFisico(id: string): Promise<void> {
  await pedir(`/api/admin/documentos/${id}/fisico`, { method: 'DELETE' }, TIMEOUT_CATALOGO_MS);
}

export async function listarTramitesAdmin(): Promise<TramiteCrudo[]> {
  return pedir<TramiteCrudo[]>('/api/tramites/admin', {}, TIMEOUT_CATALOGO_MS);
}