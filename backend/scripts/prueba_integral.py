"""Prueba de integración del backend: roles, HU-03, HU-14, HU-16 y HU-17.

Las contraseñas NO se escriben en el código: se leen de variables de entorno.

Uso (PowerShell):
    $env:POSTGRES_HOST='...'; $env:POSTGRES_PORT='5432'
    $env:POSTGRES_DB='...';   $env:POSTGRES_USER='...'; $env:POSTGRES_PASSWORD='...'
    $env:TEST_ADMIN_PASSWORD='...'
    $env:TEST_REVISOR_PASSWORD='...'
    .venv\\Scripts\\python.exe backend\\scripts\\prueba_integral.py
"""
import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, "backend")
from main import app

ADMIN_CORREO = os.environ.get("TEST_ADMIN_CORREO", "admin@munihuancayo.gob.pe")
REVISOR_CORREO = os.environ.get("TEST_REVISOR_CORREO", "revisor@munihuancayo.gob.pe")


def _password(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise SystemExit(f"Falta la variable de entorno {nombre}")
    return valor


def verificar(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise AssertionError(f"FALLO: {mensaje}")
    print(f"   OK: {mensaje}")


def test_roles_y_accesos() -> None:
    admin_pass = _password("TEST_ADMIN_PASSWORD")
    revisor_pass = _password("TEST_REVISOR_PASSWORD")

    with TestClient(app) as cliente:
        print("\n--- INICIANDO PRUEBA INTEGRAL ---")

        # 1. Login de roles (HU-13)
        r_admin = cliente.post(
            "/api/auth/login", json={"correo": ADMIN_CORREO, "password": admin_pass}
        )
        verificar(r_admin.status_code == 200, "Login Administrador")
        admin_token = r_admin.json()["access_token"]

        r_revisor = cliente.post(
            "/api/auth/login", json={"correo": REVISOR_CORREO, "password": revisor_pass}
        )
        verificar(r_revisor.status_code == 200, "Login Revisor")
        revisor_token = r_revisor.json()["access_token"]

        # 2. Gestión documental (HU-03)
        print("\n--- HU-03: Permisos de Revisor ---")
        headers_revisor = {"Authorization": f"Bearer {revisor_token}"}

        r = cliente.get("/api/documentos")
        verificar(r.status_code == 200, "Listar documentos (público)")

        docs = r.json()
        if docs:
            doc_id = docs[0]["id"]
            r = cliente.put(
                f"/api/documentos/{doc_id}/estado?estado=vigente",
                headers=headers_revisor,
            )
            verificar(r.status_code == 200, "Revisor aprueba documento (HU-03)")

        # 3. Métricas solo administrador (HU-16)
        print("\n--- HU-16: Acceso a Métricas (Revisor NO debería) ---")
        r = cliente.get("/api/metricas", headers=headers_revisor)
        verificar(r.status_code == 403, "Revisor intenta acceder a Métricas (Bloqueado)")

        r = cliente.get("/api/metricas", headers={"Authorization": f"Bearer {admin_token}"})
        verificar(r.status_code == 200, "Administrador accede a Métricas")

        # 4. Derivación y directorio (HU-17)
        print("\n--- HU-17: Derivación y Directorio ---")
        r = cliente.get("/api/oficinas")
        verificar(r.status_code == 200, "Listar oficinas")

        r = cliente.post(
            "/api/consultas",
            json={"pregunta": "Necesito una resolución para aprobar mi expediente"},
        )
        data = r.json()
        verificar(
            "derivacion" in data and data["derivacion"] is not None,
            "Consulta compleja activa derivación",
        )
        print(f"   -> Derivación detectada: {data['derivacion']['oficina']}")

        # 5. Auditoría y marcado (HU-14)
        print("\n--- HU-14: Auditoría y Marcado ---")
        r = cliente.get(
            "/api/consultas?limite=1", headers={"Authorization": f"Bearer {admin_token}"}
        )
        consulta_id = r.json()[0]["id"]

        r = cliente.post(
            f"/api/consultas/{consulta_id}/marcar",
            json={"marcado": True, "nota": "Revisión técnica"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        verificar(r.status_code == 200, "Admin marca consulta como inconsistente")

        print("\n--- PRUEBAS COMPLETADAS CON ÉXITO ---")


if __name__ == "__main__":
    test_roles_y_accesos()
