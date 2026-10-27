'use client';

import { useState } from 'react';
import { evaluarConsulta, type Valoracion } from '../lib/api';
import { ThumbDownIcon, ThumbUpIcon, CheckIcon } from './icons';

const ETIQUETAS: Record<Valoracion, string> = {
  util: 'Útil',
  parcialmente_util: 'Parcialmente útil',
  no_util: 'No útil',
};

/**
 * HU-15 — retroalimentación ciudadana: el ciudadano vota la respuesta
 * (útil / parcialmente útil / no útil) y puede dejar un comentario opcional.
 */
export default function VotoRespuesta({ consultaId }: { consultaId?: string }) {
  const [valoracion, setValoracion] = useState<Valoracion | null>(null);
  const [comentario, setComentario] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [guardado, setGuardado] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!consultaId) return null;

  const votar = async (opcion: Valoracion) => {
    if (enviando || guardado) return;
    setEnviando(true);
    setError(null);
    try {
      await evaluarConsulta(consultaId, opcion, comentario);
      setValoracion(opcion);
      setGuardado(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo registrar tu valoración.');
    } finally {
      setEnviando(false);
    }
  };

  if (guardado && valoracion) {
    return (
      <div className="mt-2 flex items-center gap-2 rounded-xl bg-emerald-soft/60 px-3 py-2 text-xs font-semibold text-emerald-deep">
        <CheckIcon className="h-4 w-4" />
        Gracias por tu valoración: {ETIQUETAS[valoracion].toLowerCase()}.
      </div>
    );
  }

  return (
    <div className="mt-2 rounded-xl border border-white/70 bg-white/60 px-3 py-2">
      <p className="text-xs font-bold uppercase tracking-wide text-mist-500">
        ¿Te ayudó esta respuesta?
      </p>
      <div className="mt-1.5 flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={enviando}
          onClick={() => votar('util')}
          className="inline-flex items-center gap-1.5 rounded-lg border border-emerald/40 bg-white px-2.5 py-1.5 text-xs font-bold text-emerald-deep transition hover:bg-emerald-soft disabled:opacity-50"
          aria-label="Marcar como útil"
        >
          <ThumbUpIcon className="h-4 w-4" />
          Útil
        </button>
        <button
          type="button"
          disabled={enviando}
          onClick={() => votar('parcialmente_util')}
          className="inline-flex items-center gap-1.5 rounded-lg border border-amber/40 bg-white px-2.5 py-1.5 text-xs font-bold text-amber-deep transition hover:bg-amber-soft disabled:opacity-50"
          aria-label="Marcar como parcialmente útil"
        >
          <ThumbUpIcon className="h-4 w-4" />
          Parcial
        </button>
        <button
          type="button"
          disabled={enviando}
          onClick={() => votar('no_util')}
          className="inline-flex items-center gap-1.5 rounded-lg border border-rose-200 bg-white px-2.5 py-1.5 text-xs font-bold text-rose-600 transition hover:bg-rose-50 disabled:opacity-50"
          aria-label="Marcar como no útil"
        >
          <ThumbDownIcon className="h-4 w-4" />
          No útil
        </button>
      </div>
      <textarea
        value={comentario}
        onChange={(e) => setComentario(e.target.value)}
        maxLength={1000}
        rows={2}
        placeholder="Comentario opcional (sin datos personales)"
        className="mt-2 w-full resize-none rounded-lg border border-mist-200 bg-white px-2.5 py-1.5 text-xs text-ink outline-none focus:border-primary-400"
      />
      {error && <p className="mt-1 text-xs font-semibold text-rose-600">{error}</p>}
    </div>
  );
}
