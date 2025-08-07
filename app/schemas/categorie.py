from pydantic import BaseModel
from typing import Optional

class CategorieCreate(BaseModel):
    nom : str

class CategorieRead(BaseModel):
    id : int
    nom : str

class CategorieUpdate(BaseModel):
    nom: Optional[str] = None