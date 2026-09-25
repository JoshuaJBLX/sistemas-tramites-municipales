export default function RobotAgent({ compact = false }: { compact?: boolean }) {
  const size = compact ? 'h-36 w-36' : 'h-56 w-56 sm:h-64 sm:w-64';
  return (
    <div className="relative flex flex-col items-center">
      {/* halo cálido */}
      <div className="absolute -top-4 h-24 w-56 rounded-full bg-amber/20 blur-2xl" aria-hidden="true" />
      <div className={`relative ${size} animate-float-y`} role="img" aria-label="Muni, asistente virtual municipal">
        <svg viewBox="0 0 200 220" className="h-full w-full drop-shadow-[0_20px_28px_rgba(20,50,87,.28)]">
          <defs>
            <linearGradient id="rb-body" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="#fff9ef" />
              <stop offset=".55" stopColor="#ffe7cc" />
              <stop offset="1" stopColor="#ffd9ad" />
            </linearGradient>
            <linearGradient id="rb-teal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="#2dd4a7" />
              <stop offset="1" stopColor="#0f766e" />
            </linearGradient>
            <radialGradient id="rb-cheek" cx=".5" cy=".5" r=".5">
              <stop offset="0" stopColor="#ff8a80" stopOpacity=".55" />
              <stop offset="1" stopColor="#ff8a80" stopOpacity="0" />
            </radialGradient>
          </defs>
          {/* brote (antena orgánica) */}
          <path d="M100 44q-3 -16 10 -22" stroke="#0f766e" strokeWidth="4" strokeLinecap="round" fill="none" />
          <path d="M108 20q14 -2 12 12 -8 -1 -12 -12Z" fill="#10b981" />
          <circle cx="112" cy="26" r="2.6" fill="#d1fae5" />
          {/* orejitas */}
          <circle cx="46" cy="98" r="11" fill="url(#rb-teal)" stroke="#fff" strokeWidth="2.5" />
          <circle cx="154" cy="98" r="11" fill="url(#rb-teal)" stroke="#fff" strokeWidth="2.5" />
          {/* cabeza */}
          <rect x="46" y="46" width="108" height="92" rx="40" fill="url(#rb-body)" stroke="#fff" strokeWidth="3" />
          {/* ojos grandes y cálidos */}
          <g className="origin-center" style={{ animation: 'blink-eye 4.6s ease-in-out infinite', transformBox: 'fill-box' }}>
            <ellipse cx="80" cy="88" rx="13" ry="15" fill="#3a3029" />
            <ellipse cx="120" cy="88" rx="13" ry="15" fill="#3a3029" />
            <circle cx="84" cy="83" r="4" fill="#fff" />
            <circle cx="124" cy="83" r="4" fill="#fff" />
            <circle cx="78" cy="91" r="1.8" fill="#fff" opacity=".8" />
            <circle cx="118" cy="91" r="1.8" fill="#fff" opacity=".8" />
          </g>
          {/* mejillas + sonrisa */}
          <ellipse cx="66" cy="108" rx="11" ry="6.5" fill="url(#rb-cheek)" />
          <ellipse cx="134" cy="108" rx="11" ry="6.5" fill="url(#rb-cheek)" />
          <path d="M90 106q10 9 20 0" stroke="#c96a52" strokeWidth="4" strokeLinecap="round" fill="none" />
          {/* cuerpo */}
          <rect x="58" y="142" width="84" height="50" rx="24" fill="url(#rb-teal)" stroke="#fff" strokeWidth="3" />
          <circle cx="100" cy="163" r="14" fill="#fff" opacity=".92" />
          <path d="M96 160q4 -5 8 0 4 -5 8 0 -3 8 -8 8 -5 0 -8 -8Z" fill="#ff6b6b" opacity=".95" />
          {/* bracitos */}
          <rect x="38" y="152" width="16" height="28" rx="8" fill="url(#rb-body)" stroke="#d98b5f" strokeWidth="3" />
          <rect x="146" y="152" width="16" height="28" rx="8" fill="url(#rb-body)" stroke="#d98b5f" strokeWidth="3" />
        </svg>
      </div>
      {/* plataforma */}
      <div className="relative mt-1 flex flex-col items-center" aria-hidden="true">
        <div className="h-6 w-48 rounded-[50%] bg-primary-900/20 blur-md" />
        <div className="relative -mt-6 h-10 w-52 overflow-hidden rounded-[50%] border border-white/70 bg-gradient-to-b from-white/90 to-emerald-soft/60 shadow-soft backdrop-blur-xl">
          <div className="absolute inset-x-6 top-1.5 h-4 rounded-[50%] border border-emerald/30" />
          <div className="absolute inset-x-12 top-3 h-3 rounded-[50%] bg-emerald/30 blur-[2px]" />
        </div>
        <div className="mt-2 flex items-center gap-2 rounded-full border border-emerald/30 bg-white/85 px-3 py-1 text-xs font-semibold text-emerald-deep shadow-soft backdrop-blur">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute h-full w-full animate-pulse-ring rounded-full bg-emerald" />
            <span className="h-2.5 w-2.5 rounded-full bg-emerald" />
          </span>
          En línea · responde con fuentes oficiales
        </div>
      </div>
    </div>
  );
}