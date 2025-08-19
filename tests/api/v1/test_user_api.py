import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import get_session
from app.models import users_et_roles, commandes_et_produits

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(engine)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def test_create_user_endpoint():

    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    resp = client.post(
        "/users/",
        json={
            "nom": "Alice",
            "prenom": "Tester",
            "email": "alice@example.com",
            "adresse": "123 Rue Test",
            "telephone": "0123456789",
            "role_id": role_id,
            "mot_de_passe": "securepassword123",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] is not None
    assert data["email"] == "alice@example.com"
    assert data["nom"] == "Alice"
    assert data["prenom"] == "Tester"
    assert data["role_id"] == role_id


def test_read_users_endpoint():

    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    u1 = {
        "nom": "User1",
        "prenom": "One",
        "email": "user1@example.com",
        "adresse": "Adr 1",
        "telephone": "111",
        "role_id": role_id,
        "mot_de_passe": "user1password",
    }
    u2 = {
        "nom": "User2",
        "prenom": "Two",
        "email": "user2@example.com",
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
    assert {"user1@example.com", "user2@example.com"} <= emails


def test_read_user_endpoint():
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    created = client.post(
        "/users/",
        json={
            "nom": "Izak",
            "prenom": "Tester",
            "email": "izak@example.com",
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
    assert data["email"] == "izak@example.com"
    assert data["nom"] == "Izak"

    resp_404 = client.get("/users/999999")
    assert resp_404.status_code == 404


def test_update_user_endpoint():
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    created = client.post(
        "/users/",
        json={
            "nom": "David",
            "prenom": "Updater",
            "email": "david@example.com",
            "adresse": "Initial Address",
            "telephone": "0000000000",
            "role_id": role_id,
            "mot_de_passe": "davidsecurepass",
        },
    )
    assert created.status_code == 201
    user_id = created.json()["id"]

    resp = client.put(
        f"/users/{user_id}",
        json={
            "email": "david.updated@example.com",
            "adresse": "Updated Address",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["email"] == "david.updated@example.com"
    assert data["adresse"] == "Updated Address"

    resp_404 = client.put("/users/999999", json={"email": "nouveau@example.com"})
    assert resp_404.status_code == 404


def test_delete_user_endpoint():
    r = client.post("/roles/", json={"nom": "client"})
    assert r.status_code in (200, 201)
    role_id = r.json()["id"]

    created = client.post(
        "/users/",
        json={
            "nom": "Eva",
            "prenom": "Delete",
            "email": "eva@example.com",
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
