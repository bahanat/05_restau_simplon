from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_role_endpoint() -> None:
    """Teste la création d'un rôle via l'endpoint POST /roles/.

    - Vérifie que le code HTTP est 200 ou 201.
    - Vérifie que le rôle créé possède un nom et un ID.
    """
    resp = client.post("/roles/", json={"nom": "client"})
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["nom"] == "client"
    assert "id" in data


def test_read_roles_endpoint() -> None:
    """Teste la récupération de tous les rôles via l'endpoint GET /roles/.

    - Crée plusieurs rôles.
    - Vérifie que la réponse est une liste et contient tous les rôles.
    """
    client.post("/roles/", json={"nom": "admin"})
    client.post("/roles/", json={"nom": "serveur"})

    resp = client.get("/roles/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    noms = {r["nom"] for r in data}
    assert {"admin", "serveur", "client"} <= noms


def test_read_role_endpoint() -> None:
    """Teste la récupération d'un rôle spécifique via GET /roles/{id}.

    - Vérifie le succès pour un rôle existant.
    - Vérifie que l'accès à un rôle inexistant renvoie 404.
    """
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


def test_update_role_endpoint() -> None:
    """Teste la mise à jour d'un rôle via PUT /roles/{id}.

    - Vérifie que la mise à jour d'un rôle existant fonctionne.
    - Vérifie que la mise à jour d'un rôle inexistant renvoie 404.
    """
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


def test_delete_role_endpoint() -> None:
    """Teste la suppression d'un rôle via DELETE /roles/{id}.

    - Vérifie que la suppression renvoie 200 ou 204 selon l'API.
    - Si 200, vérifie le message et la liste des utilisateurs affectés.
    - Vérifie que le rôle n'existe plus après suppression.
    """
    created = client.post("/roles/", json={"nom": "serveur"})
    assert created.status_code in (200, 201)
    role_id = created.json()["id"]

    resp = client.delete(f"/roles/{role_id}")
    assert resp.status_code in (200, 204)
    if resp.status_code == 200:
        payload = resp.json()
        assert "message" in payload
        assert "utilisateurs_affectés" in payload
        assert isinstance(payload["count"], int)

    get_again = client.get(f"/roles/{role_id}")
    assert get_again.status_code == 404
