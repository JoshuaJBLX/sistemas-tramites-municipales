"""Value Object: NivelConfianza."""

from enum import Enum


class NivelConfianza(str, Enum):
    ALTA = 'alta'
    MEDIA = 'media'
    BAJA = 'baja'
