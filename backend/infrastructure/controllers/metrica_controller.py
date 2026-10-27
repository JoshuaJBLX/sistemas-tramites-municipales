"""Controladores de métricas y reportes (HU-16 y HU-18).

- `GET /api/metricas`               indicadores agregados del desempeño (HU-16).
- `GET /api/evaluaciones`           calificaciones ciudadanas con su consulta (HU-15).
- `GET /api/reportes`               reporte por periodo (HU-18).
- `GET /api/reportes/exportar`      exportación CSV compatible con Excel (HU-18).

Todos exigen el rol administrador (HU-13). Las consultas se miden sobre la
última auditoría de cada consulta (`DISTINCT ON`), de modo que un acierto de
caché no duplica el indicador.
"""

import csv
import io
import os
from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel

from infrastructure.container import Container, obtener_container
from infrastructure.controllers.dependencias import requiere_administrador

router_metricas = APIRouter(prefix='/api/metricas', tags=['metricas'])
router_evaluaciones = APIRouter(prefix='/api/evaluaciones', tags=['evaluaciones'])
router_reportes = APIRouter(prefix='/api/reportes', tags=['reportes'])

# HU-16 escenario 2: alerta si la tasa de respuestas fundamentadas
# (groundedness >= 0.75, umbral ALTA del evaluador) cae por debajo del mínimo.
UMBRAL_FUNDAMENTADAS = float(os.getenv('UMBRAL_ALERTA_FUNDAMENTADAS', '0.6'))

_LIMITE_REPORTE = 5000

# Última auditoría de cada consulta dentro del periodo.
_QUERY_AUDIT_ACTUAL = """
    SELECT DISTINCT ON (consulta_id)
           consulta_id, confianza, groundedness, afirmaciones_bloqueadas,
           fuera_dominio, entidad_sugerida, duracion_ms, tramite_probable,
           registrado_en
    FROM auditoria_consultas
    WHERE registrado_en >= $1 AND registrado_en < $2
    ORDER BY consulta_id, registrado_en DESC
"""

_QUERY_CONSULTAS_PERIODO = """
    SELECT id, pregunta, intencion, creada_en
    FROM consultas
    WHERE creada_en >= $1 AND creada_en < $2
    ORDER BY creada_en DESC
    LIMIT $3
"""

_QUERY_CONSULTAS_DIA = """
    SELECT to_char(creada_en AT TIME ZONE 'UTC', 'YYYY-MM-DD') AS dia,
           COUNT(*) AS cantidad
    FROM consultas
    WHERE creada_en >= $1 AND creada_en < $2
    GROUP BY 1
    ORDER BY 1
"""

_QUERY_EVALUACIONES_PERIODO = """
    SELECT e.id, e.valoracion, e.comentario, e.creada_en,
           c.id AS consulta_id, c.pregunta, c.intencion
    FROM evaluaciones_calidad e
    JOIN consultas c ON c.id = e.consulta_id
    WHERE e.creada_en >= $1 AND e.creada_en < $2
    ORDER BY e.creada_en DESC
    LIMIT $3
"""


class MetricasResponse(BaseModel):
    """HU-16: indicadores del sistema para el panel de funcionario."""

    periodo_dias: int
    generado_en: datetime
    total_consultas: int
    consultas_periodo: int
    serie_diaria: list[dict]
    por_intencion: list[dict]
    por_confianza: list[dict]
    groundedness_promedio: float
    tasa_fundamentadas: float
    respuestas_bloqueadas: int
    consultas_fuera_dominio: int
    duracion_promedio_ms: int | None
    tramites_frecuentes: list[dict]
    total_evaluaciones: int
    satisfaccion_pct: float | None
    alerta: bool
    alerta_mensaje: str | None = None


class ReporteResponse(BaseModel):
    """HU-18: reporte consolidado de un periodo (antes de exportar)."""

    desde: date
    hasta: date
    generado_en: datetime
    consultas: int
    serie_diaria: list[dict]
    tramites_frecuentes: list[dict]
    por_confianza: list[dict]
    groundedness_promedio: float
    tasa_fundamentadas: float
    respuestas_rechazadas: int
    consultas_fuera_dominio: int
    duracion_promedio_ms: int | None
    total_evaluaciones: int
    utiles: int
    parcialmente_utiles: int
    no_utiles: int
    satisfaccion_pct: float | None


class EvaluacionAdminResponse(BaseModel):
    id: UUID
    consulta_id: UUID
    pregunta: str
    intencion: str | None = None
    valoracion: str
    comentario: str | None = None
    creada_en: datetime


def _rango(dias: int | None = None, desde: date | None = None, hasta: date | None = None):
    """Devuelve el rango [desde, hasta) en UTC con valores por defecto."""
    hoy = datetime.now(timezone.utc).date()
    fecha_desde = desde or (hoy - timedelta(days=(dias or 30) - 1))
    fecha_hasta = (hasta or hoy) + timedelta(days=1)
    return (
        datetime.combine(fecha_desde, datetime.min.time(), tzinfo=timezone.utc),
        datetime.combine(fecha_hasta, datetime.min.time(), tzinfo=timezone.utc),
        fecha_desde,
        (fecha_hasta - timedelta(days=1)),
    )


def _agrupar(filas, campo: str) -> list[dict]:
    acumulado: dict[str, int] = {}
    for fila in filas:
        clave = fila[campo] or 'sin dato'
        acumulado[clave] = acumulado.get(clave, 0) + 1
    return [
        {'clave': clave, 'cantidad': cantidad}
        for clave, cantidad in sorted(
            acumulado.items(), key=lambda item: (-item[1], item[0])
        )
    ]


async def _indicadores(container: Container, desde: datetime, hasta: datetime) -> dict:
    """Agregados compartidos entre /api/metricas y /api/reportes."""
    async with container.connection.pool.acquire() as conexion:
        total_consultas = await conexion.fetchval('SELECT COUNT(*) FROM consultas')
        serie_diaria = await conexion.fetch(
            _QUERY_CONSULTAS_DIA, desde, hasta
        )
        audit = await conexion.fetch(_QUERY_AUDIT_ACTUAL, desde, hasta)
        evaluaciones = await conexion.fetch(
            'SELECT valoracion FROM evaluaciones_calidad '
            'WHERE creada_en >= $1 AND creada_en < $2',
            desde,
            hasta,
        )

    fundamentadas = sum(1 for fila in audit if float(fila['groundedness'] or 0) >= 0.75)
    groundedness_promedio = (
        round(sum(float(fila['groundedness'] or 0) for fila in audit) / len(audit), 4)
        if audit
        else 0.0
    )
    duraciones = [fila['duracion_ms'] for fila in audit if fila['duracion_ms']]
    tramites = [
        fila['tramite_probable']
        for fila in audit
        if fila['tramite_probable']
    ]
    conteo_tramites: dict[str, int] = {}
    for nombre in tramites:
        conteo_tramites[nombre] = conteo_tramites.get(nombre, 0) + 1

    utiles = sum(1 for fila in evaluaciones if fila['valoracion'] == 'util')
    parciales = sum(
        1 for fila in evaluaciones if fila['valoracion'] == 'parcialmente_util'
    )
    no_utiles = sum(1 for fila in evaluaciones if fila['valoracion'] == 'no_util')
    total_evaluaciones = len(evaluaciones)
    satisfaccion = (
        round((utiles + 0.5 * parciales) / total_evaluaciones * 100, 1)
        if total_evaluaciones
        else None
    )

    return {
        'total_consultas': int(total_consultas or 0),
        'consultas_periodo': sum(int(fila['cantidad']) for fila in serie_diaria),
        'serie_diaria': [
            {'fecha': fila['dia'], 'cantidad': int(fila['cantidad'])}
            for fila in serie_diaria
        ],
        'por_confianza': _agrupar(audit, 'confianza'),
        'groundedness_promedio': groundedness_promedio,
        'tasa_fundamentadas': (
            round(fundamentadas / len(audit), 4) if audit else 0.0
        ),
        'respuestas_bloqueadas': sum(
            1 for fila in audit if fila['afirmaciones_bloqueadas']
        ),
        'consultas_fuera_dominio': sum(
            1 for fila in audit if fila['fuera_dominio']
        ),
        'duracion_promedio_ms': (
            round(sum(duraciones) / len(duraciones)) if duraciones else None
        ),
        'tramites_frecuentes': [
            {'nombre': nombre, 'cantidad': cantidad}
            for nombre, cantidad in sorted(
                conteo_tramites.items(), key=lambda item: (-item[1], item[0])
            )[:10]
        ],
        'total_evaluaciones': total_evaluaciones,
        'utiles': utiles,
        'parcialmente_utiles': parciales,
        'no_utiles': no_utiles,
        'satisfaccion_pct': satisfaccion,
    }


@router_metricas.get('', response_model=MetricasResponse)
async def obtener_metricas(
    dias: int = Query(default=30, ge=1, le=90),
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> MetricasResponse:
    """HU-16: indicadores de desempeño y calidad (solo administradores)."""
    desde, hasta, _, _ = _rango(dias=dias)
    datos = await _indicadores(container, desde, hasta)

    async with container.connection.pool.acquire() as conexion:
        por_intencion = await conexion.fetch(
            'SELECT COALESCE(intencion, \'sin dato\') AS clave, COUNT(*) AS cantidad '
            'FROM consultas WHERE creada_en >= $1 AND creada_en < $2 '
            'GROUP BY 1 ORDER BY 2 DESC',
            desde,
            hasta,
        )

    # Escenario 2: alerta si la tasa de respuestas fundamentadas es baja.
    alerta = 0 < datos['total_consultas'] and datos['tasa_fundamentadas'] < UMBRAL_FUNDAMENTADAS
    alerta_mensaje = (
        f'Alerta: solo el {datos["tasa_fundamentadas"] * 100:.1f} % de las respuestas '
        f'del periodo alcanzan el umbral de fundamentación (≥ 75 %). Revisa las '
        f'fuentes indexadas o el modelo.'
        if alerta
        else None
    )

    return MetricasResponse(
        periodo_dias=dias,
        generado_en=datetime.now(timezone.utc),
        consultas_periodo=datos['consultas_periodo'],
        por_intencion=[
            {'clave': fila['clave'], 'cantidad': int(fila['cantidad'])}
            for fila in por_intencion
        ],
        alerta=alerta,
        alerta_mensaje=alerta_mensaje,
        **{
            k: v
            for k, v in datos.items()
            if k
            not in (
                'consultas_periodo',
                'utiles',
                'parcialmente_utiles',
                'no_utiles',
            )
        },
    )


@router_evaluaciones.get('', response_model=list[EvaluacionAdminResponse])
async def listar_evaluaciones(
    limite: int = Query(default=50, ge=1, le=200),
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> list[EvaluacionAdminResponse]:
    """HU-15/HU-16: calificaciones ciudadanas con su consulta (solo administradores)."""
    desde, hasta, _, _ = _rango(dias=90)
    async with container.connection.pool.acquire() as conexion:
        filas = await conexion.fetch(
            _QUERY_EVALUACIONES_PERIODO, desde, hasta, limite
        )
    return [EvaluacionAdminResponse(**dict(fila)) for fila in filas]


@router_reportes.get('', response_model=ReporteResponse)
async def generar_reporte(
    desde: date | None = Query(default=None),
    hasta: date | None = Query(default=None),
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> ReporteResponse:
    """HU-18: reporte del periodo (por defecto: últimos 30 días)."""
    fecha_desde, fecha_hasta, d, h = _rango(desde=desde, hasta=hasta)
    datos = await _indicadores(container, fecha_desde, fecha_hasta)

    async with container.connection.pool.acquire() as conexion:
        audit = await conexion.fetch(_QUERY_AUDIT_ACTUAL, fecha_desde, fecha_hasta)

    por_confianza = datos['por_confianza']
    return ReporteResponse(
        desde=d,
        hasta=h,
        generado_en=datetime.now(timezone.utc),
        consultas=datos['consultas_periodo'],
        groundedness_promedio=datos['groundedness_promedio'],
        tasa_fundamentadas=datos['tasa_fundamentadas'],
        consultas_fuera_dominio=datos['consultas_fuera_dominio'],
        duracion_promedio_ms=datos['duracion_promedio_ms'],
        **{
            k: v
            for k, v in datos.items()
            if k
            not in (
                'total_consultas',
                'consultas_periodo',
                'groundedness_promedio',
                'tasa_fundamentadas',
                'respuestas_bloqueadas',
                'consultas_fuera_dominio',
                'duracion_promedio_ms',
                'por_confianza',
            )
        },
        por_confianza=por_confianza,
        respuestas_rechazadas=datos['respuestas_bloqueadas'],
    )


@router_reportes.get('/exportar')
async def exportar_reporte(
    desde: date | None = Query(default=None),
    hasta: date | None = Query(default=None),
    container: Container = Depends(obtener_container),
    _administrador: dict = Depends(requiere_administrador),
) -> Response:
    """HU-18: descarga CSV (UTF-8 con BOM, abre directo en Excel)."""
    fecha_desde, fecha_hasta, d, h = _rango(desde=desde, hasta=hasta)
    async with container.connection.pool.acquire() as conexion:
        consultas = await conexion.fetch(
            _QUERY_CONSULTAS_PERIODO, fecha_desde, fecha_hasta, _LIMITE_REPORTE
        )
        audit = await conexion.fetch(_QUERY_AUDIT_ACTUAL, fecha_desde, fecha_hasta)
        evaluaciones = await conexion.fetch(
            _QUERY_EVALUACIONES_PERIODO, fecha_desde, fecha_hasta, _LIMITE_REPORTE
        )

    audit_por_consulta = {fila['consulta_id']: fila for fila in audit}
    eval_por_consulta = {fila['consulta_id']: fila for fila in evaluaciones}

    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow([
        'consulta_id', 'fecha', 'hora_utc', 'pregunta', 'intencion', 'confianza',
        'groundedness', 'duracion_ms', 'tramite_probable', 'afirmaciones_bloqueadas',
        'fuera_dominio', 'valoracion', 'comentario',
    ])
    for consulta in consultas:
        a = audit_por_consulta.get(consulta['id'])
        e = eval_por_consulta.get(consulta['id'])
        creada = consulta['creada_en']
        escritor.writerow([
            str(consulta['id']),
            creada.strftime('%Y-%m-%d'),
            creada.strftime('%H:%M:%S'),
            consulta['pregunta'],
            consulta['intencion'] or '',
            (a['confianza'] if a else '') or '',
            (f"{float(a['groundedness'] or 0):.4f}" if a else ''),
            (a['duracion_ms'] if a and a['duracion_ms'] else ''),
            (a['tramite_probable'] if a and a['tramite_probable'] else ''),
            ('si' if a and a['afirmaciones_bloqueadas'] else 'no'),
            ('si' if a and a['fuera_dominio'] else 'no'),
            (e['valoracion'] if e else ''),
            (e['comentario'] if e and e['comentario'] else ''),
        ])

    # BOM para que Excel detecte UTF-8; filename con el periodo.
    contenido = '\ufeff' + salida.getvalue()
    nombre = f'reporte_tramites_{d.isoformat()}_a_{h.isoformat()}.csv'
    return Response(
        content=contenido,
        media_type='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename="{nombre}"'},
    )
