from collections.abc import Sequence
from datetime import datetime
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from app.crud.details import update_details_commande
from app.models.commandes_et_produits import (
    Commande,
    DetailCommande,
    Produit,
    StatusEnum,
)
from app.schemas.commande import CommandeCreate, CommandeUpdate


# --- Create ---
def create_commande(session: Session, commande_data: CommandeCreate) -> Commande:
    """Crée une nouvelle commande avec ses détails et calcule le montant total.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        commande_data (CommandeCreate): Les données de la commande à créer,
        incluant le client et les détails.

    Returns:
        Commande: La commande créée et persistée en base.

    Raises:
        SQLAlchemyError: En cas d'erreur lors de la transaction,
        celle-ci est rollbackée.
    """
    try:
        commande = Commande(
            client_id=commande_data.client_id,
            date_commande=commande_data.date_commande,
            statut=commande_data.statut or StatusEnum.en_attente,
            montant_total=0.0,
        )
        session.add(commande)
        session.flush()

        montant_total = 0.0
        for det in commande_data.details:
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
def get_commandes(
    session: Session,
    client_id: Optional[int] = None,
    date_commande: Optional[datetime] = None,
    statut: Optional[StatusEnum] = None,
) -> Sequence[Commande]:
    """Récupère une liste de commandes filtrée selon différents critères.

    Args:
        session (Session): La session SQLModel utilisée pour la requête.
        client_id (Optional[int]): Filtre par identifiant de client.
        date_commande (Optional[datetime]): Filtre par date de commande.
        statut (Optional[StatusEnum]): Filtre par statut de commande.

    Returns:
        Sequence[Commande]: Une liste de commandes correspondant aux filtres.
    """
    statement = select(Commande)

    if client_id is not None:
        statement = statement.where(Commande.client_id == client_id)
    if date_commande is not None:
        statement = statement.where(
            Commande.date_commande
            >= datetime.combine(date_commande, datetime.min.time()),
            Commande.date_commande
            < datetime.combine(date_commande, datetime.max.time()),
        )
    if statut is not None:
        statement = statement.where(Commande.statut == statut)

    result = session.exec(statement)
    return result.all()


# --- Read (par id)---
def get_commande(session: Session, commande_id: int) -> Optional[Commande]:
    """Récupère une commande spécifique par son identifiant.

    Args:
        session (Session): La session SQLModel utilisée pour la requête.
        commande_id (int): L'identifiant de la commande à récupérer.

    Returns:
        Optional[Commande]: La commande correspondante ou None si elle n'existe pas.
    """
    statement = select(Commande).where(Commande.id == commande_id)
    result = session.exec(statement)
    return result.one_or_none()


# --- Update ---
def update_commande(
    session: Session, commande_id: int, commande_data: CommandeUpdate
) -> Optional[Commande]:
    """Met à jour une commande existante avec de nouvelles informations.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        commande_id (int): L'identifiant de la commande à mettre à jour.
        commande_data (CommandeUpdate): Les nouvelles données à appliquer,
        y compris éventuellement les détails.

    Returns:
        Optional[Commande]: La commande mise à jour ou None si elle n'existe pas.
    """
    commande = session.get(Commande, commande_id)
    if not commande:
        return None

    if commande_data.details is not None:
        update_details_commande(session, commande, commande_data.details)

    for key, value in commande_data.model_dump(
        exclude_unset=True, exclude={"details"}
    ).items():
        setattr(commande, key, value)

    session.commit()
    session.refresh(commande)
    return commande


# --- Delete ---
def delete_commande(session: Session, commande_id: int) -> bool:
    """Supprime une commande existante par son identifiant.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        commande_id (int): L'identifiant de la commande à supprimer.

    Returns:
        bool: True si la commande a été supprimée avec succès,
        False si elle n'existait pas.

    Raises:
        SQLAlchemyError: En cas d'erreur lors de la suppression,
        la transaction est rollbackée.
    """
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
