import pytest
from pydantic import ValidationError

from app.schemas.detail import DetailsCreate, DetailsRead


def test_detail_create_valid() -> None:
    """
    Vérifie la création valide d'une instance de DetailsCreate.
    S'assure que les champs 'produit_id' et 'quantite' sont correctement initialisés.
    """
    payload = {
        "produit_id": 1,
        "quantite": 3,
    }
    details = DetailsCreate(**payload)

    assert details.produit_id == 1
    assert details.quantite == 3


def test_detail_create_invalid_id() -> None:
    """
    Vérifie que la création d'un détail avec un 'produit_id' non entier
    lève bien une ValidationError.
    """
    payload = {"produit_id": "abc", "quantite": 3}
    with pytest.raises(ValidationError):
        DetailsCreate(**payload)  # type: ignore[arg-type]


def test_detail_read_from_dict() -> None:
    """
    Vérifie la création d'une instance de DetailsRead depuis un dictionnaire.
    S'assure que les valeurs sont correctement assignées.
    """
    payload = {"produit_id": 1, "quantite": 3}
    details = DetailsRead(**payload)

    assert details.produit_id == 1
    assert details.quantite == 3
