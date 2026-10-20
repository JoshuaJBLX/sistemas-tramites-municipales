"""Servicio de aplicación: ServicioSLM (Small Language Model)."""

import re

from domain.entities.Documento import Documento
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort

# Estructura de salida para que la respuesta sea clara y ordenable (HU-09).
INSTRUCCION_ESTRUCTURA = (
    'Responde en dos partes y de forma breve:\n'
    '1) Un resumen en pasos numerados (máximo 4 pasos): cada línea empieza '
    'con "1.", "2." etc., seguido de un título corto en negrita (**título**) '
    'y una sola frase con la acción concreta (dónde ir, qué pagar, qué '
    'entregar, cuándo recoger).\n'
    '2) Los apartados REQUISITOS, PASOS, COSTO, PLAZO y OBSERVACIONES, cada '
    'uno en máximo 2 oraciones cortas. Si el contexto no aporta un dato, '
    'escribe "No especificado en la base documental". No inventes montos, '
    'plazos ni documentos que no aparezcan en el contexto. No repitas la '
    'misma información en varios apartados.'
)

# Instrucción para consultas generales (horarios, teléfonos, catálogo…).
INSTRUCCION_BREVE = (
    'Responde con un máximo de 3 oraciones cortas y directas, sin listas ni '
    'apartados numerados.'
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

# Límites de longitud del texto final (evita respuestas de miles de caracteres).
LIMITE_PASO = 110
LIMITE_SECCION = 200
LIMITE_TOTAL = 1100
MAXIMO_PASOS = 4

# Elementos de una lista numerada ("1.", "1)", "1 -") dentro del texto.
_NUMERADO = re.compile(r'(\d+)\s*[).\-]\s+([^;\n]{10,})')

# Negrita suelta del modelo sin cerrar (p. ej. "** Ninguno especificado").
_SIN_NEGRITA_SUELTA = re.compile(r'^\*\*\s*')

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

    async def generar(
        self, pregunta: str, contexto: list[Documento], estructura: bool = True
    ) -> str:
        if not contexto:
            return (
                'No encontré información oficial en la base documental para '
                'responder tu consulta. Te recomiendo acudir a la oficina de '
                'trámites de tu municipalidad.'
            )

        instruccion = INSTRUCCION_ESTRUCTURA if estructura else INSTRUCCION_BREVE
        salida = await self._generacion_respuesta.generar(
            pregunta, contexto, instrucciones=instruccion
        )
        # Consultas sin intención de trámite (horarios, teléfonos, catálogo…):
        # no se fuerza la estructura REQUISITOS/COSTO/… porque solo ensuciaría
        # la respuesta con datos de otros documentos.
        if not estructura:
            return self._acortar(self._sin_apartados(salida), LIMITE_TOTAL)
        # El SLM pequeño puede ignorar la plantilla: si faltan apartados, se
        # componen desde la base documental para garantizar la estructura (HU-09).
        return self.condensar(self.garantizar_estructura(salida, contexto))

    def estructura_completa(self, texto: str) -> bool:
        """Indica si la respuesta contiene los cinco apartados requeridos."""
        return all(
            self._linea_apartado(texto, apartado) is not None
            for apartado in APARTADOS_REQUERIDOS
        )

    @staticmethod
    def _linea_apartado(texto: str, apartado: str) -> int | None:
        """Índice de la línea que abre el apartado, o None si no está."""
        prefijo = f'{apartado.upper()}:'
        for indice, linea in enumerate(texto.split('\n')):
            if linea.upper().lstrip('*#- ').strip().startswith(prefijo):
                return indice
        return None

    def condensar(self, texto: str) -> str:
        """Acorta la respuesta: pasos numerados arriba y apartados compactos.

        1) Asegura un bloque inicial de pasos numerados (máximo 4); si el
        modelo no lo escribió, lo extrae de la sección PASOS.
        2) Recorta cada apartado a `LIMITE_SECCION` caracteres y el total a
        `LIMITE_TOTAL`, cortando en límite de oración y marcando "…" cuando
        falta información (HU-09 se conserva: los cinco apartados siguen
        presentes).
        """
        if not texto or not texto.strip():
            return texto

        preambulo, secciones = self._separar_secciones(texto)

        # Los pasos que escribió el modelo también se recortan; si no abrió
        # con pasos numerados, se construyen desde la sección PASOS.
        preambulo = [
            (
                f'{coincidencia.group(1)}. '
                f'{self._acortar(coincidencia.group(2).strip(), LIMITE_PASO)}'
            )
            if (coincidencia := _NUMERADO.search(linea))
            else linea
            for linea in preambulo
        ]
        if not any(_NUMERADO.search(linea) for linea in preambulo):
            cuerpo_pasos = next(
                (cuerpo for nombre, cuerpo in secciones if nombre == 'PASOS'), ''
            )
            pasos = _NUMERADO.findall(cuerpo_pasos)[:MAXIMO_PASOS]
            if pasos:
                preambulo = [
                    f'{numero}. {self._acortar(frase.strip(), LIMITE_PASO)}'
                    for numero, frase in pasos
                ]

        lineas: list[str] = []
        if preambulo:
            lineas.extend(preambulo)
            lineas.append('')

        for nombre, cuerpo in secciones:
            compacto = self._acortar(cuerpo, LIMITE_SECCION)
            lineas.append(f'{nombre}: {compacto}')

        salida = '\n'.join(lineas).strip()
        if len(salida) > LIMITE_TOTAL:
            salida = self._acortar(salida, LIMITE_TOTAL)
        return salida

    @staticmethod
    def _separar_secciones(texto: str) -> tuple[list[str], list[tuple[str, str]]]:
        """Divide la respuesta en (líneas previas a los apartados, apartados)."""
        preambulo: list[str] = []
        secciones: list[tuple[str, str]] = []
        for linea in texto.strip().split('\n'):
            limpio = linea.upper().lstrip('*#- ').strip()
            nombre = next(
                (
                    apartado
                    for apartado in APARTADOS_REQUERIDOS
                    if limpio.startswith(f'{apartado}:')
                ),
                None,
            )
            if nombre is not None:
                indice = linea.upper().find(f'{nombre}:')
                cuerpo = _SIN_NEGRITA_SUELTA.sub('', linea[indice + len(nombre) + 1 :]).strip()
                secciones.append((nombre, cuerpo))
            elif secciones:
                nombre_previo, cuerpo_previo = secciones[-1]
                # Las viñetas del modelo se conservan en líneas separadas.
                linea_limpia = _SIN_NEGRITA_SUELTA.sub('', linea.strip())
                separador = '\n' if linea_limpia.startswith(('-', '*')) else ' '
                secciones[-1] = (
                    nombre_previo,
                    f'{cuerpo_previo}{separador}{linea_limpia}'.strip(),
                )
            else:
                preambulo.append(linea.rstrip())
        return [linea for linea in preambulo if linea], secciones

    @staticmethod
    def _sin_apartados(texto: str) -> str:
        """Quita los encabezados REQUISITOS:/COSTO:/… (consultas generales)."""
        lineas: list[str] = []
        for linea in (texto or '').split('\n'):
            limpio = linea.upper().lstrip('*#- ').strip()
            for apartado in APARTADOS_REQUERIDOS:
                prefijo = f'{apartado.upper()}:'
                if limpio.startswith(prefijo):
                    indice = linea.upper().find(prefijo)
                    linea = linea[indice + len(prefijo) :].strip()
                    break
            lineas.append(linea)
        return '\n'.join(lineas)

    @staticmethod
    def _acortar(texto: str, limite: int) -> str:
        """Recorta `texto` a `limite` caracteres cortando en límite de oración."""
        texto = (texto or '').strip()
        if len(texto) <= limite:
            return texto
        corte = texto[:limite]
        finales = max(corte.rfind('. '), corte.rfind('; '), corte.rfind(', '))
        if finales > limite // 2:
            corte = corte[:finales + 1]
        else:
            corte = corte.rstrip()
            if corte and corte[-1] not in '.…':
                corte += '…'
        return corte.strip()

    def garantizar_estructura(self, texto: str, contexto: list[Documento]) -> str:
        """Completa los apartados que el modelo no redactó, usando el contexto.

        Los valores se toman de los documentos de la base documental (nunca se
        inventan): si el contexto no aporta el dato se escribe `SIN_DATO`. El
        texto del modelo se conserva como preámbulo (p. ej. pasos numerados)
        o dentro de OBSERVACIONES, sin duplicarlo en varios apartados.
        """
        faltantes = [
            apartado
            for apartado in APARTADOS_REQUERIDOS
            if self._linea_apartado(texto, apartado) is None
        ]
        if not faltantes:
            return texto

        preambulo, secciones = self._separar_secciones(texto)
        lineas: list[str] = []
        if preambulo and secciones:
            lineas.extend(preambulo)
            lineas.append('')
        for nombre, cuerpo in secciones:
            lineas.append(f'{nombre}: {cuerpo}')
        for apartado in faltantes:
            if apartado == 'OBSERVACIONES':
                # Sin apartados del modelo, su texto se conserva aquí; si ya
                # había secciones, solo el preámbulo sobrante va a observaciones.
                if not secciones:
                    cuerpo = texto.strip()
                elif preambulo:
                    cuerpo = ' '.join(preambulo).strip()
                else:
                    cuerpo = ''
                lineas.append(f'OBSERVACIONES: {cuerpo or SIN_DATO}')
            else:
                lineas.append(f'{apartado}: {self._contenido_apartado(apartado, contexto)}')
        return '\n'.join(lineas)

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