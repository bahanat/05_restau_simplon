from collections.abc import Generator

import pytest
from sqlmodel import Session, create_engine

from app.core.config import settings

test_url = settings.DATABASE_URL
engine = create_engine(test_url, echo=True)


@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()

    with Session(bind=connection) as session:
        yield session

    transaction.rollback()
    connection.close()
