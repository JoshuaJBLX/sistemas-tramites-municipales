'use client';

import { useCallback, useEffect, useState } from 'react';
import {
  descargarReporteCsv,
  obtenerMetricas,
  obtenerReporte,
  type Metricas,
  type Reporte,
} from '../lib/api';
import KpiCard from './KpiCard';
import MiniCharts from './MiniCharts';
import { AlertIcon, ChartIcon, ClockIcon, HeartIcon, UsersIcon } from './icons';

const fmtPct = (valor: number) => `${(valor * 100).toFixed(1)} %`;
const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString('es-PE', {
  day: '2-digit', month: 'short', year: 'numeric',
});

/**
 * HU-16 + HU-18 — panel con indicadores reales del backend (`/api/metricas`)
 * y exportación del reporte de periodo (`/api/reportes/exportar`, CSV con BOM).
 * Solo accesible con rol administrador (HU-13).
 */
export default function MetricasPanel() {
  const [metricas, setMetricas] = useState<Metricas | null>(null);
  const [reporte, setReporte] = useState<Reporte | null>(null);
  const [desde, setDesde] = useState('');
  const [hasta, setHasta] = useState('');
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exportando, setExportando] = useState(false);
  const [avisoExport, setAvisoExport] = useState<string | null>(null);

  const cargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const [m, r] = await Promise.all([obtenerMetricas(30), obtenerReporte()]);
      setMetricas(m);
      setReporte(r);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudieron cargar las métricas.');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => { void cargar(); }, [cargar]);

  const aplicarPeriodo = async () => {
    setCargando(true);
    setError(null);
    try {
      setReporte(await obtenerReporte(desde || undefined, hasta || undefined));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo generar el reporte.');
    } finally {
      setCargando(false);
    }
  };

  const exportar = async () => {
    setExportando(true);
    setAvisoExport(null);
    try {
      await descargarReporteCsv(desde || undefined, hasta || undefined);
      setAvisoExport('Reporte descargado. Ábrelo en Excel (CSV con UTF-8).');
    } catch (e) {
      setAvisoExport(e instanceof Error ? e.message : 'Falló la exportación.');
    } finally {
      setExportando(false);
    }
  };

  if (cargando && !metricas) {
    return (
      <div className="card-3d p-5 text-sm font-semibold text-mist-500">
        Cargando indicadores del sistema…
      </div>
    );
  }

  if (error && !metricas) {
    return (
      <div className="card-3d p-5">
        <p className="text-sm font-semibold text-rose-600">{error}</p>
        <button type="button" onClick={() => void cargar()} className="mt-2 btn-primary text-sm">
          Reintentar
        </button>
      </div>
    );
  }

  if (!metricas) return null;

  const satisfaccion = metricas.satisfaccion_pct;

  return (
    <div className="space-y-4">
      {metricas.alerta && metricas.alerta_mensaje && (
        <div className="flex items-start gap-3 rounded-2xl border border-amber/40 bg-amber-soft px-4 py-3">
          <AlertIcon className="mt-0.5 h-5 w-5 shrink-0 text-amber-deep" />
          <p className="text-sm font-semibold text-amber-deep">{metricas.alerta_mensaje}</p>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-3">
        <KpiCard
          icon={<UsersIcon className="h-6 w-6" />}
          label="Consultas totales"
          value={metricas.total_consultas.toLocaleString('es-PE')}
          delta={`${metricas.consultas_periodo} en los últimos ${metricas.periodo_dias} días`}
          tone="blue"
        />
        <KpiCard
          icon={<ChartIcon className="h-6 w-6" />}
          label="Respuestas fundamentadas"
          value={fmtPct(metricas.tasa_fundamentadas)}
          delta={`Groundedness medio ${fmtPct(metricas.groundedness_promedio)}`}
          tone="emerald"
        />
        <KpiCard
          icon={<HeartIcon className="h-6 w-6" />}
          label="Satisfacción ciudadana"
          value={satisfaccion === null ? '—' : `${satisfaccion.toFixed(1)} %`}
          delta={
            metricas.total_evaluaciones > 0
              ? `${metricas.total_evaluaciones} calificaciones recibidas`
              : 'Sin calificaciones todavía'
          }
          tone="amber"
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <MiniCharts
          serie={metricas.serie_diaria}
          satisfaccion={satisfaccion}
          fundamentadas={metricas.tasa_fundamentadas * 100}
        />
        <div className="card-3d p-5">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-ink">Tiempo de respuesta</h3>
            <ClockIcon className="h-5 w-5 text-primary-500" />
          </div>
          <p className="mt-3 text-3xl font-extrabold tracking-tight text-ink">
            {metricas.duracion_promedio_ms === null
              ? '—'
              : `${(metricas.duracion_promedio_ms / 1000).toFixed(1)} s`}
          </p>
          <p className="mt-1 text-xs font-semibold text-mist-500">
            promedio de generación de respuesta
          </p>
          <dl className="mt-4 space-y-2 border-t border-mist-200 pt-3 text-sm">
            <div className="flex justify-between">
              <dt className="text-mist-500">Respuestas bloqueadas</dt>
              <dd className="font-bold text-ink">{metricas.respuestas_bloqueadas}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-mist-500">Consultas fuera de dominio</dt>
              <dd className="font-bold text-ink">{metricas.consultas_fuera_dominio}</dd>
            </div>
          </dl>
        </div>
        <div className="card-3d p-5">
          <h3 className="font-bold text-ink">Trámites más consultados</h3>
          <ul className="mt-3 space-y-2">
            {metricas.tramites_frecuentes.slice(0, 5).map((t) => (
              <li key={t.nombre} className="flex items-center justify-between gap-2 text-sm">
                <span className="truncate text-ink" title={t.nombre}>{t.nombre}</span>
                <span className="shrink-0 rounded-full bg-primary-50 px-2 py-0.5 text-xs font-bold text-primary-600">
                  {t.cantidad}
                </span>
              </li>
            ))}
            {metricas.tramites_frecuentes.length === 0 && (
              <li className="text-sm text-mist-500">Sin trámites identificados en el periodo.</li>
            )}
          </ul>
        </div>
      </div>

      {/* HU-18: reporte por periodo + exportación CSV */}
      <div className="card-3d p-5">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h3 className="font-bold text-ink">Reporte de periodo</h3>
            <p className="text-xs font-semibold text-mist-500">
              {reporte ? `${fmtFecha(reporte.desde)} — ${fmtFecha(reporte.hasta)}` : 'Sin periodo'}
              {reporte ? ` · ${reporte.consultas} consultas` : ''}
            </p>
          </div>
          <div className="flex flex-wrap items-end gap-2">
            <label className="text-xs font-bold text-mist-500">
              Desde
              <input
                type="date"
                value={desde}
                onChange={(e) => setDesde(e.target.value)}
                className="mt-1 block rounded-lg border border-mist-200 bg-white px-2 py-1.5 text-xs text-ink outline-none focus:border-primary-400"
              />
            </label>
            <label className="text-xs font-bold text-mist-500">
              Hasta
              <input
                type="date"
                value={hasta}
                onChange={(e) => setHasta(e.target.value)}
                className="mt-1 block rounded-lg border border-mist-200 bg-white px-2 py-1.5 text-xs text-ink outline-none focus:border-primary-400"
              />
            </label>
            <button
              type="button"
              onClick={() => void aplicarPeriodo()}
              disabled={cargando}
              className="rounded-lg bg-primary-600 px-3 py-2 text-xs font-bold text-white transition hover:bg-primary-700 disabled:opacity-50"
            >
              Aplicar
            </button>
            <button
              type="button"
              onClick={() => void exportar()}
              disabled={exportando}
              className="rounded-lg bg-emerald px-3 py-2 text-xs font-bold text-white transition hover:bg-emerald-deep disabled:opacity-50"
            >
              {exportando ? 'Exportando…' : 'Descargar CSV'}
            </button>
          </div>
        </div>

        {avisoExport && <p className="mt-2 text-xs font-semibold text-emerald-deep">{avisoExport}</p>}
        {error && <p className="mt-2 text-xs font-semibold text-rose-600">{error}</p>}

        {reporte && (
          <div className="mt-4 grid gap-4 border-t border-mist-200 pt-4 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wide text-mist-500">Utilidad</p>
              <p className="mt-1 text-sm font-semibold text-ink">
                {reporte.utiles} útiles · {reporte.parcialmente_utiles} parciales · {reporte.no_utiles} no útiles
              </p>
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wide text-mist-500">Satisfacción</p>
              <p className="mt-1 text-sm font-semibold text-ink">
                {reporte.satisfaccion_pct === null ? '—' : `${reporte.satisfaccion_pct.toFixed(1)} %`}
              </p>
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wide text-mist-500">Fundamentación</p>
              <p className="mt-1 text-sm font-semibold text-ink">{fmtPct(reporte.tasa_fundamentadas)}</p>
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-wide text-mist-500">Rechazadas / fuera de dominio</p>
              <p className="mt-1 text-sm font-semibold text-ink">
                {reporte.respuestas_rechazadas} / {reporte.consultas_fuera_dominio}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
