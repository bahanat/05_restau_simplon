import pytest
from pydantic import ValidationError

from app.schemas.detail import DetailsCreate, DetailsRead


def test_detail_create_valid() -> None:
    payload = {
        "produit_id": 1,
        "quantite": 3,
    }
    details = DetailsCreate(**payload)

    assert details.produit_id == 1
    assert details.quantite == 3


def test_detail_create_invalid_id() -> None:
    payload = {"produit_id": "abc", "quantite": 3}
    with pytest.raises(ValidationError):
        DetailsCreate(**payload)  # type: ignore[arg-type]


def test_detail_read_from_dict() -> None:
    payload = {"produit_id": 1, "quantite": 3}
    details = DetailsRead(**payload)

    assert details.produit_id == 1
    assert details.quantite == 3
