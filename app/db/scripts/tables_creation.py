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

engine = create_engine(settings.DATABASE_URL, echo=True)

try:
    with engine.connect() as conn:
        print("Connected to DB successfully")
except OperationalError as e:
    print("Failed to connect:", e)

SQLModel.metadata.create_all(engine)
