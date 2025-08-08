from sqlmodel import Session, select
from app.models.commandes_et_produits import Produit, Categorie
from app.schemas.produit import ProduitCreate, ProduitUpdate
from app.db_creation import engine
from fastapi import HTTPException

def get_session():
    return Session(engine)

# Create : Création d'un produit
def create_produit(data: ProduitCreate) -> Produit:
    session = get_session()
    # Je vérifie si la produit_id renseigner par l'utilisateur existe:
    if data.categorie_id:
        categorie = session.get(Categorie, data.categorie_id)
        if not categorie:
            categories_existantes = session.exec(select(Categorie)).all()
            noms = [f"{c.id} - {c.nom}" for c in categories_existantes]
            raise HTTPException(
                status_code=400,
                detail=f"Catégorie ID {data.categorie_id} introuvable. Catégories disponibles : {noms}"
            )

    produit = Produit.model_validate(data)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit

# Read : Lecture des produits
def get_all_produits() -> list[Produit]:
    session = get_session()
    return session.exec(select(Produit)).all()

def get_produit_by_id(produit_id: int) -> Produit | None:
    session = get_session()
    return session.get(Produit, produit_id)

# Update : Mettre a jour un produit
def update_produit(produit_id: int, data: ProduitUpdate) -> Produit | None:
    session = get_session()
    produit = session.get(Produit, produit_id)
    if not produit:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(produit, key, value)
    session.commit()
    session.refresh(produit)
    return produit

# Delete : Supprimer un produit
def delete_produit(produit_id: int) -> bool:
    session = get_session()
    produit = session.get(Produit, produit_id)
    if not produit:
        return False
    session.delete(produit)
    session.commit()
    return True
