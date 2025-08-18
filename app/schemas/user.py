from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    role_id: Optional[int] = None


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    nom: str
    prenom: str
    role_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UserLoginResponse(BaseModel):
    message: str
    user: UserPublic


class UserCreate(UserBase):
    mot_de_passe: str = Field(..., min_length=10)


class UserRead(UserBase):
    id: int
    date_creation: Optional[datetime]


class UserLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    role_id: Optional[int] = None
    mot_de_passe: Optional[str] = Field(None, min_length=10, exclude=True)
