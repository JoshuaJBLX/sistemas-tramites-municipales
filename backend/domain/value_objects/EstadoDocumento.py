"""Value Object: EstadoDocumento."""

from enum import Enum


class EstadoDocumento(str, Enum):
    VIGENTE = 'vigente'
    OBSOLETO = 'obsoleto'
    EN_REVISION = 'en_revision'
    # HU-03: un documento derogado se conserva para auditoría pero deja de
    # utilizarse en las respuestas nuevas (mismo efecto que 'obsoleto', con
    # semántica normativa explícita).
    DEROGADO = 'derogado'
