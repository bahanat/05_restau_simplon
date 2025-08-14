from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.user import UserLogin, UserLoginResponse, UserPublic
from app.crud.user import get_user_by_email
from app.core.security import verification_mdp

router = APIRouter(tags=["Logins"])


@router.post("/login", response_model=UserLoginResponse)
def login(body: UserLogin, session: Session = Depends(get_session)):
    user = get_user_by_email(session, body.email)

    if not user or not verification_mdp(body.mot_de_passe, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="identifiant errone"
        )

    return UserLoginResponse(message="Login OK", user=UserPublic.from_orm(user))
