import pytest
from sqlmodel import SQLModel, create_engine, inspect

from app.db.scripts.tables_creation import init_db


@pytest.fixture
def sqlite_engine():
    """Crée un engine SQLite en mémoire pour les tests."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


def test_init_db_creates_tables(sqlite_engine, monkeypatch):
    # ⚡ Patch pour utiliser SQLite au lieu de Postgres
    monkeypatch.setattr(
        "app.db.scripts.tables_creation.create_engine", lambda *a, **k: sqlite_engine
    )

    engine = init_db()

    # Vérifier que les tables existent bien
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = {
        "roles",
        "users",
        "categories",
        "commandes",
        "details_commandes",
        "produits",
    }
    assert expected_tables.issubset(set(tables))
