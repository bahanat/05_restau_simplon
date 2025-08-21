from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success() -> None:

    role_resp = client.post("/roles/", json={"nom": "client"})
    role_id = role_resp.json()["id"]

    unique_email = f"alice_{uuid4().hex}@example.com"

    user_payload = {
        "nom": "Alice",
        "prenom": "Tester",
        "email": unique_email,
        "adresse": "123 Rue Test",
        "telephone": "0123456789",
        "role_id": role_id,
        "mot_de_passe": "securepass123",
    }
    client.post("/users/", json=user_payload)

    resp = client.post(
        "/login",
        json={"email": unique_email, "mot_de_passe": "securepass123"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Login OK"
    assert data["user"]["email"] == unique_email


def test_login_invalid_password() -> None:
    role_resp = client.post("/roles/", json={"nom": "client"})
    role_id = role_resp.json()["id"]

    unique_email = f"bob_{uuid4().hex}@example.com"

    user_payload = {
        "nom": "Bob",
        "prenom": "Tester",
        "email": unique_email,
        "adresse": "456 Rue Test",
        "telephone": "0987654321",
        "role_id": role_id,
        "mot_de_passe": "correctpassword",
    }
    client.post("/users/", json=user_payload)

    resp = client.post(
        "/login",
        json={"email": unique_email, "mot_de_passe": "wrongpassword"},
    )

    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "identifiant errone"


def test_login_nonexistent_email() -> None:

    unique_email = f"ghost_{uuid4().hex}@example.com"

    resp = client.post(
        "/login",
        json={"email": unique_email, "mot_de_passe": "whatever123"},
    )

    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "identifiant errone"
