from collections.abc import Generator

import pytest
from sqlmodel import Session, create_engine

from app.core.config import settings

test_url = settings.DATABASE_URL
engine = create_engine(test_url, echo=True)


@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    """
    Fixture pytest pour fournir une session SQLModel isolée pour chaque test.

    - Crée une connexion à la base de données de test.
    - Démarre une transaction.
    - Fournit une session liée à cette connexion.
    - Après le test, annule la transaction et ferme la connexion, assurant
      que les modifications à la base de données ne persistent pas entre les tests.
    """
    connection = engine.connect()
    transaction = connection.begin()

    with Session(bind=connection) as session:
        yield session

    transaction.rollback()
    connection.close()
