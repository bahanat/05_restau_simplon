from datetime import datetime

from sqlmodel import Session

from app.crud import commande as crud_commande
from app.schemas.commande import CommandeCreate, CommandeUpdate, StatusEnum
from app.schemas.detail import DetailsCreate


def test_create_commande(session: Session) -> None:
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
    fetched = crud_commande.get_commande(session, 1)
    assert fetched is not None
    assert fetched.id == 1


def test_update_commande(session: Session) -> None:
    update_data = CommandeUpdate(statut=StatusEnum.servie)
    updated = crud_commande.update_commande(session, 1, update_data)
    assert updated is not None


def test_delete_commande(session: Session) -> None:
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
