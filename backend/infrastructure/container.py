"""Contenedor de dependencias actualizado con módulos de documentos (HU-01..HU-04)."""

import os
from dataclasses import dataclass
from uuid import uuid4

from fastapi import Request

from application.services.EvaluadorGroundedness import EvaluadorGroundedness
from application.services.ServicioAuditoria import ServicioAuditoria
from application.services.ServicioCache import ServicioCache
from application.services.ServicioChunking import ServicioChunking
from application.services.ServicioNLP import ServicioNLP
from application.services.ServicioOrientacion import ServicioOrientacion
from application.services.ServicioRAG import ServicioRAG
from application.services.ServicioSLM import ServicioSLM
from application.use_cases.AuditarConsulta import AuditarConsulta
from application.use_cases.BuscarDocumentos import BuscarDocumentos
from application.use_cases.CargarDocumento import CargarDocumento
from application.use_cases.ClasificarIntencion import ClasificarIntencion
from application.use_cases.ConsultarTramite import ConsultarTramite
from application.use_cases.GenerarOrientacion import GenerarOrientacion
from application.use_cases.GestionarDocumentos import GestionarDocumentos
from application.use_cases.IdentificarTramiteProbable import IdentificarTramiteProbable
from application.use_cases.ProcesarDocumento import ProcesarDocumento
from application.use_cases.RegistrarConsulta import RegistrarConsulta
from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.ports.AuditoriaPort import AuditoriaPort
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.CachePort import CachePort
from domain.ports.ConsultaRepository import ConsultaRepository
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.ports.FragmentoRepository import FragmentoRepository
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort
from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from infrastructure.adapters.cache.RedisAdapter import RedisAdapter
from infrastructure.adapters.catalog.TramiteCatalogoAdapter import TramiteCatalogoAdapter
from infrastructure.adapters.documents.DocumentStorageAdapter import (
    DocumentStorageAdapter,
)
from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.adapters.extraction.ExtraccionTextoAdapter import (
    ExtraccionTextoAdapter,
)
from infrastructure.adapters.rag.BusquedaVectorialAdapter import (
    BusquedaVectorialAdapter,
)
from infrastructure.adapters.slm.OllamaAdapter import OllamaAdapter
from infrastructure.repositories.Connection import Connection
from infrastructure.repositories.ConsultaRepositoryImpl import ConsultaRepositoryImpl
from infrastructure.repositories.DocumentoRepositoryImpl import DocumentoRepositoryImpl
from infrastructure.repositories.FragmentoRepositoryImpl import FragmentoRepositoryImpl

QUERY_AUDITORIA = """
    INSERT INTO auditoria_consultas (id, consulta_id, respuesta, confianza, fuentes, registrado_en)
    VALUES ($1, $2, $3, $4, $5, NOW())
"""


class _AuditoriaPostgreSQL(AuditoriaPort):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def registrar(self, consulta: Consulta, respuesta: Respuesta) -> None:
        fuentes = ','.join(fuente.url for fuente in respuesta.fuentes) or None
        async with self._connection.pool.acquire() as conexion:
            await conexion.execute(
                QUERY_AUDITORIA,
                uuid4(),
                consulta.id,
                respuesta.texto,
                respuesta.confianza.value,
                fuentes,
            )


@dataclass
class Container:
    connection: Connection
    documento_repository: DocumentoRepository
    consulta_repository: ConsultaRepository
    fragmento_repository: FragmentoRepository
    busqueda_semantica: BusquedaSemanticaPort
    generacion_respuesta: GeneracionRespuestaPort
    cache: CachePort
    almacenamiento: DocumentStorageAdapter
    extraccion_texto: ExtraccionTextoAdapter
    tramite_catalogo: TramiteCatalogoPort
    servicio_cache: ServicioCache
    servicio_chunking: ServicioChunking
    registrar_consulta: RegistrarConsulta
    consultar_tramite: ConsultarTramite
    clasificar_intencion: ClasificarIntencion
    identificar_tramite: IdentificarTramiteProbable
    buscar_documentos: BuscarDocumentos
    generar_orientacion: GenerarOrientacion
    gestionar_documentos: GestionarDocumentos
    procesar_documento: ProcesarDocumento
    cargar_documento: CargarDocumento
    auditar_consulta: AuditarConsulta


def crear_container(dsn: str | None = None) -> Container:
    connection = Connection(dsn)

    generador_embeddings = BGE_M3Adapter()
    busqueda_semantica = BusquedaVectorialAdapter(connection, generador_embeddings)
    generacion_respuesta = OllamaAdapter()
    cache = RedisAdapter()
    almacenamiento = DocumentStorageAdapter()
    extraccion_texto = ExtraccionTextoAdapter()
    auditoria = _AuditoriaPostgreSQL(connection)

    documento_repository = DocumentoRepositoryImpl(connection)
    consulta_repository = ConsultaRepositoryImpl(connection)
    fragmento_repository = FragmentoRepositoryImpl(connection)

    tramite_catalogo = TramiteCatalogoAdapter(documento_repository)

    servicio_nlp = ServicioNLP()
    servicio_slm = ServicioSLM(generacion_respuesta)
    servicio_rag = ServicioRAG(
        busqueda_semantica=busqueda_semantica,
        servicio_slm=servicio_slm,
        top_k=int(os.getenv('RAG_TOP_K', '5')),
    )
    evaluador_groundedness = EvaluadorGroundedness()
    identificar_tramite = IdentificarTramiteProbable(tramite_catalogo)
    servicio_orientacion = ServicioOrientacion(
        servicio_rag, evaluador_groundedness, identificar_tramite
    )
    servicio_auditoria = ServicioAuditoria(auditoria, consulta_repository)
    servicio_cache = ServicioCache(
        cache, ttl_segundos=int(os.getenv('CACHE_TTL_SEGUNDOS', '3600'))
    )
    servicio_chunking = ServicioChunking()

    gestionar_documentos = GestionarDocumentos(documento_repository, busqueda_semantica)
    procesar_documento = ProcesarDocumento(
        documento_repository, fragmento_repository, servicio_chunking, busqueda_semantica
    )
    cargar_documento = CargarDocumento(
        almacenamiento, extraccion_texto, gestionar_documentos, procesar_documento
    )

    return Container(
        connection=connection,
        documento_repository=documento_repository,
        consulta_repository=consulta_repository,
        fragmento_repository=fragmento_repository,
        busqueda_semantica=busqueda_semantica,
        generacion_respuesta=generacion_respuesta,
        cache=cache,
        almacenamiento=almacenamiento,
        extraccion_texto=extraccion_texto,
        tramite_catalogo=tramite_catalogo,
        servicio_cache=servicio_cache,
        servicio_chunking=servicio_chunking,
        registrar_consulta=RegistrarConsulta(consulta_repository),
        consultar_tramite=ConsultarTramite(documento_repository, cache),
        clasificar_intencion=ClasificarIntencion(servicio_nlp),
        identificar_tramite=identificar_tramite,
        buscar_documentos=BuscarDocumentos(busqueda_semantica),
        generar_orientacion=GenerarOrientacion(servicio_orientacion),
        gestionar_documentos=gestionar_documentos,
        procesar_documento=procesar_documento,
        cargar_documento=cargar_documento,
        auditar_consulta=AuditarConsulta(servicio_auditoria),
    )


def obtener_container(request: Request) -> Container:
    return request.app.state.container