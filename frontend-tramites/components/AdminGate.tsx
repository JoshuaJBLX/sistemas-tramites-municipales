'use client';
import { useEffect, useState, type FormEvent, type ReactNode } from 'react';
import {
  cerrarSesion,
  iniciarSesion,
  leerSesion,
  obtenerSesionActual,
  type SesionUsuario,
} from '../lib/api';

/**
 * Protege el panel administrativo (HU-13): sin sesión abierta muestra el
 * formulario de acceso; con sesión válida verifica que el rol sea administrador
 * o revisor (los ciudadanos no pueden acceder al panel administrativo).
 */
export default function AdminGate({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<SesionUsuario | null>(null);
  const [cargando, setCargando] = useState(true);
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    if (!leerSesion()) {
      setCargando(false);
      return;
    }
    obtenerSesionActual()
      .then((sesion) => {
        if (sesion && sesion.rol === 'ciudadano') {
          cerrarSesion();
          setUsuario(null);
          setError('Las cuentas de ciudadano no tienen acceso al panel administrativo.');
        } else {
          setUsuario(sesion);
        }
      })
      .catch(() => cerrarSesion())
      .finally(() => setCargando(false));
  }, []);

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    setError('');
    setEnviando(true);
    try {
      const sesion = await iniciarSesion(correo.trim(), password);
      if (sesion.rol === 'ciudadano') {
        cerrarSesion();
        setError('Las cuentas de ciudadano no tienen acceso al panel administrativo. Utiliza el chat.');
        return;
      }
      setUsuario(sesion);
    } catch {
      setError('Credenciales incorrectas o sin permisos de gestión.');
    } finally {
      setEnviando(false);
    }
  }

  if (cargando) {
    return <p className="py-16 text-center text-sm text-primary-600">Verificando sesión…</p>;
  }

  if (!usuario) {
    return (
      <section className="mx-auto max-w-md px-3 pb-16 pt-10">
        <p className="eyebrow">Panel administrativo</p>
        <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-ink">Acceso restringido</h1>
        <p className="mt-2 text-sm text-primary-600">
          Ingresa con tu cuenta de administrador o revisor para gestionar el sistema.
        </p>
        <form onSubmit={enviar} className="card-3d mt-6 space-y-4 p-6">
          <label className="block">
            <span className="text-sm font-semibold text-primary-800">Correo</span>
            <input
              type="email"
              required
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              className="mt-1 w-full rounded-xl border border-primary-200 bg-white/80 px-3 py-2 text-sm outline-none focus:border-primary-500"
              placeholder="admin@munihuancayo.gob.pe"
              autoComplete="username"
            />
          </label>
          <label className="block">
            <span className="text-sm font-semibold text-primary-800">Contraseña</span>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-xl border border-primary-200 bg-white/80 px-3 py-2 text-sm outline-none focus:border-primary-500"
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </label>
          {error && <p className="rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
          <button
            type="submit"
            disabled={enviando}
            className="w-full rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-primary-700 disabled:opacity-60"
          >
            {enviando ? 'Ingresando…' : 'Ingresar'}
          </button>
        </form>
      </section>
    );
  }

  return (
    <>
      <div className="mx-auto flex max-w-7xl items-center justify-end gap-3 px-3 pt-4 sm:px-6">
        <span className="text-sm text-primary-600 font-medium">
          {usuario.nombre} · <span className="uppercase text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">{usuario.rol}</span>
        </span>
        <button
          onClick={() => {
            cerrarSesion();
            setUsuario(null);
          }}
          className="rounded-xl border border-primary-200 bg-white/70 px-3 py-1.5 text-sm font-semibold text-primary-700 transition hover:bg-white"
        >
          Cerrar sesión
        </button>
      </div>
      {children}
    </>
  );
}
