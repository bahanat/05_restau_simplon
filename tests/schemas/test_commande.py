import pytest
from pydantic import ValidationError

from app.schemas.commande import (
    CommandeCreate,
    CommandeRead,
    CommandeUpdate,
    StatusEnum,
)


def test_commande_create_valid() -> None:
    payload = {
        "client_id": 1,
        "date_commande": "2025-08-19T10:00:00",
        "statut": "en_attente",
        "montant_total": 20.0,
        "details": [{"produit_id": 1, "quantite": 2}],
    }
    commande = CommandeCreate(**payload)  # type: ignore[arg-type]

    assert commande.client_id == 1
    assert commande.statut == StatusEnum.en_attente
    assert commande.details[0].produit_id == 1
    assert commande.details[0].quantite == 2


def test_commande_create_invalid_statut() -> None:
    payload = {
        "client_id": 1,
        "statut": "invalide",
        "details": [{"produit_id": 1, "quantite": 2}],
    }
    with pytest.raises(ValidationError):
        CommandeCreate(**payload)  # type: ignore[arg-type]


def test_commande_read_from_dict() -> None:
    payload = {
        "id": 42,
        "client_id": 1,
        "date_commande": "2025-08-19T10:00:00",
        "statut": "prete",
        "montant_total": 50.0,
        "details": [{"produit_id": 1, "quantite": 5}],
    }
    commande = CommandeRead(**payload)  # type: ignore[arg-type]

    assert commande.id == 42
    assert commande.statut == StatusEnum.prete
    assert commande.details[0].quantite == 5


def test_commande_update_partial() -> None:
    payload = {"statut": "servie"}
    update = CommandeUpdate(**payload)  # type: ignore[arg-type]

    assert update.statut == StatusEnum.servie
    assert update.client_id is None
    assert update.date_commande is None


def test_commande_update_with_details() -> None:
    payload = {
        "client_id": 99,
        "details": [{"produit_id": 2, "quantite": 3}],
    }
    update = CommandeUpdate(**payload)  # type: ignore[arg-type]

    assert update.client_id == 99
    assert update.details is not None
    assert update.details[0].produit_id == 2
    assert update.details[0].quantite == 3
