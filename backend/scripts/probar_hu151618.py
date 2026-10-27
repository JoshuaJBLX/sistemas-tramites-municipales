"""Pruebas de HU-15 (retroalimentación), HU-16 (métricas) y HU-18 (reportes).

Ejecuta comprobaciones contra la API real con un `TestClient` de FastAPI.

Uso (desde backend/), con las env vars de Postgres y OPENAI_* apuntando al
entorno a probar, más la contraseña del administrador:
    ADMIN_PASSWORD=... python -m scripts.probar_hu151618
"""

import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

CORREO_ADMIN = os.getenv('ADMIN_CORREO', 'admin@munihuancayo.gob.pe')
PASSWORD_ADMIN = os.getenv('ADMIN_PASSWORD', '')


def verificar(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise AssertionError(mensaje)
    print(f'   OK {mensaje}')


def main() -> None:
    if not PASSWORD_ADMIN:
        raise SystemExit('Define ADMIN_PASSWORD (la del administrador a probar).')

    from main import app

    with TestClient(app) as cliente:
        print('0) Preparación: login admin + consulta de prueba')
        r = cliente.post(
            '/api/auth/login', json={'correo': CORREO_ADMIN, 'password': PASSWORD_ADMIN}
        )
        verificar(r.status_code == 200, 'login admin 200')
        auth = {'Authorization': f"Bearer {r.json()['access_token']}"}

        r = cliente.post('/api/consultas', json={'pregunta': 'hola'})
        verificar(r.status_code == 200, 'POST /api/consultas 200')
        consulta_id = r.json()['consulta_id']

        # ---------- HU-15 ----------
        print('HU-15) Retroalimentación ciudadana')
        r = cliente.post(
            f'/api/consultas/{consulta_id}/evaluacion',
            json={'valoracion': 'util', 'comentario': 'Muy clara, gracias'},
        )
        verificar(r.status_code == 201, 'calificar 201 (crea)')
        eval_id = r.json()['id']

        r = cliente.post(
            f'/api/consultas/{consulta_id}/evaluacion',
            json={'valoracion': 'no_util'},
        )
        verificar(r.status_code == 201, 'recalificar 201 (actualiza)')
        verificar(
            r.json()['valoracion'] == 'no_util',
            'la recalificación cambia la valoración',
        )
        verificar(
            r.json()['comentario'] == 'Muy clara, gracias',
            'el comentario previo se conserva si el nuevo no lo envía',
        )

        r = cliente.get(f'/api/consultas/{consulta_id}/evaluacion')
        verificar(r.status_code == 200, 'GET evaluación 200')
        verificar(r.json()['id'] == eval_id, 'devuelve la misma evaluación')

        r = cliente.post(
            '/api/consultas/00000000-0000-0000-0000-000000000099/evaluacion',
            json={'valoracion': 'util'},
        )
        verificar(r.status_code == 404, 'consulta inexistente -> 404')

        r = cliente.post(
            f'/api/consultas/{consulta_id}/evaluacion', json={'valoracion': 'regular'}
        )
        verificar(r.status_code == 422, 'valoración inválida -> 422')

        # ---------- HU-16 ----------
        print('HU-16) Métricas y monitoreo')
        r = cliente.get('/api/metricas')
        verificar(r.status_code == 401, 'GET /api/metricas sin token -> 401')

        r = cliente.get('/api/metricas?dias=7', headers=auth)
        verificar(r.status_code == 200, 'GET /api/metricas con token -> 200')
        m = r.json()
        for campo in (
            'total_consultas', 'consultas_periodo', 'serie_diaria', 'por_intencion',
            'por_confianza', 'groundedness_promedio', 'tasa_fundamentadas',
            'respuestas_bloqueadas', 'consultas_fuera_dominio', 'tramites_frecuentes',
            'total_evaluaciones', 'satisfaccion_pct', 'alerta',
        ):
            verificar(campo in m, f'campo "{campo}" presente')
        verificar(m['total_consultas'] >= 1, 'total_consultas >= 1')
        verificar(m['total_evaluaciones'] >= 1, 'total_evaluaciones >= 1')
        verificar(
            isinstance(m['alerta'], bool), 'alerta es booleano (escenario 2)'
        )

        r = cliente.get('/api/metricas?dias=999', headers=auth)
        verificar(r.status_code == 422, 'dias fuera de rango -> 422')

        r = cliente.get('/api/evaluaciones', headers=auth)
        verificar(r.status_code == 200, 'GET /api/evaluaciones 200')
        verificar(
            any(item['consulta_id'] == consulta_id for item in r.json()),
            'la evaluación creada aparece en el listado admin',
        )

        # ---------- HU-18 ----------
        print('HU-18) Reportes y exportación')
        r = cliente.get('/api/reportes')
        verificar(r.status_code == 401, 'GET /api/reportes sin token -> 401')

        r = cliente.get('/api/reportes', headers=auth)
        verificar(r.status_code == 200, 'GET /api/reportes con token -> 200')
        rep = r.json()
        for campo in (
            'desde', 'hasta', 'generado_en', 'consultas', 'serie_diaria',
            'tramites_frecuentes', 'por_confianza', 'groundedness_promedio',
            'tasa_fundamentadas', 'respuestas_rechazadas', 'satisfaccion_pct',
            'utiles', 'parcialmente_utiles', 'no_utiles',
        ):
            verificar(campo in rep, f'campo reporte "{campo}" presente')
        verificar(rep['consultas'] >= 1, 'reporte con consultas reales')
        verificar(rep['utiles'] + rep['parcialmente_utiles'] + rep['no_utiles'] == rep['total_evaluaciones'],
                  'desglose de evaluaciones cuadra con el total')

        r = cliente.get('/api/reportes/exportar', headers=auth)
        verificar(r.status_code == 200, 'exportar CSV 200')
        verificar(
            'text/csv' in r.headers.get('content-type', ''),
            'content-type es text/csv',
        )
        verificar(
            'attachment' in r.headers.get('content-disposition', ''),
            'cabecera de descarga (attachment)',
        )
        cuerpo = r.content.decode('utf-8-sig')
        verificar(cuerpo.splitlines()[0].startswith('consulta_id,'), 'cabecera CSV')
        verificar(
            any(consulta_id in linea for linea in cuerpo.splitlines()),
            'la consulta de prueba está en el CSV',
        )
        verificar(r.content.startswith(b'\xef\xbb\xbf'), 'BOM UTF-8 para Excel')

        print('\n=== HU-15 + HU-16 + HU-18: todas las comprobaciones pasaron ===')


if __name__ == '__main__':
    main()
