'use client';
import { CheckIcon, LinkIcon } from './icons';
import type { TramiteProbable } from '../lib/api';

/**
 * Muestra los datos del trámite que el backend identificó en la base de datos.
 * Requisitos, arancel y plazo provienen del catálogo, no del redactado del modelo.
 */
export default function TramiteProbableCard({ tramite }: { tramite: TramiteProbable }) {
  return (
    <div className="mt-3 rounded-2xl border border-emerald-100 bg-emerald-50/70 p-3">
      <p className="mb-2 flex items-center gap-1.5 text-xs font-extrabold uppercase tracking-wide text-emerald-800">
        <CheckIcon className="h-3.5 w-3.5" />
        Trámite identificado
      </p>
      <p className="text-sm font-bold text-primary-800">{tramite.nombre}</p>

      {tramite.requisitos.length > 0 && (
        <ul className="mt-2 list-inside list-disc space-y-1 text-xs text-primary-700">
          {tramite.requisitos.map((requisito, indice) => (
            <li key={indice}>{requisito}</li>
          ))}
        </ul>
      )}

      <div className="mt-2 flex flex-wrap gap-2 text-xs font-semibold text-primary-700">
        {tramite.costo > 0 && <span className="badge-blue">Arancel S/ {tramite.costo.toFixed(2)}</span>}
        {tramite.duracion_estimada_dias > 0 && (
          <span className="badge-blue">{tramite.duracion_estimada_dias} días hábiles</span>
        )}
      </div>

      {tramite.fuente_url && (
        <a
          href={tramite.fuente_url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-2 inline-flex items-center gap-1.5 text-xs font-bold text-primary-700 underline underline-offset-2 hover:text-primary-900"
        >
          <LinkIcon className="h-3.5 w-3.5" />
          Ver ficha oficial
        </a>
      )}
    </div>
  );
}