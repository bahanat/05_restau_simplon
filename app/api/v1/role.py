from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.schemas.role import RoleCreate, RoleRead
from app.crud.role import role_creation, get_all_roles, get_role_by_id
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
def read_roles(session: Session = Depends(get_session)):
    return get_all_roles(session)


# read - role par id


@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, session: Session = Depends(get_session)):
    role = get_role_by_id(session, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="role pas identifie")
    return role
