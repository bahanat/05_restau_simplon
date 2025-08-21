from collections.abc import Sequence
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.crud.commande import (
    create_commande,
    delete_commande,
    get_commande,
    get_commandes,
    update_commande,
)
from app.db.session import get_session
from app.models.commandes_et_produits import Commande, StatusEnum
from app.schemas.commande import CommandeCreate, CommandeRead, CommandeUpdate

# Router FastAPI pour gérer les commandes
router = APIRouter(prefix="/commandes", tags=["Commandes"])


@router.post("/", response_model=CommandeRead)
def create_commande_endpoint(
    commande_data: CommandeCreate, session: Session = Depends(get_session)
) -> Commande:
    """
    Crée une nouvelle commande.

    Args:
        commande_data (CommandeCreate): Données de la commande à créer.
        session (Session): Session de base de données.

    Raises:
        HTTPException: En cas d'erreur lors de la création.

    Returns:
        Commande: La commande nouvellement créée.
    """
    try:
        return create_commande(session, commande_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{commande_id}", response_model=CommandeRead)
def get_commande_endpoint(
    commande_id: int, session: Session = Depends(get_session)
) -> Commande:
    """
    Récupère une commande par son ID.

    Args:
        commande_id (int): ID de la commande.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la commande n'existe pas.

    Returns:
        Commande: La commande trouvée.
    """
    commande = get_commande(session, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.get("/", response_model=list[CommandeRead])
def list_commandes_endpoint(
    client_id: Optional[int] = None,
    date_commande: Optional[datetime] = None,
    statut: Optional[StatusEnum] = None,
    session: Session = Depends(get_session),
) -> Sequence[Commande]:
    """
    Récupère la liste des commandes, éventuellement filtrées.

    Args:
        client_id (Optional[int]): Filtre par ID du client.
        date_commande (Optional[datetime]): Filtre par date de commande.
        statut (Optional[StatusEnum]): Filtre par statut.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si aucune commande ne correspond aux filtres.

    Returns:
        Sequence[Commande]: Liste des commandes.
    """
    commandes = get_commandes(session, client_id, date_commande, statut)
    if not commandes:
        raise HTTPException(
            status_code=404,
            detail="Aucune commande trouvée avec ces conditions",
        )
    return commandes


@router.patch("/{commande_id}", response_model=CommandeRead)
def update_commande_endpoint(
    commande_id: int,
    commande_update: CommandeUpdate,
    session: Session = Depends(get_session),
) -> Commande:
    """
    Met à jour une commande existante.

    Args:
        commande_id (int): ID de la commande à modifier.
        commande_update (CommandeUpdate): Données à mettre à jour.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la commande n'existe pas ou en cas d'erreur.

    Returns:
        Commande: La commande mise à jour.
    """
    try:
        commande = update_commande(session, commande_id, commande_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.delete("/{commande_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commande_endpoint(
    commande_id: int, session: Session = Depends(get_session)
) -> None:
    """
    Supprime une commande par son ID.

    Args:
        commande_id (int): ID de la commande à supprimer.
        session (Session): Session de base de données.

    Raises:
        HTTPException: Si la commande n'existe pas.

    Returns:
        None
    """
    success = delete_commande(session, commande_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
