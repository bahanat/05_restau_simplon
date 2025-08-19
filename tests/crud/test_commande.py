from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.crud import commande as crud_commande
from app.models.commandes_et_produits import Produit, StatusEnum
from app.models.users_et_roles import User
from app.schemas.commande import CommandeCreate, CommandeUpdate


@pytest.fixture
def sqlite_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(sqlite_engine):
    with Session(sqlite_engine) as session:
        # Crée un produit et un client de test
        client = User(
            id=1,
            email="test@test.com",
            mot_de_passe="hashed",
            nom="pitt",
            prenom="leonardo",
        )
        produit = Produit(
            id=1,
            nom="Produit 1",
            description=None,
            prix=10.0,
            categorie_id=None,
            stock=1,
        )
        session.add(client)
        session.add(produit)
        session.commit()
        yield session


def test_create_commande(session):
    commande_data = CommandeCreate(
        client_id=1,
        date_commande=datetime.now(),
        details=[{"produit_id": 1, "quantite": 2}],
    )
    commande = crud_commande.create_commande(session, commande_data)
    assert commande.id is not None
    assert commande.montant_total == 20.0
    assert len(commande.details) == 1


def test_get_commande(session):
    # Crée d'abord une commande
    commande_data = CommandeCreate(
        client_id=1,
        date_commande=datetime.now(),
        details=[{"produit_id": 1, "quantite": 1}],
    )
    created = crud_commande.create_commande(session, commande_data)

    fetched = crud_commande.get_commande(session, created.id)
    assert fetched.id == created.id


def test_update_commande(session):
    commande_data = CommandeCreate(
        client_id=1,
        date_commande=datetime.now(),
        details=[{"produit_id": 1, "quantite": 1}],
    )
    commande = crud_commande.create_commande(session, commande_data)

    update_data = CommandeUpdate(statut=StatusEnum.servie)
    updated = crud_commande.update_commande(session, commande.id, update_data)
    assert updated.statut == StatusEnum.servie


def test_delete_commande(session):
    commande_data = CommandeCreate(
        client_id=1,
        date_commande=datetime.now(),
        details=[{"produit_id": 1, "quantite": 1}],
    )
    commande = crud_commande.create_commande(session, commande_data)

    deleted = crud_commande.delete_commande(session, commande.id)
    assert deleted is True
    assert crud_commande.get_commande(session, commande.id) is None
