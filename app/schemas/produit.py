from pydantic import BaseModel
from typing import Optional

class ProduitCreate(BaseModel):
    nom: str
    description : Optional[str] = None
    prix: float
    categorie_id: Optional[int] = None
    stock: int 

class ProduitRead(BaseModel):
    id : int
    nom: str
    description : Optional[str] = None
    prix: float
    categorie_id: Optional[int] = None
    stock: int 

class ProduitUpdate(BaseModel):
    nom : Optional[str]= None
    description : Optional[str]= None
    prix : Optional[float]= None
    categorie_id :Optional[int]= None
    stock : Optional[int] = None