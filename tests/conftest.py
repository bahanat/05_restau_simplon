import pytest
<<<<<<< HEAD
from sqlmodel import Session, create_engine

from app.core.config import settings

test_url = settings.DATABASE_URL
engine = create_engine(test_url, echo=True)


@pytest.fixture(scope="function")
def session():
    connection = engine.connect()
    transaction = connection.begin()

    with Session(bind=connection) as session:
        yield session

    transaction.rollback()
    connection.close()
=======
from sqlmodel import Session, SQLModel, create_engine

from app.models import commandes_et_produits, users_et_roles
from tests.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

SQLModel.metadata.create_all(engine)


@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session
>>>>>>> a2a9a7f (feat: :building_construction: creation tests - hashing test + premier fonction crud test_user ok)
