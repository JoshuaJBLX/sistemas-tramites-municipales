"""Adaptador de extracción de texto plano (HU-04, HU-01).

Admite PDF, DOCX, TXT y Markdown. Para PDFs intenta extraer texto con `pypdf`;
si no hay texto recuperable (PDF escaneado) **rasteriza las páginas con PyMuPDF
y aplica OCR con RapidOCR**, de modo que un documento escaneado también se
indexa (HU-04 / P2-13). Solo si el OCR tampoco devuelve texto se levanta
`DocumentoIlegibleError`.
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

try:
    import fitz  # PyMuPDF: rasteriza PDF escaneados sin binarios externos
except Exception:  # pragma: no cover
    fitz = None

try:
    from rapidocr import RapidOCR
except Exception:  # pragma: no cover
    RapidOCR = None

# Umbral: menos de 50 caracteres extraídos se considera PDF sin capa de texto.
_UMBRAL_TEXTO = 50
_DPI_OCR = 200

# Motor OCR perezoso y reutilizable (cargarlo cuesta ~1 s y modelos ~30 MB).
_motor_ocr = None


def _obtener_motor_ocr():
    global _motor_ocr
    if _motor_ocr is None and RapidOCR is not None:
        _motor_ocr = RapidOCR()
    return _motor_ocr


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
        texto = self._texto_capa_pdf(contenido)
        if len(texto) >= _UMBRAL_TEXTO:
            return texto

        # PDF sin capa de texto (escaneado): OCR sobre las páginas rasterizadas.
        texto_ocr = self._texto_con_ocr(contenido)
        if texto_ocr:
            return texto_ocr

        if pypdf is None:
            raise DocumentoIlegibleError(
                'No se puede extraer texto de PDF (dependencia pypdf no disponible).'
            )
        raise DocumentoIlegibleError(
            'El archivo PDF no contiene texto recuperable: es un escaneado sin '
            'capa de texto y el OCR no encontró contenido legible.'
        )

    @staticmethod
    def _texto_capa_pdf(contenido: bytes) -> str:
        """Texto nativo del PDF (capa seleccionable); '' si no la tiene."""
        if pypdf is None:
            return ''
        lector = pypdf.PdfReader(BytesIO(contenido))
        partes: list[str] = []
        for pagina in lector.pages:
            try:
                partes.append(pagina.extract_text() or '')
            except Exception:
                partes.append('')
        return '\n'.join(partes).strip()

    @staticmethod
    def _texto_con_ocr(contenido: bytes, limite_paginas: int = 20) -> str:
        """Rasteriza cada página con PyMuPDF y reconoce el texto con RapidOCR.

        Devuelve '' cuando el OCR no está disponible o no hay nada legible, para
        que el llamador decida el mensaje de error (HU-04 / P2-13).
        """
        if fitz is None or RapidOCR is None:
            return ''
        motor = _obtener_motor_ocr()
        if motor is None:
            return ''

        reconocido: list[str] = []
        with fitz.open(stream=contenido, filetype='pdf') as documento:
            for indice, pagina in enumerate(documento):
                if indice >= limite_paginas:
                    break
                pixmap = pagina.get_pixmap(dpi=_DPI_OCR)
                imagen = pixmap.tobytes('png')
                resultado = motor(imagen)
                if resultado is None:
                    continue
                lineas = getattr(resultado, 'txts', None) or ()
                if lineas:
                    reconocido.append('\n'.join(lineas))
        return '\n'.join(reconocido).strip()

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