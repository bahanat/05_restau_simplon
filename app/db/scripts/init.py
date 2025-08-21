from typing import Optional

from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel, create_engine

from app.core.config import settings
from app.models.commandes_et_produits import (  # noqa: F401
    Categorie,
    Commande,
    DetailCommande,
    Produit,
)
from app.models.users_et_roles import Role, User  # noqa: F401


def init_db(engine: Optional[Engine] = None) -> Engine:
    """Initialise la base de données (par défaut Postgres)."""
    if engine is None:
        engine = create_engine(settings.DATABASE_URL, echo=True)

    try:
        with engine.connect() as conn:
            version = conn.exec_driver_sql("SELECT version();").scalar()
            print("Connexion à la base réussie. Version:", version)

    except OperationalError as e:
        print("Connexion échouée :", e)
        raise

    SQLModel.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    init_db()
