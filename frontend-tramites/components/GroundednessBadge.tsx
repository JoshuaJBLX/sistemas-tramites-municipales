import { CheckIcon, LinkIcon } from './icons';
import type { FuenteCitada } from '../lib/api';

export function nivelColor(score?: number) {
  if (score === undefined) return 'badge-blue';
  if (score >= 0.9) return 'badge-emerald';
  if (score >= 0.75) return 'badge-amber';
  return 'badge-blue';
}

export default function GroundednessBadge({
  score, fuentes, compact = false,
}: { score?: number; fuentes?: (FuenteCitada | string)[]; compact?: boolean }) {
  const pct = score !== undefined ? Math.round(score * 100) : undefined;
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
    </div>
  );
}
