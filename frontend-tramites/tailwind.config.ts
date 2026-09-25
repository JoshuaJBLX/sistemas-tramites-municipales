import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef4fa',
          100: '#d8e6f3',
          200: '#b3cde7',
          300: '#84abd4',
          400: '#5485bd',
          500: '#3569a5',
          600: '#255387',
          700: '#1c426c',
          800: '#143257',
          900: '#0f2542',
          950: '#0a1a30',
          DEFAULT: '#143257',
        },
        secondary: '#f5a623',
        ink: '#0b1b2b',
        mist: {
          50: '#ffffff',
          100: '#f6f8fb',
          200: '#edf1f6',
          300: '#dde4ec',
          400: '#c2ccd8',
          500: '#9aa7b8',
        },
        emerald: {
          DEFAULT: '#10b981',
          soft: '#d1fae5',
          deep: '#047857',
        },
        amber: {
          DEFAULT: '#f5a623',
          soft: '#fef3c7',
          deep: '#b45309',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        'soft-sm': '0 1px 2px rgba(11,27,43,.05), 0 4px 10px -4px rgba(20,50,87,.10)',
        'soft': '0 1px 2px rgba(11,27,43,.05), 0 10px 26px -10px rgba(20,50,87,.16), 0 24px 48px -26px rgba(20,50,87,.14)',
        'soft-lg': '0 2px 4px rgba(11,27,43,.05), 0 18px 44px -14px rgba(20,50,87,.22), 0 40px 80px -40px rgba(20,50,87,.20)',
        'soft-3d': '0 1px 2px rgba(11,27,43,.05), 0 10px 26px -10px rgba(20,50,87,.16), 0 24px 48px -26px rgba(20,50,87,.14)',
        'soft-3d-lg': '0 2px 4px rgba(11,27,43,.05), 0 18px 44px -14px rgba(20,50,87,.22), 0 40px 80px -40px rgba(20,50,87,.20)',
        'lift': '0 2px 6px rgba(11,27,43,.08), 0 12px 28px -12px rgba(20,50,87,.24)',
        'neu': '0 4px 12px rgba(20,50,87,.08), 0 -2px 8px rgba(255,255,255,.8)',
        'neu-inset': 'inset 2px 2px 6px rgba(20,50,87,.08), inset -2px -2px 6px rgba(255,255,255,.9)',
        'glow-emerald': '0 0 0 3px rgba(16,185,129,.16), 0 0 20px rgba(16,185,129,.35)',
        'glow-amber': '0 0 0 3px rgba(245,166,35,.18), 0 0 20px rgba(245,166,35,.38)',
        'glow-blue': '0 0 0 3px rgba(53,105,165,.14), 0 0 24px rgba(53,105,165,.32)',
      },
      keyframes: {
        'float-y': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-14px)' },
        },
        'float-y-soft': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-7px)' },
        },
        'spin-slow': {
          to: { transform: 'rotate(360deg)' },
        },
        'pulse-ring': {
          '0%': { transform: 'scale(.9)', opacity: '.7' },
          '70%': { transform: 'scale(1.15)', opacity: '0' },
          '100%': { transform: 'scale(1.15)', opacity: '0' },
        },
        'blink-eye': {
          '0%, 92%, 100%': { transform: 'scaleY(1)' },
          '95%': { transform: 'scaleY(.08)' },
        },
        'typing-dot': {
          '0%, 60%, 100%': { transform: 'translateY(0)', opacity: '.45' },
          '30%': { transform: 'translateY(-5px)', opacity: '1' },
        },
        'rise-in': {
          from: { opacity: '0', transform: 'translateY(18px) scale(.98)' },
          to: { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
        'shimmer': {
          '0%': { backgroundPosition: '-400px 0' },
          '100%': { backgroundPosition: '400px 0' },
        },
        'bob': {
          '0%, 100%': { transform: 'translateY(0) rotate(-1deg)' },
          '50%': { transform: 'translateY(-6px) rotate(1.5deg)' },
        },
        'pop-in': {
          '0%': { transform: 'scale(.85)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
      animation: {
        'float-y': 'float-y 6s ease-in-out infinite',
        'float-y-soft': 'float-y-soft 5s ease-in-out infinite',
        'typing-dot': 'typing-dot 1.2s ease-in-out infinite',
        'spin-slow': 'spin-slow 22s linear infinite',
        'pulse-ring': 'pulse-ring 2.4s ease-out infinite',
        'blink-eye': 'blink-eye 4.6s ease-in-out infinite',
        'rise-in': 'rise-in .55s cubic-bezier(.22,.8,.32,1) both',
        'shimmer': 'shimmer 2.4s linear infinite',
        'bob': 'bob 3.6s ease-in-out infinite',
        'pop-in': 'pop-in .18s linear both',
      },
    },
  },
  plugins: [],
};

export default config;

