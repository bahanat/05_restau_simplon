from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.produit import (
    create_produit,
    delete_produit,
    get_all_produits,
    get_produit_by_id,
    update_produit,
)
from app.db.session import get_session
from app.models.commandes_et_produits import Produit
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate

# Router FastAPI pour la gestion des produits
router = APIRouter(prefix="/produits", tags=["Produits"])


@router.post("/", response_model=ProduitRead)
def create(data: ProduitCreate, session: Session = Depends(get_session)) -> Produit:
    """
    Crée un nouveau produit.

    Args:
        data (ProduitCreate): Données du produit à créer.
        session (Session): Session de base de données (injectée par FastAPI).

    Returns:
        Produit: Le produit nouvellement créé.
    """
    return create_produit(session, data)


@router.get("/", response_model=list[ProduitRead])
def read_all(session: Session = Depends(get_session)) -> Sequence[Produit]:
    """
    Récupère tous les produits disponibles.

    Args:
        session (Session): Session de base de données (injectée par FastAPI).

    Returns:
        Sequence[Produit]: Liste des produits.
    """
    return get_all_produits(session)


@router.get("/{produit_id}", response_model=ProduitRead)
def read_one(produit_id: int, session: Session = Depends(get_session)) -> Produit:
    """
    Récupère un produit spécifique par son identifiant.

    Args:
        produit_id (int): Identifiant du produit recherché.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le produit n'existe pas.

    Returns:
        Produit: Le produit correspondant.
    """
    produit = get_produit_by_id(session, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.put("/{produit_id}", response_model=ProduitRead)
def update(
    produit_id: int,
    data: ProduitUpdate,
    session: Session = Depends(get_session),
) -> Produit:
    """
    Met à jour un produit existant.

    Args:
        produit_id (int): Identifiant du produit à mettre à jour.
        data (ProduitUpdate): Données mises à jour du produit.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le produit n'existe pas.

    Returns:
        Produit: Le produit mis à jour.
    """
    produit = update_produit(session, produit_id, data)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.delete("/{produit_id}", status_code=204)
def delete(produit_id: int, session: Session = Depends(get_session)) -> None:
    """
    Supprime un produit par son identifiant.

    Args:
        produit_id (int): Identifiant du produit à supprimer.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le produit n'existe pas.

    Returns:
        None
    """
    if not delete_produit(session, produit_id):
        raise HTTPException(status_code=404, detail="Produit introuvable")
