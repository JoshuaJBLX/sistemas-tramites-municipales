"""Value Object: FormatoDocumento.

Catálogo de formatos admitidos para la carga documental (HU-01) y su relación
extensión ↔ tipo MIME. `upload` rechaza cualquier otra extensión (D-7).
"""

from __future__ import annotations

import os

# extensión (minúsculas) -> tipo MIME oficial.
FORMATOS_PERMITIDOS: dict[str, str] = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.txt': 'text/plain',
    '.md': 'text/markdown',
}

EXTENSIONES_PERMITIDAS: frozenset[str] = frozenset(FORMATOS_PERMITIDOS)
MIME_PERMITIDOS: frozenset[str] = frozenset(FORMATOS_PERMITIDOS.values())


def extension_de(nombre_archivo: str | None) -> str:
    """Devuelve la extensión en minúsculas de un nombre de archivo."""
    if not nombre_archivo:
        return ''
    return os.path.splitext(nombre_archivo)[1].lower()


def es_formato_permitido(nombre_archivo: str | None) -> bool:
    return extension_de(nombre_archivo) in EXTENSIONES_PERMITIDAS


def mime_para(nombre_archivo: str | None) -> str | None:
    """Devuelve el MIME esperado para una extensión permitida (o None)."""
    return FORMATOS_PERMITIDOS.get(extension_de(nombre_archivo))


def formatos_legibles() -> str:
    """Lista legible de extensiones permitidas para mensajes de error."""
    return ', '.join(sorted(EXTENSIONES_PERMITIDAS))