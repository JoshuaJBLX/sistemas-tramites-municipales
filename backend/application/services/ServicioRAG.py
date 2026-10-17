"""Servicio de aplicación: ServicioRAG (Retrieval-Augmented Generation)."""

import re
from uuid import uuid4

from application.services.ServicioSLM import ServicioSLM
from domain.entities.Documento import Documento
from domain.entities.Fuente import Fuente
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.value_objects.FuenteOficial import FuenteOficial

# Número de documento dentro del título (p. ej. "Resolución N° 045-2023").
_NUMERO_DOCUMENTO = re.compile(r'n[°ºo]\.?\s*([0-9][0-9\-]*)', re.IGNORECASE)


class ServicioRAG:
    """Orquesta la recuperación semántica y la generación de la respuesta."""

    def __init__(
        self,
        busqueda_semantica: BusquedaSemanticaPort,
        servicio_slm: ServicioSLM,
        top_k: int = 5,
    ) -> None:
        self._busqueda_semantica = busqueda_semantica
        self._servicio_slm = servicio_slm
        self._top_k = top_k

    async def recuperar(self, pregunta: str) -> list[Documento]:
        """Recupera los documentos vigentes más relevantes para la pregunta."""
        documentos = await self._busqueda_semantica.buscar(pregunta, top_k=self._top_k)
        return [documento for documento in documentos if documento.esta_vigente()]

    async def responder(
        self, pregunta: str, contexto: list[Documento] | None = None
    ) -> tuple[str, list[Fuente]]:
        """Genera la respuesta y las fuentes citadas que la sustentan."""
        documentos = contexto if contexto is not None else await self.recuperar(pregunta)

        if not documentos:
            texto = await self._servicio_slm.generar(pregunta, [])
            return texto, []

        texto = await self._servicio_slm.generar(pregunta, documentos)
        return texto, self.construir_fuentes(documentos)

    @staticmethod
    def construir_fuentes(documentos: list[Documento]) -> list[Fuente]:
        """Convierte los documentos recuperados en fuentes citables.

        Si la recuperación fue por fragmento (HU-04), la cita muestra el chunk
        que de verdad sustenta la respuesta en lugar de las primeras líneas del
        documento completo. Cada fuente lleva los metadatos disponibles del
        documento: número, fecha de publicación y versión (HU-10 / P3-08).
        """
        return [
            Fuente(
                id=uuid4(),
                documento_id=documento.id,
                tipo=FuenteOficial.PORTAL_MUNICIPAL,
                url=documento.url_origen,
                fragmento=(documento.fragmento_destacado or documento.contenido)[:280],
                titulo=documento.titulo,
                numero=ServicioRAG._extraer_numero(documento.titulo),
                fecha=(
                    documento.fecha_publicacion.isoformat()
                    if documento.fecha_publicacion
                    else ''
                ),
                version=documento.version or '',
            )
            for documento in documentos
        ]

    @staticmethod
    def _extraer_numero(titulo: str) -> str:
        """Extrae el número de resolución/ordenanza del título, si existe."""
        coincidencia = _NUMERO_DOCUMENTO.search(titulo or '')
        return coincidencia.group(1) if coincidencia else ''