from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    serveur = "serveur"


class RoleBase(BaseModel):
    nom: RoleEnum


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int


class RoleUpdate(BaseModel):
    nom: Optional[RoleEnum] = None
