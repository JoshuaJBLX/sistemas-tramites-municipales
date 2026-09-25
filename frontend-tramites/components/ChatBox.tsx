'use client';

import { useState } from 'react';
import { enviarConsulta, SUGERENCIAS_RAPIDAS } from '../lib/api';
import Loading from './Loading';
import ChatThread, { ChatMsg } from './ChatThread';
import { SendIcon, SparkIcon } from './icons';

export default function ChatBox({ compact = false }: { compact?: boolean }) {
  const [mensajes, setMensajes] = useState<ChatMsg[]>([]);
  const [entrada, setEntrada] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleEnviar = async (texto?: string) => {
    const pregunta = (texto ?? entrada).trim();
    if (!pregunta || cargando) return;
    setMensajes((prev) => [...prev, { autor: 'usuario', texto: pregunta }]);
    setEntrada('');
    setCargando(true);
    try {
      const r = await enviarConsulta(pregunta);
      setMensajes((prev) => [...prev, {
        autor: 'asistente', texto: r.texto,
        fuentes: r.fuentes, groundedness: r.groundedness, confianza: r.confianza,
      }]);
    } catch {
      setMensajes((prev) => [...prev, { autor: 'asistente', texto: 'Ocurrió un error al procesar la consulta. Intenta nuevamente.' }]);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className={`flex min-h-0 flex-col gap-3 ${compact ? '' : ''}`}>
      <div className={`glass flex min-h-0 flex-col gap-2 rounded-3xl p-4 ${compact ? 'h-[380px]' : 'h-[420px]'}`}>
        <ChatThread mensajes={mensajes} cargando={cargando} />
        {cargando && <Loading />}
        {mensajes.length === 0 && (
          <div className="flex flex-wrap gap-2 px-1 pb-1">
            {SUGERENCIAS_RAPIDAS.slice(0, compact ? 2 : 4).map((s) => (
              <button key={s} onClick={() => handleEnviar(s)} className="chip">
                ✨ {s}
              </button>
            ))}
          </div>
        )}
      </div>
      <div className="glass flex items-center gap-2 rounded-3xl p-2 pl-4">
        <SparkIcon className="h-5 w-5 shrink-0 text-emerald" />
        <input
          className="min-w-0 flex-1 bg-transparent text-sm text-ink outline-none placeholder:text-mist-500"
          value={entrada}
          onChange={(e) => setEntrada(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleEnviar()}
          placeholder="Escribe tu consulta sobre un trámite..."
          aria-label="Escribe tu consulta"
        />
        <button className="btn-primary-3d !rounded-full !px-5 !py-2.5 text-sm" onClick={() => handleEnviar()} disabled={cargando} aria-label="Enviar mensaje">
          <SendIcon className="h-5 w-5" />
          <span className="hidden sm:inline">Enviar</span>
        </button>
      </div>
    </div>
  );
}

