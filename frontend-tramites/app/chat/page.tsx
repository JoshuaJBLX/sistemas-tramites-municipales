'use client';
import ChatBox from '../../components/ChatBox';
import RobotAgent from '../../components/RobotAgent';
import GroundednessBadge from '../../components/GroundednessBadge';
import { ShieldIcon } from '../../components/icons';

export default function ChatPage() {
  return (
    <section className="mx-auto max-w-7xl px-3 pb-16 pt-6 sm:px-6">
      <div className="grid items-start gap-6 lg:grid-cols-[1fr_420px]">
        {/* Columna principal: chat desktop */}
        <div className="animate-rise-in">
          <p className="eyebrow">Asistente conversacional · RAG + SLM</p>
          <h1 className="mt-1 text-3xl font-extrabold tracking-tight text-ink sm:text-4xl">
            Habla con Muni, tu orientador municipal
          </h1>
          <p className="mt-2 max-w-xl text-sm text-mist-500">
            Respuestas fundamentadas en ordenanzas y TUPA vigente. Cada respuesta cita sus fuentes oficiales.
          </p>
          <div className="glass-strong mt-5 rounded-[2rem] p-4 sm:p-6">
            <ChatBox />
            <p className="mt-3 flex items-center gap-2 text-xs text-mist-500">
              <ShieldIcon className="h-4 w-4" /> Tus consultas se registran con fines de auditoría y mejora del servicio.
            </p>
          </div>
        </div>

        {/* Mockup móvil */}
        <div className="flex justify-center lg:sticky lg:top-24 animate-rise-in" style={{ animationDelay: '120ms' }}>
          <div className="relative w-[300px] rounded-[3rem] border-[5px] border-white bg-gradient-to-b from-white to-mist-100 p-2 shadow-soft-lg">
            <div className="overflow-hidden rounded-[2.4rem] bg-mist-100 shadow-inner">
              {/* notch */}
              <div className="relative bg-gradient-to-b from-primary-800 to-primary-600 px-4 pb-3 pt-4 text-white">
                <div className="mx-auto mb-2 h-5 w-24 rounded-full bg-primary-950/80" />
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/70">Municipalidad Provincial de Junín</p>
                <p className="text-sm font-extrabold">Muni · En línea</p>
              </div>
              <div className="flex h-[380px] flex-col gap-2 overflow-y-auto scroll-thin p-3">
                <div className="bubble-user !text-xs">¿Qué necesito para mi partida de nacimiento?</div>
                <div className="bubble-bot !text-xs">
                  <p>Certificado de nacimiento del hospital, DNI de la madre y del padre. Trámite inmediato.</p>
                  <GroundednessBadge score={0.97} fuentes={[{ titulo: 'TUPA 2023 · N.º 188' }]} compact />
                </div>
                <div className="bubble-user !text-xs">¿Y la licencia de funcionamiento?</div>
                <div className="bubble-bot !text-xs">
                  <p>Solicitud, DNI del titular, título de propiedad y plano de ubicación. Plazo 5–15 días hábiles.</p>
                  <GroundednessBadge score={0.94} fuentes={[{ titulo: 'TUPA 2023 · Licencias' }]} compact />
                </div>
              </div>
              <div className="border-t border-white/60 bg-white/80 p-2.5 backdrop-blur-xl">
                <div className="flex items-center gap-2 rounded-full bg-white px-3 py-2 shadow-inner">
                  <span className="flex-1 text-xs text-mist-500">Escribe tu consulta…</span>
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-b from-primary-600 to-primary-800 text-sm text-white shadow-lift">➤</span>
                </div>
                <div className="mt-2 flex gap-1.5">
                  {['Requisitos', 'Costos', 'Plazos'].map((s) => (
                    <span key={s} className="chip !px-2.5 !py-1 !text-[10px]">✨ {s}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Robot de apoyo (solo desktop, sutil) */}
      <div className="pointer-events-none fixed bottom-6 right-6 hidden xl:block">
        <RobotAgent compact />
      </div>
    </section>
  );
}

