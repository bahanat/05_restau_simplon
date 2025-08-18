from collections.abc import Sequence
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.crud.role import (
    delete_role,
    get_all_roles,
    get_role_by_id,
    role_creation,
    update_role,
)
from app.db.session import get_session
from app.models.users_et_roles import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(
    role_data: RoleCreate, session: Session = Depends(get_session)
) -> Role:
    return role_creation(session, role_data)


@router.get("/", response_model=List[RoleRead])
def read_roles_endpoint(
    session: Session = Depends(get_session),
) -> Sequence[Role]:
    return get_all_roles(session)


@router.get("/{role_id}", response_model=RoleRead)
def read_role_endpoint(role_id: int, session: Session = Depends(get_session)) -> Role:
    role = get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return role


@router.put("/{role_id}", response_model=RoleRead)
def update_role_endpoint(
    role_id: int,
    role_data: RoleUpdate,
    session: Session = Depends(get_session),
) -> Role:
    updated_role = update_role(session, role_id, role_data)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return updated_role


@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role_endpoint(
    role_id: int, session: Session = Depends(get_session)
) -> dict[str, object]:
    utilisateurs = delete_role(session, role_id)
    if utilisateurs is None:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return {
        "message": (
            "Rôle supprimé. "
            "Les utilisateurs liés n'ont plus de role attribué. "
            "Mettre à jour absolument !"
        ),
        "utilisateurs_affectés": utilisateurs,
        "count": len(utilisateurs),
    }
