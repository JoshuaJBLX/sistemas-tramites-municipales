import MetricasPanel from '../../components/MetricasPanel';
import AuditLog from '../../components/AuditLog';
import DocumentManager from '../../components/DocumentManager';
import AdminGate from '../../components/AdminGate';
import QuickAccessCard from '../../components/QuickAccessCard';
import { ChartIcon, DocIcon, ClockIcon } from '../../components/icons';

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
        {/* Accesos rápidos del administrador (diseño de tarjetas de la portada). */}
        <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <QuickAccessCard href="#documentos" title="Gestión Documental" subtitle="Subir, indexar y aprobar documentos" icon={<DocIcon />} accent="from-primary-500 to-primary-800" />
          <QuickAccessCard href="#metricas" title="Métricas" subtitle="KPIs, satisfacción y reportes" icon={<ChartIcon />} accent="from-amber to-amber-deep" />
          <QuickAccessCard href="#auditoria" title="Auditoría" subtitle="Registro de consultas con filtros" icon={<ClockIcon />} accent="from-emerald to-emerald-deep" />
        </div>
        {/* HU-16/HU-18: indicadores y reportes reales de la API (HU-13: solo admin). */}
        <div className="mt-5" id="metricas">
          <MetricasPanel />
        </div>
        <div className="mt-4" id="auditoria">
          <AuditLog />
        </div>
        <div className="mt-4" id="documentos">
          <DocumentManager />
        </div>
      </section>
    </AdminGate>
  );
}