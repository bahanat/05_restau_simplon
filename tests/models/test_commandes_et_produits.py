from sqlalchemy import inspect
from sqlmodel import Session


def test_tables_creation(session: Session) -> None:
    """
    Vérifie que toutes les tables attendues sont créées dans la base de données.

    Args:
        session (Session): Session SQLAlchemy/SQLModel connectée à la base de test.

    Raises:
        AssertionError: Si une ou plusieurs tables attendues ne sont pas présentes.
    """
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

    # Vérifie que toutes les tables attendues existent
    assert expected_tables.issubset(set(tables))
