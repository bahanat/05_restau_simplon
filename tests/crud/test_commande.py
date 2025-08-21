from datetime import datetime

from sqlmodel import Session

from app.crud import commande as crud_commande
from app.schemas.commande import CommandeCreate, CommandeUpdate, StatusEnum
from app.schemas.detail import DetailsCreate


def test_create_commande(session: Session) -> None:
    """Teste la création d'une commande avec détails et vérifie la persistance.

    Vérifie que l'objet créé a un ID, un montant total calculé et que les détails
    sont correctement associés.
    """
    commande_data = CommandeCreate(
        client_id=1,
        statut=StatusEnum.en_attente,
        date_commande=datetime.now(),
        details=[DetailsCreate(produit_id=1, quantite=2)],
    )
    commande = crud_commande.create_commande(session, commande_data)
    assert commande.id is not None
    assert commande.montant_total != 0.0
    assert len(commande.details) == 1


def test_get_commande(session: Session) -> None:
    """Teste la récupération d'une commande existante par ID."""
    fetched = crud_commande.get_commande(session, 1)
    assert fetched is not None
    assert fetched.id == 1


def test_update_commande(session: Session) -> None:
    """Teste la mise à jour du statut d'une commande existante."""
    update_data = CommandeUpdate(statut=StatusEnum.servie)
    updated = crud_commande.update_commande(session, 1, update_data)
    assert updated is not None


def test_delete_commande(session: Session) -> None:
    """Teste la suppression d'une commande.

    Vérifie que la commande est supprimée et qu'elle n'existe plus en base.
    """
    commande_data = CommandeCreate(
        client_id=1,
        date_commande=datetime.now(),
        details=[DetailsCreate(produit_id=1, quantite=5)],
    )
    commande = crud_commande.create_commande(session, commande_data)
    assert commande.id is not None

    deleted = crud_commande.delete_commande(session, commande.id)
    assert deleted is True
    assert crud_commande.get_commande(session, commande.id) is None
