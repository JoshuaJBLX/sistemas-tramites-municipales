'use client';
import { useEffect, useState } from 'react';
import { obtenerEstadoServicios, type EstadoServicios } from '../lib/api';

const items: { key: keyof EstadoServicios; label: string }[] = [
  { key: 'api', label: 'API FastAPI' },
  { key: 'database', label: 'Base de datos + pgvector' },
  { key: 'redis', label: 'Redis caché' },
  { key: 'ollama', label: 'SLM Ollama' },
];

const OPERATIVO = 'operativo';

export function StatusDot({ on = true }: { on?: boolean }) {
  return (
    <span className="relative flex h-3.5 w-3.5">
      {on && <span className="absolute h-full w-full animate-pulse-ring rounded-full bg-emerald" />}
      <span className={`h-3.5 w-3.5 rounded-full border-2 border-white shadow ${on ? 'bg-emerald shadow-glow-emerald' : 'bg-amber shadow-glow-amber'}`} />
    </span>
  );
}

export default function ServiceStatus() {
  const [state, setState] = useState<EstadoServicios | null>(null);

  useEffect(() => {
    obtenerEstadoServicios().then(setState).catch(() => {});
  }, []);

  const operativo = (clave: keyof EstadoServicios) => state?.[clave] === OPERATIVO;
  const todosOperativos = state !== null && items.every((s) => operativo(s.key));

  return (
    <div className="card-3d p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Monitoreo de servicios</h3>
        {state === null ? (
          <span className="badge-blue">Comprobando…</span>
        ) : todosOperativos ? (
          <span className="badge-emerald"><StatusDot on /> Todo operativo</span>
        ) : (
          <span className="badge-amber"><StatusDot on={false} /> Verificación parcial</span>
        )}
      </div>
      <ul className="mt-4 space-y-3">
        {items.map((s) => (
          <li key={s.key} className="flex items-center justify-between rounded-2xl border border-white/60 bg-white/60 px-4 py-2.5 shadow-sm backdrop-blur">
            <span className="flex items-center gap-3 text-sm font-semibold text-primary-800">
              <StatusDot on={operativo(s.key)} />
              {s.label}
            </span>
            {/* El backend solo expone /health: el resto se informa tal cual, sin inventar métricas. */}
            <span className="font-mono text-xs text-primary-600">{state?.[s.key] ?? 'sin verificar'}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}