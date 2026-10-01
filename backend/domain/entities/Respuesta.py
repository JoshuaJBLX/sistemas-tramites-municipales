"""Entidad de dominio: Respuesta."""

from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.Fuente import Fuente
from domain.value_objects.NivelConfianza import NivelConfianza
from domain.value_objects.TramiteProbable import TramiteProbable


@dataclass
class Respuesta:
    id: UUID
    consulta_id: UUID
    texto: str
    confianza: NivelConfianza
    fuentes: list[Fuente] = field(default_factory=list)
    groundedness: float = 0.0
    confianza_intencion: float = 0.0
    pide_aclaracion: bool = False
    tramite_probable: TramiteProbable | None = None

    def es_confiable(self) -> bool:
        return self.confianza in (NivelConfianza.ALTA, NivelConfianza.MEDIA)

    def con_datos_estructurados(self) -> str:
        """Agrega al texto los datos verificados del trámite del catálogo.

        La respuesta del SLM puede reformular los datos; los requisitos, el arancel y el plazo se
        toman textualmente de la base de datos para que el ciudadano reciba datos verificables y
        no redactados por el modelo (HU-07).
        """
        if self.tramite_probable is None:
            return self.texto

        partes = [self.texto.rstrip()]

        requisitos = self.tramite_probable.resumen_requisitos()
        if requisitos:
            lista = '\n'.join(f'  {indice}. {valor}' for indice, valor in enumerate(requisitos, 1))
            partes.append(
                'Requisitos registrados en el catálogo oficial de la municipalidad:\n'
                f'{lista}'
            )

        detalles = []
        if self.tramite_probable.costo > 0:
            detalles.append(
                f'arancel S/ {self.tramite_probable.costo:.2f} según el catálogo'
            )
        if self.tramite_probable.duracion_estimada_dias > 0:
            detalles.append(
                f'plazo estimado de {self.tramite_probable.duracion_estimada_dias} días hábiles'
            )
        if detalles:
            partes.append('Datos del catálogo: ' + '; '.join(detalles) + '.')

        if self.tramite_probable.fuente_url:
            partes.append(f'Ficha del trámite: {self.tramite_probable.fuente_url}')

        return '\n\n'.join(partes)