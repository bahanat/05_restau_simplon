from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.schemas.user import UserRead, UserUpdate
from app.crud.user import get_all_users, get_user_by_id, update_user
from app.db.session import get_session

router = APIRouter(prefix="/users", tags=["Users"])


# Read - tous les utilisateurs


@router.get("/", response_model=List[UserRead])
def read_users(session: Session = Depends(get_session)):
    return get_all_users(session)


# Read - utilisateur par id


@router.get("/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


# update utilisateur


@router.put("/{user_id}", response_model=UserRead)
def update_user_endpoint(
    user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)
):
    updated_user = update_user(session, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user
