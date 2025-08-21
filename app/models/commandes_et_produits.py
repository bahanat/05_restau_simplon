from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .users_et_roles import User


class StatusEnum(str, Enum):
    """
    Enumération des différents statuts possibles d'une commande.
    """

    en_attente = "en_attente"
    en_preparation = "en_preparation"
    prete = "prete"
    servie = "servie"


class Categorie(SQLModel, table=True):
    """
    Modèle représentant une catégorie de produits.
    """

    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    produits: List["Produit"] = Relationship(back_populates="categorie")


class Produit(SQLModel, table=True):
    """
    Modèle représentant un produit du menu.
    """

    __tablename__ = "produits"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    prix: float
    categorie_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    stock: int

    # Relations
    categorie: Optional[Categorie] = Relationship(back_populates="produits")
    details_commandes: List["DetailCommande"] = Relationship(back_populates="produit")


class Commande(SQLModel, table=True):
    """
    Modèle représentant une commande passée par un client.
    """

    __tablename__ = "commandes"

    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="users.id")
    date_commande: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    statut: StatusEnum = Field(default=StatusEnum.en_attente)
    montant_total: float = Field(default=0.0)

    # Relations
    client: "User" = Relationship(back_populates="commandes")
    details: List["DetailCommande"] = Relationship(
        back_populates="commande",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        },  # Supprime les détails liés lors de la suppression de la commande
    )


class DetailCommande(SQLModel, table=True):
    """
    Modèle représentant le détail d'une commande :
    quels produits et en quelles quantités.
    """

    __tablename__ = "details_commandes"

    commande_id: int = Field(foreign_key="commandes.id", primary_key=True)
    produit_id: int = Field(foreign_key="produits.id", primary_key=True)
    quantite: int

    # Relations
    commande: Commande = Relationship(back_populates="details")
    produit: Produit = Relationship(back_populates="details_commandes")
