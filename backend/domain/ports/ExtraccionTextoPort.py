"""Puerto: ExtraccionTextoPort.

Extrae el texto plano de un archivo oficial (PDF, DOCX, TXT, MD). Si el archivo
es legible en formato pero no contiene texto recuperable (p. ej. un PDF escaneado
sin capa OCR), el adaptador levanta `DocumentoIlegibleError` (HU-04, HU-01).
"""

from abc import ABC, abstractmethod

from domain.errors import DocumentoIlegibleError, FormatoNoSoportadoError


class ExtraccionTextoPort(ABC):
    @abstractmethod
    def soporta(self, nombre_archivo: str) -> bool:
        """Indica si la extensión del archivo es un formato extraíble."""
        ...

    @abstractmethod
    async def extraer(self, nombre_archivo: str, contenido: bytes) -> str:
        """Devuelve el texto plano del archivo.

        Levanta FormatoNoSoportadoError para extensiones no admitidas y
        DocumentoIlegibleError cuando el archivo no tiene texto recuperable.
        """
        ...

    @abstractmethod
    def formatos_soportados(self) -> list[str]:
        """Extensiones admitidas (para la UI y los mensajes de error)."""
        ...