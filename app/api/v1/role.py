from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.crud.role import (
    role_creation,
    get_all_roles,
    get_role_by_id,
    update_role,
    delete_role,
)
from app.db.session import get_session

router = APIRouter(prefix="/roles", tags=["Roles"])

# creation - role


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(
    role_data: RoleCreate, session: Session = Depends(get_session)
):
    return role_creation(session, role_data)


# read tous le roles


@router.get("/", response_model=List[RoleRead])
def read_roles_endpoint(session: Session = Depends(get_session)):
    return get_all_roles(session)


# read - role par id


@router.get("/{role_id}", response_model=RoleRead)
def read_role_endpoint(role_id: int, session: Session = Depends(get_session)):
    role = get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="role pas identifie")
    return role


# update - role


@router.put("/{role_id}", response_model=RoleRead)
def update_role_endpoint(
    role_id: int, role_data: RoleUpdate, session: Session = Depends(get_session)
):
    updated_role = update_role(session, role_id, role_data)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role non trouvé")
    return updated_role


# delete - role


@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role_endpoint(role_id: int, session: Session = Depends(get_session)):
    utilisateurs = delete_role(session, role_id)
    if utilisateurs is None:
        raise HTTPException(status_code=404, detail="Role non trouvé")
    return {
        "message": "role supprime. Les utilisateurs lies n'ont plus de role.SVp,mettez les a jour",
        "utilisateurs_affectés": utilisateurs,
        "count": len(utilisateurs),
    }
