from sqlalchemy import inspect
from sqlmodel import Session


def test_tables_creation(session: Session):
    engine = session.get_bind()
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = {
        "produits",
        "commandes",
        "details_commandes",
        "categories",
        "users",
        "roles",
    }
    assert expected_tables.issubset(set(tables))
