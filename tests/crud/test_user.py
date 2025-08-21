from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from collections.abc import Sequence

from app.core.security import hash_mdp
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(session: Session, user_in: UserCreate) -> User:
    user = User(
        nom=user_in.nom,
        prenom=user_in.prenom,
        email=user_in.email,
        adresse=user_in.adresse,
        telephone=user_in.telephone,
        mot_de_passe=hash_mdp(user_in.mot_de_passe),
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
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


def get_all_users(session: Session) -> Sequence[User]:
    return session.exec(select(User)).all()


def update_user(session: Session, user_id: int, user_in: UserUpdate) -> User | None:
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "mot_de_passe":
            setattr(user, key, hash_mdp(value))
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
    user = get_user_by_id(session, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
