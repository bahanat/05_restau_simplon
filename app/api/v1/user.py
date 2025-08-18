from collections.abc import Sequence
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.crud.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)
from app.db.session import get_session
from app.models.users_et_roles import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: UserCreate, session: Session = Depends(get_session)
) -> User:
    return create_user(session, user_data)


@router.get("/", response_model=List[UserRead])
def read_users_endpoint(
    session: Session = Depends(get_session),
) -> Sequence[User]:
    return get_all_users(session)


@router.get("/{user_id}", response_model=UserRead)
def read_user_endpoint(user_id: int, session: Session = Depends(get_session)) -> User:
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
) -> User:
    updated_user = update_user(session, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)) -> None:
    success = delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
