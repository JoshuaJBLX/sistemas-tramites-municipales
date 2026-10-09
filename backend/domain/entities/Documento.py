"""Entidad de dominio: Documento.

Representa un documento oficial municipal (TUPA, ordenanza, reglamento,
procedimiento). En PMV2 la entidad incorpora los metadatos de HU-02
(version, fecha_publicacion, fuente), HU-03 (derogación/baja lógica) y
HU-04 (fragmentación para el índice vectorial).
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID

from domain.value_objects.EstadoDocumento import EstadoDocumento

_DEFAULT_VERSION = '1.0'


@dataclass
class Documento:
    id: UUID
    tramite_id: UUID
    titulo: str
    contenido: str
    url_origen: str
    estado: EstadoDocumento
    # --- Metadatos documentales (HU-02) ---
    version: str = _DEFAULT_VERSION
    fecha_publicacion: date | None = None
    # --- Carga documental (HU-01 / G-12) ---
    archivo_nombre: str | None = None
    mime_type: str | None = None
    hash_contenido: str | None = None
    # --- Procesamiento RAG (HU-04 / G-13) ---
    fragmentado: bool = False
    fragmento_destacado: str | None = None
    # --- Baja lógica (HU-03) ---
    eliminado_en: datetime | None = None
    # --- Internos técnicos ---
    embedding: list[float] | None = None
    actualizado_en: datetime | None = None
    indexado: bool = False
    puntuacion_similitud: float = 0.0

    def esta_vigente(self) -> bool:
        """Un documento solo participa en respuestas si está vigente y activo."""
        return (
            self.estado == EstadoDocumento.VIGENTE
            and self.eliminado_en is None
        )

    def esta_eliminado(self) -> bool:
        return self.eliminado_en is not None

    def esta_publicable(self) -> bool:
        """HU-02: publicación exige versión, fecha de emisión y fuente oficial."""
        return bool(self.version.strip()) and self.fecha_publicacion is not None and bool(
            self.url_origen.strip()
        )

    def requiere_metadatos(self) -> str | None:
        """Devuelve qué metadatos faltan para publicar, o None si están listos."""
        faltantes: list[str] = []
        if not self.version.strip():
            faltantes.append('version')
        if self.fecha_publicacion is None:
            faltantes.append('fecha_publicacion')
        if not self.url_origen.strip():
            faltantes.append('url_origen')
        return ', '.join(faltantes) if faltantes else None