from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def unique_email(prefix : str ="user") -> str:
    return f"{prefix}_{uuid4().hex}@example.com"


def test_create_user_endpoint() -> None:
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    email = unique_email("alice")

    resp = client.post(
        "/users/",
        json={
            "nom": "Alice",
            "prenom": "Tester",
            "email": email,
            "adresse": "123 Rue Test",
            "telephone": "0123456789",
            "role_id": role_id,
            "mot_de_passe": "securepassword123",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] is not None
    assert data["email"] == email
    assert data["nom"] == "Alice"
    assert data["prenom"] == "Tester"
    assert data["role_id"] == role_id


def test_read_users_endpoint() -> None:
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    u1 = {
        "nom": "User1",
        "prenom": "One",
        "email": unique_email("user1"),
        "adresse": "Adr 1",
        "telephone": "111",
        "role_id": role_id,
        "mot_de_passe": "user1password",
    }
    u2 = {
        "nom": "User2",
        "prenom": "Two",
        "email": unique_email("user2"),
        "adresse": "Adr 2",
        "telephone": "222",
        "role_id": role_id,
        "mot_de_passe": "user2password",
    }

    assert client.post("/users/", json=u1).status_code == 201
    assert client.post("/users/", json=u2).status_code == 201

    resp = client.get("/users/")
    assert resp.status_code == 200
    data = resp.json()
    emails = {u["email"] for u in data}
    assert u1["email"] in emails
    assert u2["email"] in emails


def test_read_user_endpoint() -> None:
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    email = unique_email("izak")

    created = client.post(
        "/users/",
        json={
            "nom": "Izak",
            "prenom": "Tester",
            "email": email,
            "adresse": "456 Rue Exemple",
            "telephone": "9876543210",
            "role_id": role_id,
            "mot_de_passe": "izaksecurepass",
        },
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    resp = client.get(f"/users/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["email"] == email
    assert data["nom"] == "Izak"

    resp_404 = client.get("/users/999999")
    assert resp_404.status_code == 404


def test_update_user_endpoint() -> None:
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    email = unique_email("david")

    created = client.post(
        "/users/",
        json={
            "nom": "David",
            "prenom": "Updater",
            "email": email,
            "adresse": "Initial Address",
            "telephone": "0000000000",
            "role_id": role_id,
            "mot_de_passe": "davidsecurepass",
        },
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    new_email = unique_email("david_updated")

    resp = client.put(
        f"/users/{user_id}",
        json={
            "email": new_email,
            "adresse": "Updated Address",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["email"] == new_email
    assert data["adresse"] == "Updated Address"

    resp_404 = client.put("/users/999999", json={"email": unique_email("nouveau")})
    assert resp_404.status_code == 404


def test_delete_user_endpoint() -> None:
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    email = unique_email("eva")

    created = client.post(
        "/users/",
        json={
            "nom": "Eva",
            "prenom": "Delete",
            "email": email,
            "adresse": "123 Rue Suppression",
            "telephone": "123123123",
            "role_id": role_id,
            "mot_de_passe": "secreteva1234",
        },
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    resp = client.delete(f"/users/{user_id}")
    assert resp.status_code == 204

    get_again = client.get(f"/users/{user_id}")
    assert get_again.status_code == 404
