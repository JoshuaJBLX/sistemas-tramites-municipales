import MetricasPanel from '../../components/MetricasPanel';
import ServiceStatus from '../../components/ServiceStatus';
import AuditLog from '../../components/AuditLog';
import DocumentManager from '../../components/DocumentManager';
import AdminGate from '../../components/AdminGate';
import QuickAccessCard from '../../components/QuickAccessCard';
import { ChartIcon, DocIcon, ClockIcon, ShieldIcon } from '../../components/icons';

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
          <QuickAccessCard href="#documentos" title="Carga de documentos" subtitle="Subir y indexar normas oficiales" icon={<DocIcon />} accent="from-primary-500 to-primary-800" />
          <QuickAccessCard href="#metricas" title="Métricas" subtitle="KPIs, satisfacción y reportes" icon={<ChartIcon />} accent="from-amber to-amber-deep" />
          <QuickAccessCard href="#auditoria" title="Auditoría" subtitle="Registro de consultas en vivo" icon={<ClockIcon />} accent="from-emerald to-emerald-deep" />
          <QuickAccessCard href="#estado" title="Estado del servicio" subtitle="API, base de datos e IA" icon={<ShieldIcon />} accent="from-primary-700 to-primary-950" />
        </div>
        {/* HU-16/HU-18: indicadores y reportes reales de la API (HU-13: solo admin). */}
        <div className="mt-5" id="metricas">
          <MetricasPanel />
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-2">
          <div id="estado"><ServiceStatus /></div>
          <div id="auditoria"><AuditLog /></div>
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-1">
          <div id="documentos"><DocumentManager /></div>
        </div>
      </section>
    </AdminGate>
  );
}
