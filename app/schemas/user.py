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


# Lecture utilisateur


class UserRead(UserBase):
    id: int
    date_creation: Optional[datetime]


# Connexion - login utilisateur


class UserLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str


# Comme le e-mail est dejà verifié, MAJ sans e-mail mais oui pour le mot de passe


class UserUpdate(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    adresse: Optional[str]
    telephone: Optional[str]
    role_id: Optional[int]
    mot_de_passe: Optional[str] = Field(None, min_length=10)
