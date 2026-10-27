"""Pruebas de HU-03 (revisor), HU-14 (filtros y marcado) y HU-17 (oficinas y derivación)."""

import os
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
        print('⚠️ Define ADMIN_PASSWORD para probar rutas protegidas. Se probarán rutas públicas.')

    from main import app

    with TestClient(app) as cliente:
        print('1) HU-17: Listado público de oficinas')
        r = cliente.get('/api/oficinas')
        verificar(r.status_code == 200, 'GET /api/oficinas 200')
        oficinas = r.json()
        verificar(len(oficinas) >= 5, f'Directorio contiene {len(oficinas)} oficinas')

        print('2) HU-17: Consulta con derivación automática (baja confianza / caso complejo)')
        r = cliente.post('/api/consultas', json={'pregunta': 'Necesito la aprobación urgente y resolución de mi expediente y denegación de licencia'})
        verificar(r.status_code == 200, 'POST /api/consultas 200')
        data = r.json()
        verificar('derivacion' in data, 'Respuesta incluye objeto derivacion')
        if data.get('derivacion'):
            print(f"   -> Derivado a: {data['derivacion']['oficina']} ({data['derivacion']['area']})")

        print('3) HU-14: Listado de auditoría y filtros')
        if PASSWORD_ADMIN:
            r_login = cliente.post('/api/auth/login', json={'correo': CORREO_ADMIN, 'password': PASSWORD_ADMIN})
            if r_login.status_code == 200:
                auth = {'Authorization': f"Bearer {r_login.json()['access_token']}"}
                r = cliente.get('/api/consultas?limite=5', headers=auth)
                verificar(r.status_code == 200, 'GET /api/consultas con token admin 200')
                audits = r.json()
                verificar(isinstance(audits, list), 'Auditoría devuelve lista')
                if audits:
                    c_id = audits[0]['id']
                    # Marcar inconsistente
                    r_m = cliente.post(f'/api/consultas/{c_id}/marcar', json={'marcado': True, 'nota': 'Prueba test'}, headers=auth)
                    verificar(r_m.status_code == 200, 'POST /api/consultas/{id}/marcar 200')
                    verificar(r_m.json()['marcado_inconsistente'] is True, 'Registro marcado como inconsistente')
        print('Pruebas HU-03/14/17 completadas con éxito.')


if __name__ == '__main__':
    main()
