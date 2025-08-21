"""Tests d’intégration pour le CRUD des commandes.

Ce module couvre :
- la création de commande (POST /commandes/),
- la récupération d’une commande par id (GET /commandes/{id}),
- la liste des commandes (GET /commandes/),
- la mise à jour partielle (PATCH /commandes/{id}),
- la suppression (DELETE /commandes/{id}).

Notes :
- Le paramètre `session: Session` est fourni par une fixture pytest (non incluse ici).
- La base doit contenir au moins un utilisateur et des données minimales
pour que les tests passent.
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models.commandes_et_produits import Commande, StatusEnum

client = TestClient(app)


@pytest.mark.parametrize("statut", [StatusEnum.en_attente, StatusEnum.servie])
def test_create_commande(session: Session, statut: StatusEnum) -> None:
    """Crée une commande et vérifie que le statut
    et le client sont correctement renvoyés.

    Args:
        session: Session SQLModel injectée par pytest (non utilisée directement ici).
        statut: Valeur du statut à tester (paramétrée par pytest).

    Assertions:
        - Réponse HTTP 200 (l’endpoint POST /commandes/ n’indique pas de 201 explicite).
        - Le `client_id` renvoyé correspond à la requête.
        - Le `statut` renvoyé correspond à la valeur demandée.
    """
    payload = {
        "client_id": 1,
        "date_commande": datetime.now().isoformat(),
        "statut": statut.value,  # on envoie la valeur string de l'Enum
        "details": [],
    }

    response = client.post("/commandes/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == payload["client_id"]
    assert data["statut"] == statut.value


def test_get_commande(session: Session) -> None:
    """Récupère une commande existante par son identifiant.

    Préconditions:
        - Au moins une commande existe en base
        (créée par un test précédent ou des fixtures).

    Assertions:
        - Réponse HTTP 200.
        - L’`id` retourné correspond à celui demandé.
    """
    commande = session.exec(select(Commande)).first()
    assert commande is not None

    response = client.get(f"/commandes/{commande.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == commande.id


def test_list_commandes(session: Session) -> None:
    """Liste les commandes existantes et vérifie le format de la réponse.

    Assertions:
        - Réponse HTTP 200.
        - Le corps est une liste non vide.
    """
    response = client.get("/commandes/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_commande(session: Session) -> None:
    """Met à jour partiellement une commande (changement de statut).

    Préconditions:
        - Au moins une commande existe en base.

    Remarque:
        - Si la validation exige une chaîne plutôt que l'Enum,
        utilisez `StatusEnum.servie.value`.

    Assertions:
        - Réponse HTTP 200.
        - Le `statut` retourné correspond à la valeur demandée.
    """
    commande = session.exec(select(Commande)).first()
    assert commande is not None

    payload = {"statut": StatusEnum.servie}

    response = client.patch(f"/commandes/{commande.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    # Si vous utilisez .value dans le payload, adaptez également cette assertion.
    assert data["statut"] == StatusEnum.servie


def test_delete_commande(session: Session) -> None:
    """Supprime une commande existante puis vérifie qu’elle n’est plus accessible.

    Préconditions:
        - Au moins une commande existe en base.

    Assertions:
        - Réponse HTTP 204 lors de la suppression.
        - Réponse HTTP 404 lors d’une tentative d’accès ultérieure à la commande.
    """
    commande = session.exec(select(Commande)).first()
    assert commande is not None

    response = client.delete(f"/commandes/{commande.id}")
    assert response.status_code == 204

    response = client.get(f"/commandes/{commande.id}")
    assert response.status_code == 404
