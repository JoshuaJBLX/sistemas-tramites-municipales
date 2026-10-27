import Link from 'next/link';
import RobotAgent from '../components/RobotAgent';
import TramiteCard from '../components/TramiteCard';
import { ShieldIcon } from '../components/icons';
import GroundednessBadge from '../components/GroundednessBadge';
import { obtenerTramites, obtenerTramitesDestacados, type Tramite } from '../lib/api';

export const dynamic = 'force-dynamic';

export default async function HomePage() {
  // Vitrina dinámica: los trámites más consultados (o aleatorios si aún no hay
  // consultas). Al ser `force-dynamic`, cada visita recalcula la selección.
  const destacados = await obtenerTramitesDestacados(4).catch(() => null);
  const tramites = destacados?.tramites ?? (await obtenerTramites().catch(() => [] as Tramite[]));
  const consultasDestacados = tramites.reduce(
    (total, t) => total + ('consultas' in t ? (t as { consultas?: number }).consultas ?? 0 : 0),
    0,
  );
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
              <p className="eyebrow">MUN AI · Municipalidad Provincial de Huancayo</p>
              <h1 className="h-display mt-2">Tus trámites,<br />
                <span className="text-gradient-warm">guiados por MUN AI</span>
              </h1>
              <p className="mt-3 max-w-md text-sm leading-relaxed text-mist-500">
                Sistema basado en SLM para la orientación de trámites municipales, con
                respuestas fundamentadas en ordenanzas y TUPA vigente.
              </p>
              <div className="mt-5 flex flex-wrap gap-3">
                <Link href="/chat" className="btn-primary-3d">Hablar con MUN AI →</Link>
                <Link href="/tramites" className="btn-neu">Ver catálogo</Link>
              </div>
              <div className="mt-6 grid grid-cols-2 gap-3">
                <div className="card-3d px-3 py-3 text-center"><p className="text-lg font-extrabold text-ink">{tramites.length}</p><p className="text-[10px] font-bold uppercase tracking-widest text-mist-500">Trámites en catálogo</p></div>
                <div className="card-3d px-3 py-3 text-center"><p className="text-lg font-extrabold text-ink">{consultasDestacados > 0 ? consultasDestacados : 'Nuevo'}</p><p className="text-[10px] font-bold uppercase tracking-widest text-mist-500">Consultas a estos trámites</p></div>
              </div>
            </div>
            <div className="flex items-center justify-center"><RobotAgent /></div>
          </div>
        </div>
        <div className="flex justify-center animate-rise-in">
          <div className="w-[300px] rounded-[3rem] border-[5px] border-white bg-gradient-to-b from-white to-mist-100 p-2 shadow-soft-lg">
            <div className="overflow-hidden rounded-[2.4rem] bg-mist-100 shadow-inner">
              <div className="bg-gradient-to-b from-primary-800 to-primary-600 px-4 pb-3 pt-4 text-white">
                <div className="mx-auto mb-2 h-5 w-24 rounded-full bg-primary-950/80" />
                <div className="flex items-center gap-2">
                  <span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/20"><ShieldIcon className="h-6 w-6" /></span>
                  <div><p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/70">Municipalidad Provincial de Huancayo</p><p className="text-sm font-extrabold">MUN AI · En línea</p></div>
                </div>
              </div>
              <div className="flex h-[340px] flex-col gap-2 overflow-hidden p-3">
                <div className="bubble-user !text-xs">¿Cuánto cuesta la licencia?</div>
                <div className="bubble-bot !text-xs"><p>Plazo 5–15 días hábiles según giro · arancel en TUPA 2023.</p><GroundednessBadge score={0.94} fuentes={[{ titulo: 'TUPA 2023 · Licencias' }]} compact /></div>
                <div className="bubble-user !text-xs">¿Horario de mesa de partes?</div>
                <div className="bubble-bot !text-xs"><p>Lun–Vie 8:00–17:30.</p><GroundednessBadge score={0.91} fuentes={[{ titulo: 'Directorio oficial' }]} compact /></div>
              </div>
              <div className="border-t border-white/60 bg-white/80 p-2.5">
                <div className="flex items-center gap-2 rounded-full bg-white px-3 py-2 shadow-inner"><span className="flex-1 text-xs text-mist-500">Pregunta a MUN AI…</span><Link href="/chat" className="flex h-8 w-8 items-center justify-center rounded-full bg-emerald text-sm text-white" aria-label="Abrir chat">➤</Link></div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="mt-10">
        <div className="flex flex-wrap items-end justify-between gap-2">
          <div>
            <p className="eyebrow">
              {destacados?.criterio === 'mas_solicitados'
                ? 'Los más consultados por la ciudadanía'
                : 'Selección rotativa del catálogo'}
            </p>
            <h2 className="text-2xl font-extrabold text-ink">Catálogo destacado</h2>
          </div>
          <Link href="/tramites" className="btn-neu !py-2 text-sm">Ver todo →</Link>
        </div>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {tramites.slice(0, 4).map((t, i) => (
            <TramiteCard key={t.id} tramite={t} index={i} />
          ))}
        </div>
        {tramites.length === 0 && (
          <p className="mt-3 text-xs text-mist-500">El catálogo no está disponible en este momento.</p>
        )}
      </section>
    </div>
  );
}
