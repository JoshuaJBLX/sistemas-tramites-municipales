"""Contenedor de dependencias: cablea puertos del dominio con sus adaptadores.

Este módulo es la única pieza de infraestructura que conoce todas las
implementaciones concretas y las inyecta en los casos de uso.
"""

import os
from dataclasses import dataclass
from uuid import uuid4

from application.services.EvaluadorGroundedness import EvaluadorGroundedness
from application.services.ServicioAuditoria import ServicioAuditoria
from application.services.ServicioCache import ServicioCache
from application.services.ServicioNLP import ServicioNLP
from application.services.ServicioOrientacion import ServicioOrientacion
from application.services.ServicioRAG import ServicioRAG
from application.services.ServicioSLM import ServicioSLM
from application.use_cases.AuditarConsulta import AuditarConsulta
from application.use_cases.BuscarDocumentos import BuscarDocumentos
from application.use_cases.ClasificarIntencion import ClasificarIntencion
from application.use_cases.ConsultarTramite import ConsultarTramite
from application.use_cases.GenerarOrientacion import GenerarOrientacion
from application.use_cases.GestionarDocumentos import GestionarDocumentos
from application.use_cases.RegistrarConsulta import RegistrarConsulta
from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.ports.AuditoriaPort import AuditoriaPort
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.CachePort import CachePort
from domain.ports.ConsultaRepository import ConsultaRepository
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort
from infrastructure.adapters.cache.RedisAdapter import RedisAdapter
from infrastructure.adapters.documents.DocumentStorageAdapter import DocumentStorageAdapter
from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.adapters.rag.BusquedaVectorialAdapter import BusquedaVectorialAdapter
from infrastructure.adapters.slm.OllamaAdapter import OllamaAdapter
from infrastructure.repositories.Connection import Connection
from infrastructure.repositories.ConsultaRepositoryImpl import ConsultaRepositoryImpl
from infrastructure.repositories.DocumentoRepositoryImpl import DocumentoRepositoryImpl

QUERY_AUDITORIA = """
    INSERT INTO auditoria_consultas (id, consulta_id, respuesta, confianza, fuentes, registrado_en)
    VALUES ($1, $2, $3, $4, $5, NOW())
"""


class _AuditoriaPostgreSQL(AuditoriaPort):
    """Persiste la trazabilidad de las interacciones en PostgreSQL."""

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
    """Agrupa adaptadores, servicios y casos de uso listos para inyectar."""

    connection: Connection
    documento_repository: DocumentoRepository
    consulta_repository: ConsultaRepository
    busqueda_semantica: BusquedaSemanticaPort
    generacion_respuesta: GeneracionRespuestaPort
    cache: CachePort
    almacenamiento: DocumentStorageAdapter
    servicio_cache: ServicioCache
    registrar_consulta: RegistrarConsulta
    consultar_tramite: ConsultarTramite
    clasificar_intencion: ClasificarIntencion
    buscar_documentos: BuscarDocumentos
    generar_orientacion: GenerarOrientacion
    gestionar_documentos: GestionarDocumentos
    auditar_consulta: AuditarConsulta


def crear_container(dsn: str | None = None) -> Container:
    """Construye el grafo de dependencias con las implementaciones por defecto."""
    connection = Connection(dsn)

    # Adaptadores de salida.
    generador_embeddings = BGE_M3Adapter()
    busqueda_semantica = BusquedaVectorialAdapter(connection, generador_embeddings)
    generacion_respuesta = OllamaAdapter()
    cache = RedisAdapter()
    almacenamiento = DocumentStorageAdapter()
    auditoria = _AuditoriaPostgreSQL(connection)

    # Repositorios.
    documento_repository = DocumentoRepositoryImpl(connection)
    consulta_repository = ConsultaRepositoryImpl(connection)

    # Servicios de aplicación.
    servicio_nlp = ServicioNLP()
    servicio_slm = ServicioSLM(generacion_respuesta)
    servicio_rag = ServicioRAG(
        busqueda_semantica=busqueda_semantica,
        servicio_slm=servicio_slm,
        top_k=int(os.getenv('RAG_TOP_K', '5')),
    )
    evaluador_groundedness = EvaluadorGroundedness()
    servicio_orientacion = ServicioOrientacion(servicio_rag, evaluador_groundedness)
    servicio_auditoria = ServicioAuditoria(auditoria, consulta_repository)
    servicio_cache = ServicioCache(
        cache, ttl_segundos=int(os.getenv('CACHE_TTL_SEGUNDOS', '3600'))
    )

    # Casos de uso.
    return Container(
        connection=connection,
        documento_repository=documento_repository,
        consulta_repository=consulta_repository,
        busqueda_semantica=busqueda_semantica,
        generacion_respuesta=generacion_respuesta,
        cache=cache,
        almacenamiento=almacenamiento,
        servicio_cache=servicio_cache,
        registrar_consulta=RegistrarConsulta(consulta_repository),
        consultar_tramite=ConsultarTramite(documento_repository, cache),
        clasificar_intencion=ClasificarIntencion(servicio_nlp),
        buscar_documentos=BuscarDocumentos(busqueda_semantica),
        generar_orientacion=GenerarOrientacion(servicio_orientacion),
        gestionar_documentos=GestionarDocumentos(documento_repository, busqueda_semantica),
        auditar_consulta=AuditarConsulta(servicio_auditoria),
    )


def obtener_container(request) -> Container:
    """Dependencia de FastAPI que expone el contenedor desde app.state."""
    return request.app.state.container
