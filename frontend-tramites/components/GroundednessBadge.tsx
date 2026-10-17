import { CheckIcon, LinkIcon } from './icons';
import type { FuenteCitada } from '../lib/api';

export function nivelColor(score?: number) {
  if (score === undefined) return 'badge-blue';
  if (score >= 0.9) return 'badge-emerald';
  if (score >= 0.75) return 'badge-amber';
  return 'badge-blue';
}

function metadatosFuente(f: FuenteCitada) {
  return [f.version ? `v${f.version}` : '', f.fecha || ''].filter(Boolean).join(' · ');
}

export default function GroundednessBadge({
  score, fuentes, compact = false,
}: { score?: number; fuentes?: (FuenteCitada | string)[]; compact?: boolean }) {
  const pct = score !== undefined ? Math.round(score * 100) : undefined;
  const fuentesObj = (fuentes ?? []).filter((f): f is FuenteCitada => typeof f !== 'string');
  const titulos = (fuentes ?? []).map((f) => (typeof f === 'string' ? f : f.titulo)).filter(Boolean);
  return (
    <div className={`flex flex-wrap items-center gap-2 ${compact ? '' : 'mt-2'}`}>
      <span className={nivelColor(score)} title="Porcentaje de la respuesta respaldado por documentos oficiales">
        <CheckIcon className="h-3.5 w-3.5" />
        Groundedness{pct !== undefined ? ` ${pct}%` : ''}
      </span>
      {titulos.slice(0, 2).map((t, i) => (
        <span key={i} className="badge-blue">
          <LinkIcon className="h-3.5 w-3.5" />
          {t}
        </span>
      ))}
      {titulos.length > 2 && (
        <span className="text-xs font-semibold text-primary-500">+{titulos.length - 2} fuentes</span>
      )}
      {fuentesObj.length > 0 && (
        <details className="w-full">
          <summary className="badge-blue inline-flex cursor-pointer select-none">
            Ver fuentes con fecha y versión ({fuentesObj.length})
          </summary>
          <ul className="mt-2 space-y-2">
            {fuentesObj.map((f, i) => (
              <li
                key={i}
                className="rounded-2xl border border-white/60 bg-white/70 px-3 py-2 text-xs text-primary-900"
              >
                <p className="font-semibold">
                  {f.titulo || 'Documento oficial'}
                  {f.numero ? ` · N° ${f.numero}` : ''}
                </p>
                {metadatosFuente(f) && <p className="text-mist-500">{metadatosFuente(f)}</p>}
                {f.fragmento && <p className="mt-1 line-clamp-2 text-mist-500">{f.fragmento}</p>}
                {f.url && (
                  <a
                    href={f.url}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-1 inline-block break-all text-primary-500 hover:underline"
                  >
                    {f.url}
                  </a>
                )}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
