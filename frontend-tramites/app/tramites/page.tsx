'use client';
import { useEffect, useState } from 'react';
import TramiteCard from '../../components/TramiteCard';
import { SearchIcon } from '../../components/icons';
import { obtenerTramites, obtenerTramitesRelacionados, Tramite, TramiteRelacionado } from '../../lib/api';

export default function TramitesPage() {
  const [todos, setTodos] = useState<Tramite[]>([]);
  const [q, setQ] = useState('');
  const [cat, setCat] = useState('Todas');
  const [error, setError] = useState<string | null>(null);
  const [cargando, setCargando] = useState(true);

  const [seleccion, setSeleccion] = useState<Tramite | null>(null);
  const [relacionados, setRelacionados] = useState<TramiteRelacionado[]>([]);
  const [cargandoRel, setCargandoRel] = useState(false);
  const [errorRel, setErrorRel] = useState<string | null>(null);

  useEffect(() => {
    obtenerTramites()
      .then(setTodos)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : 'No se pudo cargar el catálogo.'))
      .finally(() => setCargando(false));
  }, []);

  const seleccionar = async (tramite: Tramite) => {
    if (seleccion?.id === tramite.id) {
      setSeleccion(null);
      setRelacionados([]);
      return;
    }
    setSeleccion(tramite);
    setRelacionados([]);
    setErrorRel(null);
    setCargandoRel(true);
    try {
      setRelacionados(await obtenerTramitesRelacionados(tramite.id));
    } catch (e: unknown) {
      setErrorRel(e instanceof Error ? e.message : 'No se pudieron cargar los trámites relacionados.');
    } finally {
      setCargandoRel(false);
    }
  };

  const cats = ['Todas', ...Array.from(new Set(todos.map((t) => t.categoria).filter(Boolean) as string[]))];
  const list = todos.filter((t) =>
    (cat === 'Todas' || t.categoria === cat) &&
    (q === '' || `${t.nombre} ${t.descripcion}`.toLowerCase().includes(q.toLowerCase())),
  );

  return (
    <section className="mx-auto max-w-7xl px-3 pb-16 pt-6 sm:px-6">
      <p className="eyebrow">Catálogo oficial · TUPA vigente</p>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <h1 className="text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">Trámites y servicios</h1>
        <span className="badge-blue">{list.length} resultados</span>
      </div>
      <div className="glass mt-5 flex flex-col gap-3 rounded-3xl p-4 sm:flex-row">
        <label className="flex flex-1 items-center gap-2 rounded-2xl border border-white/70 bg-white/70 px-4 py-2.5 shadow-inner backdrop-blur-xl">
          <SearchIcon className="h-5 w-5 text-primary-400" />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Buscar por nombre o palabra clave…" className="w-full bg-transparent text-sm outline-none placeholder:text-mist-500" aria-label="Buscar trámites" />
        </label>
        <div className="flex flex-wrap gap-2">
          {cats.map((c) => (
            <button key={c} onClick={() => setCat(c)}
              className={`rounded-full px-4 py-2 text-xs font-bold transition ${cat === c ? 'bg-primary-800 text-white shadow-lift' : 'bg-white/70 text-primary-700 shadow-sm hover:-translate-y-0.5'}`}>
              {c}
            </button>
          ))}
        </div>
      </div>
      {seleccion && (
        <section className="glass mt-5 rounded-3xl p-5" aria-live="polite">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <p className="eyebrow !text-[10px]">Recomendación · HU-12</p>
              <h2 className="text-lg font-extrabold tracking-tight text-ink">
                Trámites relacionados con «{seleccion.nombre}»
              </h2>
            </div>
            <button
              type="button"
              onClick={() => { setSeleccion(null); setRelacionados([]); }}
              className="rounded-full bg-white/80 px-4 py-2 text-xs font-bold text-primary-700 shadow-sm"
            >
              Cerrar
            </button>
          </div>
          {cargandoRel && (
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[0, 1, 2].map((i) => <div key={i} className="skeleton h-40" />)}
            </div>
          )}
          {!cargandoRel && errorRel && (
            <p className="mt-3 text-sm font-semibold text-amber-800">{errorRel}</p>
          )}
          {!cargandoRel && !errorRel && relacionados.length === 0 && (
            <p className="mt-3 text-sm text-mist-500">Sin recomendaciones para este trámite.</p>
          )}
          {!cargandoRel && relacionados.length > 0 && (
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {relacionados.map((t, i) => (
                <div key={t.id} className="relative">
                  <TramiteCard tramite={t} index={i} onSeleccionar={seleccionar} />
                  <span className="absolute right-4 top-4 rounded-full bg-white/90 px-2 py-1 text-[10px] font-bold text-primary-700 shadow-sm">
                    {Math.round(t.similitud * 100)} % afín
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      )}
      {error && (
        <div className="mt-6 rounded-2xl border border-amber-300 bg-amber-50 p-4 text-sm font-semibold text-amber-800">
          No se pudo cargar el catálogo de trámites: {error}
        </div>
      )}
      {!error && cargando && <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{[0, 1, 2].map((i) => <div key={i} className="skeleton h-48" />)}</div>}
      {!error && !cargando && list.length === 0 && (
        <p className="mt-6 text-sm text-mist-500">No hay trámites que coincidan con la búsqueda.</p>
      )}
      {!error && list.length > 0 && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {list.map((t, i) => (
            <TramiteCard
              key={t.id}
              tramite={t}
              index={i}
              seleccionado={seleccion?.id === t.id}
              onSeleccionar={seleccionar}
            />
          ))}
        </div>
      )}
    </section>
  );
}
