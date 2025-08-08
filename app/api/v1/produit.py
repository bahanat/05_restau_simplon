from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate
from app.crud.produit import (
    create_produit,
    get_all_produits,
    get_produit_by_id,
    update_produit,
    delete_produit,
)

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.post("/", response_model=ProduitRead)
def create(data: ProduitCreate, session: Session = Depends(get_session)):
    return create_produit(session, data)


@router.get("/", response_model=list[ProduitRead])
def read_all(session: Session = Depends(get_session)):
    return get_all_produits(
        session,
    )


@router.get("/{produit_id}", response_model=ProduitRead)
def read_one(produit_id: int, session: Session = Depends(get_session)):
    produit = get_produit_by_id(session, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.put("/{produit_id}", response_model=ProduitRead)
def update(
    produit_id: int, data: ProduitUpdate, session: Session = Depends(get_session)
):
    produit = update_produit(session, produit_id, data)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.delete("/{produit_id}", status_code=204)
def delete(produit_id: int, session: Session = Depends(get_session)):
    if not delete_produit(session, produit_id):
        raise HTTPException(status_code=404, detail="Produit introuvable")
