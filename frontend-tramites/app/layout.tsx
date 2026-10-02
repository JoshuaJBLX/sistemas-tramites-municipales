import type { Metadata } from 'next';
import Navbar from '../components/Navbar';
import './globals.css';

export const metadata: Metadata = {
  title: 'MUN AI · Sistema basado en SLM para la orientación de trámites municipales',
  description:
    'Sistema basado en SLM para la orientación de trámites municipales en la Municipalidad Provincial de Huancayo, con respuestas fundamentadas en el TUPA 2023: requisitos, aranceles y plazos oficiales.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <footer className="mx-auto max-w-7xl px-3 pb-8 sm:px-6">
          <div className="glass flex flex-col items-center justify-between gap-2 rounded-3xl px-6 py-4 text-xs text-mist-500 sm:flex-row">
            <p>
              <strong className="text-primary-800">Municipalidad Provincial de Huancayo</strong>
              {' · '}
              Sistema basado en SLM para la orientación de trámites municipales
            </p>
            <p>Respuestas con fuentes oficiales · groundedness visible · auditoría total</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
