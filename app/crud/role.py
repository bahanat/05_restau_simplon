from sqlmodel import Session, select
from typing import List, Optional
from app.models.users_et_roles import Role
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
