from collections.abc import Sequence

from sqlmodel import Session, select

from app.models.commandes_et_produits import Categorie
from app.schemas.categorie import CategorieCreate, CategorieUpdate


# --- Create ---
def create_categorie(session: Session, categorie_data: CategorieCreate) -> Categorie:
    categorie = Categorie.model_validate(categorie_data)
    session.add(categorie)
    session.commit()
    session.refresh(categorie)
    return categorie


# --- Read ---
def get_all_categories(session: Session) -> Sequence[Categorie]:
    return session.exec(select(Categorie)).all()


# --- Read (par id) ---
def get_categorie_by_id(session: Session, categorie_id: int) -> Categorie | None:
    return session.get(Categorie, categorie_id)


# --- Read (par nom) ---
def get_categorie_by_nom(session: Session, categorie_nom: str) -> Categorie | None:
    statement = select(Categorie).where(Categorie.nom == categorie_nom)
    return session.exec(statement).first()


# --- Update ---
def update_categorie(
    session: Session, categorie_id: int, data: CategorieUpdate
) -> Categorie | None:
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(categorie, key, value)
    session.commit()
    session.refresh(categorie)
    return categorie


# --- Delete ---
def delete_categorie(session: Session, categorie_id: int) -> bool:
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return False
    session.delete(categorie)
    session.commit()
    return True
