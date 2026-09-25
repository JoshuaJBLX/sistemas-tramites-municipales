"""Caso de uso: BuscarDocumentos."""

from domain.entities.Documento import Documento
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort


class BuscarDocumentos:
    """Recupera documentos oficiales relevantes para una consulta."""

    def __init__(self, busqueda_semantica: BusquedaSemanticaPort) -> None:
        self._busqueda_semantica = busqueda_semantica

    async def ejecutar(self, consulta: str, top_k: int = 5) -> list[Documento]:
        if not consulta or not consulta.strip():
            return []

        documentos = await self._busqueda_semantica.buscar(consulta.strip(), top_k=top_k)

        return [documento for documento in documentos if documento.esta_vigente()]