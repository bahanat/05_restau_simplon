from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .commandes_et_produits import Commande


class RoleEnum(str, Enum):
    """
    Enumération des rôles possibles pour les utilisateurs.
    """

    admin = "admin"
    client = "client"
    serveur = "serveur"


class Role(SQLModel, table=True):
    """
    Modèle représentant un rôle attribué à un ou plusieurs utilisateurs.
    """

    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: RoleEnum

    # Relation avec les utilisateurs ayant ce rôle
    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    """
    Modèle représentant un utilisateur.
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    email: str = Field(
        index=True, sa_column_kwargs={"unique": True}
    )  # Email unique pour chaque utilisateur
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    mot_de_passe: str
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    date_creation: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relations
    role: Optional[Role] = Relationship(
        back_populates="users"
    )  # Lien vers le rôle de l'utilisateur
    commandes: List["Commande"] = Relationship(
        back_populates="client"
    )  # Commandes passées par l'utilisateur
