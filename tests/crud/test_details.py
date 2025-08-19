from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from app.crud.details import update_details_commande
from app.models.commandes_et_produits import Commande, DetailCommande, Produit
from app.models.users_et_roles import User
from app.schemas.detail import DetailsUpdate


@pytest.fixture
def sqlite_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(sqlite_engine):
    with Session(sqlite_engine) as session:
        # Crée un client et des produits pour les tests
        client = User(
            id=1,
            email="test@test.com",
            mot_de_passe="hashed",
            nom="pitt",
            prenom="leonardo",
        )
        produit1 = Produit(
            id=1,
            nom="Produit 1",
            description=None,
            prix=10.0,
            categorie_id=None,
            stock=1,
        )
        produit2 = Produit(
            id=2,
            nom="Produit 2",
            description=None,
            prix=5.0,
            categorie_id=None,
            stock=4,
        )
        session.add_all([client, produit1, produit2])
        session.commit()

        # Crée une commande initiale avec 1 détail
        commande = Commande(
            client_id=1, date_commande=datetime.now(), montant_total=10.0
        )
        session.add(commande)
        session.flush()  # génère l'id de la commande

        detail = DetailCommande(commande_id=commande.id, produit_id=1, quantite=1)
        session.add(detail)
        session.commit()
        session.refresh(commande)
        yield session


def test_update_details_commande(session):
    # Récupère la commande existante correctement
    commande = session.exec(select(Commande)).first()

    # Nouvelle liste de détails
    new_details = [
        DetailsUpdate(produit_id=1, quantite=2),
        DetailsUpdate(produit_id=2, quantite=3),
    ]

    update_details_commande(session, commande, new_details)
    session.commit()
    session.refresh(commande)

    # Vérifie que les détails ont été mis à jour
    assert len(commande.details) == 2

    # Vérifie le montant total : 2*10 + 3*5 = 35
    assert commande.montant_total == 35.0

    # Vérifie que chaque detail a le bon produit et quantité
    produits_quantites = {(d.produit_id, d.quantite) for d in commande.details}
    assert produits_quantites == {(1, 2), (2, 3)}
