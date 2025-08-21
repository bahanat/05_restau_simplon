import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_role_endpoint():
    resp = client.post("/roles/", json={"nom": "client"})
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["nom"] == "client"
    assert "id" in data


def test_read_roles_endpoint():
    client.post("/roles/", json={"nom": "admin"})
    client.post("/roles/", json={"nom": "serveur"})

    resp = client.get("/roles/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    noms = {r["nom"] for r in data}
    assert {"admin", "serveur", "client"} <= noms


def test_read_role_endpoint():
    created = client.post("/roles/", json={"nom": "serveur"})
    assert created.status_code in (200, 201)
    role_id = created.json()["id"]

    resp = client.get(f"/roles/{role_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == role_id
    assert data["nom"] == "serveur"

    resp_404 = client.get("/roles/999999")
    assert resp_404.status_code == 404


def test_update_role_endpoint():
    created = client.post("/roles/", json={"nom": "client"})
    assert created.status_code in (200, 201)
    role_id = created.json()["id"]

    resp = client.put(f"/roles/{role_id}", json={"nom": "admin"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == role_id
    assert data["nom"] == "admin"

    resp_404 = client.put("/roles/999999", json={"nom": "serveur"})
    assert resp_404.status_code == 404


def test_delete_role_endpoint():
    created = client.post("/roles/", json={"nom": "serveur"})
    assert created.status_code in (200, 201)
    role_id = created.json()["id"]

    resp = client.delete(f"/roles/{role_id}")
    # depende de tu API: puede devolver 200 o 204
    assert resp.status_code in (200, 204)
    if resp.status_code == 200:
        payload = resp.json()
        assert "message" in payload
        assert "utilisateurs_affectés" in payload
        assert isinstance(payload["count"], int)

    get_again = client.get(f"/roles/{role_id}")
    assert get_again.status_code == 404
