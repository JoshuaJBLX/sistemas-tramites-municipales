"""Adaptador: DocumentStorageAdapter implementa AlmacenamientoDocumentosPort."""

import os
from pathlib import Path
from uuid import uuid4

from domain.ports.AlmacenamientoDocumentosPort import AlmacenamientoDocumentosPort
from domain.value_objects.FormatoDocumento import extension_de


class DocumentStorageAdapter(AlmacenamientoDocumentosPort):
    """Guarda archivos originales con nombre seguro en el sistema de archivos."""

    def __init__(self, directorio_base: str | None = None) -> None:
        self._directorio_base = Path(
            directorio_base or os.getenv('DOCUMENTS_PATH', './storage/documentos')
        )

    def guardar(self, nombre_archivo: str, contenido: bytes) -> str:
        self._directorio_base.mkdir(parents=True, exist_ok=True)
        ext = extension_de(nombre_archivo)
        nombre_seguro = f'{uuid4().hex}{ext}'
        ruta = self._directorio_base / nombre_seguro
        ruta.write_bytes(contenido)
        return nombre_seguro

    def leer(self, nombre_archivo: str) -> bytes:
        ruta = self._directorio_base / nombre_archivo
        if not ruta.exists():
            raise FileNotFoundError(f'El documento {nombre_archivo} no existe.')
        return ruta.read_bytes()

    def eliminar(self, nombre_archivo: str) -> None:
        ruta = self._directorio_base / nombre_archivo
        if ruta.exists():
            ruta.unlink()

    def listar(self) -> list[str]:
        if not self._directorio_base.exists():
            return []
        return sorted(archivo.name for archivo in self._directorio_base.iterdir())