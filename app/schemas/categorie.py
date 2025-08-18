from typing import Optional

from pydantic import BaseModel


class CategorieCreate(BaseModel):
    nom: str


class CategorieRead(BaseModel):
    id: int
    nom: str


class CategorieUpdate(BaseModel):
    nom: Optional[str] = None
