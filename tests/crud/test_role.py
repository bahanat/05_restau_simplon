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


from app.models.users_et_roles import Role, User
from app.schemas.role import RoleCreate, RoleUpdate, RoleEnum
from app.crud.role import (
    role_creation,
    get_all_roles,
    get_role_by_id,
    update_role,
    delete_role,
)

# --- Test create_role---


def test_role_creation(session):
    role_data = RoleCreate(nom=RoleEnum.serveur)

    created_role = role_creation(session, role_data)

    assert created_role is not None
    assert created_role.id is not None
    assert created_role.nom == RoleEnum.serveur


# --- Test get_all_roles ---


def test_get_all_roles(session):

    role1 = role_creation(session, RoleCreate(nom=RoleEnum.admin))
    role2 = role_creation(session, RoleCreate(nom=RoleEnum.serveur))

    roles = get_all_roles(session)

    noms = [r.nom for r in roles]

    assert role1.nom in noms
    assert role2.nom in noms


# --- Test get_all_roles ---


def test_get_role_by_id(session):

    role_data = RoleCreate(nom=RoleEnum.serveur)
    created_role = role_creation(session, role_data)

    retrieved_role = get_role_by_id(session, created_role.id)

    assert retrieved_role is not None
    assert retrieved_role.id == created_role.id
    assert retrieved_role.nom == RoleEnum.serveur


def test_update_role(session):
    role_data = RoleCreate(nom=RoleEnum.client)
    created_role = role_creation(session, role_data)

    update_data = RoleUpdate(nom=RoleEnum.serveur)

    updated_role = update_role(session, created_role.id, update_data)

    assert updated_role is not None
    assert updated_role.id == created_role.id
    assert updated_role.nom == RoleEnum.serveur

    refetched = get_role_by_id(session, created_role.id)
    assert refetched.nom == RoleEnum.serveur


def test_delete_role(session):
    role = role_creation(session, RoleCreate(nom=RoleEnum.client))

    user = User(
        nom="Test",
        prenom="User",
        email="testuser@example.com",
        adresse="123 Rue Test",
        telephone="1234567890",
        role_id=role.id,
        mot_de_passe="hashedpassword",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.role_id == role.id

    affected_users = delete_role(session, role.id)

    assert user.id in affected_users

    updated_user = session.get(User, user.id)
    assert updated_user is not None
    assert updated_user.role_id is None

    assert session.get(Role, role.id) is None
