from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Class pour creation et lecture - user


class UserBase(BaseModel):
    email: EmailStr
    nom: Optional[str]
    prenom: Optional[str]
    adresse: Optional[str]
    telephone: Optional[str]
    role_id: Optional[int]


# Creation, donc UserBase + mdp


class UserCreate(UserBase):
    mot_de_passe: str = Field(..., min_length=10)
