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


def test_create_role_endpoint():
    resp = client.post("/roles/", json={"nom": "client"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["nom"] == "client"
    assert "id" in data


def test_read_roles_endpoint():
    client.post("/roles/", json={"nom": "admin"})
    client.post("/roles/", json={"nom": "client"})

    resp = client.get("/roles/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    noms = {r["nom"] for r in data}
    assert "admin" in noms and "client" in noms


def test_read_role_endpoint():
    created = client.post("/roles/", json={"nom": "serveur"})
    assert created.status_code == 201
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
    role_id = created.json()["id"]

    resp = client.put(f"/roles/{role_id}", json={"nom": "admin"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == role_id
    assert data["nom"] == "admin"

    resp_404 = client.put("/roles/999999", json={"nom": "serveur"})
    assert resp_404.status_code == 404


def test_delete_role_endpoint():
    created = client.post("/roles/", json={"nom": "client"})
    role_id = created.json()["id"]

    resp = client.delete(f"/roles/{role_id}")
    assert resp.status_code == 200
    payload = resp.json()
    assert "message" in payload
    assert "utilisateurs_affectés" in payload
    assert payload["count"] == 0

    get_again = client.get(f"/roles/{role_id}")
    assert get_again.status_code == 404
