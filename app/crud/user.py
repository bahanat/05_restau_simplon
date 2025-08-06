# comme il n'a pas de relation entre fichiers de un meme dossier, pas besoin de type_checking

from sqlmodel import Session
from app.models.users_et_roles import User
from app.schemas.user import UserCreate
from app.core.security import hash_mot_de_passe


# dans user_creation pas de id et date car il seront cree automatiquement selon la construction de SQL Model
def user_creation(session: Session, user_data: UserCreate) -> User:

    user = User(
        nom=user_data.nom,
        prenom=user_data.prenom,
        email=user_data.email,
        adresse=user_data.adresse,
        telephone=user_data.telephone,
        role_id=user_data.role_id,
        mot_de_passe=hash_mot_de_passe(user_data.mot_de_passe),
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
