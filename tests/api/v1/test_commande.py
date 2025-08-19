import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db.session import get_session
from app.main import app
from app.models.commandes_et_produits import (
    Categorie,
    Commande,
    DetailCommande,
    Produit,
)
from app.models.users_et_roles import Role, User


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    return TestClient(app)


def test_create_commande(client, session):
    session.exec(
        text(
            "INSERT INTO produits (id, nom, prix, stock) VALUES (1, 'Produit 1', 10.0, 10)"
        )
    )
    session.commit()

    payload = {
        "client_id": 1,
        "date_commande": "2025-08-19T10:00:00",
        "statut": "en_attente",
        "details": [{"produit_id": 1, "quantite": 2}],
    }

    response = client.post("/commandes/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == 1
    assert data["montant_total"] == 20.0


def test_get_commande_not_found(client):
    response = client.get("/commandes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Commande non trouvée"
