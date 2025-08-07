from fastapi import APIRouter, HTTPException
from app.schemas.produit import ProduitCreate, ProduitRead, ProduitUpdate
from app.crud.produit import (
    create_produit, get_all_produits, get_produit_by_id,
    update_produit, delete_produit
)

router = APIRouter(prefix="/produits", tags=["Produits"])

# CREATE:
@router.post("/", response_model=ProduitRead)
def create(data: ProduitCreate):
    return create_produit(data)

# READ
@router.get("/", response_model=list[ProduitRead])
def read_all():
    return get_all_produits()

@router.get("/{produit_id}", response_model=ProduitRead)
def read_one(produit_id: int):
    produit = get_produit_by_id(produit_id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit

# UPDATE
@router.put("/{produit_id}", response_model=ProduitRead)
def update(produit_id: int, data: ProduitUpdate):
    produit = update_produit(produit_id, data)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return produit

# DELETE 
@router.delete("/{produit_id}", status_code=204)
def delete(produit_id: int):
    if not delete_produit(produit_id):
        raise HTTPException(status_code=404, detail="Produit introuvable")
