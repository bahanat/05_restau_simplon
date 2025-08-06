from pydantic import BaseModel
from typing import Optional

# classe base pour roles


class RoleBase(BaseModel):
    nom: str


# classe base pour le roles,
# si besoin au future de creer un role il faudra le faire dans crud ou/et Api (a verifier)


class RoleCreate(RoleBase):
    pass

# lecture role

class RoleRead(RoleBase):
    id: int

# Update si besoin pour un role

class RoleUpdate
