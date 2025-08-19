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


def test_login_success():
    role_resp = client.post("/roles/", json={"nom": "client"})
    role_id = role_resp.json()["id"]
    user_payload = {
        "nom": "Alice",
        "prenom": "Tester",
        "email": "alice@example.com",
        "adresse": "123 Rue Test",
        "telephone": "0123456789",
        "role_id": role_id,
        "mot_de_passe": "securepass123",
    }
    client.post("/users/", json=user_payload)

    # --- login ---
    resp = client.post(
        "/login",
        json={"email": "alice@example.com", "mot_de_passe": "securepass123"},
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Login OK"
    assert data["user"]["email"] == "alice@example.com"


# --- test login wrong password ---


def test_login_invalid_password():
    role_resp = client.post("/roles/", json={"nom": "client"})
    role_id = role_resp.json()["id"]

    user_payload = {
        "nom": "Bob",
        "prenom": "Tester",
        "email": "bob@example.com",
        "adresse": "456 Rue Test",
        "telephone": "0987654321",
        "role_id": role_id,
        "mot_de_passe": "correctpassword",
    }
    client.post("/users/", json=user_payload)

    resp = client.post(
        "/login",
        json={"email": "bob@example.com", "mot_de_passe": "wrongpassword"},
    )

    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "identifiant errone"


def test_login_nonexistent_email():

    resp = client.post(
        "/login",
        json={"email": "ghost@example.com", "mot_de_passe": "whatever123"},
    )

    assert resp.status_code == 400
    data = resp.json()
    assert data["detail"] == "identifiant errone"
