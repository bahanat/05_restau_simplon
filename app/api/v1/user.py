from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List


from app.schemas.user import UserRead
from app.crud.user import get_all_users
from app.db.session import get_session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserRead])
def read_users(session: Session = Depends(get_session)):
    return get_all_users(session)
