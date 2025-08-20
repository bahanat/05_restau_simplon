from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models.commandes_et_produits import Commande, StatusEnum

client = TestClient(app)


@pytest.mark.parametrize("statut", [StatusEnum.en_attente, StatusEnum.servie])
def test_create_commande(session: Session, statut):
    payload = {
        "client_id": 1,
        "date_commande": datetime.now().isoformat(),
        "statut": statut.value,
        "details": [],
    }

    response = client.post("/commandes/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == payload["client_id"]
    assert data["statut"] == statut.value


def test_get_commande(session: Session):
    commande = session.exec(select(Commande)).first()
    assert commande is not None

    response = client.get(f"/commandes/{commande.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == commande.id


def test_list_commandes(session: Session):
    response = client.get("/commandes/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_commande(session: Session):
    commande = session.exec(select(Commande)).first()
    payload = {"statut": StatusEnum.servie}

    response = client.patch(f"/commandes/{commande.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["statut"] == StatusEnum.servie


def test_delete_commande(session: Session):
    commande = session.exec(select(Commande)).first()

    response = client.delete(f"/commandes/{commande.id}")
    assert response.status_code == 204

    response = client.get(f"/commandes/{commande.id}")
    assert response.status_code == 404
