const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Render free se duerme tras 15 min sin tráfico: la primera petición en frío
// tarda ~30-60 s en despertar el servicio, así que los timeouts cubren ese
// arranque (catálogo 60 s, consulta 90 s).
const TIMEOUT_CONSULTA_MS = 90000;
const TIMEOUT_CATALOGO_MS = 60000;

// ---------- Sesión (HU-13): token JWT en localStorage ----------
const CLAVE_SESION = 'tramites_sesion';

export interface SesionUsuario {
  id: string;
  nombre: string;
  correo: string;
  rol: string;
}

interface SesionGuardada {
  access_token: string;
  usuario: SesionUsuario;
}

export function leerSesion(): SesionGuardada | null {
  if (typeof window === 'undefined') return null;
  try {
    const crudo = window.localStorage.getItem(CLAVE_SESION);
    return crudo ? (JSON.parse(crudo) as SesionGuardada) : null;
  } catch {
    return null;
  }
}

export function cerrarSesion(): void {
  if (typeof window !== 'undefined') window.localStorage.removeItem(CLAVE_SESION);
}

export async function iniciarSesion(correo: string, password: string): Promise<SesionUsuario> {
  const data = await pedir<SesionGuardada>(
    '/api/auth/login',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ correo, password }),
    },
    TIMEOUT_CATALOGO_MS,
  );
  if (typeof window !== 'undefined') window.localStorage.setItem(CLAVE_SESION, JSON.stringify(data));
  return data.usuario;
}

export async function obtenerSesionActual(): Promise<SesionUsuario | null> {
  const sesion = leerSesion();
  if (!sesion) return null;
  try {
    const usuario = await pedir<SesionUsuario>('/api/auth/me', {}, TIMEOUT_CATALOGO_MS);
    return usuario;
  } catch {
    cerrarSesion();
    return null;
  }
}

export interface FuenteCitada {
  titulo: string;
  fragmento?: string;
  url?: string;
  numero?: string;
  fecha?: string;
  version?: string;
}

export interface Derivacion {
  oficina: string;
  area: string;
  telefono: string | null;
  correo: string | null;
  horario: string;
  direccion: string;
  motivo: string;
}

export interface Oficina {
  id: string;
  nombre: string;
  area: string;
  telefono: string | null;
  correo: string | null;
  horario: string;
  direccion: string;
  responsable: string | null;
  activa: boolean;
  creada_en: string;
}

export interface RespuestaConsulta {
  consulta_id: string;
  texto: string;
  fuentes: FuenteCitada[];
  confianza: string;
  groundedness: number;
  confianza_intencion: number;
  pide_aclaracion: boolean;
  afirmaciones_bloqueadas: boolean;
  fuera_dominio: boolean;
  entidad_sugerida: string;
  intencion: string;
  tramite_probable: TramiteProbable | null;
  // HU-17
  derivacion: Derivacion | null;
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
  area?: string | null;
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
    // HU-13: si hay sesión abierta se adjunta el JWT en Authorization.
    const sesion = leerSesion();
    const cabeceras = new Headers(init.headers);
    if (sesion && !cabeceras.has('Authorization')) {
      cabeceras.set('Authorization', `Bearer ${sesion.access_token}`);
    }
    const response = await fetch(`${API_URL}${url}`, { ...init, headers: cabeceras, signal: controller.signal });
    if (!response.ok) {
      const detalle = await leerDetalle(response);
      throw new Error(detalle ?? `El servidor respondió ${response.status}.`);
    }
    // 204 No Content (DELETE) y respuestas sin cuerpo: no hay JSON que leer (D-20).
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return undefined as T;
    }
    const texto = await response.text();
    if (!texto.trim()) return undefined as T;
    return JSON.parse(texto) as T;
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
    consulta_id: data.consulta_id ?? '',
    texto: data.texto ?? 'Sin respuesta del servidor.',
    fuentes: Array.isArray(data.fuentes) ? (data.fuentes as FuenteCitada[]) : [],
    confianza: data.confianza ?? 'desconocida',
    groundedness: typeof data.groundedness === 'number' ? data.groundedness : 0,
    confianza_intencion: typeof data.confianza_intencion === 'number' ? data.confianza_intencion : 0,
    pide_aclaracion: Boolean(data.pide_aclaracion),
    afirmaciones_bloqueadas: Boolean(data.afirmaciones_bloqueadas),
    fuera_dominio: Boolean(data.fuera_dominio),
    entidad_sugerida: data.entidad_sugerida ?? '',
    intencion: data.intencion ?? 'desconocida',
    tramite_probable: data.tramite_probable ?? null,
  };
}

// ---------- Auditoría (HU-10 / HU-14): trazabilidad real de las consultas ----------
export interface RegistroAuditoria {
  id: string;
  pregunta: string;
  intencion?: string | null;
  creada_en: string;
  respuesta?: string | null;
  confianza?: string | null;
  groundedness: number;
  afirmaciones_bloqueadas: boolean;
  fuera_dominio: boolean;
  entidad_sugerida: string;
  fuentes: FuenteCitada[];
  registrado_en?: string | null;
  // HU-14
  marcado_inconsistente?: boolean;
  nota_revision?: string | null;
  inconsistente?: boolean;
}

export interface FiltrosAuditoria {
  limite?: number;
  desde?: string; // ISO 8601
  hasta?: string; // ISO 8601
  tramite?: string;
  usuario_id?: string;
}

export async function obtenerAuditoria(filtros: FiltrosAuditoria = {}): Promise<RegistroAuditoria[]> {
  const { limite = 20, desde, hasta, tramite, usuario_id } = filtros;
  const search = new URLSearchParams();
  search.set('limite', String(limite));
  if (desde) search.set('desde', desde);
  if (hasta) search.set('hasta', hasta);
  if (tramite) search.set('tramite', tramite);
  if (usuario_id) search.set('usuario_id', usuario_id);
  const data = await pedir<RegistroAuditoria[]>(
    `/api/consultas?${search.toString()}`,
    {},
    TIMEOUT_CATALOGO_MS,
  );
  return Array.isArray(data) ? data : [];
}

/** HU-14: marcar/desmarcar registro como inconsistente (solo admin). */
export async function marcarInconsistente(
  consultaId: string,
  marcado: boolean,
  nota?: string,
): Promise<RegistroAuditoria> {
  return pedir<RegistroAuditoria>(
    `/api/consultas/${consultaId}/marcar`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ marcado, nota: nota || null }),
    },
    TIMEOUT_CATALOGO_MS,
  );
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
  area_responsable?: string | null;
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
    area: fila.area_responsable ?? null,
  };
}

export interface TramiteRelacionado extends Tramite {
  similitud: number;
}

export async function obtenerTramites(): Promise<Tramite[]> {
  const data = await pedir<TramiteCrudo[]>('/api/tramites', {}, TIMEOUT_CATALOGO_MS);
  return Array.isArray(data) ? data.map(mapearTramite) : [];
}

export interface TramiteDestacado extends Tramite {
  consultas: number;
}

export interface CatalogoDestacado {
  tramites: TramiteDestacado[];
  criterio: 'mas_solicitados' | 'aleatorio';
}

/** Vitrina de la portada: los trámites más consultados o, sin datos, aleatorios. */
export async function obtenerTramitesDestacados(limite = 4): Promise<CatalogoDestacado> {
  const data = await pedir<{ tramites: (TramiteCrudo & { consultas?: number })[]; criterio?: string }>(
    `/api/tramites/destacados?limite=${limite}`,
    {},
    TIMEOUT_CATALOGO_MS,
  );
  return {
    tramites: Array.isArray(data.tramites)
      ? data.tramites.map((fila) => ({ ...mapearTramite(fila), consultas: fila.consultas ?? 0 }))
      : [],
    criterio: data.criterio === 'mas_solicitados' ? 'mas_solicitados' : 'aleatorio',
  };
}

export async function obtenerTramitesRelacionados(
  tramiteId: string,
  limite = 4,
): Promise<TramiteRelacionado[]> {
  const data = await pedir<(TramiteCrudo & { similitud: number })[]>(
    `/api/tramites/${tramiteId}/relacionados?limite=${limite}`,
    {},
    TIMEOUT_CATALOGO_MS,
  );
  return Array.isArray(data)
    ? data.map((fila) => ({ ...mapearTramite(fila), similitud: fila.similitud ?? 0 }))
    : [];
}

// ---------- Directorio de oficinas (HU-17) ----------
export async function listarOficinas(soloActivas = true): Promise<Oficina[]> {
  const data = await pedir<Oficina[]>(
    `/api/oficinas?solo_activas=${soloActivas}`,
    {},
    TIMEOUT_CATALOGO_MS,
  );
  return Array.isArray(data) ? data : [];
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

export type EstadoDocumentoAdmin = 'vigente' | 'obsoleto' | 'en_revision' | 'derogado';

export async function cambiarEstadoDocumento(
  id: string,
  estado: EstadoDocumentoAdmin,
): Promise<DocumentoAdmin> {
  return pedir<DocumentoAdmin>(
    `/api/admin/documentos/${id}/estado`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ estado }),
    },
    TIMEOUT_CATALOGO_MS,
  );
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

// ---------- Retroalimentación (HU-15): voto sobre la respuesta ----------
export type Valoracion = 'util' | 'parcialmente_util' | 'no_util';

export interface Evaluacion {
  id: string;
  consulta_id: string;
  valoracion: Valoracion;
  comentario: string | null;
  creada_en: string;
  actualizada_en?: string | null;
}

export async function evaluarConsulta(
  consultaId: string,
  valoracion: Valoracion,
  comentario?: string,
): Promise<Evaluacion> {
  return pedir<Evaluacion>(
    `/api/consultas/${consultaId}/evaluacion`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ valoracion, comentario: comentario || null }),
    },
    TIMEOUT_CATALOGO_MS,
  );
}

export async function obtenerEvaluacion(consultaId: string): Promise<Evaluacion | null> {
  try {
    return await pedir<Evaluacion>(
      `/api/consultas/${consultaId}/evaluacion`,
      {},
      TIMEOUT_CATALOGO_MS,
    );
  } catch {
    return null;
  }
}

// ---------- Métricas (HU-16) y reportes (HU-18): solo administrador ----------
export interface Metricas {
  periodo_dias: number;
  generado_en: string;
  total_consultas: number;
  consultas_periodo: number;
  serie_diaria: { fecha: string; cantidad: number }[];
  por_intencion: { clave: string; cantidad: number }[];
  por_confianza: { clave: string; cantidad: number }[];
  groundedness_promedio: number;
  tasa_fundamentadas: number;
  respuestas_bloqueadas: number;
  consultas_fuera_dominio: number;
  duracion_promedio_ms: number | null;
  tramites_frecuentes: { nombre: string; cantidad: number }[];
  total_evaluaciones: number;
  satisfaccion_pct: number | null;
  alerta: boolean;
  alerta_mensaje: string | null;
}

export interface Reporte {
  desde: string;
  hasta: string;
  generado_en: string;
  consultas: number;
  serie_diaria: { fecha: string; cantidad: number }[];
  tramites_frecuentes: { nombre: string; cantidad: number }[];
  por_confianza: { clave: string; cantidad: number }[];
  groundedness_promedio: number;
  tasa_fundamentadas: number;
  respuestas_rechazadas: number;
  consultas_fuera_dominio: number;
  duracion_promedio_ms: number | null;
  total_evaluaciones: number;
  utiles: number;
  parcialmente_utiles: number;
  no_utiles: number;
  satisfaccion_pct: number | null;
}

export interface EvaluacionAdmin {
  id: string;
  consulta_id: string;
  pregunta: string;
  intencion?: string | null;
  valoracion: Valoracion;
  comentario: string | null;
  creada_en: string;
}

export async function obtenerMetricas(dias = 30): Promise<Metricas> {
  return pedir<Metricas>(`/api/metricas?dias=${dias}`, {}, TIMEOUT_CATALOGO_MS);
}

export async function obtenerEvaluacionesAdmin(limite = 50): Promise<EvaluacionAdmin[]> {
  const data = await pedir<EvaluacionAdmin[]>(
    `/api/evaluaciones?limite=${limite}`,
    {},
    TIMEOUT_CATALOGO_MS,
  );
  return Array.isArray(data) ? data : [];
}

export async function obtenerReporte(desde?: string, hasta?: string): Promise<Reporte> {
  const search = new URLSearchParams();
  if (desde) search.set('desde', desde);
  if (hasta) search.set('hasta', hasta);
  const qs = search.toString();
  return pedir<Reporte>(`/api/reportes${qs ? `?${qs}` : ''}`, {}, TIMEOUT_CATALOGO_MS);
}

/**
 * HU-18: descarga el reporte del periodo como CSV (el backend emite UTF-8 con
 * BOM para que Excel lo abra con acentos correctos).
 */
export async function descargarReporteCsv(desde?: string, hasta?: string): Promise<void> {
  const search = new URLSearchParams();
  if (desde) search.set('desde', desde);
  if (hasta) search.set('hasta', hasta);
  const qs = search.toString();
  const sesion = leerSesion();
  const controller = new AbortController();
  const temporizador = setTimeout(() => controller.abort(), TIMEOUT_CATALOGO_MS);
  try {
    const response = await fetch(`${API_URL}/api/reportes/exportar${qs ? `?${qs}` : ''}`, {
      headers: sesion ? { Authorization: `Bearer ${sesion.access_token}` } : undefined,
      signal: controller.signal,
    });
    if (!response.ok) throw new Error(`El servidor respondió ${response.status}.`);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const enlace = document.createElement('a');
    const disposicion = response.headers.get('content-disposition') ?? '';
    const coincide = /filename="([^"]+)"/.exec(disposicion);
    enlace.href = url;
    enlace.download = coincide?.[1] ?? 'reporte_tramites.csv';
    document.body.appendChild(enlace);
    enlace.click();
    enlace.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('La exportación está tardando demasiado. Intenta de nuevo.');
    }
    throw error;
  } finally {
    clearTimeout(temporizador);
  }
}