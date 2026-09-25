'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { ShieldIcon, MenuIcon, CloseIcon } from './icons';

const links = [
  { href: '/', label: 'Inicio' },
  { href: '/tramites', label: 'Trámites' },
  { href: '/chat', label: 'Asistente' },
  { href: '/admin', label: 'Admin' },
];

export default function Navbar() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-50 px-3 pt-3 sm:px-6">
      <nav className="glass-strong mx-auto flex max-w-7xl items-center justify-between gap-3 rounded-3xl px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-b from-primary-600 to-primary-900 shadow-lift">
            <ShieldIcon className="h-8 w-8" />
          </span>
          <span className="leading-tight">
            <span className="block text-[10px] font-bold uppercase tracking-[0.22em] text-primary-500">Municipalidad Provincial de Junín</span>
            <span className="block text-base font-extrabold text-ink">Trámites Digitales</span>
          </span>
        </Link>
        <div className="hidden items-center gap-1 md:flex">
          {links.map((l) => (
            <Link key={l.href} href={l.href}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition-all duration-200 ${path === l.href ? 'bg-gradient-to-b from-primary-600 to-primary-800 text-white shadow-lift' : 'text-primary-800 hover:bg-primary-50 hover:-translate-y-0.5'}`}>
              {l.label}
            </Link>
          ))}
          <Link href="/chat" className="btn-emerald-3d ml-2 !py-2.5 text-sm">Consultar ahora</Link>
        </div>
        <button className="btn-neu !p-2.5 md:hidden" onClick={() => setOpen(!open)} aria-label="Abrir menú">
          {open ? <CloseIcon className="h-5 w-5" /> : <MenuIcon className="h-5 w-5" />}
        </button>
      </nav>
      {open && (
        <div className="glass-strong mx-auto mt-2 max-w-7xl rounded-3xl p-3 md:hidden animate-rise-in">
          {links.map((l) => (
            <Link key={l.href} href={l.href} onClick={() => setOpen(false)}
              className={`block rounded-2xl px-4 py-2.5 text-sm font-semibold ${path === l.href ? 'bg-primary-800 text-white' : 'text-primary-800'}`}>
              {l.label}
            </Link>
          ))}
        </div>
      )}
    </header>
  );
}

