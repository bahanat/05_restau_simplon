from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import password_checking
from app.crud.user import get_user_by_email
from app.db.session import get_session
from app.schemas.user import UserLogin, UserLoginResponse, UserPublic

# Router pour les endpoints liés à l'authentification
router = APIRouter(tags=["Logins"])


@router.post("/login", response_model=UserLoginResponse)
def login(
    body: UserLogin, session: Session = Depends(get_session)
) -> UserLoginResponse:
    """
    Authentifie un utilisateur avec son email et mot de passe.

    Args:
        body (UserLogin): Les informations de connexion fournies
        par l'utilisateur (email et mot de passe).
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException:
            - 400 BAD REQUEST si l'email ou le mot de passe est incorrect.

    Returns:
        UserLoginResponse: Un message de confirmation
        et les informations publiques de l'utilisateur.
    """
    user = get_user_by_email(session, body.email)

    # Vérification des identifiants
    if not user or not password_checking(body.mot_de_passe, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="identifiant errone",
        )

    # Retourne la réponse avec les infos publiques de l'utilisateur
    return UserLoginResponse(message="Login OK", user=UserPublic.model_validate(user))
