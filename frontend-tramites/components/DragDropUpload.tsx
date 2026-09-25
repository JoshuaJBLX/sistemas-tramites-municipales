'use client';
import { useState } from 'react';
import { UploadIcon, CheckIcon } from './icons';

export default function DragDropUpload() {
  const [drag, setDrag] = useState(false);
  const [files, setFiles] = useState<string[]>([]);
  return (
    <div className="card-3d p-5">
      <h3 className="font-bold text-ink">Carga de documentos oficiales</h3>
      <p className="mt-1 text-xs text-mist-500">PDF, DOCX · se vectorizan con BGE-M3 y se auditan</p>
      <div
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); setFiles((p) => [...p, ...Array.from(e.dataTransfer.files).map((f) => f.name)]); }}
        className={`mt-4 flex flex-col items-center justify-center gap-2 rounded-3xl border-2 border-dashed px-6 py-8 text-center transition-all duration-300 ${drag ? 'border-emerald bg-emerald-soft/60 shadow-glow-emerald scale-[1.01]' : 'border-primary-200 bg-white/60 hover:border-primary-400 hover:shadow-glow-blue'}`}
      >
        <span className={`flex h-12 w-12 items-center justify-center rounded-2xl text-white shadow-lift transition ${drag ? 'bg-gradient-to-b from-emerald to-emerald-deep' : 'bg-gradient-to-b from-primary-500 to-primary-800'}`}>
          <UploadIcon className="h-6 w-6" />
        </span>
        <p className="text-sm font-bold text-primary-800">{drag ? 'Suelta para indexar' : 'Arrastra y suelta tus archivos'}</p>
        <p className="text-xs text-mist-500">o</p>
        <label className="btn-neu cursor-pointer !px-4 !py-2 text-sm">
          Seleccionar archivos
          <input type="file" multiple className="hidden" onChange={(e) => setFiles((p) => [...p, ...Array.from(e.target.files ?? []).map((f) => f.name)])} />
        </label>
      </div>
      {files.length > 0 && (
        <ul className="mt-3 space-y-2">
          {files.map((f, i) => (
            <li key={i} className="flex items-center gap-2 rounded-2xl bg-emerald-soft/70 px-3 py-2 text-xs font-semibold text-emerald-deep">
              <CheckIcon className="h-4 w-4" /> {f} · listo para indexar
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
