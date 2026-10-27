'use client';
import { useEffect, useState, useRef, useCallback } from 'react';
import { UploadIcon, CheckIcon, FileIcon, AlertIcon } from './icons';
import {
  listarDocumentosAdmin,
  listarTramitesAdmin,
  subirDocumento,
  reprocesarDocumento,
  cambiarEstadoDocumento,
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
  const [subiendo, setSubiendo] = useState(false);
  const dropzoneRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [form, setForm] = useState({
    tramite_id: '',
    titulo: '',
    url_origen: '',
    version: '1.0',
    fecha_publicacion: '',
    estado: 'vigente',
    archivo: null as File | null,
  });

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const [t, d] = await Promise.all([
        listarTramitesAdmin(),
        listarDocumentosAdmin({ incluir_eliminados: true, limite: 100 }),
      ]);
      setTramites(t.map((x) => ({ id: x.id, nombre: x.nombre })));
      setDocs(d);
    } catch (e: any) {
      setMsg(e.message || 'Error al cargar');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const handleFileSelect = (file: File | null) => {
    setForm((prev) => ({ ...prev, archivo: file }));
    if (file) {
      setMsg(null);
    }
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dropzoneRef.current?.classList.add('border-emerald', 'bg-emerald-soft/60', 'shadow-glow-emerald');
  };

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dropzoneRef.current?.classList.remove('border-emerald', 'bg-emerald-soft/60', 'shadow-glow-emerald');
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dropzoneRef.current?.classList.remove('border-emerald', 'bg-emerald-soft/60', 'shadow-glow-emerald');
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
  };

  const openFileDialog = () => fileInputRef.current?.click();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.archivo) return setMsg('Selecciona un archivo');
    if (!form.tramite_id) return setMsg('Selecciona un trámite');
    if (!form.titulo.trim()) return setMsg('Ingresa un título');
    if (!form.url_origen.trim()) return setMsg('Ingresa la URL de origen');

    const fd = new FormData();
    fd.append('tramite_id', form.tramite_id);
    fd.append('titulo', form.titulo);
    fd.append('url_origen', form.url_origen);
    fd.append('version', form.version);
    if (form.fecha_publicacion) fd.append('fecha_publicacion', form.fecha_publicacion);
    fd.append('estado', form.estado);
    fd.append('archivo', form.archivo);

    setSubiendo(true);
    setMsg(null);
    try {
      await subirDocumento(fd);
      setMsg('Documento cargado e indexado correctamente');
      setForm((prev) => ({ ...prev, archivo: null, titulo: '', url_origen: '' }));
      await cargar();
    } catch (e: any) {
      setMsg(e.message || 'Error al subir');
    } finally {
      setSubiendo(false);
    }
  };

  const formatoArchivo = (file: File) => {
    const kb = (file.size / 1024).toFixed(1);
    return `${file.name} (${kb} KB, ${file.type || 'tipo desconocido'})`;
  };

  return (
    <div className="card-3d p-5">
      <h3 className="font-bold text-ink">Gestión Documental</h3>
      <p className="mt-1 text-xs text-mist-500">Carga conectada · validación · extracción · chunking · indexado</p>

      <form onSubmit={onSubmit} className="mt-4 grid gap-2 sm:grid-cols-2">
        <select
          className="rounded-xl border px-3 py-2 text-sm"
          value={form.tramite_id}
          onChange={(e) => setForm({ ...form, tramite_id: e.target.value })}
          required
        >
          <option value="">Seleccionar trámite</option>
          {tramites.map((t) => (
            <option key={t.id} value={t.id}>
              {t.nombre}
            </option>
          ))}
        </select>
        <input
          className="rounded-xl border px-3 py-2 text-sm"
          placeholder="Título del documento"
          value={form.titulo}
          onChange={(e) => setForm({ ...form, titulo: e.target.value })}
          required
        />
        <input
          className="rounded-xl border px-3 py-2 text-sm sm:col-span-2"
          placeholder="URL origen (fuente oficial)"
          value={form.url_origen}
          onChange={(e) => setForm({ ...form, url_origen: e.target.value })}
          required
        />
        <input
          className="rounded-xl border px-3 py-2 text-sm"
          placeholder="Versión (ej. 1.0)"
          value={form.version}
          onChange={(e) => setForm({ ...form, version: e.target.value })}
        />
        <input
          type="date"
          className="rounded-xl border px-3 py-2 text-sm"
          value={form.fecha_publicacion}
          onChange={(e) => setForm({ ...form, fecha_publicacion: e.target.value })}
        />
        <select
          className="rounded-xl border px-3 py-2 text-sm"
          value={form.estado}
          onChange={(e) => setForm({ ...form, estado: e.target.value })}
        >
          <option value="vigente">Vigente</option>
          <option value="en_revision">En revisión</option>
          <option value="obsoleto">Obsoleto</option>
          <option value="derogado">Derogado</option>
        </select>

        {/* Dropzone + file input */}
        <div className="sm:col-span-2">
          <div
            ref={dropzoneRef}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={openFileDialog}
            className={`relative flex flex-col items-center justify-center gap-2 rounded-3xl border-2 border-dashed px-6 py-8 text-center cursor-pointer transition-all duration-300 ${
              form.archivo
                ? 'border-emerald bg-emerald-soft/60'
                : 'border-primary-200 bg-white/60 hover:border-primary-400 hover:shadow-glow-blue'
            }`}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && openFileDialog()}
            aria-label="Área de carga de archivos"
          >
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".pdf,.docx,.txt,.md"
              onChange={(e) => handleFileSelect(e.target.files?.[0] || null)}
              disabled={subiendo}
            />
            <span
              className={`flex h-12 w-12 items-center justify-center rounded-2xl text-white shadow-lift transition ${
                form.archivo
                  ? 'bg-gradient-to-b from-emerald to-emerald-deep'
                  : 'bg-gradient-to-b from-primary-500 to-primary-800'
              }`}
            >
              <UploadIcon className="h-6 w-6" />
            </span>
            <p className="text-sm font-bold text-primary-800">
              {form.archivo ? 'Archivo listo para indexar' : 'Arrastra y suelta tu archivo aquí'}
            </p>
            <p className="text-xs text-mist-500">o haz clic para seleccionar · PDF, DOCX, TXT, MD</p>
            {form.archivo && (
              <div className="w-full max-w-md mt-2 rounded-xl bg-white/80 p-3 text-left text-xs border border-emerald-200">
                <div className="flex items-center gap-2 text-emerald-deep">
                  <CheckIcon className="h-4 w-4 shrink-0" />
                  <span className="font-semibold truncate">{formatoArchivo(form.archivo)}</span>
                </div>
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    handleFileSelect(null);
                  }}
                  className="mt-1 text-xs text-primary-600 hover:underline"
                >
                  Cambiar archivo
                </button>
              </div>
            )}
          </div>
        </div>
        <button
          className="btn-neu text-sm sm:col-span-2"
          disabled={subiendo || !form.archivo}
        >
          {subiendo ? 'Indexando…' : 'Cargar y indexar'}
        </button>
      </form>

      {msg && (
        <p className={`mt-2 text-xs ${msg.startsWith('Error') ? 'text-red-600' : 'text-emerald-700'}`}>
          {msg}
        </p>
      )}

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
            {docs.map((d) => (
              <tr key={d.id} className="border-t">
                <td className="py-2 max-w-[280px] truncate">{d.titulo}</td>
                <td className="py-2">
                  <span
                    className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      d.estado === 'vigente'
                        ? 'bg-emerald-100 text-emerald-800'
                        : d.estado === 'en_revision'
                        ? 'bg-amber-100 text-amber-800'
                        : d.estado === 'obsoleto'
                        ? 'bg-mist-100 text-mist-800'
                        : 'bg-red-100 text-red-800'
                    }`}
                  >
                    {d.estado}
                  </span>
                </td>
                <td className="py-2">{d.version || '-'}</td>
                <td className="py-2">{d.fecha_publicacion || '-'}</td>
                <td className="py-2">
                  {d.indexado ? (
                    <span className="inline-flex items-center gap-1 text-emerald-700">
                      <CheckIcon className="h-3 w-3" /> Sí
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-amber-700">
                      <AlertIcon className="h-3 w-3" /> No
                    </span>
                  )}
                </td>
                <td className="py-2">
                  {d.fragmentado ? (
                    <span className="inline-flex items-center gap-1 text-emerald-700">
                      <CheckIcon className="h-3 w-3" /> Sí
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-amber-700">
                      <AlertIcon className="h-3 w-3" /> No
                    </span>
                  )}
                </td>
                <td className="py-2 flex flex-wrap gap-1">
                  {d.estado !== 'vigente' && (
                    <button
                      className="rounded-lg border border-emerald-400 bg-emerald-50 px-2 py-1 font-semibold text-emerald-700"
                      title="Marcar el documento como vigente (aprobación de calidad)"
                      onClick={async () => {
                        try {
                          await cambiarEstadoDocumento(d.id, 'vigente');
                          setMsg(`«${d.titulo}» aprobado y marcado como vigente`);
                          await cargar();
                        } catch (e: any) {
                          setMsg(e.message);
                        }
                      }}
                    >
                      Aprobar
                    </button>
                  )}
                  <button
                    className="rounded-lg border px-2 py-1"
                    title="Reprocesar (extraer, fragmentar, indexar)"
                    onClick={async () => {
                      try {
                        await reprocesarDocumento(d.id);
                        await cargar();
                      } catch (e: any) {
                        setMsg(e.message);
                      }
                    }}
                  >
                    Reprocesar
                  </button>
                  <button
                    className="rounded-lg border px-2 py-1"
                    title="Baja lógica (marcar como eliminado, se conserva para auditoría)"
                    onClick={async () => {
                      if (confirm('¿Dar de baja lógicamente? El documento se conserva para auditoría.')) {
                        try {
                          await eliminarDocumentoLogico(d.id);
                          await cargar();
                        } catch (e: any) {
                          setMsg(e.message);
                        }
                      }
                    }}
                  >
                    Dar de baja
                  </button>
                  <button
                    className="rounded-lg border px-2 py-1 text-red-600"
                    title="Eliminar FÍSICAMENTE (no se deshace)"
                    onClick={async () => {
                      if (confirm('¿Eliminar FÍSICAMENTE? Esta acción no se deshace.')) {
                        try {
                          await eliminarDocumentoFisico(d.id);
                          await cargar();
                        } catch (e: any) {
                          setMsg(e.message);
                        }
                      }
                    }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {docs.length === 0 && (
          <p className="mt-4 text-center text-sm text-mist-500">No hay documentos cargados aún.</p>
        )}
      </div>
    </div>
  );
}