import KpiCard from '../../components/KpiCard';
import MiniCharts from '../../components/MiniCharts';
import ServiceStatus from '../../components/ServiceStatus';
import AuditLog from '../../components/AuditLog';
import DocumentManager from '../../components/DocumentManager';
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
          <span className="badge-blue">Huancayo · todas las sedes</span>
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
      <div className="mt-4 grid gap-4 lg:grid-cols-1">
        <DocumentManager />
      </div>
    </section>
  );
}
