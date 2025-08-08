from sqlmodel import Session, select
from typing import List, Optional
from app.models.users_et_roles import Role, User
from app.schemas.role import RoleCreate, RoleUpdate

# creation roles


def role_creation(session: Session, role_data: RoleCreate) -> Role:
    role = Role(nom=role_data.nom)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


# read tous les roles


def get_all_roles(session: Session) -> List[Role]:
    return session.exec(select(Role)).all()


# read role par id


def get_role_by_id(session: Session, role_id: int) -> Optional[Role]:
    return session.get(Role, role_id)


# update role


def update_role(
    session: Session, role_id: int, role_data: RoleUpdate
) -> Optional[Role]:
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


# delete role


def delete_role(session: Session, role_id: int) -> Optional[List[int]]:
    role = session.get(Role, role_id)
    if not role:
        return None

    users_with_role = session.exec(select(User).where(User.role_id == role_id)).all()

    users_affected = [u.id for u in users_with_role]

    for u in users_with_role:
        u.role_id = None

    session.delete(role)
    session.commit()

    return users_affected
