"""Servicio de aplicación: ServicioNLP."""

import re
import unicodedata

from domain.value_objects.IntencionConsulta import IntencionConsulta

# Patrones léxicos simples para clasificación de intención.
_PATRONES_INTENCION: dict[IntencionConsulta, tuple[str, ...]] = {
    IntencionConsulta.CONSULTAR_REQUISITOS: (
        'requisito',
        'necesito',
        'documento',
        'papeles',
        'que debo presentar',
    ),
    IntencionConsulta.CONSULTAR_COSTO: (
        'costo',
        'cuanto cuesta',
        'precio',
        'pago',
        'tarifa',
        'tasa',
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
        'oficina',
        'horario',
    ),
    IntencionConsulta.SALUDO: ('hola', 'buenos dias', 'buenas tardes', 'buenas noches'),
}


class ServicioNLP:
    """Clasificación de intención y normalización de texto de las consultas."""

    async def clasificar_intencion(self, pregunta: str) -> IntencionConsulta:
        texto = self._normalizar(pregunta)

        for intencion, patrones in _PATRONES_INTENCION.items():
            if any(patron in texto for patron in patrones):
                return intencion

        return IntencionConsulta.OTRO

    @staticmethod
    def _normalizar(texto: str) -> str:
        """Pasa el texto a minúsculas y elimina tildes y signos de puntuación."""
        sin_tildes = ''.join(
            caracter
            for caracter in unicodedata.normalize('NFD', texto.lower())
            if unicodedata.category(caracter) != 'Mn'
        )
        return re.sub(r'[^\w\s]', ' ', sin_tildes).strip()