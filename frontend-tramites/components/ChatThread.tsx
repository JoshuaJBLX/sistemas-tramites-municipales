'use client';
import { useEffect, useRef } from 'react';
import GroundednessBadge from './GroundednessBadge';
import type { FuenteCitada } from '../lib/api';

export interface ChatMsg {
  autor: 'usuario' | 'asistente';
  texto: string;
  fuentes?: (FuenteCitada | string)[];
  groundedness?: number;
  confianza?: string;
}

export function MuniAvatar() {
  return (
    <span className="avatar-muni" aria-hidden="true">
      <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none">
        <circle cx="12" cy="10" r="5.5" fill="#fff" opacity=".95" />
        <circle cx="10.2" cy="9.2" r="1.1" fill="#0f766e" />
        <circle cx="13.8" cy="9.2" r="1.1" fill="#0f766e" />
        <path d="M10.4 11.6q1.6 1.5 3.2 0" stroke="#0f766e" strokeWidth="1.4" strokeLinecap="round" />
        <path d="M12 4.2V3M11 4.6h2M12 4.2l-1.3.8M12 4.2l1.3.8" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" />
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

export default function ChatThread({ mensajes, cargando }: { mensajes: ChatMsg[]; cargando: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: 'smooth' }); }, [mensajes, cargando]);
  return (
    <div ref={ref} className="scroll-thin flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-1 py-2">
      {mensajes.length === 0 && (
        <div className="flex items-end gap-2 animate-rise-in">
          <MuniAvatar />
          <div className="bubble-bot !rounded-2xl">
            <p className="font-semibold text-primary-800">¡Hola! Soy Muni, tu asistente virtual 👋</p>
            <p className="mt-1 text-sm text-mist-500">Pregúntame por requisitos, costos y plazos. Respondo solo con información oficial, para que todo sea claro y sencillo.</p>
          </div>
        </div>
      )}
      {mensajes.map((m, i) =>
        m.autor === 'usuario' ? (
          <div key={i} className="bubble-user animate-rise-in">{m.texto}</div>
        ) : (
          <div key={i} className="flex items-end gap-2 animate-rise-in max-w-[95%]">
            <MuniAvatar />
            <div className="min-w-0">
              <div className="bubble-bot !rounded-2xl">
                <p>{m.texto}</p>
                <GroundednessBadge score={m.groundedness} fuentes={m.fuentes} />
              </div>
            </div>
          </div>
        ),
      )}
      {cargando && <TypingDots />}
    </div>
  );
}