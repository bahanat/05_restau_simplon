from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    serveur = "serveur"


# classe base pour roles


class RoleBase(BaseModel):
    nom: RoleEnum


# classe pour creer un role,
# si besoin au future de creer un role il faudra le faire dans crud ou/et Api (a verifier)


class RoleCreate(RoleBase):
    pass


# lecture - role


class RoleRead(RoleBase):
    id: int


# Update si besoin pour un role -update a partir de BaseModel


class RoleUpdate(BaseModel):
    nom: Optional[RoleEnum] = None


# Pas de login pour les roles normalement. donc pas de RoleLogin
