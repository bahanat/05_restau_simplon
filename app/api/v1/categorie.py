from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.categorie import (
    create_categorie,
    delete_categorie,
    get_all_categories,
    get_categorie_by_id,
    update_categorie,
)
from app.db.session import get_session
from app.models.commandes_et_produits import Categorie
from app.schemas.categorie import (
    CategorieCreate,
    CategorieRead,
    CategorieUpdate,
)

# Router FastAPI pour la gestion des catégories
router = APIRouter(prefix="/categories", tags=["Catégories"])


@router.post("/", response_model=CategorieRead)
def create(data: CategorieCreate, session: Session = Depends(get_session)) -> Categorie:
    """
    Crée une nouvelle catégorie.

    Args:
        data (CategorieCreate): Données de la nouvelle catégorie.
        session (Session): Session de base de données.

    Returns:
        Categorie: La catégorie créée.
    """
    return create_categorie(session, data)


@router.get("/", response_model=list[CategorieRead])
def read(session: Session = Depends(get_session)) -> Sequence[Categorie]:
    """
    Récupère la liste de toutes les catégories.

    Args:
        session (Session): Session de base de données.

    Returns:
        Sequence[Categorie]: Liste des catégories.
    """
    return get_all_categories(session)


@router.get("/{categorie_id}", response_model=CategorieRead)
def read_one(categorie_id: int, session: Session = Depends(get_session)) -> Categorie:
    """
    Récupère une catégorie spécifique par son ID.

    Args:
        categorie_id (int): ID de la catégorie.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la catégorie n'existe pas.

    Returns:
        Categorie: La catégorie correspondante.
    """
    categorie = get_categorie_by_id(session, categorie_id)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie


@router.put("/{categorie_id}", response_model=CategorieRead)
def update(
    categorie_id: int,
    data: CategorieUpdate,
    session: Session = Depends(get_session),
) -> Categorie:
    """
    Met à jour une catégorie existante.

    Args:
        categorie_id (int): ID de la catégorie à modifier.
        data (CategorieUpdate): Données à mettre à jour.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la catégorie n'existe pas.

    Returns:
        Categorie: La catégorie mise à jour.
    """
    categorie = update_categorie(session, categorie_id, data)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie


@router.delete("/{categorie_id}", status_code=204)
def delete(categorie_id: int, session: Session = Depends(get_session)) -> None:
    """
    Supprime une catégorie par son ID.

    Args:
        categorie_id (int): ID de la catégorie à supprimer.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la catégorie n'existe pas.

    Returns:
        None
    """
    if not delete_categorie(session, categorie_id):
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
