interface KpiProps { icon: React.ReactNode; label: string; value: string; delta: string; tone: 'blue' | 'emerald' | 'amber'; }

const tones = {
  blue: 'from-primary-600 to-primary-800',
  emerald: 'from-emerald to-emerald-deep',
  amber: 'from-[#f7b955] to-amber-deep',
};

export default function KpiCard({ icon, label, value, delta, tone }: KpiProps) {
  return (
    <div className="card-3d group relative overflow-hidden p-5">
      <div className="absolute -right-8 -top-8 h-28 w-28 rounded-full bg-amber-soft/50 blur-2xl transition group-hover:scale-125" aria-hidden="true" />
      <div className="relative flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.18em] text-mist-500">{label}</p>
          <p className="mt-1 text-3xl font-extrabold tracking-tight text-ink">{value}</p>
          <p className="mt-1 text-xs font-semibold text-emerald-deep">{delta}</p>
        </div>
        <div className={`flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-b ${tones[tone]} text-white shadow-lift`}>
          {icon}
        </div>
      </div>
    </div>
  );
}