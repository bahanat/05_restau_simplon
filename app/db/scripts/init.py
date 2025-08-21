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
    """
    Initialise la base de données.

    Cette fonction crée toutes les tables définies dans les modèles SQLModel
    et vérifie la connexion à la base de données. Si aucun moteur n'est fourni,
    elle utilise l'URL de la base définie dans `settings.DATABASE_URL`.

    Args:
        engine (Optional[Engine]): Moteur SQLAlchemy à utiliser pour la connexion.
            Si None, un moteur est créé automatiquement
            avec l'URL définie dans `settings`.

    Returns:
        Engine: L'objet Engine SQLAlchemy utilisé pour la connexion à la base.

    Raises:
        OperationalError: Si la connexion à la base de données échoue.
    """
    if engine is None:
        engine = create_engine(settings.DATABASE_URL, echo=True)

    try:
        with engine.connect() as conn:
            version = conn.exec_driver_sql("SELECT version();").scalar()
            print("Connexion à la base réussie. Version:", version)

    except OperationalError as e:
        print("Connexion échouée :", e)
        raise

    # Crée toutes les tables définies dans les modèles SQLModel
    SQLModel.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    """
    Point d'entrée pour exécuter le script directement.
    Initialise la base de données et crée toutes les tables.
    """
    init_db()
