from collections.abc import Sequence
from typing import Optional

from sqlmodel import Session, select

from app.models.users_et_roles import Role, User
from app.schemas.role import RoleCreate, RoleUpdate


# --- Create ---
def role_creation(session: Session, role_data: RoleCreate) -> Role:
    """Crée un nouveau rôle dans la base de données.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        role_data (RoleCreate): Les données du rôle à créer.

    Returns:
        Role: L'instance du rôle créé.
    """
    role = Role(nom=role_data.nom)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


# --- Read ---
def get_all_roles(session: Session) -> Sequence[Role]:
    """Récupère tous les rôles présents dans la base de données.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.

    Returns:
        Sequence[Role]: Une séquence contenant tous les rôles.
    """
    return session.exec(select(Role)).all()


# --- Read (par id) ---
def get_role_by_id(session: Session, role_id: int) -> Optional[Role]:
    """Récupère un rôle par son ID.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        role_id (int): L'ID du rôle à récupérer.

    Returns:
        Optional[Role]: L'instance du rôle si trouvée, sinon None.
    """
    return session.get(Role, role_id)


# --- Update ---
def update_role(
    session: Session, role_id: int, role_data: RoleUpdate
) -> Optional[Role]:
    """Met à jour un rôle existant.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        role_id (int): L'ID du rôle à mettre à jour.
        role_data (RoleUpdate): Les données à mettre à jour.

    Returns:
        Optional[Role]: L'instance du rôle mise à jour si elle existe, sinon None.
    """
    role = session.get(Role, role_id)
    if not role:
        return None

    update_data = role_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)

    session.add(role)
    session.commit()
    session.refresh(role)
    return role


# --- Delete ---
def delete_role(session: Session, role_id: int) -> list[int | None]:
    """Supprime un rôle et dissocie tous les utilisateurs associés.

    Avant suppression, tous les utilisateurs ayant ce rôle voient leur `role_id`
    remis à None.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        role_id (int): L'ID du rôle à supprimer.

    Returns:
        list[int | None]: La liste des IDs des utilisateurs affectés par la suppression.
                          Retourne une liste vide si le rôle n'existe pas.
    """
    role = session.get(Role, role_id)
    if not role:
        return []

    users_with_role = session.exec(select(User).where(User.role_id == role_id)).all()

    users_affected = [u.id for u in users_with_role]

    for u in users_with_role:
        u.role_id = None

    session.delete(role)
    session.commit()

    return users_affected
