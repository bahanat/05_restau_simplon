from collections.abc import Sequence

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.commandes_et_produits import Categorie, Produit
from app.schemas.produit import ProduitCreate, ProduitUpdate


# --- Create ---
def create_produit(session: Session, data: ProduitCreate) -> Produit:
    """Crée un nouveau produit dans la base de données.

    Vérifie d'abord si la catégorie associée existe. Si la catégorie
    n'existe pas, une HTTPException est levée.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        data (ProduitCreate): Les données du produit à créer.

    Raises:
        HTTPException: Si la catégorie associée n'existe pas.

    Returns:
        Produit: L'instance du produit créé.
    """
    if data.categorie_id:
        categorie = session.get(Categorie, data.categorie_id)
        if not categorie:
            categories_existantes = session.exec(select(Categorie)).all()
            noms = [f"{c.id} - {c.nom}" for c in categories_existantes]
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Catégorie ID {data.categorie_id} introuvable. "
                    f"Catégories disponibles : {noms}"
                ),
            )

    produit = Produit.model_validate(data)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit


# --- Read ---
def get_all_produits(session: Session) -> Sequence[Produit]:
    """Récupère tous les produits de la base de données.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.

    Returns:
        Sequence[Produit]: Une séquence contenant tous les produits.
    """
    return session.exec(select(Produit)).all()


# --- Read (par id) ---
def get_produit_by_id(session: Session, produit_id: int) -> Produit | None:
    """Récupère un produit par son ID.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        produit_id (int): L'ID du produit à récupérer.

    Returns:
        Produit | None: L'instance du produit si trouvée, sinon None.
    """
    return session.get(Produit, produit_id)


# --- Update ---
def update_produit(
    session: Session, produit_id: int, data: ProduitUpdate
) -> Produit | None:
    """Met à jour un produit existant.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        produit_id (int): L'ID du produit à mettre à jour.
        data (ProduitUpdate): Les données à mettre à jour.

    Returns:
        Produit | None: L'instance du produit mise à jour si elle existe, sinon None.
    """
    produit = session.get(Produit, produit_id)
    if not produit:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(produit, key, value)
    session.commit()
    session.refresh(produit)
    return produit


# --- Delete ---
def delete_produit(session: Session, produit_id: int) -> bool:
    """Supprime un produit par son ID.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        produit_id (int): L'ID du produit à supprimer.

    Returns:
        bool: True si le produit a été supprimé, False si le produit n'existe pas.
    """
    produit = session.get(Produit, produit_id)
    if not produit:
        return False
    session.delete(produit)
    session.commit()
    return True
