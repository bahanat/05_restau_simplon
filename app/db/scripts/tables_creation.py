from sqlmodel import SQLModel, create_engine
from app.core.config import settings
from sqlalchemy.exc import OperationalError

from app.models.commandes_et_produits import *
from app.models.users_et_roles import *

engine = create_engine(settings.DATABASE_URL, echo=True)

try:
    with engine.connect() as conn:
        print("Connected to DB successfully")
except OperationalError as e:
    print("Failed to connect:", e)

SQLModel.metadata.create_all(engine)
