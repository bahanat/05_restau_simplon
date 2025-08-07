from typing import Optional, List, Dict
from datetime import datetime
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.detail import DetailsCreate
from app.crud.details import update_details_commande

from app.models.commandes_et_produits import (
    Commande,
    Produit,
    DetailCommande,
    StatusEnum,
)
from app.models.users_et_roles import User


# --- Create ---
def create_commande(
    session: Session,
    client_id: int,
    details: List[DetailsCreate],
    date_commande: Optional[datetime] = None,
    statut: Optional[str] = None,
) -> Commande:
    try:
        commande = Commande(
            client_id=client_id,
            date_commande=date_commande,
            statut=StatusEnum(statut),
            montant_total=0.0,
        )
        session.add(commande)
        session.flush()

        montant_total = 0.0
        for det in details:
            detail = DetailCommande(
                commande_id=commande.id,
                produit_id=det.produit_id,
                quantite=det.quantite,
            )
            session.add(detail)

            produit = session.get(Produit, det.produit_id)
            if produit:
                montant_total += produit.prix * det.quantite

        commande.montant_total = round(montant_total, 2)

        session.commit()
        session.refresh(commande)
        return commande

    except SQLAlchemyError as e:
        session.rollback()
        raise e


# --- Read ---
def get_commande(session: Session, commande_id: int) -> Optional[Commande]:
    statement = select(Commande).where(Commande.id == commande_id)
    result = session.exec(statement)
    return result.one_or_none()


# --- Update ---
def update_commande(
    session: Session, commande_id: int, updates: Dict
) -> Optional[Commande]:
    commande = session.get(Commande, commande_id)
    if not commande:
        return None

    for key, value in updates.items():
        if key != "details" and hasattr(commande, key) and value is not None:
            setattr(commande, key, value)

    if "details" in updates and updates["details"] is not None:
        update_details_commande(session, commande, updates["details"])

    session.commit()
    session.refresh(commande)
    return commande


# --- Delete ---
def delete_commande(session: Session, commande_id: int) -> bool:
    commande = session.get(Commande, commande_id)
    if not commande:
        return False

    try:
        session.delete(commande)
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        raise
