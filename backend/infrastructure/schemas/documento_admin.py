import re
from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, field_validator


def normalizar_texto(s: str | None) -> str:
    if not s:
        return ''
    return re.sub(r'\s+', ' ', s).strip()


class DocumentoAdminRequest(BaseModel):
    tramite_id: str
    titulo: str
    contenido: str
    url_origen: str
    estado: str = 'vigente'
    version: str = '1.0'
    fecha_publicacion: Optional[date] = None

    @field_validator('titulo', 'contenido', 'url_origen')
    @classmethod
    def _no_vacio(cls, v: str) -> str:
        v2 = normalizar_texto(v)
        if not v2:
            raise ValueError('campo obligatorio')
        return v2

    @field_validator('estado')
    @classmethod
    def _estado_valido(cls, v: str) -> str:
        v2 = normalizar_texto(v).lower()
        permitido = {'vigente', 'obsoleto', 'en_revision', 'derogado'}
        if v2 not in permitido:
            raise ValueError('estado inválido')
        return v2


class DocumentoAdminResponse(BaseModel):
    id: str
    tramite_id: str
    titulo: str
    url_origen: str
    estado: str
    indexado: bool
    version: str
    fecha_publicacion: Optional[date] = None
    fragmentado: bool
    archivo_nombre: Optional[str] = None
    mime_type: Optional[str] = None
    hash_contenido: Optional[str] = None
    actualizado_en: Optional[datetime] = None
    eliminado_en: Optional[datetime] = None