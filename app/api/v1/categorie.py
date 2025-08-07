from fastapi import APIRouter, HTTPException
from app.schemas.categorie import CategorieCreate, CategorieRead, CategorieUpdate
from app.crud.categorie import (
    create_categorie, get_all_categories, get_categorie_by_id,
    update_categorie, delete_categorie
)

router = APIRouter(prefix="/categories", tags=["Catégories"])

# CREATE:
@router.post("/", response_model=CategorieRead)
def create(data: CategorieCreate):
    return create_categorie(data)

# READ
@router.get("/", response_model=list[CategorieRead])
def read():
    return get_all_categories()

    
@router.get("/{categorie_id}", response_model=CategorieRead)
def read_one(categorie_id: int):
    categorie = get_categorie_by_id(categorie_id)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie

# UPDATE
@router.put("/{categorie_id}", response_model=CategorieRead)
def update(categorie_id: int, data: CategorieUpdate):
    categorie = update_categorie(categorie_id, data)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie

# DELETE 
@router.delete("/{categorie_id}", status_code=204)
def delete(categorie_id: int):
    if not delete_categorie(categorie_id):
        raise HTTPException(status_code=404, detail="Catégorie introuvable")