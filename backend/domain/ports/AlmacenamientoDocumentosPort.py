"""Puerto: AlmacenamientoDocumentosPort.

Abstracción del almacenamiento físico de los archivos originales de los
documentos municipales (sistema de archivos, S3, etc.).
"""

from abc import ABC, abstractmethod


class AlmacenamientoDocumentosPort(ABC):
    @abstractmethod
    def guardar(self, nombre_archivo: str, contenido: bytes) -> str:
        """Guarda el archivo y devuelve el nombre con el que quedó almacenado."""
        ...

    @abstractmethod
    def leer(self, nombre_archivo: str) -> bytes:
        ...

    @abstractmethod
    def eliminar(self, nombre_archivo: str) -> None:
        ...

    @abstractmethod
    def listar(self) -> list[str]:
        ...