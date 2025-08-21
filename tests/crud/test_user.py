from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.security import hash_password
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(session: Session, user_in: UserCreate) -> User:
    """Crée un nouvel utilisateur et le persiste en base.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        user_in (UserCreate): données du nouvel utilisateur

    Returns:
        User: instance de l'utilisateur créé

    Raises:
        IntegrityError: si la contrainte d'unicité (email) est violée
    """
    user = User(
        nom=user_in.nom,
        prenom=user_in.prenom,
        email=user_in.email,
        adresse=user_in.adresse,
        telephone=user_in.telephone,
        mot_de_passe=hash_password(user_in.mot_de_passe),
        role_id=user_in.role_id,
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Récupère un utilisateur par son ID.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        user_id (int): identifiant de l'utilisateur

    Returns:
        User | None: utilisateur correspondant ou None si non trouvé
    """
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    """Récupère un utilisateur par son email.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        email (str): email de l'utilisateur

    Returns:
        User | None: utilisateur correspondant ou None si non trouvé
    """
    return session.exec(select(User).where(User.email == email)).first()


def get_all_users(session: Session) -> Sequence[User]:
    """Récupère tous les utilisateurs.

    Args:
        session (Session): session SQLAlchemy/SQLModel

    Returns:
        Sequence[User]: liste des utilisateurs
    """
    return session.exec(select(User)).all()


def update_user(session: Session, user_id: int, user_in: UserUpdate) -> User | None:
    """Met à jour un utilisateur existant avec de nouvelles valeurs.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        user_id (int): ID de l'utilisateur à mettre à jour
        user_in (UserUpdate): données à mettre à jour

    Returns:
        User | None: utilisateur mis à jour ou None si l'utilisateur n'existe pas

    Raises:
        IntegrityError: si la contrainte d'unicité (email) est violée
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "mot_de_passe":
            setattr(user, key, hash_password(value))
        else:
            setattr(user, key, value)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    """Supprime un utilisateur existant.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        user_id (int): ID de l'utilisateur à supprimer

    Returns:
        bool: True si la suppression a réussi, False si l'utilisateur n'existait pas
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
