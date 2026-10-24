"""Adaptador: DocumentStorageAdapterSupabase implementa AlmacenamientoDocumentosPort usando Supabase Storage."""

import os
from uuid import uuid4

try:
    from supabase import create_client, Client
except ImportError:
    raise ImportError(
        "Para usar Supabase Storage, instala: pip install supabase"
    )

from domain.ports.AlmacenamientoDocumentosPort import AlmacenamientoDocumentosPort
from domain.value_objects.FormatoDocumento import extension_de


class DocumentStorageAdapterSupabase(AlmacenamientoDocumentosPort):
    """Guarda archivos en Supabase Storage en lugar de sistema de archivos local.

    Esto es necesario para despliegues en Render/Vercel donde el almacenamiento
    local es efímero y se borra en cada deploy.
    """

    def __init__(self) -> None:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridos "
                "para DocumentStorageAdapterSupabase"
            )

        self._client: Client = create_client(supabase_url, supabase_key)
        self._bucket = os.getenv('SUPABASE_STORAGE_BUCKET', 'documentos')
        self._path_prefix = 'documentos'

    def guardar(self, nombre_archivo: str, contenido: bytes) -> str:
        """Guarda un archivo en Supabase Storage."""
        ext = extension_de(nombre_archivo)
        nombre_seguro = f'{uuid4().hex}{ext}'
        ruta_completa = f'{self._path_prefix}/{nombre_seguro}'

        try:
            self._client.storage.from_(self._bucket).upload(
                path=ruta_completa,
                file=contenido,
                file_options={'content-type': 'application/octet-stream'}
            )
            return nombre_seguro
        except Exception as e:
            raise RuntimeError(f'Error al guardar en Supabase Storage: {e}')

    def leer(self, nombre_archivo: str) -> bytes:
        """Lee un archivo desde Supabase Storage."""
        ruta_completa = f'{self._path_prefix}/{nombre_archivo}'

        try:
            response = self._client.storage.from_(self._bucket).download(ruta_completa)
            return response
        except Exception as e:
            raise FileNotFoundError(
                f'El documento {nombre_archivo} no existe en Supabase Storage: {e}'
            )

    def eliminar(self, nombre_archivo: str) -> None:
        """Elimina un archivo de Supabase Storage."""
        ruta_completa = f'{self._path_prefix}/{nombre_archivo}'

        try:
            self._client.storage.from_(self._bucket).remove([ruta_completa])
        except Exception as e:
            raise RuntimeError(f'Error al eliminar de Supabase Storage: {e}')

    def listar(self) -> list[str]:
        """Lista todos los archivos en el bucket."""
        try:
            response = self._client.storage.from_(self._bucket).list(
                path=self._path_prefix
            )
            # response es una lista de objetos con 'name'
            return [item['name'] for item in response if item.get('name')]
        except Exception as e:
            raise RuntimeError(f'Error al listar archivos en Supabase Storage: {e}')
