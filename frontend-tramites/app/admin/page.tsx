import KpiCard from '../../components/KpiCard';
import MiniCharts from '../../components/MiniCharts';
import ServiceStatus from '../../components/ServiceStatus';
import AuditLog from '../../components/AuditLog';
import DragDropUpload from '../../components/DragDropUpload';
import { TramiteIcon, UsersIcon, HeartIcon } from '../../components/icons';

export const dynamic = 'force-dynamic';

export default function AdminPage() {
  return (
    <section className="mx-auto max-w-7xl px-3 pb-16 pt-6 sm:px-6">
      <p className="eyebrow">Panel administrativo</p>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <h1 className="text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">Dashboard de métricas</h1>
        <div className="flex gap-2">
          <span className="badge-emerald">● En vivo</span>
          <span className="badge-blue">Junín · todas las sedes</span>
        </div>
      </div>
      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <KpiCard icon={<TramiteIcon className="h-6 w-6" />} label="Procedimientos TUPA" value="252" delta="TUPA 2023 vigente" tone="blue" />
        <KpiCard icon={<UsersIcon className="h-6 w-6" />} label="Consultas" value="1,236" delta="▲ +12% esta semana" tone="emerald" />
        <KpiCard icon={<HeartIcon className="h-6 w-6" />} label="Satisfacción" value="98%" delta="▲ +0.6 pts · 1.180 votos" tone="amber" />
      </div>
      <div className="mt-4 grid gap-4 lg:grid-cols-3">
        <MiniCharts />
        <ServiceStatus />
        <AuditLog />
      </div>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <DragDropUpload />
        <div className="card-3d p-5">
          <h3 className="font-bold text-ink">Gestión documental</h3>
          <p className="mt-1 text-xs text-mist-500">Versiones vigentes indexadas con BGE-M3 + pgvector</p>
          <ul className="mt-3 space-y-2 text-sm">
            {[
              ['TUPA 2023 · Registro Civil N.º 188', 'v3 · 97% groundedness', 'badge-emerald'],
              ['TUPA 2023 · Licencias N.º 9', 'v5 · 94% groundedness', 'badge-emerald'],
              ['Directorio de oficinas 2026', 'actualizando…', 'badge-amber'],
            ].map(([t, s, b]) => (
              <li key={t} className="flex items-center justify-between gap-2 rounded-2xl border border-white/60 bg-white/60 px-4 py-2.5 backdrop-blur">
                <span className="font-semibold text-primary-800">{t}</span>
                <span className={b as string}>{s}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
