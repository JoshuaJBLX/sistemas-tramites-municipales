"""Adaptador de almacenamiento de documentos (sistema de archivos local)."""

import os
from pathlib import Path


class DocumentStorageAdapter:
    """Guarda y recupera los archivos originales de los documentos oficiales."""

    def __init__(self, directorio_base: str | None = None) -> None:
        self._directorio_base = Path(
            directorio_base or os.getenv('DOCUMENTS_PATH', './storage/documentos')
        )

    def guardar(self, nombre_archivo: str, contenido: bytes) -> Path:
        self._directorio_base.mkdir(parents=True, exist_ok=True)
        ruta = self._directorio_base / nombre_archivo
        ruta.write_bytes(contenido)
        return ruta

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