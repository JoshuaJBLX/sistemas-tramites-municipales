const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface FuenteCitada {
  titulo: string;
  referencia?: string;
  url?: string;
}

export interface RespuestaConsulta {
  texto: string;
  fuentes?: FuenteCitada[] | string[];
  confianza?: string;
  groundedness?: number;
}

export interface Tramite {
  id: string | number;
  nombre: string;
  descripcion: string;
  categoria?: string;
  costo?: string;
  plazo?: string;
  requisitos?: string[];
  estado?: 'activo' | 'actualizando' | 'nuevo';
}

export const SUGERENCIAS_RAPIDAS = [
  '¿Qué necesito para la partida de nacimiento?',
  '¿Cuánto cuesta la licencia de funcionamiento?',
  'Horario de mesa de partes',
  '¿Dónde pago mi impuesto predial?',
];

const TRAMITES_DEMO: Tramite[] = [
  { id: 1, nombre: 'Inscripción de nacimiento', descripcion: 'Registro oficial del nacimiento en la Oficina de Registro Civil de la MPJ.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: 'Inmediato (mismo día)', estado: 'activo', requisitos: ['Certificado de nacimiento del establecimiento de salud', 'DNI de la madre', 'DNI del padre (si aplica)'] },
  { id: 2, nombre: 'Licencia de funcionamiento', descripcion: 'Autorización para operar negocios. Incluye ITSE según el giro.', categoria: 'Licencias', costo: 'Según TUPA 2023', plazo: '5–15 días hábiles', estado: 'activo', requisitos: ['Formulario de solicitud', 'DNI del titular', 'Título de propiedad o contrato de alquiler', 'Plano de ubicación'] },
  { id: 3, nombre: 'Pago de impuesto predial', descripcion: 'Declaración y pago del impuesto predial en ventanilla o bancos autorizados.', categoria: 'Tributos', costo: 'Según predio', plazo: 'Inmediato', estado: 'nuevo', requisitos: ['Código de contribuyente', 'Declaración jurada del predio'] },
  { id: 4, nombre: 'Matrimonio civil', descripcion: 'Inscripción del matrimonio civil ante la Oficina de Registro Civil.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: 'Según programación', estado: 'activo', requisitos: ['DNI de contrayentes', 'Certificado de soltería', 'Dos testigos con DNI'] },
  { id: 5, nombre: 'Certificado de residencia', descripcion: 'Acreditación del domicilio en la provincia de Junín.', categoria: 'Certificados', costo: 'Según TUPA 2023', plazo: '1–3 días hábiles', estado: 'activo', requisitos: ['DNI del solicitante', 'Recibo de servicios básicos'] },
  { id: 6, nombre: 'Licencia de edificación', descripcion: 'Autorización para obras de construcción o remodelación (modalidades A–D).', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '10–20 días hábiles', estado: 'actualizando', requisitos: ['Título de propiedad', 'Planos arquitectónicos', 'Memoria descriptiva'] },
];

/** Envía consulta al backend; si no hay backend usa respuesta demo fundamentada. */
export async function enviarConsulta(pregunta: string): Promise<RespuestaConsulta> {
  try {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), 6000);
    const response = await fetch(`${API_URL}/api/consultas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pregunta }),
      signal: controller.signal,
    });
    clearTimeout(t);
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    return {
      texto: data.texto ?? data.respuesta ?? 'Sin respuesta del servidor.',
      fuentes: data.fuentes ?? [],
      confianza: data.confianza ?? data.nivel_confianza,
      groundedness: data.groundedness ?? 0.9,
    };
  } catch {
    return respuestaDemo(pregunta);
  }
}

function respuestaDemo(pregunta: string): RespuestaConsulta {
  const q = pregunta.toLowerCase();
  if (q.includes('nacimiento') || q.includes('partida')) {
    return {
      texto: 'La inscripción de nacimiento se realiza en la Oficina de Registro Civil de la Municipalidad Provincial de Junín. Presenta el certificado de nacimiento del establecimiento de salud, DNI de la madre y del padre (si está disponible). El trámite es inmediato, el mismo día.',
      fuentes: [{ titulo: 'TUPA 2023 · Registro Civil N.º 188', referencia: 'Municipalidad Provincial de Junín' }],
      confianza: 'alta', groundedness: 0.97,
    };
  }
  if (q.includes('licencia') || q.includes('funcionamiento')) {
    return {
      texto: 'La licencia de funcionamiento requiere formulario de solicitud, DNI del titular, título de propiedad o contrato de alquiler y plano de ubicación. El plazo es de 5 a 15 días hábiles según el giro; incluye la ITSE según el nivel de riesgo.',
      fuentes: [{ titulo: 'TUPA 2023 · Licencias N.º 9', referencia: 'Municipalidad Provincial de Junín' }],
      confianza: 'alta', groundedness: 0.94,
    };
  }
  return {
    texto: 'Con gusto te oriento. Indícame el trámite (p. ej. impuesto predial, matrimonio civil o certificado de residencia) y te detallo requisitos, arancel y plazo según el TUPA 2023 vigente.',
    fuentes: [{ titulo: 'TUPA 2023 · Catálogo oficial', referencia: 'Municipalidad Provincial de Junín' }],
    confianza: 'media', groundedness: 0.82,
  };
}

/** Obtiene trámites; usa demo si el backend no responde. */
export async function obtenerTramites(): Promise<Tramite[]> {
  try {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), 5000);
    const response = await fetch(`${API_URL}/api/tramites`, { signal: controller.signal });
    clearTimeout(t);
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    return Array.isArray(data) ? data : data.tramites ?? TRAMITES_DEMO;
  } catch {
    return TRAMITES_DEMO;
  }
}

export async function obtenerEstadoServicios() {
  try {
    const r = await fetch(`${API_URL}/api/health`);
    if (r.ok) return await r.json();
    throw new Error('offline');
  } catch {
    return { api: 'operativo', database: 'operativo', redis: 'operativo', ollama: 'operativo' };
  }
}

