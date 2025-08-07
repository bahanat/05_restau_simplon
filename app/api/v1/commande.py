from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.commande import CommandeCreate, CommandeRead, CommandeUpdate
from app.crud.commande import (
    create_commande,
    get_commande,
    update_commande,
    delete_commande,
)
from app.db.session import get_session

router = APIRouter(prefix="/commandes", tags=["commandes"])


@router.post("/", response_model=CommandeRead)
def create_commande_endpoint(
    data: CommandeCreate, session: Session = Depends(get_session)
):
    try:
        commande = create_commande(
            session=session,
            client_id=data.client_id,
            details=data.details,
            date_commande=data.date_commande,
            statut=data.statut,
        )
        return commande
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{commande_id}", response_model=CommandeRead)
def get_commande_endpoint(commande_id: int, session: Session = Depends(get_session)):
    commande = get_commande(session, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.patch("/{commande_id}", response_model=CommandeRead)
def update_commande_endpoint(
    commande_id: int,
    commande_update: CommandeUpdate,
    session: Session = Depends(get_session),
):
    updates = commande_update.dict(exclude_unset=True)
    commande = update_commande(session, commande_id, updates)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@router.delete("/{commande_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commande_endpoint(commande_id: int, session: Session = Depends(get_session)):
    success = delete_commande(session, commande_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
