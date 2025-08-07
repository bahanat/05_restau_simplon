from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .commandes_et_produits import Commande


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    email: str = Field(index=True, sa_column_kwargs={"unique": True})
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    mot_de_passe: str
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    date_creation: datetime = Field(default_factory=datetime.now(timezone.utc))

    role: Optional[Role] = Relationship(back_populates="users")
    commandes: List["Commande"] = Relationship(back_populates="client")


from app.models.commandes_et_produits import Commande  # ligne a enlever pour merge
