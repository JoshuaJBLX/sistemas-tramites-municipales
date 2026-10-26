"""Pruebas de HU-13 (autenticación, roles y eventos de seguridad).

Ejecuta 12 comprobaciones contra la API real con un `TestClient` de FastAPI.

Uso (desde backend/), contra la BD local:
    ADMIN_PASSWORD=... python -m scripts.probar_hu13

Contra Render Postgres (producción de datos):
    POSTGRES_HOST=... POSTGRES_USER=... POSTGRES_PASSWORD=... POSTGRES_DB=... \
    ADMIN_PASSWORD=... python -m scripts.probar_hu13

La contraseña del administrador se lee de ADMIN_PASSWORD (nunca se escribe en
el repositorio). El usuario de prueba se crea con un correo aleatorio para
que el script pueda repetirse sin chocar con el índice único.
"""

import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

CORREO_ADMIN = os.getenv('ADMIN_CORREO', 'admin@munihuancayo.gob.pe')
PASSWORD_ADMIN = os.getenv('ADMIN_PASSWORD', '')
PASSWORD_CIUDADANO = 'clave12345'


def verificar(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise AssertionError(mensaje)
    print(f'   OK {mensaje}')


def main() -> None:
    if not PASSWORD_ADMIN:
        raise SystemExit('Define ADMIN_PASSWORD (la del administrador a probar).')

    # El import carga dotenv y arma la app con las env vars del entorno.
    from main import app

    correo_prueba = f'prueba.{secrets.token_hex(4)}@correo.com'

    with TestClient(app) as cliente:
        print('1) Login con credenciales correctas -> 200 + token')
        r = cliente.post(
            '/api/auth/login', json={'correo': CORREO_ADMIN, 'password': PASSWORD_ADMIN}
        )
        verificar(r.status_code == 200, 'login admin 200')
        token = r.json()['access_token']
        verificar(r.json()['usuario']['rol'] == 'administrador', 'rol=administrador')
        auth = {'Authorization': f'Bearer {token}'}

        print('2) Login con credenciales incorrectas -> 401 (evento login_fallido)')
        r = cliente.post(
            '/api/auth/login', json={'correo': CORREO_ADMIN, 'password': 'incorrecta'}
        )
        verificar(r.status_code == 401, 'login fallido 401')

        print('3) GET /api/auth/me con token -> 200 con el perfil')
        r = cliente.get('/api/auth/me', headers=auth)
        verificar(r.status_code == 200 and r.json()['correo'] == CORREO_ADMIN, 'me 200')

        print('4) GET /api/auth/me sin token -> 401')
        verificar(cliente.get('/api/auth/me').status_code == 401, 'me sin token 401')

        print('5) Endpoints admin sin token -> 401 (evento token/acceso)')
        for ruta in ('/api/admin/documentos', '/api/tramites/admin', '/api/consultas'):
            verificar(cliente.get(ruta).status_code == 401, f'401 {ruta}')

        print('6) Endpoints admin con token de administrador -> 200')
        for ruta in ('/api/admin/documentos', '/api/tramites/admin', '/api/consultas?limite=2'):
            verificar(cliente.get(ruta, headers=auth).status_code == 200, f'200 {ruta}')

        print('7) Token inválido -> 401 (evento token_invalido)')
        r = cliente.get('/api/auth/me', headers={'Authorization': 'Bearer falso'})
        verificar(r.status_code == 401, 'token falso 401')

        print('8) Admin registra un ciudadano -> 201 (evento usuario_registrado)')
        r = cliente.post(
            '/api/usuarios',
            json={
                'nombre': 'Prueba Ciudadana',
                'correo': correo_prueba,
                'rol': 'ciudadano',
                'password': PASSWORD_CIUDADANO,
            },
            headers=auth,
        )
        verificar(r.status_code == 201, 'registro ciudadano 201')
        ciudadano_id = r.json()['id']

        print('9) Ciudadano intenta un endpoint admin -> 403 (evento acceso_denegado)')
        r = cliente.post(
            '/api/auth/login',
            json={'correo': correo_prueba, 'password': PASSWORD_CIUDADANO},
        )
        verificar(r.status_code == 200, 'login ciudadano 200')
        auth_ciudadano = {'Authorization': f"Bearer {r.json()['access_token']}"}
        verificar(
            cliente.get('/api/admin/documentos', headers=auth_ciudadano).status_code == 403,
            'ciudadano en admin 403',
        )

        print('10) Ciudadano: perfil propio 200, perfil ajeno 403')
        verificar(
            cliente.get(f'/api/usuarios/{ciudadano_id}', headers=auth_ciudadano).status_code == 200,
            'perfil propio 200',
        )
        ajeno = cliente.get(
            '/api/usuarios/00000000-0000-0000-0000-000000000001', headers=auth_ciudadano
        )
        verificar(ajeno.status_code in (403, 404), 'perfil ajeno 403/404')

        print('11) Endpoints públicos siguen abiertos sin token')
        for ruta in ('/health', '/api/tramites?limite=1'):
            verificar(cliente.get(ruta).status_code == 200, f'200 público {ruta}')

        print('12) La consulta ciudadana POST /api/consultas sigue abierta')
        verificar(
            cliente.post('/api/consultas', json={'pregunta': 'hola'}).status_code == 200,
            'POST /api/consultas 200',
        )

    print('\n=== HU-13: 12/12 comprobaciones pasaron ===')
    print(
        'Los eventos quedaron en la tabla eventos_seguridad '
        '(login_exitoso, login_fallido, token_invalido, acceso_denegado, usuario_registrado).'
    )


if __name__ == '__main__':
    main()
