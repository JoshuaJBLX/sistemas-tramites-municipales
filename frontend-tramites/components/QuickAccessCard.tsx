'use client';

import Link from 'next/link';

interface Props {
  href: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  accent: string;
}

export default function QuickAccessCard({ href, title, subtitle, icon, accent }: Props) {
  return (
    <Link
      href={href}
      className="card-3d group relative flex items-center gap-4 overflow-hidden p-4 text-left"
    >
      <span className="pointer-events-none absolute -right-8 -top-8 h-24 w-24 rounded-full bg-amber-soft/50 blur-2xl transition group-hover:scale-150" aria-hidden="true" />
      <span className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-[1.4rem] bg-gradient-to-b text-white shadow-lift transition duration-300 group-hover:scale-105 group-hover:-rotate-3 ${accent}`}>
        <span className="[&>svg]:h-8 [&>svg]:w-8">{icon}</span>
      </span>
      <span className="relative">
        <span className="block font-bold text-ink">{title}</span>
        <span className="block text-xs text-mist-500">{subtitle}</span>
      </span>
      <span className="relative ml-auto text-xl font-bold text-mist-300 transition duration-300 group-hover:translate-x-1 group-hover:text-primary-500">→</span>
    </Link>
  );
}