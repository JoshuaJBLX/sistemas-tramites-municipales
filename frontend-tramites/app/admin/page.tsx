import MetricasPanel from '../../components/MetricasPanel';
import ServiceStatus from '../../components/ServiceStatus';
import AuditLog from '../../components/AuditLog';
import DocumentManager from '../../components/DocumentManager';
import AdminGate from '../../components/AdminGate';

export const dynamic = 'force-dynamic';

export default function AdminPage() {
  return (
    <AdminGate>
      <section className="mx-auto max-w-7xl px-3 pb-16 pt-6 sm:px-6">
        <p className="eyebrow">Panel administrativo</p>
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">Dashboard de métricas</h1>
          <div className="flex gap-2">
            <span className="badge-emerald">● En vivo</span>
            <span className="badge-blue">Huancayo · todas las sedes</span>
          </div>
        </div>
        {/* HU-16/HU-18: indicadores y reportes reales de la API (HU-13: solo admin). */}
        <div className="mt-5">
          <MetricasPanel />
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <ServiceStatus />
          <AuditLog />
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-1">
          <DocumentManager />
        </div>
      </section>
    </AdminGate>
  );
}
