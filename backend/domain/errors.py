"""Errores de dominio del módulo documental (PMV2).

Se definen aquí para que la capa de aplicación y los adaptadores compartan un
vocabulario de error que no dependa de la infraestructura (FastAPI, disco, etc.).
"""


class DomainError(Exception):
    """Error base de la capa de dominio."""


class DocumentoInvalidoError(DomainError):
    """El documento no cumple las reglas de negocio (p. ej. metadatos)."""


class FormatoNoSoportadoError(DocumentoInvalidoError):
    """La extensión o el tipo MIME del archivo no está permitido."""


class DocumentoIlegibleError(DomainError):
    """No se pudo extraer texto del archivo (p. ej. PDF escaneado sin OCR)."""
