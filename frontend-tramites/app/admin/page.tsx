'use client';
import { useEffect, useState } from 'react';
import MetricasPanel from '../../components/MetricasPanel';
import AuditLog from '../../components/AuditLog';
import DocumentManager from '../../components/DocumentManager';
import AdminGate from '../../components/AdminGate';
import QuickAccessCard from '../../components/QuickAccessCard';
import { ChartIcon, DocIcon, ClockIcon } from '../../components/icons';
import { leerSesion, type SesionUsuario } from '../../lib/api';

export const dynamic = 'force-dynamic';

export default function AdminPage() {
  const [rol, setRol] = useState<string | null>(null);

  useEffect(() => {
    const sesion = leerSesion();
    if (sesion) {
      setRol(sesion.usuario.rol);
    }
  }, []);

  const esAdmin = rol === 'administrador';
  const esRevisor = rol === 'revisor';

  return (
    <AdminGate>
      <section className="mx-auto max-w-7xl px-3 pb-16 pt-6 sm:px-6">
        <p className="eyebrow">Panel administrativo</p>
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">
            {esAdmin ? 'Dashboard de métricas' : 'Panel de Gestión'}
          </h1>
          <div className="flex gap-2">
            <span className="badge-emerald">● En vivo</span>
            <span className="badge-blue">Huancayo · todas las sedes</span>
          </div>
        </div>

        {/* Accesos rápidos dinámicos por rol. */}
        <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <QuickAccessCard
            href="#documentos"
            title="Gestión Documental"
            subtitle="Subir, indexar y aprobar documentos"
            icon={<DocIcon />}
            accent="from-primary-500 to-primary-800"
          />
          {esAdmin && (
            <>
              <QuickAccessCard
                href="#metricas"
                title="Métricas"
                subtitle="KPIs, satisfacción y reportes"
                icon={<ChartIcon />}
                accent="from-amber to-amber-deep"
              />
              <QuickAccessCard
                href="#auditoria"
                title="Auditoría"
                subtitle="Registro de consultas con filtros"
                icon={<ClockIcon />}
                accent="from-emerald to-emerald-deep"
              />
            </>
          )}
        </div>

        {/* El revisor solo ve Gestión Documental (HU-03). El admin ve todo. */}
        {esAdmin && (
          <>
            <div className="mt-5" id="metricas">
              <MetricasPanel />
            </div>
            <div className="mt-4" id="auditoria">
              <AuditLog />
            </div>
          </>
        )}

        <div className="mt-4" id="documentos">
          <DocumentManager />
        </div>

        {esRevisor && (
          <div className="mt-8 rounded-2xl bg-primary-50 border border-primary-100 p-6">
            <p className="text-sm text-primary-800 font-medium">
              Tu cuenta tiene el rol de <span className="font-bold">revisor municipal</span>.
            </p>
            <p className="mt-1 text-xs text-primary-600">
              Tienes acceso a la gestión de la base de conocimientos. Para acceder a métricas avanzadas o auditoría de ciudadanos, contacta con el administrador del sistema.
            </p>
          </div>
        )}
      </section>
    </AdminGate>
  );
}
