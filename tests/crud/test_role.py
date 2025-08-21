from sqlmodel import Session, select
from collections.abc import Sequence

from app.models.users_et_roles import Role, User
from app.schemas.role import RoleCreate, RoleUpdate


def role_creation(session: Session, role_in: RoleCreate) -> Role:
    role = Role(nom=role_in.nom)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def get_all_roles(session: Session) -> Sequence[Role]:
    return session.exec(select(Role)).all()


def get_role_by_id(session: Session, role_id: int) -> Role | None:
    return session.get(Role, role_id)


def update_role(session: Session, role_id: int, role_in: RoleUpdate) -> Role | None:
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
    role = get_role_by_id(session, role_id)
    if not role:
        return []

    # desvincular usuarios del rol
    users = session.exec(select(User).where(User.role_id == role.id)).all()
    affected_users = []
    for user in users:
        user.role_id = None
        affected_users.append(user.id)

    session.delete(role)
    session.commit()
    return affected_users
