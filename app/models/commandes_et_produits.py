from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

if TYPE_CHECKING:
    from .users_et_roles import User


class StatusEnum(str, Enum):
    en_attente = "en_attente"
    en_preparation = "en_preparation"
    prete = "prete"
    servie = "servie"


class Categorie(SQLModel, table=True):
    __tablename__ = "categories"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    produits: List["Produit"] = Relationship(back_populates="categorie")


class Produit(SQLModel, table=True):
    __tablename__ = "produits"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    prix: float
    categorie_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    stock: int

    categorie: Optional[Categorie] = Relationship(back_populates="produits")
    details_commandes: List["DetailCommande"] = Relationship(back_populates="produit")


class Commande(SQLModel, table=True):
    __tablename__ = "commandes"
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="users.id")
    date_commande: datetime = Field(default_factory=datetime.now(timezone.utc))
    statut: StatusEnum = Field(default=StatusEnum.en_attente)
    montant_total: float = Field(default=0.0)

    client: "User" = Relationship(back_populates="commandes")
    details: List["DetailCommande"] = Relationship(
        back_populates="commande",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class DetailCommande(SQLModel, table=True):
    __tablename__ = "details_commandes"
    commande_id: int = Field(foreign_key="commandes.id", primary_key=True)
    produit_id: int = Field(foreign_key="produits.id", primary_key=True)
    quantite: int

    commande: Commande = Relationship(back_populates="details")
    produit: Produit = Relationship(back_populates="details_commandes")


from app.models.users_et_roles import User  # ligne a enlever pour merge
