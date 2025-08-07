from sqlmodel import select, Session
from app.db_creation import engine
from app.schemas.categorie import CategorieCreate, CategorieRead, CategorieUpdate
from app.models.commandes_et_produits import Categorie


def get_session():
    return Session(engine)

# Create : Création d'une catégorie
def create_categorie(categorie_data: CategorieCreate) -> Categorie:
    session = get_session()
    categorie = Categorie.model_validate(categorie_data)
    session.add(categorie)
    session.commit()
    session.refresh(categorie)
    return categorie

# Read : Lecture de categorie 
def get_all_categories() -> list[Categorie]:
    session = get_session()
    return session.exec(select(Categorie)).all()

def get_categorie_by_id(categorie_id: int) -> Categorie | None:
    session = get_session()
    return session.get(Categorie, categorie_id)


def get_categorie_by_nom(categorie_nom: str) -> Categorie | None:
    session = get_session()
    return session.get(Categorie, categorie_nom)
    
    
# Update : Mettre a jour une categorie
def update_categorie(categorie_id: int, data: CategorieUpdate) -> Categorie | None:
    session = get_session()
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(categorie, key, value)
    session.commit()
    session.refresh(categorie)
    return categorie


# Delete : Supprimer une categorie
def delete_categorie(categorie_id: int) -> bool:
    session = get_session()
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return False
    session.delete(categorie)
    session.commit()
    return True