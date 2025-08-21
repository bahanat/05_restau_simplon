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

# Router FastAPI pour la gestion des rôles utilisateurs
router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role_endpoint(
    role_data: RoleCreate, session: Session = Depends(get_session)
) -> Role:
    """
    Crée un nouveau rôle utilisateur.

    Args:
        role_data (RoleCreate): Données du rôle à créer.
        session (Session): Session de base de données (injectée par FastAPI).

    Returns:
        Role: Le rôle nouvellement créé.
    """
    return role_creation(session, role_data)


@router.get("/", response_model=List[RoleRead])
def read_roles_endpoint(session: Session = Depends(get_session)) -> Sequence[Role]:
    """
    Récupère la liste de tous les rôles existants.

    Args:
        session (Session): Session de base de données (injectée par FastAPI).

    Returns:
        Sequence[Role]: Liste de tous les rôles.
    """
    return get_all_roles(session)


@router.get("/{role_id}", response_model=RoleRead)
def read_role_endpoint(role_id: int, session: Session = Depends(get_session)) -> Role:
    """
    Récupère un rôle spécifique par son identifiant.

    Args:
        role_id (int): Identifiant du rôle recherché.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le rôle n'existe pas.

    Returns:
        Role: Le rôle correspondant.
    """
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
    """
    Met à jour un rôle existant.

    Args:
        role_id (int): Identifiant du rôle à mettre à jour.
        role_data (RoleUpdate): Nouvelles données du rôle.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le rôle n'existe pas.

    Returns:
        Role: Le rôle mis à jour.
    """
    updated_role = update_role(session, role_id, role_data)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return updated_role


@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role_endpoint(
    role_id: int, session: Session = Depends(get_session)
) -> dict[str, object]:
    """
    Supprime un rôle par son identifiant.

    ⚠️ Les utilisateurs liés perdent ce rôle, il est donc conseillé
    de les mettre à jour immédiatement.

    Args:
        role_id (int): Identifiant du rôle à supprimer.
        session (Session): Session de base de données (injectée par FastAPI).

    Raises:
        HTTPException: 404 si le rôle n'existe pas.

    Returns:
        dict[str, object]: Message de confirmation, liste des utilisateurs affectés,
        et le nombre total d'utilisateurs impactés.
    """
    utilisateurs = delete_role(session, role_id)
    if utilisateurs is None:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return {
        "message": (
            "Rôle supprimé. "
            "Les utilisateurs liés n'ont plus de rôle attribué. "
            "Mettre à jour absolument !"
        ),
        "utilisateurs_affectés": utilisateurs,
        "count": len(utilisateurs),
    }
