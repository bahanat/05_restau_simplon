from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.commandes_et_produits import Produit, Categorie
from app.schemas.produit import ProduitCreate, ProduitUpdate
from app.db_creation import engine


# --- Create ---
def create_produit(session: Session, data: ProduitCreate) -> Produit:
    # Je vérifie si le categorie_id renseigné par l'utilisateur existe
    if data.categorie_id:
        categorie = session.get(Categorie, data.categorie_id)
        if not categorie:
            categories_existantes = session.exec(select(Categorie)).all()
            noms = [f"{c.id} - {c.nom}" for c in categories_existantes]
            raise HTTPException(
                status_code=400,
                detail=f"Catégorie ID {data.categorie_id} introuvable. Catégories disponibles : {noms}",
            )

    produit = Produit.model_validate(data)
    session.add(produit)
    session.commit()
    session.refresh(produit)
    return produit


# --- Read ---
def get_all_produits(
    session: Session,
) -> list[Produit]:
    return session.exec(select(Produit)).all()


# --- Read (par id) ---
def get_produit_by_id(session: Session, produit_id: int) -> Produit | None:
    return session.get(Produit, produit_id)


# --- Update ---
def update_produit(
    session: Session, produit_id: int, data: ProduitUpdate
) -> Produit | None:
    produit = session.get(Produit, produit_id)
    if not produit:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(produit, key, value)
    session.commit()
    session.refresh(produit)
    return produit


# --- Delete ---
def delete_produit(session: Session, produit_id: int) -> bool:
    produit = session.get(Produit, produit_id)
    if not produit:
        return False
    session.delete(produit)
    session.commit()
    return True
