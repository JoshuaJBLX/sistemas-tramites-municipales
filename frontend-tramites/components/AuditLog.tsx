'use client';

import { useEffect, useState } from 'react';
import { obtenerAuditoria, RegistroAuditoria } from '../lib/api';

function tonoDeConfianza(confianza?: string | null) {
  if (confianza === 'alta') return 'bg-emerald';
  if (confianza === 'media') return 'bg-amber';
  if (confianza === 'baja') return 'bg-primary-500';
  return 'bg-mist-400';
}

function horaDe(iso?: string | null) {
  if (!iso) return '--:--:--';
  const fecha = new Date(iso);
  return Number.isNaN(fecha.getTime())
    ? '--:--:--'
    : fecha.toLocaleTimeString('es-PE', { hour12: false });
}

function mensajeDe(r: RegistroAuditoria) {
  const partes: string[] = [`Consulta: ${r.pregunta.slice(0, 70)}${r.pregunta.length > 70 ? '…' : ''}`];
  if (r.fuera_dominio) {
    partes.push(`fuera de dominio → ${r.entidad_sugerida || 'otra entidad'}`);
  } else if (r.afirmaciones_bloqueadas) {
    partes.push('afirmación bloqueada (sin respaldo documental)');
  } else if (r.confianza) {
    partes.push(`confianza ${r.confianza} · groundedness ${Math.round((r.groundedness ?? 0) * 100)}%`);
  }
  if (r.fuentes?.length) partes.push(`${r.fuentes.length} fuente(s) citada(s)`);
  return partes.join(' · ');
}

export default function AuditLog() {
  const [registros, setRegistros] = useState<RegistroAuditoria[]>([]);
  const [estado, setEstado] = useState<'cargando' | 'ok' | 'error'>('cargando');

  useEffect(() => {
    let activo = true;
    obtenerAuditoria(15)
      .then((datos) => {
        if (!activo) return;
        setRegistros(datos);
        setEstado('ok');
      })
      .catch(() => {
        if (!activo) return;
        setEstado('error');
      });
    return () => {
      activo = false;
    };
  }, []);

  return (
    <div className="card-3d relative overflow-hidden p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Auditoría / Logs</h3>
        <span className="badge-blue">{estado === 'error' ? 'Sin conexión' : 'En vivo'}</span>
      </div>
      <ul className="scroll-thin mt-4 max-h-56 space-y-2.5 overflow-y-auto pr-1">
        {estado === 'cargando' && (
          <li className="rounded-2xl border border-white/60 bg-white/60 px-3 py-2.5 text-xs text-mist-500">
            Cargando auditoría desde la API…
          </li>
        )}
        {estado === 'error' && (
          <li className="rounded-2xl border border-amber/40 bg-amber-soft px-3 py-2.5 text-xs text-amber-deep">
            No se pudo consultar la auditoría. Verifica que la API esté disponible.
          </li>
        )}
        {estado === 'ok' && registros.length === 0 && (
          <li className="rounded-2xl border border-white/60 bg-white/60 px-3 py-2.5 text-xs text-mist-500">
            Aún no hay consultas registradas. Envía una consulta desde el chat.
          </li>
        )}
        {registros.map((r, i) => (
          <li
            key={r.id}
            className="flex items-start gap-3 rounded-2xl border border-white/60 bg-white/60 px-3 py-2.5 font-mono text-xs text-primary-900 shadow-sm backdrop-blur animate-rise-in"
            style={{ animationDelay: `${i * 70}ms` }}
          >
            <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${tonoDeConfianza(r.confianza)} shadow`} />
            <span className="text-mist-500">{horaDe(r.registrado_en || r.creada_en)}</span>
            <span className="font-sans font-medium">{mensajeDe(r)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
