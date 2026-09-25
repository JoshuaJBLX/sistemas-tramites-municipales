const rows = [
  { t: '09:42:11', msg: 'Consulta #8.412 respondida · groundedness 97% · 240 ms', tone: 'bg-emerald' },
  { t: '09:41:03', msg: 'Documento indexado: TUPA 2023 · Registro Civil (BGE-M3)', tone: 'bg-primary-500' },
  { t: '09:38:57', msg: 'Caché Redis HIT en trámite "impuesto predial"', tone: 'bg-primary-500' },
  { t: '09:35:20', msg: 'Alerta suave: latencia SLM 1.9 s · reintento OK', tone: 'bg-amber' },
  { t: '09:31:44', msg: 'Auditoría: 1.236 consultas registradas hoy', tone: 'bg-emerald' },
];

export default function AuditLog() {
  return (
    <div className="card-3d relative overflow-hidden p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Auditoría / Logs</h3>
        <span className="badge-blue">En vivo</span>
      </div>
      <ul className="scroll-thin mt-4 max-h-56 space-y-2.5 overflow-y-auto pr-1">
        {rows.map((r, i) => (
          <li key={i} className="flex items-start gap-3 rounded-2xl border border-white/60 bg-white/60 px-3 py-2.5 font-mono text-xs text-primary-900 shadow-sm backdrop-blur animate-rise-in" style={{ animationDelay: `${i * 70}ms` }}>
            <span className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${r.tone} shadow`} />
            <span className="text-mist-500">{r.t}</span>
            <span className="font-sans font-medium">{r.msg}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
