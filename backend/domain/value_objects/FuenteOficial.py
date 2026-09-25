"""Value Object: FuenteOficial."""

from enum import Enum


class FuenteOficial(str, Enum):
    PORTAL_MUNICIPAL = 'portal_municipal'
    NORMATIVA_LEGAL = 'normativa_legal'
    TUPA = 'tupa'
    DOCUMENTO_INTERNO = 'documento_interno'
