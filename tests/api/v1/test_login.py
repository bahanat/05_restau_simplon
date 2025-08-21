from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success() -> None:
    """Teste la connexion réussie d'un utilisateur avec des identifiants valides.

    - Crée un rôle temporaire "client".
    - Crée un utilisateur unique lié à ce rôle.
    - Tente de se connecter avec le mot de passe correct.
    - Vérifie que le code HTTP est 200 et que l'email renvoyé est correct.
    """
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
    """Teste la connexion avec un mot de passe incorrect.

    - Crée un rôle temporaire "client".
    - Crée un utilisateur unique lié à ce rôle.
    - Tente de se connecter avec un mot de passe erroné.
    - Vérifie que le code HTTP est 400 et le message d'erreur correct.
    """
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
    """Teste la connexion avec un email inexistant.

    - Tente de se connecter avec un email unique qui n'existe pas.
    - Vérifie que le code HTTP est 400 et le message d'erreur correct.
    """
    unique_email = f"ghost_{uuid4().hex}@example.com"

    resp = client.post(
        "/login",
        json={"email": unique_email, "mot_de_passe": "whatever123"},
    )

    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "identifiant errone"
