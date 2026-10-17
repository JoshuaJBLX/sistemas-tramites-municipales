"""Adaptador: TramiteCatalogoAdapter (consulta de trámites en PostgreSQL)."""

import re
from unicodedata import normalize
from uuid import UUID

import numpy as np

from domain.ports.TramiteCatalogoPort import TramiteCatalogoPort
from domain.value_objects.TramiteProbable import TramiteProbable
from infrastructure.repositories.PostgreSQLRepository import PostgreSQLRepository

QUERY_TRAMITES_POR_DOCUMENTOS = """
    SELECT t.id, t.nombre, t.requisitos, t.costo, t.duracion_estimada_dias,
           t.area_responsable,
           MIN(d.url_origen) AS url_origen,
           COUNT(d.id) AS documentos_coincidentes
    FROM tramites t
    JOIN documentos d ON d.tramite_id = t.id
    WHERE d.id = ANY($1::uuid[])
    GROUP BY t.id, t.nombre, t.requisitos, t.costo, t.duracion_estimada_dias,
             t.area_responsable
    ORDER BY documentos_coincidentes DESC, t.nombre
"""

# Documentos con embedding de un trámite concreto (origen de la recomendación).
QUERY_EMBEDDINGS_TRAMITE = """
    SELECT d.embedding
    FROM documentos d
    WHERE d.tramite_id = $1
      AND d.embedding IS NOT NULL
      AND d.estado = 'vigente'
      AND d.eliminado_en IS NULL
"""

# Documentos con embedding del resto del catálogo (candidatos relacionados).
QUERY_EMBEDDINGS_CANDIDATOS = """
    SELECT t.id, t.nombre, t.requisitos, t.costo, t.duracion_estimada_dias,
           t.area_responsable, d.url_origen, d.embedding
    FROM tramites t
    JOIN documentos d ON d.tramite_id = t.id
    WHERE t.id <> $1
      AND d.embedding IS NOT NULL
      AND d.estado = 'vigente'
      AND d.eliminado_en IS NULL
"""

# Similitud mínima para considerar que dos trámites se relacionan (HU-12).
UMBRAL_RELACION = 0.30

# Catálogo completo para el fallback léxico (trámites sin documentos indexados).
QUERY_TRAMITES_CATALOGO = """
    SELECT id, nombre, descripcion, requisitos, costo, duracion_estimada_dias,
           area_responsable
    FROM tramites
    ORDER BY nombre
"""

# Umbral de similitud léxica (Jaccard sobre tokens) para el fallback.
UMBRAL_RELACION_LEXICO = 0.10

_STOPWORDS = frozenset(
    'al algo algun alguna ante bajo cada con contra de del desde donde dos el ella '
    'ellas el les en entre era eran es esa ese eso esta estaba estan estar este esta '
    'esto fue han hasta hay la las le les lo los mas me mi muy no nos o otra otro para '
    'pero por porque que quien quienes se ser si sin sobre su sus tambien tan tanto te '
    'tiene traer un una uno y ya'.split()
)


def _tokens(texto: str) -> set[str]:
    """Tokens del texto sin acentos, en minúsculas y sin palabras vacías."""
    plano = (
        normalize('NFKD', texto or '')
        .encode('ascii', 'ignore')
        .decode('ascii')
        .lower()
    )
    return {
        token
        for token in re.findall(r'[a-z0-9]+', plano)
        if len(token) > 2 and token not in _STOPWORDS
    }


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _coseno(a, b) -> float:
    va = np.asarray(a, dtype=np.float32)
    vb = np.asarray(b, dtype=np.float32)
    minimo = min(va.size, vb.size)
    if minimo == 0:
        return 0.0
    va, vb = va[:minimo], vb[:minimo]
    norma = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if norma == 0.0:
        return 0.0
    return float(np.dot(va, vb) / norma)


class TramiteCatalogoAdapter(TramiteCatalogoPort):
    """Resuelve los trámites del catálogo a partir de los documentos recuperados."""

    def __init__(self, repository: PostgreSQLRepository) -> None:
        self._repository = repository

    async def buscar_por_documentos(
        self, documento_ids: list[UUID]
    ) -> list[TramiteProbable]:
        if not documento_ids:
            return []

        filas = await self._repository.obtener_muchos(
            QUERY_TRAMITES_POR_DOCUMENTOS, list(documento_ids)
        )

        return [
            TramiteProbable(
                id=fila['id'],
                nombre=fila['nombre'],
                requisitos=list(fila['requisitos'] or []),
                costo=float(fila['costo'] or 0.0),
                duracion_estimada_dias=int(fila['duracion_estimada_dias'] or 0),
                fuente_url=fila['url_origen'],
                documentos_coincidentes=int(fila['documentos_coincidentes']),
                area_responsable=fila['area_responsable'],
            )
            for fila in filas
        ]

    async def relacionados(
        self, tramite_id: UUID, limite: int = 4
    ) -> list[TramiteProbable]:
        """Ordena el resto del catálogo por similitud con el trámite indicado.

        El perfil del trámite origen es el vector medio de sus documentos; cada
        candidato puntúa con su documento más parecido a ese perfil (HU-12).
        Los trámites sin documentos indexados (p. ej. los 252 del TUPA) usan un
        fallback léxico sobre nombre, descripción y requisitos.
        """
        origen = await self._repository.obtener_muchos(
            QUERY_EMBEDDINGS_TRAMITE, tramite_id
        )
        if not origen:
            return await self._relacionados_lexicos(tramite_id, limite)

        perfil = self._vector_medio([fila['embedding'] for fila in origen])
        if perfil is None:
            return await self._relacionados_lexicos(tramite_id, limite)

        candidatos = await self._repository.obtener_muchos(
            QUERY_EMBEDDINGS_CANDIDATOS, tramite_id
        )

        puntajes: dict[UUID, tuple[TramiteProbable, float]] = {}
        for fila in candidatos:
            similitud = _coseno(perfil, fila['embedding'])
            if similitud < UMBRAL_RELACION:
                continue
            tramite = TramiteProbable(
                id=fila['id'],
                nombre=fila['nombre'],
                requisitos=list(fila['requisitos'] or []),
                costo=float(fila['costo'] or 0.0),
                duracion_estimada_dias=int(fila['duracion_estimada_dias'] or 0),
                fuente_url=fila['url_origen'],
                area_responsable=fila['area_responsable'],
            )
            previo = puntajes.get(tramite.id)
            if previo is None or similitud > previo[1]:
                puntajes[tramite.id] = (tramite, similitud)

        ordenados = sorted(puntajes.values(), key=lambda par: -par[1])[:limite]
        for tramite, similitud in ordenados:
            tramite.puntaje_relevancia = round(similitud, 3)
        return [tramite for tramite, _ in ordenados]

    async def _relacionados_lexicos(
        self, tramite_id: UUID, limite: int
    ) -> list[TramiteProbable]:
        """Fallback sin embeddings: similitud Jaccard sobre nombre+descripción+requisitos."""
        filas = await self._repository.obtener_muchos(QUERY_TRAMITES_CATALOGO)
        origen = next((fila for fila in filas if fila['id'] == tramite_id), None)
        if origen is None:
            return []

        perfil = _tokens(
            f"{origen['nombre']} {origen['descripcion'] or ''} "
            f"{' '.join(origen['requisitos'] or [])}"
        )
        if not perfil:
            return []

        puntajes: list[tuple[TramiteProbable, float]] = []
        for fila in filas:
            if fila['id'] == tramite_id:
                continue
            candidato = _tokens(
                f"{fila['nombre']} {fila['descripcion'] or ''} "
                f"{' '.join(fila['requisitos'] or [])}"
            )
            similitud = _jaccard(perfil, candidato)
            if similitud < UMBRAL_RELACION_LEXICO:
                continue
            puntajes.append(
                (
                    TramiteProbable(
                        id=fila['id'],
                        nombre=fila['nombre'],
                        requisitos=list(fila['requisitos'] or []),
                        costo=float(fila['costo'] or 0.0),
                        duracion_estimada_dias=int(fila['duracion_estimada_dias'] or 0),
                        area_responsable=fila['area_responsable'],
                    ),
                    similitud,
                )
            )

        ordenados = sorted(puntajes, key=lambda par: -par[1])[:limite]
        for tramite, similitud in ordenados:
            tramite.puntaje_relevancia = round(similitud, 3)
        return [tramite for tramite, _ in ordenados]

    @staticmethod
    def _vector_medio(embeddings) -> list[float] | None:
        """Centroide de los embeddings de un trámite (promedio componente a componente)."""
        vectores = [e for e in embeddings if e]
        if not vectores:
            return None
        matriz = np.asarray(vectores, dtype=np.float32)
        media = matriz.mean(axis=0)
        norma = float(np.linalg.norm(media))
        if norma == 0.0:
            return None
        return (media / norma).tolist()