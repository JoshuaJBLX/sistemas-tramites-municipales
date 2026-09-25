"""Servicio de aplicación: ServicioRAG (Retrieval-Augmented Generation)."""

from uuid import uuid4

from application.services.ServicioSLM import ServicioSLM
from domain.entities.Documento import Documento
from domain.entities.Fuente import Fuente
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.value_objects.FuenteOficial import FuenteOficial


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
        """Convierte los documentos recuperados en fuentes citables."""
        return [
            Fuente(
                id=uuid4(),
                documento_id=documento.id,
                tipo=FuenteOficial.PORTAL_MUNICIPAL,
                url=documento.url_origen,
                fragmento=documento.contenido[:280],
            )
            for documento in documentos
        ]