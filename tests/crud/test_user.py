import pytest
from sqlmodel import SQLModel, Session, create_engine, select

DATABASE_URL = "sqlite://"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

from app.models import users_et_roles, commandes_et_produits
from app.models.commandes_et_produits import Commande, DetailCommande, Produit

SQLModel.metadata.create_all(engine)


@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session


from app.core.security import verification_mdp
from app.crud.user import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    delete_user,
)
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserUpdate
from app.models.users_et_roles import Role, RoleEnum
from sqlalchemy.exc import IntegrityError

# --- creation role pour tests ---


def ensure_role_exists(session, nom: RoleEnum) -> Role:
    existing_role = session.exec(select(Role).where(Role.nom == nom)).first()
    if existing_role:
        return existing_role
    role = Role(nom=nom)
    session.add(role)
    session.commit()
    session.refresh(role)

    return role


# --- Test create_user ---
def test_create_user(session):
    role = ensure_role_exists(session, RoleEnum.client)

    user_data = UserCreate(
        nom="Alice",
        prenom="Test",
        email="alice@example.com",
        adresse="123 Rue Test",
        telephone="0123456789",
        role_id=role.id,
        mot_de_passe="securepass",
    )

    user = create_user(session, user_data)

    assert isinstance(user, User)
    assert user.id is not None
    assert user.email == "alice@example.com"
    assert verification_mdp("securepass", user.mot_de_passe) is True


# --- Test get_all_users ---


def test_get_all_users(session):
    role = ensure_role_exists(session, RoleEnum.client)

    user1 = UserCreate(
        nom="User1",
        prenom="Test1",
        email="user1@example.com",
        adresse="Adresse 1",
        telephone="000111222",
        role_id=role.id,
        mot_de_passe="user1pass12345",
    )
    user2 = UserCreate(
        nom="User2",
        prenom="Test2",
        email="user2@example.com",
        adresse="Adresse 2",
        telephone="333444555",
        role_id=1,
        mot_de_passe="user2pass123456",
    )

    create_user(session, user1)
    create_user(session, user2)

    all_users = get_all_users(session)

    emails = [u.email for u in all_users]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


# --- Test get_user_by_id ---


def test_get_user_by_id(session):
    role = ensure_role_exists(session, RoleEnum.client)

    user_data = UserCreate(
        nom="izak",
        prenom="Tester",
        email="izak@example.com",
        adresse="456 Rue Exemple",
        telephone="9876543210",
        role_id=role.id,
        mot_de_passe="izaksecurepass",
    )

    created_user = create_user(session, user_data)

    retrieved_user = get_user_by_id(session, created_user.id)

    assert retrieved_user is not None
    assert retrieved_user.email == "izak@example.com"
    assert retrieved_user.nom == "izak"


# --- Test get_user_by_email ---


def test_get_user_by_email(session):
    role = ensure_role_exists(session, RoleEnum.client)

    user_data = UserCreate(
        nom="Harley",
        prenom="Testnom",
        email="harley@example.com",
        adresse="789 Rue Claire",
        telephone="1112223333",
        role_id=role.id,
        mot_de_passe="harleypassword",
    )

    create_user(session, user_data)

    found_user = get_user_by_email(session, "harley@example.com")

    assert found_user is not None
    assert found_user.nom == "Harley"
    assert found_user.prenom == "Testnom"

    # --- Test update_user ---


def test_update_user(session):
    role = ensure_role_exists(session, RoleEnum.client)

    original_email = "david@example.com"
    new_email = "david.updated@example.com"

    user_data = UserCreate(
        nom="David",
        prenom="Updatest",
        email=original_email,
        adresse="Initial Address",
        telephone="0000000000",
        role_id=role.id,
        mot_de_passe="davidsecurepass",
    )

    created_user = create_user(session, user_data)

    update_data = UserUpdate(
        email=new_email,
        adresse="Updated Address",
    )

    updated_user = update_user(session, created_user.id, update_data)

    assert updated_user is not None
    assert updated_user.email == new_email
    assert updated_user.adresse == "Updated Address"


# --- Test update_user_ verification email unique ---


def test_email_uniqueness_constraint(session):

    role = ensure_role_exists(session, RoleEnum.client)

    email = "duplicate@example.com"

    user1 = UserCreate(
        nom="Alice",
        prenom="Test",
        email=email,
        adresse="123 Rue",
        telephone="0123456789",
        role_id=role.id,
        mot_de_passe="alicepassword",
    )

    user2 = UserCreate(
        nom="Bob",
        prenom="Duplicate",
        email=email,
        adresse="456 Avenue",
        telephone="0987654321",
        role_id=role.id,
        mot_de_passe="bobpassword",
    )

    create_user(session, user1)

    with pytest.raises(IntegrityError):
        create_user(session, user2)


def test_delete_user(session):

    role = ensure_role_exists(session, RoleEnum.client)

    user_data = UserCreate(
        nom="Eva",
        prenom="Delete",
        email="eva.to.delete@example.com",
        adresse="123 Rue Suppression",
        telephone="123123123",
        role_id=role.id,
        mot_de_passe="secreteva1234",
    )
    user = create_user(session, user_data)

    produit = Produit(nom="Pizza Margherita", prix=10.0, stock=50)
    session.add(produit)
    session.commit()

    commande = Commande(client_id=user.id)
    session.add(commande)
    session.commit()

    detail = DetailCommande(commande_id=commande.id, produit_id=produit.id, quantite=2)
    session.add(detail)
    session.commit()

    assert (
        session.exec(select(Commande).where(Commande.client_id == user.id)).first()
        is not None
    )
    assert (
        session.exec(
            select(DetailCommande).where(DetailCommande.commande_id == commande.id)
        ).first()
        is not None
    )

    deleted = delete_user(session, user.id)

    assert deleted is True
    assert get_user_by_id(session, user.id) is None
    assert (
        session.exec(select(Commande).where(Commande.client_id == user.id)).first()
        is None
    )
    assert (
        session.exec(
            select(DetailCommande).where(DetailCommande.commande_id == commande.id)
        ).first()
        is None
    )
