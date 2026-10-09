"""Caso de uso: CargarDocumento.

Orquesta la carga documental de extremo a extremo (HU-01):
1. Valida que la extensión del archivo sea un formato permitido (D-7).
2. Extrae el texto plano del archivo (PDF/DOCX/TXT/MD) (HU-01/HU-04).
3. Almacena el archivo original con un nombre seguro.
4. Registra el documento con metadatos (HU-02) y lo indexa vectorialmente.
5. Procesa fragmentos si el texto lo permite (HU-04).
"""

from __future__ import annotations

import hashlib
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from application.use_cases.GestionarDocumentos import GestionarDocumentos
from application.use_cases.ProcesarDocumento import ProcesarDocumento
from domain.entities.Documento import Documento
from domain.errors import DocumentoIlegibleError, FormatoNoSoportadoError
from domain.ports.AlmacenamientoDocumentosPort import AlmacenamientoDocumentosPort
from domain.ports.ExtraccionTextoPort import ExtraccionTextoPort
from domain.value_objects.EstadoDocumento import EstadoDocumento
from domain.value_objects.FormatoDocumento import formatos_legibles, mime_para


class CargarDocumento:
    def __init__(
        self,
        almacenamiento: AlmacenamientoDocumentosPort,
        extraccion: ExtraccionTextoPort,
        gestionar_documentos: GestionarDocumentos,
        procesar_documento: ProcesarDocumento,
    ) -> None:
        self._almacenamiento = almacenamiento
        self._extraccion = extraccion
        self._gestionar_documentos = gestionar_documentos
        self._procesar_documento = procesar_documento

    async def ejecutar(
        self,
        *,
        tramite_id: UUID,
        titulo: str,
        url_origen: str,
        version: str,
        fecha_publicacion: date | None,
        estado: EstadoDocumento,
        nombre_archivo: str,
        contenido: bytes,
    ) -> Documento:
        if not self._extraccion.soporta(nombre_archivo):
            raise FormatoNoSoportadoError(
                f'Formato no soportado. Extensiones permitidas: {formatos_legibles()}.'
            )

        texto = await self._extraccion.extraer(nombre_archivo, contenido)
        if not texto.strip():
            raise DocumentoIlegibleError(
                'El archivo no contiene texto recuperable. Si es un PDF escaneado, '
                'requiere OCR o revisión manual.'
            )

        # Nombre de almacenamiento seguro y único (se conserva la extensión).
        nombre_guardado = self._almacenamiento.guardar(nombre_archivo, contenido)

        documento = Documento(
            id=uuid4(),
            tramite_id=tramite_id,
            titulo=titulo.strip(),
            contenido=texto,
            url_origen=url_origen.strip(),
            estado=estado,
            version=version or '1.0',
            fecha_publicacion=fecha_publicacion,
            archivo_nombre=nombre_guardado,
            mime_type=mime_para(nombre_archivo),
            hash_contenido=hashlib.sha256(contenido).hexdigest(),
            actualizado_en=datetime.now(timezone.utc),
        )

        guardado = await self._gestionar_documentos.registrar(documento)

        # La fragmentación nunca debe tumbar el alta: si falla, el documento
        # queda indexado completo y se puede reprocesar después (endpoint dedicado).
        try:
            await self._procesar_documento.ejecutar(guardado.id)
        except Exception:  # noqa: BLE001 - el alta es lo importante (HU-01)
            pass

        return await self._gestionar_documentos.obtener(guardado.id)