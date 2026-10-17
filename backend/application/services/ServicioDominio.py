"""Servicio de aplicación: ServicioDominio (HU-11).

Distingue consultas del dominio municipal de consultas que pertenecen a otra
entidad (SUNAT, RENIEC, AFP/ONP, EsSalud, PNP, SUNARP, Migraciones…). La
detección es léxica y conservadora: si la pregunta también contiene un ancla
municipal clara (predial, TUPA, licencia de funcionamiento…), se mantiene el
flujo municipal.
"""

import re
import unicodedata
from dataclasses import dataclass

MOTIVO_BASE = (
    'Este asistente solo orienta sobre trámites y servicios de la municipalidad.'
)

# (patrones normalizados, nombre de la entidad sugerida, URL oficial).
_ENTIDADES_EXTERNAS: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (
        ('sunat',),
        'el Servicio de Impuestos Nacionales (SUNAT)',
        'https://www.sunat.gob.pe',
    ),
    (
        ('reniec', 'partida de nacimiento', 'certificado de nacimiento'),
        'el Registro Nacional de Identificación y Estado Civil (RENIEC)',
        'https://www.reniec.gob.pe',
    ),
    (
        ('afp', 'onp', 'pension', 'jubilacion', 'sbs'),
        'el Sistema de Pensiones (tu AFP u ONP, supervisado por la SBS)',
        'https://www.sbs.gob.pe',
    ),
    (
        ('essalud', 'minsa', 'ministerio de salud'),
        'EsSalud / el Ministerio de Salud',
        'https://www.gob.pe/essalud',
    ),
    (
        ('sunarp', 'registro de propiedad', 'escritura publica'),
        'la Superintendencia Nacional de los Registros Públicos (SUNARP)',
        'https://www.sunarp.gob.pe',
    ),
    (
        ('pnp', 'comisaria', 'policia nacional'),
        'la Policía Nacional del Perú',
        'https://www.pnp.gob.pe',
    ),
    (
        ('pasaporte', 'migraciones'),
        'la Dirección General de Migraciones',
        'https://www.migraciones.gob.pe',
    ),
    (
        ('indecopi',),
        'la Comisión de Protección al Consumidor (INDECOPI)',
        'https://www.indecopi.gob.pe',
    ),
    (
        ('poder judicial', 'fiscalia', 'ministerio publico', 'juzgado'),
        'el Poder Judicial / Ministerio Público',
        'https://www.pj.gob.pe',
    ),
    (
        ('sutran', 'interprovincial', 'mtc'),
        'el Ministerio de Transportes y Comunicaciones (MTC/SUTRAN)',
        'https://www.gob.pe/mtc',
    ),
)

# Anclas del dominio municipal: si aparecen junto a una entidad externa, la
# consulta sigue siendo municipal ("pago del impuesto predial: ¿SUNAT?").
_ANCLAS_MUNICIPALES: tuple[str, ...] = (
    'municipalidad',
    'muni',
    'tupa',
    'predial',
    'bando',
    'serenazgo',
    'zonificacion',
    'permiso de obra',
    'licencia de funcionamiento',
    'contribucion',
    'paradero',
    'mercado municipal',
    'desague',
    'agua potable',
    'habilitacion urbana',
    'codigo de edificacion',
    'inspeccion de seguridad',
    'certificado de zonificacion',
)

# Patrones cortos que pueden aparecer como palabra suelta (no como subcadena).
_PATRONES_CORTOS = {'afp', 'onp', 'pnp', 'sbs', 'mtc'}


@dataclass
class EvaluacionDominio:
    fuera_de_dominio: bool
    entidad_sugerida: str = ''
    entidad_url: str = ''
    motivo: str = ''


class ServicioDominio:
    """Clasificador de dominio municipal vs. externo (HU-11)."""

    def evaluar(self, pregunta: str) -> EvaluacionDominio:
        texto = self._normalizar(pregunta)
        if not texto:
            return EvaluacionDominio(False)

        entidad = self._entidad_externa(texto)
        if entidad is None:
            return EvaluacionDominio(False)

        if any(ancla in texto for ancla in _ANCLAS_MUNICIPALES):
            return EvaluacionDominio(False)

        nombre, url = entidad
        return EvaluacionDominio(
            fuera_de_dominio=True,
            entidad_sugerida=nombre,
            entidad_url=url,
            motivo=MOTIVO_BASE,
        )

    @classmethod
    def _entidad_externa(cls, texto: str) -> tuple[str, str] | None:
        for patrones, nombre, url in _ENTIDADES_EXTERNAS:
            for patron in patrones:
                if cls._coincide(texto, patron):
                    return nombre, url
        return None

    @staticmethod
    def _coincide(texto: str, patron: str) -> bool:
        if patron in _PATRONES_CORTOS or len(patron) <= 4:
            return re.search(rf'\b{re.escape(patron)}\b', texto) is not None
        return patron in texto

    @staticmethod
    def _normalizar(texto: str) -> str:
        sin_tildes = ''.join(
            caracter
            for caracter in unicodedata.normalize('NFD', texto.lower())
            if unicodedata.category(caracter) != 'Mn'
        )
        return re.sub(r'[^\w\s]', ' ', sin_tildes).strip()
