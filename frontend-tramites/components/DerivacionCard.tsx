'use client';
import { Derivacion } from '../lib/api';

export default function DerivacionCard({ derivacion }: { derivacion: Derivacion }) {
  return (
    <div className="mt-3 rounded-2xl border border-amber-300 bg-amber-50 p-4 shadow-sm animate-rise-in">
      <p className="text-sm font-bold text-amber-900">Oficina recomendada para tu caso</p>
      <p className="mt-1 text-xs text-amber-800">{derivacion.motivo}</p>
      <div className="mt-3 space-y-1 text-xs">
        <p className="font-semibold text-amber-950">{derivacion.oficina}</p>
        <p className="text-amber-800">{derivacion.area}</p>
        <p className="text-amber-700">📞 {derivacion.telefono || 'Sin teléfono'} · ✉️ {derivacion.correo || 'Sin correo'}</p>
        <p className="text-amber-600">🕒 {derivacion.horario}</p>
        <p className="text-amber-600">📍 {derivacion.direccion}</p>
      </div>
    </div>
  );
}