"""Servicio de aplicación: ServicioChunking.

Divide el contenido de un documento en fragmentos con solape (HU-04 / G-13).
Estrategia: primero por párrafos, luego por oraciones para párrafos largos, y
finalmente se agrupan hasta `tamano_fragmento` caracteres conservando `solape`
caracteres del fragmento anterior para no partir frases en los bordes.
"""

from __future__ import annotations

import re

# Separadores para estimar "oraciones" sin depender de NLTK.
_PATRON_ORACION = re.compile(r'(?<=[.!?;:])\s+')
_ESPACIOS = re.compile(r'\s+')


class ServicioChunking:
    def __init__(self, tamano_fragmento: int = 800, solape: int = 120) -> None:
        if tamano_fragmento <= 0 or solape < 0 or solape >= tamano_fragmento:
            raise ValueError('tamano_fragmento > 0 y 0 <= solape < tamano_fragmento')
        self._tamano_fragmento = tamano_fragmento
        self._solape = solape

    def dividir(self, texto: str) -> list[str]:
        """Divide el texto en fragmentos de tamaño acotado con solape."""
        texto = _ESPACIOS.sub(' ', texto).strip()
        if not texto:
            return []

        unidades = self._dividir_en_unidades(texto)
        return self._agrupar(unidades)

    def _dividir_en_unidades(self, texto: str) -> list[str]:
        """Convierte el texto en una lista de unidades cortas (párrafos/oraciones)."""
        unidades: list[str] = []
        for parrafo in re.split(r'\n{2,}', texto):
            parrafo = parrafo.strip()
            if not parrafo:
                continue
            if len(parrafo) <= self._tamano_fragmento:
                unidades.append(parrafo)
                continue
            # Párrafo largo: se corta por oraciones.
            for oracion in _PATRON_ORACION.split(parrafo):
                oracion = oracion.strip()
                if oracion:
                    unidades.append(oracion)
        return unidades

    def _agrupar(self, unidades: list[str]) -> list[str]:
        """Agrupa las unidades en fragmentos de tamaño máximo con solape."""
        fragmentos: list[str] = []
        actual = ''

        for unidad in unidades:
            if not actual:
                actual = unidad
                continue

            if len(actual) + len(unidad) + 1 <= self._tamano_fragmento:
                actual = f'{actual} {unidad}'
            else:
                fragmentos.append(actual)
                # Solape: reutiliza el final del fragmento anterior para no
                # perder contexto entre cortes.
                cola = actual[-self._solape:] if self._solape > 0 else ''
                actual = f'{cola} {unidad}'.strip()

        if actual:
            fragmentos.append(actual)
        return fragmentos