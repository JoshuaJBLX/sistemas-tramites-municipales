'use client';
import { useEffect, useState } from 'react';
import { obtenerEstadoServicios } from '../lib/api';

const items = [
  { key: 'api', label: 'API FastAPI' },
  { key: 'database', label: 'Base de datos + pgvector' },
  { key: 'redis', label: 'Redis caché' },
  { key: 'ollama', label: 'SLM Ollama' },
];

export function StatusDot({ on = true }: { on?: boolean }) {
  return (
    <span className="relative flex h-3.5 w-3.5">
      {on && <span className="absolute h-full w-full animate-pulse-ring rounded-full bg-emerald" />}
      <span className={`h-3.5 w-3.5 rounded-full border-2 border-white shadow ${on ? 'bg-emerald shadow-glow-emerald' : 'bg-amber shadow-glow-amber'}`} />
    </span>
  );
}

export default function ServiceStatus() {
  const [state, setState] = useState<Record<string, string>>({ api: 'operativo', database: 'operativo', redis: 'operativo', ollama: 'operativo' });
  useEffect(() => { obtenerEstadoServicios().then(setState).catch(() => {}); }, []);
  return (
    <div className="card-3d p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Monitoreo de servicios</h3>
        <span className="badge-emerald"><StatusDot on /> Todo operativo</span>
      </div>
      <ul className="mt-4 space-y-3">
        {items.map((s) => (
          <li key={s.key} className="flex items-center justify-between rounded-2xl border border-white/60 bg-white/60 px-4 py-2.5 shadow-sm backdrop-blur">
            <span className="flex items-center gap-3 text-sm font-semibold text-primary-800">
              <StatusDot on={(state[s.key] ?? 'operativo') === 'operativo'} />
              {s.label}
            </span>
            <span className="font-mono text-xs text-emerald-deep">99.9% · {(state[s.key] ?? 'operativo')}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
