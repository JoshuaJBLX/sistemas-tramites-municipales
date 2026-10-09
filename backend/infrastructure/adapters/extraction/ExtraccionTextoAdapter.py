"""Adaptador de extracción de texto plano (HU-04, HU-01).

Admite PDF, DOCX, TXT y Markdown. Para PDFs intenta extraer texto; si no hay
texto recuperable (PDF escaneado), levanta `DocumentoIlegibleError`.
"""

from __future__ import annotations

import asyncio
from io import BytesIO

from domain.errors import DocumentoIlegibleError, FormatoNoSoportadoError
from domain.ports.ExtraccionTextoPort import ExtraccionTextoPort
from domain.value_objects.FormatoDocumento import (
    FORMATOS_PERMITIDOS,
    extension_de,
)

try:
    import pypdf
except Exception:  # pragma: no cover - dependencia opcional en entornos extraños
    pypdf = None

try:
    from docx import Document as DocxDocument
except Exception:  # pragma: no cover
    DocxDocument = None


class ExtraccionTextoAdapter(ExtraccionTextoPort):
    """Extrae texto de archivos oficiales municipales."""

    def soporta(self, nombre_archivo: str) -> bool:
        return extension_de(nombre_archivo) in FORMATOS_PERMITIDOS

    async def extraer(self, nombre_archivo: str, contenido: bytes) -> str:
        return await asyncio.to_thread(self._extraer_sincrono, nombre_archivo, contenido)

    def _extraer_sincrono(self, nombre_archivo: str, contenido: bytes) -> str:
        ext = extension_de(nombre_archivo)
        if ext not in FORMATOS_PERMITIDOS:
            raise FormatoNoSoportadoError(f'Formato no soportado: {ext}')

        if ext == '.pdf':
            return self._extraer_pdf(contenido)
        if ext == '.docx':
            return self._extraer_docx(contenido)
        if ext in ('.txt', '.md'):
            return self._extraer_texto(contenido)
        raise FormatoNoSoportadoError(f'Formato no soportado: {ext}')

    def _extraer_pdf(self, contenido: bytes) -> str:
        if pypdf is None:
            # Fallback conservador: impide cargar un PDF sin poder extraer texto
            raise DocumentoIlegibleError(
                'No se puede extraer texto de PDF (dependencia pypdf no disponible).'
            )
        lector = pypdf.PdfReader(BytesIO(contenido))
        partes: list[str] = []
        for pagina in lector.pages:
            try:
                texto_pagina = pagina.extract_text() or ''
            except Exception:
                texto_pagina = ''
            partes.append(texto_pagina)
        texto = '\n'.join(partes).strip()
        if len(texto) < 50:
            raise DocumentoIlegibleError(
                'El archivo PDF no contiene texto recuperable (posible escaneado '
                'sin capa OCR).'
            )
        return texto

    def _extraer_docx(self, contenido: bytes) -> str:
        if DocxDocument is None:
            raise DocumentoIlegibleError(
                'No se puede extraer texto de DOCX (dependencia python-docx '
                'no disponible).'
            )
        doc = DocxDocument(BytesIO(contenido))
        textos = [p.text for p in doc.paragraphs]
        texto = '\n'.join(textos).strip()
        if len(texto) < 5:
            raise DocumentoIlegibleError(
                'El archivo DOCX no contiene texto recuperable.'
            )
        return texto

    def _extraer_texto(self, contenido: bytes) -> str:
        # UTF-8 con fallbacks comunes.
        for encoding in ('utf-8', 'latin-1', 'cp1252', 'iso-8859-15'):
            try:
                return contenido.decode(encoding)
            except UnicodeError:
                continue
        return contenido.decode('utf-8', errors='replace')

    def formatos_soportados(self) -> list[str]:
        return sorted(FORMATOS_PERMITIDOS.keys())