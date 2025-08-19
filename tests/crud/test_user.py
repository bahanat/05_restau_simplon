from app.core.security import verification_mdp
from app.crud.user import create_user
from app.models.users_et_roles import User
from app.schemas.user import UserCreate


def test_create_user(session):
    user_data = UserCreate(
        nom="Alice",
        prenom="Test",
        email="alice@example.com",
        adresse="123 Rue Test",
        telephone="0123456789",
        role_id=1,
        mot_de_passe="securepass",
    )

    user = create_user(session, user_data)

    assert isinstance(user, User)
    assert user.id is not None
    assert user.email == "alice@example.com"
    assert verification_mdp("securepass", user.mot_de_passe) is True
