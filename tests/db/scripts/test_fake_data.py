import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from app.db.scripts.fake_data import create_fake_data
from app.models.commandes_et_produits import (
    Categorie,
    Commande,
    DetailCommande,
    Produit,
)
from app.models.users_et_roles import Role, RoleEnum, User


@pytest.fixture(name="session")
def session_fixture():
    """Crée une base SQLite en mémoire pour les tests."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_fake_data(session, monkeypatch):
    # ⚠️ Patch le moteur de la fonction pour qu'elle utilise notre DB de test
    import app.db.scripts.fake_data as fake_data

    monkeypatch.setattr(fake_data, "engine", session.bind)

    # Appel de la fonction
    create_fake_data()

    # Vérifier rôles
    roles = session.exec(select(Role)).all()
    assert len(roles) == 3
    assert set(r.nom for r in roles) == {
        RoleEnum.admin,
        RoleEnum.client,
        RoleEnum.serveur,
    }

    # Vérifier utilisateurs
    users = session.exec(select(User)).all()
    assert len(users) == 5

    # Vérifier catégories
    categories = session.exec(select(Categorie)).all()
    assert {c.nom for c in categories} == {
        "Entrée",
        "Plat",
        "Dessert",
        "Boisson",
        "Autre",
    }

    # Vérifier produits
    produits = session.exec(select(Produit)).all()
    assert len(produits) >= 5  # 5 par catégorie

    # Vérifier commandes
    commandes = session.exec(select(Commande)).all()
    assert len(commandes) == 10

    # Vérifier détails
    details = session.exec(select(DetailCommande)).all()
    assert len(details) > 0
