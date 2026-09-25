export default function Loading() {
  return (
    <div className="flex items-center gap-2 self-start rounded-2xl border border-white/60 bg-white/70 px-3 py-2 text-xs font-semibold text-primary-600 shadow-sm backdrop-blur" role="status" aria-label="Procesando consulta">
      <span className="h-2 w-2 rounded-full bg-primary-500" style={{ animation: 'typing-dot 1.2s ease-in-out 0s infinite' }} />
      <span className="h-2 w-2 rounded-full bg-primary-500" style={{ animation: 'typing-dot 1.2s ease-in-out .18s infinite' }} />
      <span className="h-2 w-2 rounded-full bg-emerald" style={{ animation: 'typing-dot 1.2s ease-in-out .36s infinite' }} />
      <span>Muni está consultando fuentes oficiales…</span>
    </div>
  );
}
