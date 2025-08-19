import pytest
from sqlalchemy import inspect
from sqlmodel import SQLModel, create_engine

from app.models.commandes_et_produits import (  # noqa: F401
    Categorie,
    Commande,
    DetailCommande,
    Produit,
)
from app.models.users_et_roles import Role, User  # noqa: F401


@pytest.fixture
def engine():
    return create_engine("sqlite:///:memory:")


def test_tables_creation(engine):
    SQLModel.metadata.create_all(engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "produits" in tables
    assert "commandes" in tables
    assert "details_commandes" in tables
    assert "categories" in tables
