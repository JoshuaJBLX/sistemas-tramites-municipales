"""Value Object: EstadoDocumento."""

from enum import Enum


class EstadoDocumento(str, Enum):
    VIGENTE = 'vigente'
    OBSOLETO = 'obsoleto'
    EN_REVISION = 'en_revision'
