/**
 * Volumetric SVG icon set — soft 3D gradients, no external dependencies.
 */
interface IconProps { className?: string; }
const base = 'h-6 w-6';

export function ShieldIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" fill="none" className={className} aria-hidden="true">
      <defs>
        <linearGradient id="sh-blue" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3569a5" />
          <stop offset="1" stopColor="#0f2542" />
        </linearGradient>
        <linearGradient id="sh-gold" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#ffd97a" />
          <stop offset="1" stopColor="#f5a623" />
        </linearGradient>
      </defs>
      <path d="M24 3 41 9v13c0 10.5-7.2 18.4-17 23C14.2 40.4 7 32.5 7 22V9L24 3Z" fill="url(#sh-blue)" stroke="#ffffff" strokeWidth="2" />
      <path d="M24 8.5 36 12.6V22c0 7.9-5.2 14-12 17.4C17.2 36 12 29.9 12 22v-9.4L24 8.5Z" fill="none" stroke="url(#sh-gold)" strokeWidth="2.4" />
      <path d="M24 15v9M18.5 20.5h11" stroke="url(#sh-gold)" strokeWidth="2.6" strokeLinecap="round" />
      <circle cx="24" cy="30.5" r="3.2" fill="url(#sh-gold)" />
    </svg>
  );
}

export function TramiteIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" fill="none" className={className} aria-hidden="true">
      <defs>
        <linearGradient id="tr-doc" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#ffffff" />
          <stop offset="1" stopColor="#d8e6f3" />
        </linearGradient>
      </defs>
      <path d="M12 5h16l9 9v29H12V5Z" fill="url(#tr-doc)" stroke="#143257" strokeWidth="2.4" strokeLinejoin="round" />
      <path d="M28 5v9h9" stroke="#143257" strokeWidth="2.4" strokeLinejoin="round" />
      <path d="M17 24h14M17 29h14M17 34h9" stroke="#3569a5" strokeWidth="2.4" strokeLinecap="round" />
      <circle cx="34" cy="35" r="8" fill="#10b981" stroke="#fff" strokeWidth="2.4" />
      <path d="M30.5 35l2.4 2.4 4.6-5" stroke="#fff" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function OrdenanzaIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" fill="none" className={className} aria-hidden="true">
      <defs>
        <linearGradient id="or-book" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#5485bd" />
          <stop offset="1" stopColor="#143257" />
        </linearGradient>
      </defs>
      <path d="M9 10c5-2.5 10-2.5 15 0v28c-5-2.5-10-2.5-15 0V10Z" fill="url(#or-book)" stroke="#0f2542" strokeWidth="2.2" strokeLinejoin="round" />
      <path d="M24 10c5-2.5 10-2.5 15 0v28c-5-2.5-10-2.5-15 0" fill="#d8e6f3" stroke="#0f2542" strokeWidth="2.2" strokeLinejoin="round" />
      <path d="M15 17c2.4-1 4.7-1 7 0M15 22c2.4-1 4.7-1 7 0M28 17c1.8.6 3.4.6 5 0M28 22c1.8.6 3.4.6 5 0" stroke="#f5a623" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function DirectorioIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" fill="none" className={className} aria-hidden="true">
      <circle cx="17" cy="16" r="8" fill="#d8e6f3" stroke="#143257" strokeWidth="2.4" />
      <circle cx="17" cy="16" r="3.2" fill="#3569a5" />
      <path d="M5 40c1.5-6.5 6-10 12-10s10.5 3.5 12 10" fill="#b3cde7" stroke="#143257" strokeWidth="2.4" strokeLinecap="round" />
      <circle cx="33" cy="15" r="6.5" fill="#d1fae5" stroke="#047857" strokeWidth="2.2" />
      <path d="M30 15h6M33 12v6" stroke="#047857" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function AyudaIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 48 48" fill="none" className={className} aria-hidden="true">
      <defs>
        <linearGradient id="ay-bub" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#ffffff" />
          <stop offset="1" stopColor="#d8e6f3" />
        </linearGradient>
      </defs>
      <path d="M8 8h32v22H24l-8 7v-7H8V8Z" fill="url(#ay-bub)" stroke="#143257" strokeWidth="2.4" strokeLinejoin="round" />
      <path d="M24 17c-.4-3-2.8-5-6-5-3.4 0-6 2.5-6 6 0 4.5 6 4.5 6 9" stroke="#f5a623" strokeWidth="3" strokeLinecap="round" />
      <circle cx="24" cy="33.5" r="2" fill="#f5a623" />
    </svg>
  );
}
export function ChatIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M4 5h16v11H9l-5 4V5Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <path d="M8 9.5h8M8 12.5h5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function SendIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M4 12 20 4l-4.5 16-4-6.5L4 12Z" fill="currentColor" opacity=".95" />
      <path d="M11.5 13.5 20 4" stroke="#fff" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export function SparkIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M12 2c.7 4.8 3.2 7.3 8 8-4.8.7-7.3 3.2-8 8-.7-4.8-3.2-7.3-8-8 4.8-.7 7.3-3.2 8-8Z" fill="currentColor" />
    </svg>
  );
}

export function CheckIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="m5 12.5 4.5 4.5L19 7.5" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function AlertIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M12 3 22 20H2L12 3Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <path d="M12 10v4" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
      <circle cx="12" cy="17" r="1.3" fill="currentColor" />
    </svg>
  );
}

export function UploadIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M12 16V4m0 0 5 5m-5-5L7 9" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function SearchIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2.2" />
      <path d="m16.5 16.5 5 5" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function ChartIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M4 20V4M4 20h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M8 16v-5m4 5V8m4 8v-3" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" />
    </svg>
  );
}

export function DocIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M6 2h8l4 4v16H6V2Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
      <path d="M14 2v4h4M9 12h6M9 15.5h6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export function ClockIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <circle cx="12" cy="12" r="8.5" stroke="currentColor" strokeWidth="2" />
      <path d="M12 7.5V12l3.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function UsersIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <circle cx="9" cy="8" r="3.5" stroke="currentColor" strokeWidth="2" />
      <path d="M3 20c1-3.5 3.2-5.5 6-5.5s5 2 6 5.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export function HeartIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M12 20.5S3.5 15.5 3.5 9.6C3.5 7 5.5 5 8 5c1.7 0 3.1.9 4 2.3C12.9 5.9 14.3 5 16 5c2.5 0 4.5 2 4.5 4.6 0 5.9-8.5 10.9-8.5 10.9Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" />
    </svg>
  );
}

export function MenuIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function CloseIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M6 6l12 12M18 6 6 18" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  );
}

export function LinkIcon({ className = base }: IconProps) {
  return (
    <svg viewBox="0 0 24 24" fill="none" className={className} aria-hidden="true">
      <path d="M10 14a4.5 4.5 0 0 0 6.4.4l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.7 1.7M14 10a4.5 4.5 0 0 0-6.4-.4l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.7-1.7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}
