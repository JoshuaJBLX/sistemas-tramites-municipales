'use client';
import { useEffect, useState } from 'react';
import TramiteCard from '../../components/TramiteCard';
import { SearchIcon } from '../../components/icons';
import { obtenerTramites, Tramite } from '../../lib/api';

export default function TramitesPage() {
  const [todos, setTodos] = useState<Tramite[]>([]);
  const [q, setQ] = useState('');
  const [cat, setCat] = useState('Todas');

  useEffect(() => { obtenerTramites().then(setTodos); }, []);
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
      {list.length === 0 && <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{[0, 1, 2].map((i) => <div key={i} className="skeleton h-48" />)}</div>}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((t, i) => (
          <TramiteCard key={t.id} tramite={t} index={i} />
        ))}
      </div>
    </section>
  );
}
