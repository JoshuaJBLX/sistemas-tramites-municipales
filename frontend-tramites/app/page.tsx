import Link from 'next/link';
import RobotAgent from '../components/RobotAgent';
import QuickAccessCard from '../components/QuickAccessCard';
import ChatBox from '../components/ChatBox';
import TramiteCard from '../components/TramiteCard';
import KpiCard from '../components/KpiCard';
import MiniCharts from '../components/MiniCharts';
import ServiceStatus from '../components/ServiceStatus';
import AuditLog from '../components/AuditLog';
import DragDropUpload from '../components/DragDropUpload';
import { TramiteIcon, OrdenanzaIcon, DirectorioIcon, AyudaIcon, ShieldIcon } from '../components/icons';
import { UsersIcon, HeartIcon, ChartIcon } from '../components/icons';
import GroundednessBadge from '../components/GroundednessBadge';
import { obtenerTramites } from '../lib/api';

export const dynamic = 'force-dynamic';

export default async function HomePage() {
  const tramites = await obtenerTramites();
  return (
    <div className="mx-auto max-w-7xl px-3 pb-20 pt-6 sm:px-6">
      <section className="grid items-start gap-6 xl:grid-cols-[1fr_340px]">
        <div className="glass-strong relative overflow-hidden rounded-[2rem] p-6 sm:p-8 animate-rise-in">
          <div className="pointer-events-none absolute -right-20 -top-24 h-64 w-64 rounded-full bg-amber-soft/50 blur-3xl" aria-hidden="true" />
          <div className="pointer-events-none absolute -bottom-24 -left-20 h-64 w-64 rounded-full bg-emerald-soft/50 blur-3xl" aria-hidden="true" />
          <div className="relative flex flex-wrap items-center gap-2">
            <span className="badge-emerald">● Sistema en línea</span>
            <span className="badge-blue">RAG + SLM · BGE-M3 · pgvector</span>
          </div>
          <div className="relative mt-4 grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
            <div>
              <p className="eyebrow">Ecosistema digital · Municipalidad Provincial de Junín</p>
              <h1 className="h-display mt-2">Tus trámites,<br />
                <span className="text-gradient-warm">guiados por Muni</span>
              </h1>
              <p className="mt-3 max-w-md text-sm leading-relaxed text-mist-500">
                Asistente virtual con respuestas fundamentadas en ordenanzas y TUPA vigente.
              </p>
              <div className="mt-5 flex flex-wrap gap-3">
                <Link href="/chat" className="btn-primary-3d">Hablar con Muni →</Link>
                <Link href="/tramites" className="btn-neu">Ver catálogo</Link>
              </div>
              <div className="mt-6 grid grid-cols-3 gap-3">
                <div className="card-3d px-3 py-3 text-center"><p className="text-lg font-extrabold text-ink">252</p><p className="text-[10px] font-bold uppercase tracking-widest text-mist-500">Procedimientos TUPA</p></div>
                <div className="card-3d px-3 py-3 text-center"><p className="text-lg font-extrabold text-ink">1,236</p><p className="text-[10px] font-bold uppercase tracking-widest text-mist-500">Consultas</p></div>
                <div className="card-3d px-3 py-3 text-center"><p className="text-lg font-extrabold text-ink">98%</p><p className="text-[10px] font-bold uppercase tracking-widest text-mist-500">Satisfacción</p></div>
              </div>
            </div>
            <div className="flex items-center justify-center"><RobotAgent /></div>
          </div>
          <div className="relative mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <QuickAccessCard href="/tramites" title="Trámites" subtitle="Catálogo, costos y plazos" icon={<TramiteIcon />} accent="from-primary-500 to-primary-800" />
            <QuickAccessCard href="/tramites" title="Ordenanzas" subtitle="Normas vigentes" icon={<OrdenanzaIcon />} accent="from-amber to-amber-deep" />
            <QuickAccessCard href="/admin" title="Directorio" subtitle="Oficinas y contacto" icon={<DirectorioIcon />} accent="from-emerald to-emerald-deep" />
            <QuickAccessCard href="/chat" title="Ayuda" subtitle="Pregunta a Muni" icon={<AyudaIcon />} accent="from-primary-700 to-primary-950" />
          </div>
        </div>
        <div className="flex justify-center animate-rise-in">
          <div className="w-[300px] rounded-[3rem] border-[5px] border-white bg-gradient-to-b from-white to-mist-100 p-2 shadow-soft-lg">
            <div className="overflow-hidden rounded-[2.4rem] bg-mist-100 shadow-inner">
              <div className="bg-gradient-to-b from-primary-800 to-primary-600 px-4 pb-3 pt-4 text-white">
                <div className="mx-auto mb-2 h-5 w-24 rounded-full bg-primary-950/80" />
                <div className="flex items-center gap-2">
                  <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20"><ShieldIcon className="h-6 w-6" /></span>
                  <div><p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/70">Municipalidad Provincial de Junín</p><p className="text-sm font-extrabold">Muni · En línea 🟢</p></div>
                </div>
              </div>
              <div className="flex h-[340px] flex-col gap-2 overflow-hidden p-3">
                <div className="bubble-user !text-xs">¿Cuánto cuesta la licencia?</div>
                <div className="bubble-bot !text-xs"><p>Plazo 5–15 días hábiles según giro · arancel en TUPA 2023.</p><GroundednessBadge score={0.94} fuentes={[{ titulo: 'TUPA 2023 · Licencias' }]} compact /></div>
                <div className="bubble-user !text-xs">¿Horario de mesa de partes?</div>
                <div className="bubble-bot !text-xs"><p>Lun–Vie 8:00–17:30.</p><GroundednessBadge score={0.91} fuentes={[{ titulo: 'Directorio oficial' }]} compact /></div>
              </div>
              <div className="border-t border-white/60 bg-white/80 p-2.5">
                <div className="flex items-center gap-2 rounded-full bg-white px-3 py-2 shadow-inner"><span className="flex-1 text-xs text-mist-500">Pregunta a Muni…</span><Link href="/chat" className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald text-sm text-white" aria-label="Abrir chat">➤</Link></div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="mt-10">
        <div className="flex items-end justify-between">
          <div><p className="eyebrow">Panel de administración</p><h2 className="text-2xl font-extrabold text-ink">Métricas y operación en vivo</h2></div>
          <Link href="/admin" className="btn-neu !py-2 text-sm">Abrir panel →</Link>
        </div>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <KpiCard icon={<TramiteIcon className="h-6 w-6" />} label="Procedimientos TUPA" value="252" delta="TUPA 2023 vigente" tone="blue" />
          <KpiCard icon={<UsersIcon className="h-6 w-6" />} label="Consultas" value="1,236" delta="▲ +12% esta semana" tone="emerald" />
          <KpiCard icon={<HeartIcon className="h-6 w-6" />} label="Satisfacción" value="98%" delta="▲ +0.6 pts" tone="amber" />
        </div>
        <div className="mt-4 grid gap-4 lg:grid-cols-3">
          <MiniCharts />
          <ServiceStatus />
          <AuditLog />
        </div>
      </section>
      <section className="mt-10 grid gap-4 lg:grid-cols-2">
        <div>
          <div className="flex items-end justify-between"><h2 className="text-2xl font-extrabold text-ink">Catálogo destacado</h2><Link href="/tramites" className="btn-neu !py-2 text-sm">Ver todo →</Link></div>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            {tramites.slice(0, 4).map((t, i) => (
              <TramiteCard key={t.id} tramite={t} index={i} />
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-4">
          <div className="glass-strong rounded-[2rem] p-5">
            <h2 className="flex items-center gap-2 font-extrabold text-ink"><ChartIcon className="h-5 w-5 text-primary-600" /> Prueba el chat aquí mismo</h2>
            <div className="mt-3"><ChatBox compact /></div>
          </div>
          <DragDropUpload />
        </div>
      </section>
    </div>
  );
}

