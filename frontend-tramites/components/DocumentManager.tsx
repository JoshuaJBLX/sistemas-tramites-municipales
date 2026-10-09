'use client';
import { useEffect, useState } from 'react';
import {
  listarDocumentosAdmin,
  listarTramitesAdmin,
  subirDocumento,
  reprocesarDocumento,
  eliminarDocumentoLogico,
  eliminarDocumentoFisico,
  type DocumentoAdmin,
} from '@/lib/api';

type TramiteLite = { id: string; nombre: string };

export default function DocumentManager() {
  const [tramites, setTramites] = useState<TramiteLite[]>([]);
  const [docs, setDocs] = useState<DocumentoAdmin[]>([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  const [form, setForm] = useState({
    tramite_id: '',
    titulo: '',
    url_origen: '',
    version: '1.0',
    fecha_publicacion: '',
    estado: 'vigente',
    archivo: null as File | null,
  });

  const cargar = async () => {
    setLoading(true);
    try {
      const [t, d] = await Promise.all([
        listarTramitesAdmin(),
        listarDocumentosAdmin({ incluir_eliminados: true, limite: 100 }),
      ]);
      setTramites(t.map(x => ({ id: x.id, nombre: x.nombre })));
      setDocs(d);
    } catch (e: any) {
      setMsg(e.message || 'Error al cargar');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { cargar(); }, []);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.archivo) return setMsg('Selecciona un archivo');
    const fd = new FormData();
    fd.append('tramite_id', form.tramite_id);
    fd.append('titulo', form.titulo);
    fd.append('url_origen', form.url_origen);
    fd.append('version', form.version);
    if (form.fecha_publicacion) fd.append('fecha_publicacion', form.fecha_publicacion);
    fd.append('estado', form.estado);
    fd.append('archivo', form.archivo);
    setMsg(null);
    try {
      await subirDocumento(fd);
      setMsg('Documento cargado e indexado correctamente');
      await cargar();
    } catch (e: any) {
      setMsg(e.message || 'Error al subir');
    }
  };

  return (
    <div className="card-3d p-5">
      <h3 className="font-bold text-ink">Gestión documental (HU-01–HU-04)</h3>
      <p className="mt-1 text-xs text-mist-500">Carga conectada · validación · extracción · chunking · indexado</p>

      <form onSubmit={onSubmit} className="mt-4 grid gap-2 sm:grid-cols-2">
        <select
          className="rounded-xl border px-3 py-2 text-sm"
          value={form.tramite_id}
          onChange={e => setForm({ ...form, tramite_id: e.target.value })}
          required
        >
          <option value="">Seleccionar trámite</option>
          {tramites.map(t => <option key={t.id} value={t.id}>{t.nombre}</option>)}
        </select>
        <input className="rounded-xl border px-3 py-2 text-sm" placeholder="Título" value={form.titulo} onChange={e => setForm({ ...form, titulo: e.target.value })} required />
        <input className="rounded-xl border px-3 py-2 text-sm" placeholder="URL origen (fuente oficial)" value={form.url_origen} onChange={e => setForm({ ...form, url_origen: e.target.value })} required />
        <input className="rounded-xl border px-3 py-2 text-sm" placeholder="Versión (ej. 1.0)" value={form.version} onChange={e => setForm({ ...form, version: e.target.value })} />
        <input type="date" className="rounded-xl border px-3 py-2 text-sm" value={form.fecha_publicacion} onChange={e => setForm({ ...form, fecha_publicacion: e.target.value })} />
        <select className="rounded-xl border px-3 py-2 text-sm" value={form.estado} onChange={e => setForm({ ...form, estado: e.target.value })}>
          <option value="vigente">Vigente</option>
          <option value="en_revision">En revisión</option>
          <option value="obsoleto">Obsoleto</option>
          <option value="derogado">Derogado</option>
        </select>
        <input type="file" className="rounded-xl border px-3 py-2 text-sm" accept=".pdf,.docx,.txt,.md" onChange={e => setForm({ ...form, archivo: e.target.files?.[0] || null })} required />
        <button className="btn-neu text-sm sm:col-span-2">Cargar y indexar</button>
      </form>

      {msg && <p className="mt-2 text-xs text-amber-700">{msg}</p>}

      <div className="mt-4 overflow-x-auto">
        <table className="min-w-full text-xs">
          <thead>
            <tr className="text-left text-mist-500">
              <th className="py-2">Título</th>
              <th className="py-2">Estado</th>
              <th className="py-2">Versión</th>
              <th className="py-2">Fecha</th>
              <th className="py-2">Indexado</th>
              <th className="py-2">Fragmentado</th>
              <th className="py-2">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {docs.map(d => (
              <tr key={d.id} className="border-t">
                <td className="py-2 max-w-[280px] truncate">{d.titulo}</td>
                <td className="py-2">{d.estado}</td>
                <td className="py-2">{d.version || '-'}</td>
                <td className="py-2">{d.fecha_publicacion || '-'}</td>
                <td className="py-2">{d.indexado ? 'Sí' : 'No'}</td>
                <td className="py-2">{d.fragmentado ? 'Sí' : 'No'}</td>
                <td className="py-2 flex gap-1">
                  <button className="rounded-lg border px-2 py-1" onClick={async () => { try { await reprocesarDocumento(d.id); await cargar(); } catch (e:any) { setMsg(e.message); } }}>Reprocesar</button>
                  <button className="rounded-lg border px-2 py-1" onClick={async () => { if (confirm('¿Baja lógica?')) { await eliminarDocumentoLogico(d.id); await cargar(); } }}>Dar de baja</button>
                  <button className="rounded-lg border px-2 py-1 text-red-600" onClick={async () => { if (confirm('¿Eliminar FÍSICAMENTE? Esta acción no se deshace.')) { await eliminarDocumentoFisico(d.id); await cargar(); } }}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}