from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.crud.categorie import (
    create_categorie,
    get_all_categories,
    get_categorie_by_id,
    update_categorie,
    delete_categorie,
)
from app.schemas.categorie import CategorieCreate, CategorieRead, CategorieUpdate

router = APIRouter(prefix="/categories", tags=["Catégories"])


@router.post("/", response_model=CategorieRead)
def create(data: CategorieCreate, session: Session = Depends(get_session)):
    return create_categorie(session, data)


@router.get("/", response_model=list[CategorieRead])
def read(session: Session = Depends(get_session)):
    return get_all_categories(session)


@router.get("/{categorie_id}", response_model=CategorieRead)
def read_one(categorie_id: int, session: Session = Depends(get_session)):
    categorie = get_categorie_by_id(session, categorie_id)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie


@router.put("/{categorie_id}", response_model=CategorieRead)
def update(
    categorie_id: int, data: CategorieUpdate, session: Session = Depends(get_session)
):
    categorie = update_categorie(session, categorie_id, data)
    if not categorie:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    return categorie


@router.delete("/{categorie_id}", status_code=204)
def delete(categorie_id: int, session: Session = Depends(get_session)):
    if not delete_categorie(session, categorie_id):
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
