'use client';

import type { Tramite } from '../lib/api';
import { DocIcon, ClockIcon } from './icons';

const badgeByEstado: Record<string, string> = {
  activo: 'badge-emerald',
  nuevo: 'badge-blue',
  actualizando: 'badge-amber',
};

export default function TramiteCard({ tramite, index = 0 }: { tramite: Tramite; index?: number }) {
  return (
    <article
      className="card-3d group relative overflow-hidden p-5 animate-rise-in"
      style={{ animationDelay: `${Math.min(index, 8) * 60}ms` }}
    >
      <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-amber-soft/60 blur-2xl transition group-hover:scale-150" aria-hidden="true" />
    <div className="absolute -left-12 -bottom-12 h-32 w-32 rounded-full bg-emerald-soft/50 blur-2xl transition group-hover:scale-150" aria-hidden="true" />
      <div className="relative">
        <div className="flex items-start justify-between gap-2">
          <span className="flex h-11 w-11 items-center justify-center rounded-full bg-gradient-to-b from-emerald to-emerald-deep text-white shadow-lift">
            <DocIcon className="h-6 w-6" />
          </span>
          {tramite.estado && <span className={badgeByEstado[tramite.estado] ?? 'badge-blue'}>{tramite.estado}</span>}
        </div>
        {tramite.categoria && <p className="eyebrow mt-3 !text-[10px]">{tramite.categoria}</p>}
        <h2 className="mt-1 text-lg font-extrabold tracking-tight text-ink">{tramite.nombre}</h2>
        <p className="mt-1 text-sm leading-relaxed text-mist-500">{tramite.descripcion}</p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs font-semibold">
          {tramite.costo && <span className="chip">💰 {tramite.costo}</span>}
          {tramite.plazo && <span className="chip"><ClockIcon className="h-3.5 w-3.5" /> {tramite.plazo}</span>}
        </div>
        {tramite.requisitos && tramite.requisitos.length > 0 && (
          <ul className="mt-3 space-y-1 border-t border-mist-200 pt-3 text-xs text-primary-800">
            {tramite.requisitos.slice(0, 3).map((req, i) => (
              <li key={i} className="flex items-center gap-2">
                <span className="flex h-4 w-4 items-center justify-center rounded-full bg-emerald-soft text-[10px] font-bold text-emerald-deep">✓</span>
                {req}
              </li>
            ))}
          </ul>
        )}
      </div>
    </article>
  );
}

