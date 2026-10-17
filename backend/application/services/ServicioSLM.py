"""Servicio de aplicación: ServicioSLM (Small Language Model)."""

from domain.entities.Documento import Documento
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort

PLANTILLA_SISTEMA = (
    'Eres un asistente municipal. Responde únicamente con la información '
    'contenida en el contexto proporcionado. Si el contexto no contiene la '
    'respuesta, indícalo explícitamente y sugiere acudir a la municipalidad.'
)

# Estructura de salida para que la respuesta sea clara y ordenable (HU-09).
INSTRUCCION_ESTRUCTURA = (
    'Organiza la respuesta en estos apartados, solo si el contexto los respalda: '
    'REQUISITOS, PASOS, COSTO, PLAZO y OBSERVACIONES. Si el contexto no aporta '
    'un dato, escribe "No especificado en la base documental" en ese apartado. '
    'No inventes montos, plazos ni documentos que no aparezcan en el contexto.'
)

# Apartados que la respuesta final debe contener siempre (HU-09).
APARTADOS_REQUERIDOS: tuple[str, ...] = (
    'REQUISITOS',
    'PASOS',
    'COSTO',
    'PLAZO',
    'OBSERVACIONES',
)

# Texto literal que reemplaza a un apartado sin respaldo documental.
SIN_DATO = 'No especificado en la base documental'

# Palabras clave de la base documental que permiten rellenar cada apartado.
_CLAVES_APARTADO: dict[str, tuple[str, ...]] = {
    'REQUISITOS': ('requisit', 'document', 'dni', 'adjunt', 'presentar'),
    'PASOS': ('paso', 'proceso', 'solicitud', 'mesa de partes', 'tramitar', 'inscrib'),
    'COSTO': ('costo', 'arancel', 'tasa', 'pago', 'soles', 's/'),
    'PLAZO': ('plazo', 'dia', 'hábil', 'habil', 'atencion', 'inmediato', 'plazos'),
    'OBSERVACIONES': (),
}


class ServicioSLM:
    """Construye el prompt y delega la generación al modelo de lenguaje."""

    def __init__(self, generacion_respuesta: GeneracionRespuestaPort) -> None:
        self._generacion_respuesta = generacion_respuesta

    async def generar(self, pregunta: str, contexto: list[Documento]) -> str:
        if not contexto:
            return (
                'No encontré información oficial en la base documental para '
                'responder tu consulta. Te recomiendo acudir a la oficina de '
                'trámites de tu municipalidad.'
            )

        salida = await self._generacion_respuesta.generar(pregunta, contexto)
        # El SLM pequeño puede ignorar la plantilla: si faltan apartados, se
        # componen desde la base documental para garantizar la estructura (HU-09).
        return self.garantizar_estructura(salida, contexto)

    def construir_prompt(self, pregunta: str, contexto: list[Documento]) -> str:
        # Con recuperación por fragmento el modelo recibe el chunk relevante y
        # no el documento entero: prompt más corto y más preciso (HU-04).
        fragmentos = '\n\n'.join(
            f'[Documento: {documento.titulo}]\n'
            f'{documento.fragmento_destacado or documento.contenido}'
            for documento in contexto
        )
        return (
            f'{PLANTILLA_SISTEMA}\n\n{INSTRUCCION_ESTRUCTURA}'
            f'\n\nContexto:\n{fragmentos}\n\nPregunta: {pregunta}'
        )

    def estructura_completa(self, texto: str) -> bool:
        """Indica si la respuesta contiene los cinco apartados requeridos."""
        superior = texto.upper()
        return all(f'{apartado}:' in superior for apartado in APARTADOS_REQUERIDOS)

    def garantizar_estructura(self, texto: str, contexto: list[Documento]) -> str:
        """Completa los apartados que el modelo no redactó, usando el contexto.

        Los valores se toman de los documentos de la base documental (nunca se
        inventan): si el contexto no aporta el dato se escribe `SIN_DATO`. La
        respuesta original del modelo se conserva, dentro de OBSERVACIONES o al
        final del texto, según el caso.
        """
        faltantes = [
            apartado
            for apartado in APARTADOS_REQUERIDOS
            if f'{apartado.upper()}:' not in texto.upper()
        ]
        if not faltantes:
            return texto

        cuerpo = texto.strip()
        lineas: list[str] = []
        for apartado in faltantes:
            if apartado == 'OBSERVACIONES':
                # La respuesta del modelo se conserva aquí, sin duplicarla.
                lineas.append(f'OBSERVACIONES: {cuerpo or SIN_DATO}')
            else:
                lineas.append(f'{apartado}: {self._contenido_apartado(apartado, contexto)}')

        if 'OBSERVACIONES' in faltantes:
            return '\n'.join(lineas)
        return '\n'.join(lineas + ['', cuerpo])

    def _contenido_apartado(self, apartado: str, contexto: list[Documento]) -> str:
        """Extrae de la base documental las frases que respaldan un apartado."""
        claves = _CLAVES_APARTADO.get(apartado, ())
        if not claves or not contexto:
            return SIN_DATO

        hallazgos: list[str] = []
        for documento in contexto:
            for oracion in self._oraciones(f'{documento.contenido} {documento.titulo}'):
                bajo = oracion.lower()
                if any(clave in bajo for clave in claves) and oracion not in hallazgos:
                    hallazgos.append(oracion)
                    if len(hallazgos) >= 3:
                        break
            if len(hallazgos) >= 3:
                break

        return ' '.join(hallazgos) if hallazgos else SIN_DATO

    @staticmethod
    def _oraciones(texto: str) -> list[str]:
        """Divide el texto en oraciones de al menos 15 caracteres."""
        bruto = texto.replace('\n', ' ').split('.')
        return [
            parte.strip() + '.'
            for parte in bruto
            if len(parte.strip()) >= 15
        ]