from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.produit import (
    create_produit,
    delete_produit,
    get_all_produits,
    get_produit_by_id,
    update_produit,
)
from app.db.session import get_session
from app.models.commandes_et_produits import Produit
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate

router = APIRouter(prefix="/produits", tags=["Produits"])


@router.post("/", response_model=ProduitRead)
def create(data: ProduitCreate, session: Session = Depends(get_session)) -> Produit:
    return create_produit(session, data)


@router.get("/", response_model=list[ProduitRead])
def read_all(session: Session = Depends(get_session)) -> Sequence[Produit]:
    return get_all_produits(
        session,
    )


@router.get("/{produit_id}", response_model=ProduitRead)
def read_one(produit_id: int, session: Session = Depends(get_session)) -> Produit:
    produit = get_produit_by_id(session, produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.put("/{produit_id}", response_model=ProduitRead)
def update(
    produit_id: int,
    data: ProduitUpdate,
    session: Session = Depends(get_session),
) -> Produit:
    produit = update_produit(session, produit_id, data)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit


@router.delete("/{produit_id}", status_code=204)
def delete(produit_id: int, session: Session = Depends(get_session)) -> None:
    if not delete_produit(session, produit_id):
        raise HTTPException(status_code=404, detail="Produit introuvable")
