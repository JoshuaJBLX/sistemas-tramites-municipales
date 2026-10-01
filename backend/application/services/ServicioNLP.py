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

        # (intención, patrones coincidentes, peso de especificidad)
        candidatos = [
            (intencion, [p for p in patrones if p in texto])
            for intencion, patrones in _PATRONES_INTENCION.items()
        ]
        candidatos = [c for c in candidatos if c[1]]

        if not candidatos:
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
