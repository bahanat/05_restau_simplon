# comme il n'a pas de relation entre fichiers de un meme dossier, pas besoin de type_checking

from sqlmodel import Session
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserUpdate
from app.models.commandes_et_produits import (
    Commande,
    DetailCommande,
)  # pour delete - je dois supprimer avant les commandes d'utilisateur
from app.core.security import hash_password
from sqlmodel import select


# dans user_creation pas de id et date car il seront cree automatiquement selon la construction de SQL Model
def user_creation(session: Session, user_data: UserCreate) -> User:

    user = User(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        adresse=user_data.adresse,
        telephone=user_data.telephone,
        role_id=user_data.role_id,
        mot_de_passe=hash_password(user_data.mot_de_passe),
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Read - tous les utilisateurs


def get_all_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()


# Read -  utilisateur par Id


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


# update users (avec mot_de_passe mais pas visible dans FastApi)


def update_user(session: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None

    update_data = user_data.dict(exclude_unset=True)

    if "mot_de_passe" in update_data and update_data["mot_de_passe"]:
        update_data["mot_de_passe"] = hash_password(update_data["mot_de_passe"])

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Delete pour completer CRUD - Delete pour users. utiise bool dans la fonction car l'utilisateur supprime, je vais voir le status pas l'utilisateur


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False

    commandes = session.exec(
        select(Commande).where(Commande.client_id == user_id)
    ).all()  # pour supprimer commandes et detailcommandes d'utilisateur a supprimer
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
