"""Caso de uso: ProcesarDocumento.

Divide el contenido de un documento en fragmentos con solape y genera el
embedding de cada fragmento (HU-04 / G-13). Es idempotente: reprocesar un
documento reemplaza sus fragmentos anteriores.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from application.services.ServicioChunking import ServicioChunking
from domain.entities.Documento import Documento
from domain.entities.FragmentoDocumento import FragmentoDocumento
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.ports.FragmentoRepository import FragmentoRepository


class ProcesarDocumento:
    def __init__(
        self,
        documento_repository: DocumentoRepository,
        fragmento_repository: FragmentoRepository,
        chunking: ServicioChunking,
        busqueda_semantica: BusquedaSemanticaPort,
    ) -> None:
        self._documento_repository = documento_repository
        self._fragmento_repository = fragmento_repository
        self._chunking = chunking
        self._busqueda_semantica = busqueda_semantica

    async def ejecutar(self, documento_id: UUID) -> Documento | None:
        """Procesa el documento y devuelve el documento actualizado."""
        documento = await self._documento_repository.obtener_por_id(documento_id)
        if documento is None or documento.esta_eliminado():
            return None

        textos = self._chunking.dividir(documento.contenido)

        # Reprocesar siempre reemplaza los fragmentos anteriores (idempotente).
        await self._fragmento_repository.eliminar_por_documento(documento.id)

        ahora = datetime.now(timezone.utc)
        fragmentos: list[FragmentoDocumento] = []
        for orden, texto in enumerate(textos):
            fragmentos.append(
                FragmentoDocumento(
                    id=uuid4(),
                    documento_id=documento.id,
                    orden=orden,
                    contenido=texto,
                    embedding=await self._busqueda_semantica.generar_embedding(texto),
                    creado_en=ahora,
                )
            )

        if fragmentos:
            await self._fragmento_repository.guardar_lote(fragmentos)

        documento.fragmentado = bool(fragmentos)
        # El upsert conserva el embedding del documento (COALESCE) y solo
        # actualiza la marca `fragmentado`.
        return await self._documento_repository.guardar(documento)