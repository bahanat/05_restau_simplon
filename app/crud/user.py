from collections.abc import Sequence
from typing import Optional

from sqlmodel import Session, select

from app.core.security import hash_mdp
from app.models.commandes_et_produits import (
    Commande,
    DetailCommande,
)
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserUpdate


# --- Create ---
def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        adresse=user_data.adresse,
        telephone=user_data.telephone,
        role_id=user_data.role_id,
        mot_de_passe=hash_mdp(user_data.mot_de_passe),
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# --- Read ---
def get_all_users(session: Session) -> Sequence[User]:
    return session.exec(select(User)).all()


# --- Read (par id) ---
def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


# --- Read (par email) ---
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()


# --- Update ---
def update_user(session: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)

    if "mot_de_passe" in update_data and update_data["mot_de_passe"]:
        update_data["mot_de_passe"] = hash_mdp(update_data["mot_de_passe"])

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# --- Delete ---
def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False

    commandes = session.exec(
        select(Commande).where(Commande.client_id == user_id)
    ).all()
    for commande in commandes:
        details = session.exec(
            select(DetailCommande).where(DetailCommande.commande_id == commande.id)
        ).all()
        for detail in details:
            session.delete(detail)
        session.delete(commande)

    session.delete(user)
    session.commit()
    return True
