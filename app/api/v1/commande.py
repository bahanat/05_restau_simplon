from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from datetime import datetime

from app.schemas.commande import CommandeCreate, CommandeRead, CommandeUpdate
from app.models.commandes_et_produits import StatusEnum
from app.crud.commande import (
    create_commande,
    get_commande,
    get_commandes,
    update_commande,
    delete_commande,
)
from app.db.session import get_session

router = APIRouter(prefix="/commandes", tags=["commandes"])


@router.post("/", response_model=CommandeRead)
def create_commande_endpoint(
    commande_data: CommandeCreate, session: Session = Depends(get_session)
):
    try:
        return create_commande(session, commande_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{commande_id}", response_model=CommandeRead)
def get_commande_endpoint(commande_id: int, session: Session = Depends(get_session)):
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
):
    commandes = get_commandes(session, client_id, date_commande, statut)
    if not commandes:
        raise HTTPException(
            status_code=404, detail="Aucune commande trouvée avec ces conditions"
        )
    return commandes


@router.patch("/{commande_id}", response_model=CommandeRead)
def update_commande_endpoint(
    commande_id: int,
    commande_update: CommandeUpdate,
    session: Session = Depends(get_session),
):
    try:
        commande = update_commande(session, commande_id, commande_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.delete("/{commande_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commande_endpoint(commande_id: int, session: Session = Depends(get_session)):
    success = delete_commande(session, commande_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
