"""Servicio de aplicación: ServicioNLP."""

import re
import unicodedata

from domain.value_objects.ClasificacionIntencion import ClasificacionIntencion
from domain.value_objects.IntencionConsulta import IntencionConsulta

# Patrones léxicos para clasificación de intención (HU-06).
# Se usan raíces, no palabras completas, para tolerar conjugaciones y plurales
# ("requisito", "requisitos", "requisite", "necesito", "necesitar").
_PATRONES_INTENCION: dict[IntencionConsulta, tuple[str, ...]] = {
    IntencionConsulta.CONSULTAR_REQUISITOS: (
        'requisit',
        'necesit',
        'que debo llevar',
        'que debo presentar',
        'document',
        'papel',
        'carne',
    ),
    IntencionConsulta.CONSULTAR_COSTO: (
        'cost',
        'cuesta',
        'precio',
        'pago',
        'pagare',
        'tarifa',
        'arancel',
        'tasa',
    ),
    IntencionConsulta.CONSULTAR_PLAZO: (
        'plazo',
        'cuanto tiempo',
        'cuantos dias',
        'dias habiles',
        'cuanto demora',
        'tiempo de atencion',
    ),
    IntencionConsulta.CONSULTAR_PASOS: (
        'paso',
        'como hago',
        'como solicito',
        'como se tramita',
        'procedimiento',
        'como obtengo',
    ),
    IntencionConsulta.CONSULTAR_AREA: (
        'area',
        'oficina',
        'a quien me dirijo',
        'que unidad',
        'que entidad',
    ),
    IntencionConsulta.CONSULTAR_ESTADO: (
        'estado',
        'avance',
        'seguimiento',
        'en que va',
        'expediente',
    ),
    IntencionConsulta.CONSULTAR_UBICACION: (
        'donde',
        'ubicacion',
        'direccion',
        'horario',
        'en que lugar',
    ),
    IntencionConsulta.SALUDO: (
        'hola',
        'buenos dias',
        'buenas tardes',
        'buenas noches',
    ),
}

# Peso base de una intención detectada y bonificación por cada patrón adicional.
_CONFIANZA_BASE = 0.55
_CONFIANZA_POR_PATRON = 0.15
_UMBRAL_EMPATE = 0.75

# Palabras funcionales del español: si una consulta no contiene ninguna y
# tampoco coincide con un patrón de intención, se considera sin sentido.
_PALABRAS_COMUNES = frozenset({
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'en',
    'que', 'para', 'con', 'por', 'y', 'o', 'a', 'al', 'mi', 'tu', 'su', 'me',
    'te', 'se', 'nos', 'como', 'cuanto', 'cuanta', 'cuantos', 'cuantas',
    'cuesta', 'cuestan', 'donde', 'cuando', 'quien', 'cual', 'cuales', 'este',
    'esta', 'esto', 'ese', 'esa', 'eso', 'hay', 'tengo', 'necesito', 'necesita',
    'quiero', 'puedo', 'debo', 'es', 'son', 'ser', 'estan', 'fue', 'sin',
    'sobre', 'entre', 'tambien', 'solo', 'ya', 'no', 'si', 'hay', 'hay',
})


class ServicioNLP:
    """Clasificación de intención y normalización de texto de las consultas."""

    async def clasificar_intencion(self, pregunta: str) -> IntencionConsulta:
        """Clasifica la intención (compatibilidad con el uso previo)."""
        return (await self.clasificar(pregunta)).intencion

    async def clasificar(self, pregunta: str) -> ClasificacionIntencion:
        """Clasifica la intención con su confianza y detecta ambigüedad.

        Gana la intención con más patrones coincidentes; ante empate gana la de
        patrón más específico ("cuanto cuesta" sobre "pago"). Si ninguna
        intención coincide, o si dos son indistinguibles, se marca como pendiente
        de aclaración del ciudadano (HU-05, HU-06).
        """
        texto = self._normalizar(pregunta)

        # Pregunta sin sentido: texto vacío, demasiado corto, sin vocales o
        # sin ninguna palabra reconocible (evita consultar el RAG con ruido).
        if self._sin_sentido(texto):
            return ClasificacionIntencion.con_sin_sentido()

        # (intención, patrones coincidentes, peso de especificidad)
        candidatos = [
            (intencion, [p for p in patrones if p in texto])
            for intencion, patrones in _PATRONES_INTENCION.items()
        ]
        candidatos = [c for c in candidatos if c[1]]

        if not candidatos:
            # Sin intención clara: si tampoco contiene palabras comunes del
            # español, se considera que la consulta no tiene sentido.
            if self._sin_palabras_reconocibles(texto):
                return ClasificacionIntencion.con_sin_sentido()
            return ClasificacionIntencion.sin_patron()

        mejor = max(candidatos, key=lambda c: (len(c[1]), sum(map(len, c[1]))))
        peso_ganador = (len(mejor[1]), sum(map(len, mejor[1])))
        empata = any(
            intencion is not mejor[0] and (len(matches), sum(map(len, matches))) == peso_ganador
            for intencion, matches in candidatos
        )

        confianza = min(1.0, _CONFIANZA_BASE + _CONFIANZA_POR_PATRON * (len(mejor[1]) - 1))
        if empata:
            confianza = min(confianza, _UMBRAL_EMPATE - 0.05)

        return ClasificacionIntencion(mejor[0], round(confianza, 2), empata)

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Pasa el texto a minúsculas y elimina tildes y signos de puntuación."""
        sin_tildes = ''.join(
            caracter
            for caracter in unicodedata.normalize('NFD', texto.lower())
            if unicodedata.category(caracter) != 'Mn'
        )
        return re.sub(r'[^\w\s]', ' ', sin_tildes).strip()

    @staticmethod
    def _sin_sentido(texto: str) -> bool:
        """Detecta una consulta sin sentido (vacía, muy corta o sin palabras).

        Criterios: menos de 2 caracteres; menos de 2 letras; ninguna vocal;
        o una sola palabra repetida (p. ej. ``aaaa``). No marca como sin
        sentido una consulta corta pero válida como ``hola`` o ``que cuesta``.
        """
        limpio = texto.strip()
        if len(limpio) < 2:
            return True
        letras = [c for c in limpio if c.isalpha()]
        if len(letras) < 2:
            return True
        if not any(c in 'aeiou' for c in limpio):
            return True
        palabras = limpio.split()
        if len(palabras) == 1 and len(set(palabras[0])) == 1:
            return True
        return False

    @staticmethod
    def _sin_palabras_reconocibles(texto: str) -> bool:
        """Indica si la consulta no contiene ninguna palabra común del español."""
        return not any(palabra in _PALABRAS_COMUNES for palabra in texto.split())
