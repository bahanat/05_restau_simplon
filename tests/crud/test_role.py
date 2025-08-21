from collections.abc import Sequence

from sqlmodel import Session, select

from app.models.users_et_roles import Role, User
from app.schemas.role import RoleCreate, RoleUpdate


def role_creation(session: Session, role_in: RoleCreate) -> Role:
    """Crée un nouveau rôle et le persiste en base.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        role_in (RoleCreate): données du rôle à créer

    Returns:
        Role: instance du rôle créé
    """
    role = Role(nom=role_in.nom)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def get_all_roles(session: Session) -> Sequence[Role]:
    """Récupère tous les rôles existants.

    Args:
        session (Session): session SQLAlchemy/SQLModel

    Returns:
        Sequence[Role]: liste des rôles
    """
    return session.exec(select(Role)).all()


def get_role_by_id(session: Session, role_id: int) -> Role | None:
    """Récupère un rôle par son ID.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        role_id (int): identifiant du rôle

    Returns:
        Role | None: rôle correspondant ou None si non trouvé
    """
    return session.get(Role, role_id)


def update_role(session: Session, role_id: int, role_in: RoleUpdate) -> Role | None:
    """Met à jour un rôle existant avec de nouvelles valeurs.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        role_id (int): ID du rôle à mettre à jour
        role_in (RoleUpdate): données à mettre à jour

    Returns:
        Role | None: rôle mis à jour ou None si l'ID n'existe pas
    """
    role = get_role_by_id(session, role_id)
    if not role:
        return None

    update_data = role_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)

    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def delete_role(session: Session, role_id: int) -> list[int | None]:
    """Supprime un rôle et détache tous les utilisateurs associés.

    Args:
        session (Session): session SQLAlchemy/SQLModel
        role_id (int): ID du rôle à supprimer

    Returns:
        list[int | None]: liste des IDs des utilisateurs dont le rôle a été supprimé
    """
    role = get_role_by_id(session, role_id)
    if not role:
        return []

    # Détacher les utilisateurs associés
    users = session.exec(select(User).where(User.role_id == role.id)).all()
    affected_users = []
    for user in users:
        user.role_id = None
        affected_users.append(user.id)

    session.delete(role)
    session.commit()
    return affected_users
