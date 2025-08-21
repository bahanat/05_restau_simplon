from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

# Création de l'engine SQLModel à partir de l'URL de la base de données
engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """Fournit une session SQLModel pour interagir avec la base de données.

    Utilise un contexte `with` pour garantir que la session est correctement
    fermée après usage, même en cas d'exception.

    Yields:
        Generator[Session, None, None]: Une session SQLModel utilisable pour les
        opérations CRUD.
    """
    with Session(engine) as session:
        yield session
