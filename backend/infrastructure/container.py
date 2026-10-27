"""Contenedor de dependencias actualizado con módulos de documentos (HU-01..HU-04)."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Request

from application.services.EvaluadorGroundedness import EvaluadorGroundedness
from application.services.ServicioAuditoria import ServicioAuditoria
from application.services.ServicioCache import ServicioCache
from application.services.ServicioChunking import ServicioChunking
from application.services.ServicioDominio import ServicioDominio
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
from application.use_cases.RecomendarTramites import RecomendarTramites
from application.use_cases.RegistrarConsulta import RegistrarConsulta
from domain.entities.Consulta import Consulta
from domain.entities.Respuesta import Respuesta
from domain.entities.Trazabilidad import Trazabilidad
from domain.ports.AuditoriaPort import AuditoriaPort
from domain.ports.BusquedaSemanticaPort import BusquedaSemanticaPort
from domain.ports.CachePort import CachePort
from domain.ports.ConsultaRepository import ConsultaRepository
from domain.ports.DocumentoRepository import DocumentoRepository
from domain.ports.FragmentoRepository import FragmentoRepository
from domain.ports.GeneracionRespuestaPort import GeneracionRespuestaPort
from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.FuenteOficial import FuenteOficial
from domain.value_objects.IntencionConsulta import IntencionConsulta
from infrastructure.adapters.cache.RedisAdapter import RedisAdapter
from infrastructure.adapters.catalog.TramiteCatalogoAdapter import TramiteCatalogoAdapter
from infrastructure.adapters.documents.DocumentStorageAdapter import (
    DocumentStorageAdapter,
)
from infrastructure.adapters.documents.DocumentStorageAdapterSupabase import (
    DocumentStorageAdapterSupabase,
)
from infrastructure.adapters.embeddings.BGE_M3Adapter import BGE_M3Adapter
from infrastructure.adapters.embeddings.OpenAIEmbeddingsAdapter import (
    OpenAIEmbeddingsAdapter,
)
from infrastructure.adapters.extraction.ExtraccionTextoAdapter import (
    ExtraccionTextoAdapter,
)
from infrastructure.adapters.rag.BusquedaVectorialAdapter import (
    BusquedaVectorialAdapter,
)
from infrastructure.adapters.slm.OllamaAdapter import OllamaAdapter
from infrastructure.adapters.slm.OpenRouterAdapter import OpenRouterAdapter
from infrastructure.repositories.Connection import Connection
from infrastructure.repositories.ConsultaRepositoryImpl import ConsultaRepositoryImpl
from infrastructure.repositories.DocumentoRepositoryImpl import DocumentoRepositoryImpl
from infrastructure.repositories.FragmentoRepositoryImpl import FragmentoRepositoryImpl

QUERY_AUDITORIA = """
    INSERT INTO auditoria_consultas (
        id, consulta_id, respuesta, confianza, fuentes, fuentes_detalle,
        groundedness, fuera_dominio, afirmaciones_bloqueadas, entidad_sugerida,
        duracion_ms, tramite_probable, registrado_en
    )
    VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8, $9, $10, $11, $12, NOW())
"""

# HU-10 (D-9): la trazabilidad une la consulta con su última respuesta
# auditada (texto, confianza, groundedness y fuentes con metadatos).
# HU-14: añade marcado_inconsistente, nota_revision e inconsistencia automática
# (respuesta existe Y (sin fuentes O sin evaluación)).
_TRAZABILIDAD_COLUMNAS = """
    SELECT c.id, c.usuario_id, c.pregunta, c.intencion, c.creada_en,
           a.respuesta, a.confianza, a.groundedness, a.fuentes_detalle,
           a.fuera_dominio, a.afirmaciones_bloqueadas, a.entidad_sugerida,
           a.duracion_ms, a.tramite_probable, a.registrado_en,
           a.marcado_inconsistente, a.nota_revision,
           (a.respuesta IS NOT NULL AND (
               COALESCE(a.fuentes_detalle, '[]') = '[]' OR
               NOT EXISTS (SELECT 1 FROM evaluaciones_calidad e WHERE e.consulta_id = c.id)
           )) AS inconsistente
    FROM consultas c
    LEFT JOIN LATERAL (
        SELECT respuesta, confianza, groundedness, fuentes_detalle,
               fuera_dominio, afirmaciones_bloqueadas, entidad_sugerida,
               duracion_ms, tramite_probable, registrado_en,
               marcado_inconsistente, nota_revision
        FROM auditoria_consultas
        WHERE consulta_id = c.id
        ORDER BY registrado_en DESC
        LIMIT 1
    ) a ON TRUE
"""

QUERY_TRAZABILIDAD_POR_ID = _TRAZABILIDAD_COLUMNAS + 'WHERE c.id = $1'
QUERY_TRAZABILIDAD_LISTA = (
    _TRAZABILIDAD_COLUMNAS + 'ORDER BY c.creada_en DESC LIMIT $1'
)

# HU-14: listado filtrado por fecha, texto (pregunta o trámite probable), usuario.
QUERY_TRAZABILIDAD_FILTRADA = (
    _TRAZABILIDAD_COLUMNAS + """
    WHERE ($2::timestamptz IS NULL OR c.creada_en >= $2)
      AND ($3::timestamptz IS NULL OR c.creada_en <= $3)
      AND ($4::text IS NULL OR c.pregunta ILIKE '%' || $4 || '%'
                       OR a.tramite_probable ILIKE '%' || $4 || '%')
      AND ($5::uuid IS NULL OR c.usuario_id = $5)
    ORDER BY c.creada_en DESC LIMIT $1
"""
)

# HU-14: marcar/desmarcar registro como inconsistente para revisión.
QUERY_MARCAR_INCONSISTENTE = """
    UPDATE auditoria_consultas
    SET marcado_inconsistente = $2,
        nota_revision = $3,
        marcado_en = NOW(),
        marcado_por = $4
    WHERE consulta_id = $1
"""


def _serializar_fuente(fuente) -> dict:
    """Metadatos de la fuente para el JSON de auditoría (HU-10)."""
    return {
        'url': fuente.url,
        'fragmento': fuente.fragmento,
        'titulo': fuente.titulo,
        'numero': fuente.numero,
        'fecha': fuente.fecha,
        'version': fuente.version,
        'documento_id': str(fuente.documento_id),
    }


def _mapear_trazabilidad(fila) -> Trazabilidad:
    from domain.entities.Fuente import Fuente

    detalle = fila['fuentes_detalle'] or []
    if isinstance(detalle, str):
        detalle = json.loads(detalle)
    fuentes = [
        Fuente(
            id=uuid4(),
            documento_id=UUID(str(item['documento_id']))
            if item.get('documento_id')
            else uuid4(),
            tipo=FuenteOficial.PORTAL_MUNICIPAL,
            url=item.get('url', ''),
            fragmento=item.get('fragmento', ''),
            titulo=item.get('titulo', ''),
            numero=item.get('numero', ''),
            fecha=item.get('fecha', ''),
            version=item.get('version', ''),
        )
        for item in detalle
        if isinstance(item, dict)
    ]

    consulta = Consulta(
        id=fila['id'],
        usuario_id=fila['usuario_id'],
        pregunta=fila['pregunta'],
        intencion=IntencionConsulta(fila['intencion']) if fila['intencion'] else None,
        creada_en=fila['creada_en'],
    )

    return Trazabilidad(
        consulta=consulta,
        respuesta=fila['respuesta'],
        confianza=fila['confianza'],
        groundedness=float(fila['groundedness'] or 0.0),
        fuentes=fuentes,
        fuera_dominio=bool(fila['fuera_dominio']),
        afirmaciones_bloqueadas=bool(fila['afirmaciones_bloqueadas']),
        entidad_sugerida=fila['entidad_sugerida'] or '',
        duracion_ms=fila['duracion_ms'],
        tramite_probable=fila['tramite_probable'],
        registrado_en=fila['registrado_en'],
        # HU-14
        marcado_inconsistente=bool(fila.get('marcado_inconsistente', False)),
        nota_revision=fila.get('nota_revision'),
        inconsistente=bool(fila.get('inconsistente', False)),
    )


class _AuditoriaPostgreSQL(AuditoriaPort):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    async def registrar(
        self,
        consulta: Consulta,
        respuesta: Respuesta,
        duracion_ms: int | None = None,
    ) -> None:
        fuentes = ','.join(fuente.url for fuente in respuesta.fuentes) or None
        detalle = json.dumps(
            [_serializar_fuente(fuente) for fuente in respuesta.fuentes]
        )
        tramite = respuesta.tramite_probable
        async with self._connection.pool.acquire() as conexion:
            await conexion.execute(
                QUERY_AUDITORIA,
                uuid4(),
                consulta.id,
                respuesta.texto,
                respuesta.confianza.value,
                fuentes,
                detalle,
                respuesta.groundedness,
                respuesta.fuera_dominio,
                respuesta.afirmaciones_bloqueadas,
                respuesta.entidad_sugerida or None,
                duracion_ms,
                tramite.nombre if tramite is not None else None,
            )

    async def obtener_trazabilidad(self, consulta_id: UUID) -> Trazabilidad | None:
        async with self._connection.pool.acquire() as conexion:
            fila = await conexion.fetchrow(QUERY_TRAZABILIDAD_POR_ID, consulta_id)
        return _mapear_trazabilidad(fila) if fila else None

    async def listar_trazabilidad(self, limite: int = 20) -> list[Trazabilidad]:
        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(QUERY_TRAZABILIDAD_LISTA, limite)
        return [_mapear_trazabilidad(fila) for fila in filas]

    # HU-14: listado filtrado.
    async def listar_trazabilidad_filtrada(
        self,
        limite: int = 20,
        desde: datetime | None = None,
        hasta: datetime | None = None,
        texto: str | None = None,
        usuario_id: UUID | None = None,
    ) -> list[Trazabilidad]:
        async with self._connection.pool.acquire() as conexion:
            filas = await conexion.fetch(
                QUERY_TRAZABILIDAD_FILTRADA, limite, desde, hasta, texto, usuario_id
            )
        return [_mapear_trazabilidad(fila) for fila in filas]

    # HU-14: marcar/desmarcar como inconsistente.
    async def marcar_inconsistente(
        self,
        consulta_id: UUID,
        marcado: bool,
        nota: str | None,
        marcado_por: str,
    ) -> None:
        async with self._connection.pool.acquire() as conexion:
            await conexion.execute(
                QUERY_MARCAR_INCONSISTENTE, consulta_id, marcado, nota, marcado_por
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
    recomendar_tramites: RecomendarTramites
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

    # Embeddings por API si hay OPENAI_API_KEY (Render free: 512MB, sin torch),
    # sino modelo local BGE-M3 (desarrollo/Docker/Fly con requirements-ml.txt)
    if os.getenv('OPENAI_API_KEY'):
        generador_embeddings = OpenAIEmbeddingsAdapter()
    else:
        generador_embeddings = BGE_M3Adapter()
    busqueda_semantica = BusquedaVectorialAdapter(connection, generador_embeddings)

    # Usar OpenRouter si hay API key, sino Ollama local
    if os.getenv('OPENROUTER_API_KEY'):
        generacion_respuesta = OpenRouterAdapter()
    else:
        generacion_respuesta = OllamaAdapter()

    cache = RedisAdapter()

    # Usar Supabase Storage si está configurado, sino almacenamiento local
    if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SERVICE_ROLE_KEY'):
        almacenamiento = DocumentStorageAdapterSupabase()
    else:
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
    servicio_dominio = ServicioDominio()
    servicio_orientacion = ServicioOrientacion(
        servicio_rag,
        evaluador_groundedness,
        identificar_tramite,
        servicio_dominio,
        catalogo=tramite_catalogo,
    )
    servicio_auditoria = ServicioAuditoria(auditoria, consulta_repository)
    servicio_cache = ServicioCache(
        cache, ttl_segundos=int(os.getenv('CACHE_TTL_SEGUNDOS', '3600'))
    )
    servicio_chunking = ServicioChunking()

    gestionar_documentos = GestionarDocumentos(
        documento_repository, busqueda_semantica, almacenamiento
    )
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
        recomendar_tramites=RecomendarTramites(tramite_catalogo),
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