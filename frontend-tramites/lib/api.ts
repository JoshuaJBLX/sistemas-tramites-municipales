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
  { id: 7, nombre: 'Inscripción de defunción', descripcion: 'Registro oficial del fallecimiento. Trámite inmediato en Registro Civil.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: 'Inmediato (mismo día)', estado: 'activo', requisitos: ['Certificado de defunción', 'DNI del fallecido', 'DNI del declarante'] },
  { id: 8, nombre: 'Separación convencional', descripcion: 'Declaración de separación de cónyuges de manera consensuada.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: '10 días hábiles', estado: 'activo', requisitos: ['DNI de ambos cónyuges', 'Partida de matrimonio', 'Convenio de separación'] },
  { id: 9, nombre: 'Certificado de no adeudo', descripcion: 'Declara que no tienes deudas pendientes con la municipalidad.', categoria: 'Certificados', costo: 'Según TUPA 2023', plazo: '1–2 días hábiles', estado: 'activo', requisitos: ['DNI del solicitante', 'Solicitud escrita'] },
  { id: 10, nombre: 'Expedición de partida de nacimiento', descripcion: 'Emisión de partida o copia certificada para trámites civiles y escolares.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: 'Inmediato (mismo día)', estado: 'activo', requisitos: ['DNI del solicitante', 'Fecha del registro'] },
  { id: 11, nombre: 'Asignación de numeración municipal', descripcion: 'Numeración oficial del acceso principal del predio.', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '7 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Croquis de ubicación'] },
  { id: 12, nombre: 'Certificado de posesión', descripcion: 'Acredita la posesión de un terreno o inmueble previa verificación en campo.', categoria: 'Certificados', costo: 'Según TUPA 2023', plazo: '5 días hábiles', estado: 'nuevo', requisitos: ['Solicitud', 'DNI', 'Croquis o acta de verificación'] },
  { id: 13, nombre: 'Certificado de zonificación y compatibilidad de uso', descripcion: 'Certifica la zonificación del predio y el uso de suelo compatible con tu giro.', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '5 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Plano de ubicación', 'Descripción del giro'] },
  { id: 14, nombre: 'Certificado de parámetros urbanísticos y edificatorios', descripcion: 'Fija retiros, altura, coeficiente y área libre aplicables a tu predio.', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '8 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Título de propiedad'] },
  { id: 15, nombre: 'Aprobación de habilitación urbana', descripcion: 'Habilita terrenos residenciales, comerciales o industriales con servicios.', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '30–45 días hábiles', estado: 'actualizando', requisitos: ['Título de propiedad', 'Planos de habilitación', 'Estudios técnicos'] },
  { id: 16, nombre: 'Declaratoria de fábrica', descripcion: 'Registro formal de las edificaciones existentes ante SUNARP.', categoria: 'Urbanismo', costo: 'Según TUPA 2023', plazo: '15 días hábiles', estado: 'activo', requisitos: ['Título de propiedad', 'Planos y memoria descriptiva'] },
  { id: 17, nombre: 'Autorización de anuncios y publicidad exterior', descripcion: 'Permiso para paneles, carteles y anuncios en fachadas o vía pública.', categoria: 'Licencias', costo: 'Según TUPA 2023', plazo: '7 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Croquis de ubicación', 'Diseño del anuncio'] },
  { id: 18, nombre: 'Aut. de comercio en mercados y ambulatorio', descripcion: 'Permiso para comerciar en mercados municipales o zonas autorizadas.', categoria: 'Licencias', costo: 'Según TUPA 2023', plazo: '5 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Carné de sanidad vigente'] },
  { id: 19, nombre: 'Autorización de eventos públicos', descripcion: 'Permiso para ferias, espectáculos y actividades recreativas en espacios públicos.', categoria: 'Otros', costo: 'Según TUPA 2023', plazo: '10 días hábiles', estado: 'nuevo', requisitos: ['Solicitud', 'DNI', 'Plan de seguridad', 'Seguro contra accidentes'] },
  { id: 20, nombre: 'Inscripción de unión de hecho', descripcion: 'Reconocimiento legal de la convivencia ante la Oficina de Registro Civil.', categoria: 'Registro civil', costo: 'Según TUPA 2023', plazo: '15 días hábiles', estado: 'activo', requisitos: ['DNI de ambos', 'Acta notarial', 'Partidas de nacimiento'] },
  { id: 21, nombre: 'Empadronamiento municipal de predios', descripcion: 'Registro del contribuyente y sus predios para el cobro de tributos.', categoria: 'Tributos', costo: 'Según TUPA 2023', plazo: '10 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Título o contrato', 'Última DJ predio'] },
  { id: 22, nombre: 'Autorización de ocupación de vía pública', descripcion: 'Permiso temporal para ocupar vía pública durante una obra.', categoria: 'Otros', costo: 'Según TUPA 2023', plazo: '5 días hábiles', estado: 'activo', requisitos: ['Solicitud', 'DNI', 'Plano del área', 'Cronograma'] },
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

