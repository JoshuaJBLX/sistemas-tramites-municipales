'use client';
import { useEffect, useMemo, useRef, useState } from 'react';
import GroundednessBadge from './GroundednessBadge';
import TramiteProbableCard from './TramiteProbableCard';
import VotoRespuesta from './VotoRespuesta';
import type { FuenteCitada, TramiteProbable } from '../lib/api';

export interface ChatMsg {
  autor: 'usuario' | 'asistente';
  texto: string;
  fuentes?: (FuenteCitada | string)[];
  groundedness?: number;
  confianza?: string;
  intencion?: string;
  pideAclaracion?: boolean;
  afirmacionBloqueada?: boolean;
  fueraDominio?: boolean;
  entidadSugerida?: string;
  tramiteProbable?: TramiteProbable | null;
  fallo?: boolean;
  /** HU-15: id de la consulta para poder calificar la respuesta. */
  consultaId?: string;
}

/** Límite de caracteres visibles antes de ofrecer "Ver más". */
const LIMITE_COLAPSO = 420;

type Bloque =
  | { tipo: 'paso'; numero: string; texto: string }
  | { tipo: 'apartado'; nombre: string; texto: string }
  | { tipo: 'parrafo'; texto: string };

function parsear(texto: string): Bloque[] {
  const bloques: Bloque[] = [];
  for (const linea of texto.split('\n')) {
    const paso = /^(\d+)\.\s+(.*)$/.exec(linea.trim());
    if (paso) {
      bloques.push({ tipo: 'paso', numero: paso[1], texto: paso[2] });
      continue;
    }
    const apartado = /^(REQUISITOS|PASOS|COSTO|PLAZO|OBSERVACIONES):\s*(.*)$/i.exec(linea.trim());
    if (apartado) {
      bloques.push({
        tipo: 'apartado',
        nombre: apartado[1].toUpperCase(),
        texto: apartado[2],
      });
      continue;
    }
    if (linea.trim()) bloques.push({ tipo: 'parrafo', texto: linea.trim() });
  }
  return bloques;
}

/** Renderiza **negrita** dentro del texto de un bloque. */
function conNegrita(texto: string) {
  const partes = texto.split(/\*\*([^*]+)\*\*/g);
  return partes.map((parte, i) =>
    i % 2 === 1 ? (
      <strong key={i} className="font-bold text-primary-900">{parte}</strong>
    ) : (
      <span key={i}>{parte}</span>
    ),
  );
}

function BloqueMensaje({ bloque }: { bloque: Bloque }) {
  if (bloque.tipo === 'paso') {
    return (
      <div className="flex gap-2.5 py-1">
        <span
          className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-emerald text-[11px] font-bold text-white"
          aria-hidden="true"
        >
          {bloque.numero}
        </span>
        <p className="text-sm leading-relaxed text-primary-900">{conNegrita(bloque.texto)}</p>
      </div>
    );
  }
  if (bloque.tipo === 'apartado') {
    return (
      <div className="mt-2 first:mt-0">
        <p className="text-[11px] font-extrabold uppercase tracking-wide text-emerald-deep">
          {bloque.nombre}
        </p>
        {bloque.texto && (
          <p className="mt-0.5 text-sm leading-relaxed text-primary-800">
            {conNegrita(bloque.texto)}
          </p>
        )}
      </div>
    );
  }
  return <p className="py-0.5 text-sm leading-relaxed text-primary-900">{conNegrita(bloque.texto)}</p>;
}

export function MuniAvatar() {
  return (
    <span className="avatar-muni" aria-hidden="true">
      <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none">
        <circle cx="12" cy="10" r="5.5" fill="#fff" opacity=".95" />
        <circle cx="10.2" cy="9.2" r="1.1" fill="#0f766e" />
        <circle cx="13.8" cy="9.2" r="1.1" fill="#0f766e" />
        <path d="M10.4 11.6q1.6 1.5 3.2 0" stroke="#0f766e" strokeWidth="1.4" strokeLinecap="round" />
        <path d="M12 4.2V3M11.4 4.6h2M12 4.2l-1.3.8M12 4.2l1.3.8" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" />
      </svg>
    </span>
  );
}

export function TypingDots() {
  return (
    <div className="bubble-bot flex items-center gap-1.5 !py-3.5 !rounded-2xl" aria-label="El asistente está escribiendo">
      {[0, 1, 2].map((i) => (
        <span key={i} className="h-2 w-2 rounded-full bg-emerald" style={{ animation: `typing-dot 1.2s ease-in-out ${i * 0.18}s infinite` }} />
      ))}
    </div>
  );
}

function MensajeAsistente({ m }: { m: ChatMsg }) {
  const [expandido, setExpandido] = useState(false);
  const bloques = useMemo(() => parsear(m.texto || ''), [m.texto]);
  const largo = (m.texto || '').length > LIMITE_COLAPSO;
  const visibles = useMemo(() => {
    if (!largo || expandido) return bloques;
    const salida: Bloque[] = [];
    let usados = 0;
    for (const bloque of bloques) {
      const peso = bloque.texto.length + 12;
      if (usados + peso > LIMITE_COLAPSO && salida.length > 0) break;
      salida.push(bloque);
      usados += peso;
    }
    return salida;
  }, [bloques, largo, expandido]);
  const fuente = m.fuentes?.find((f): f is FuenteCitada => typeof f !== 'string' && !!f.titulo);

  return (
    <div className="flex items-end gap-2 animate-rise-in max-w-[95%]">
      <MuniAvatar />
      <div className="min-w-0">
        <div className={`bubble-bot !rounded-2xl ${m.fallo ? 'border-amber-300' : ''}`}>
          {m.fueraDominio && (
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-primary-500">
              Fuera del alcance municipal{m.entidadSugerida ? ` → ${m.entidadSugerida}` : ''}
            </p>
          )}
          {m.afirmacionBloqueada && (
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-amber-700">
              Afirmación bloqueada por falta de respaldo documental
            </p>
          )}
          {m.pideAclaracion && (
            <p className="mb-1 text-xs font-bold uppercase tracking-wide text-amber-700">
              Necesito que precises tu consulta
            </p>
          )}
          {visibles.map((bloque, i) => (
            <BloqueMensaje key={i} bloque={bloque} />
          ))}
          {largo && (
            <button
              type="button"
              onClick={() => setExpandido((valor) => !valor)}
              className="mt-1 text-xs font-bold text-emerald-deep hover:underline"
            >
              {expandido ? 'Ver menos ▲' : 'Ver más ▼'}
            </button>
          )}
          {fuente && (
            <p className="mt-2 border-t border-white/60 pt-2 text-xs text-mist-500">
              Fuente oficial:{' '}
              {fuente.url ? (
                <a
                  href={fuente.url}
                  target="_blank"
                  rel="noreferrer"
                  className="font-semibold text-primary-500 hover:underline"
                >
                  {fuente.titulo}
                </a>
              ) : (
                <span className="font-semibold text-primary-700">{fuente.titulo}</span>
              )}
            </p>
          )}
          {m.tramiteProbable && <TramiteProbableCard tramite={m.tramiteProbable} />}
          {!m.fallo && <GroundednessBadge score={m.groundedness} fuentes={m.fuentes} />}
          {!m.fallo && <VotoRespuesta consultaId={m.consultaId} />}
        </div>
      </div>
    </div>
  );
}

export default function ChatThread({ mensajes, cargando }: { mensajes: ChatMsg[]; cargando: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: 'smooth' }); }, [mensajes, cargando]);
  return (
    <div ref={ref} className="scroll-thin flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-1 py-2">
      {mensajes.length === 0 && (
        <div className="flex items-end gap-2 animate-rise-in">
          <MuniAvatar />
          <div className="bubble-bot !rounded-2xl">
            <p className="font-semibold text-primary-800">¡Hola! Soy MUN AI, tu asistente virtual de trámites municipales 👋</p>
            <p className="mt-1 text-sm text-mist-500">Pregúntame por requisitos, costos y plazos. Respondo solo con información oficial, para que todo sea claro y sencillo.</p>
          </div>
        </div>
      )}
      {mensajes.map((m, i) =>
        m.autor === 'usuario' ? (
          <div key={i} className="bubble-user animate-rise-in">{m.texto}</div>
        ) : (
          <MensajeAsistente key={i} m={m} />
        ),
      )}
      {cargando && <TypingDots />}
    </div>
  );
}
