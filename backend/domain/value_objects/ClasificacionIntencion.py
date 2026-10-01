"""Value Object: ClasificacionIntencion.

Resultado de clasificar la intención de una consulta: no solo qué intención se
detectó, sino con cuánta confianza y si el resultado es lo bastante claro como
para responder o si conviene pedir aclaración al ciudadano (HU-05, HU-06).
"""

from dataclasses import dataclass

from domain.value_objects.IntencionConsulta import IntencionConsulta

# Confianza mínima para responder sin pedir aclaración.
CONFIANZA_MINIMA = 0.5


@dataclass
class ClasificacionIntencion:
    intencion: IntencionConsulta
    confianza: float
    empata: bool = False

    @property
    def requiere_aclaracion(self) -> bool:
        """Indica si la pregunta es demasiado ambigua para responderla."""
        return (
            self.intencion == IntencionConsulta.OTRO
            or self.empata
            or self.confianza < CONFIANZA_MINIMA
        )

    @classmethod
    def sin_patron(cls, empata: bool = False) -> 'ClasificacionIntencion':
        return cls(intencion=IntencionConsulta.OTRO, confianza=0.0, empata=empata)