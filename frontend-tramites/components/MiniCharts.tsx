function Donut({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 34;
  const c = 2 * Math.PI * r;
  return (
    <div className="flex items-center gap-3">
      <div className="relative h-20 w-20" style={{ filter: 'drop-shadow(0 6px 10px rgba(20,50,87,.18))' }}>
        <svg viewBox="0 0 84 84" className="h-20 w-20 -rotate-90">
          <circle cx="42" cy="42" r={r} fill="none" stroke="#edf1f6" strokeWidth="11" />
          <circle cx="42" cy="42" r={r} fill="none" stroke={color} strokeWidth="11" strokeLinecap="round"
            strokeDasharray={`${(value / 100) * c} ${c}`} />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-sm font-extrabold text-ink">{value}%</span>
      </div>
      <span className="text-xs font-bold uppercase tracking-wider text-mist-500">{label}</span>
    </div>
  );
}

const bars = [
  { d: 'Lun', h: 42 }, { d: 'Mar', h: 68 }, { d: 'Mié', h: 54 },
  { d: 'Jue', h: 86 }, { d: 'Vie', h: 72 }, { d: 'Sáb', h: 38 }, { d: 'Dom', h: 26 },
];

export default function MiniCharts() {
  return (
    <div className="card-3d p-5">
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-ink">Métricas de atención</h3>
        <span className="badge-blue">Últimos 7 días</span>
      </div>
      <div className="mt-4 flex items-end justify-between gap-2">
        {bars.map((b, i) => (
          <div key={b.d} className="flex flex-1 flex-col items-center gap-1.5">
            <div
              className={`w-full max-w-[38px] rounded-xl border border-white/50 bg-gradient-to-t shadow-soft-sm ${i === 3 ? 'from-amber-deep via-amber to-[#ffd97a]' : 'from-primary-800 via-primary-500 to-primary-300'}`}
              style={{ height: `${b.h * 1.5}px` }}
              title={`${b.d}: ${b.h * 18} consultas`}
            />
            <span className="text-[10px] font-bold text-mist-500">{b.d}</span>
          </div>
        ))}
      </div>
      <div className="mt-5 grid grid-cols-1 gap-4 border-t border-mist-200 pt-4 sm:grid-cols-2">
        <Donut value={98} label="Satisfacción" color="#10b981" />
        <Donut value={87} label="Resueltas 1er contacto" color="#3569a5"/>
      </div>
      {/* línea de tendencia */}
      <svg viewBox="0 0 300 60" className="mt-4 h-14 w-full" aria-hidden="true">
        <defs>
          <linearGradient id="ln-fill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#10b981" stopOpacity=".35" />
            <stop offset="1" stopColor="#10b981" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d="M0 48 30 40 60 43 90 30 120 33 150 22 180 26 210 14 240 18 270 8 300 10V60H0Z" fill="url(#ln-fill)" />
        <path d="M0 48 30 40 60 43 90 30 120 33 150 22 180 26 210 14 240 18 270 8 300 10" fill="none" stroke="#047857" strokeWidth="2.5" strokeLinecap="round" />
      </svg>
    </div>
  );
}
