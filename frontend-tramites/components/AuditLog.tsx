'use client';

import { useEffect, useState } from 'react';
import { AlertIcon, CheckIcon, CalendarIcon, SearchIcon, UserIcon } from './icons';
import { obtenerAuditoria, marcarInconsistente, RegistroAuditoria, FiltrosAuditoria } from '../lib/api';

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

function fechaCorta(iso?: string | null) {
  if (!iso) return '--/--/----';
  const fecha = new Date(iso);
  return Number.isNaN(fecha.getTime())
    ? '--/--/----'
    : fecha.toLocaleDateString('es-PE');
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
  const [filtros, setFiltros] = useState<FiltrosAuditoria>({ limite: 15 });
  const [aplicando, setAplicando] = useState(false);

  const cargar = async () => {
    setEstado('cargando');
    setAplicando(true);
    try {
      const datos = await obtenerAuditoria(filtros);
      setRegistros(datos);
      setEstado('ok');
    } catch {
      setEstado('error');
    } finally {
      setAplicando(false);
    }
  };

  useEffect(() => {
    cargar();
  }, []);

  const handleFiltrar = (e: React.FormEvent) => {
    e.preventDefault();
    cargar();
  };

  const handleMarcar = async (registro: RegistroAuditoria, marcado: boolean) => {
    const nota = prompt('Nota de revisión (opcional):', registro.nota_revision || '');
    if (nota === null) return; // cancelado
    try {
      const actualizado = await marcarInconsistente(registro.id, marcado, nota);
      setRegistros((prev) => prev.map((r) => (r.id === registro.id ? actualizado : r)));
    } catch (e: any) {
      alert(e.message || 'No se pudo marcar');
    }
  };

  return (
    <div className="card-3d p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Auditoría de consultas</h3>
        <span className="badge-blue">{estado === 'error' ? 'Sin conexión' : 'En vivo'}</span>
      </div>

      {/* Filtros HU-14 */}
      <form onSubmit={handleFiltrar} className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
        <div className="relative">
          <CalendarIcon className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-mist-500" />
          <input
            type="date"
            className="rounded-xl border px-8 py-2 text-sm"
            value={filtros.desde ? filtros.desde.slice(0, 10) : ''}
            onChange={(e) => setFiltros({ ...filtros, desde: e.target.value ? e.target.value + 'T00:00:00.000Z' : undefined })}
            placeholder="Desde"
            title="Fecha desde"
          />
        </div>
        <div className="relative">
          <CalendarIcon className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-mist-500" />
          <input
            type="date"
            className="rounded-xl border px-8 py-2 text-sm"
            value={filtros.hasta ? filtros.hasta.slice(0, 10) : ''}
            onChange={(e) => setFiltros({ ...filtros, hasta: e.target.value ? e.target.value + 'T23:59:59.999Z' : undefined })}
            placeholder="Hasta"
            title="Fecha hasta"
          />
        </div>
        <div className="relative">
          <SearchIcon className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-mist-500" />
          <input
            type="text"
            className="rounded-xl border px-8 py-2 text-sm"
            value={filtros.tramite || ''}
            onChange={(e) => setFiltros({ ...filtros, tramite: e.target.value || undefined })}
            placeholder="Trámite o pregunta"
            title="Buscar en pregunta o trámite probable"
          />
        </div>
        <div className="relative">
          <UserIcon className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-mist-500" />
          <input
            type="text"
            className="rounded-xl border px-8 py-2 text-sm"
            value={filtros.usuario_id || ''}
            onChange={(e) => setFiltros({ ...filtros, usuario_id: e.target.value || undefined })}
            placeholder="Usuario (UUID)"
            title="Filtrar por ID de usuario"
          />
        </div>
        <button type="submit" className="btn-neu text-sm sm:col-span-4 lg:col-span-1" disabled={aplicando}>
          {aplicando ? 'Filtrando…' : 'Filtrar'}
        </button>
      </form>

      <ul className="scroll-thin mt-4 max-h-72 space-y-2.5 overflow-y-auto pr-1">
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
            No hay consultas que coincidan con los filtros.
          </li>
        )}
        {registros.map((r, i) => (
          <li
            key={r.id}
            className={`flex items-start gap-3 rounded-2xl border border-white/60 bg-white/60 px-3 py-2.5 font-mono text-xs text-primary-900 shadow-sm backdrop-blur animate-rise-in ${
              r.inconsistente ? 'border-amber-300 bg-amber-soft/30' : ''
            }`}
            style={{ animationDelay: `${i * 50}ms` }}
          >
            <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${tonoDeConfianza(r.confianza)} shadow`} />
            <span className="text-mist-500 whitespace-nowrap">{fechaCorta(r.registrado_en || r.creada_en)} {horaDe(r.registrado_en || r.creada_en)}</span>
            <span className="font-sans font-medium flex-1 min-w-0">{mensajeDe(r)}</span>
            {r.inconsistente && (
              <span className="flex items-center gap-1 rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-deep shrink-0">
                <AlertIcon className="h-3 w-3" /> Inconsistente
              </span>
            )}
            {r.marcado_inconsistente && (
              <span className="flex items-center gap-1 rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-bold text-emerald-deep shrink-0">
                <CheckIcon className="h-3 w-3" /> Marcado
              </span>
            )}
            <button
              className="shrink-0 rounded-lg border px-2 py-1 text-[10px] hover:bg-primary-50 transition"
              onClick={() => handleMarcar(r, !r.marcado_inconsistente)}
              title={r.marcado_inconsistente ? 'Desmarcar como inconsistente' : 'Marcar como inconsistente'}
            >
              {r.marcado_inconsistente ? 'Desmarcar' : 'Marcar'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}