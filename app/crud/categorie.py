from collections.abc import Sequence

from sqlmodel import Session, select

from app.models.commandes_et_produits import Categorie
from app.schemas.categorie import CategorieCreate, CategorieUpdate


# --- Create ---
def create_categorie(session: Session, categorie_data: CategorieCreate) -> Categorie:
    """Crée une nouvelle catégorie dans la base de données.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        categorie_data (CategorieCreate): Les données de la catégorie à créer.

    Returns:
        Categorie: L'objet Categorie créé et persistant en base.
    """
    categorie = Categorie.model_validate(categorie_data)
    session.add(categorie)
    session.commit()
    session.refresh(categorie)
    return categorie


# --- Read ---
def get_all_categories(session: Session) -> Sequence[Categorie]:
    """Récupère toutes les catégories de la base de données.

    Args:
        session (Session): La session SQLModel utilisée pour la requête.

    Returns:
        Sequence[Categorie]: Une liste de toutes les catégories existantes.
    """
    return session.exec(select(Categorie)).all()


# --- Read (par id) ---
def get_categorie_by_id(session: Session, categorie_id: int) -> Categorie | None:
    """Récupère une catégorie par son identifiant.

    Args:
        session (Session): La session SQLModel utilisée pour la requête.
        categorie_id (int): L'identifiant de la catégorie à récupérer.

    Returns:
        Categorie | None: La catégorie correspondante, ou None si elle n'existe pas.
    """
    return session.get(Categorie, categorie_id)


# --- Read (par nom) ---
def get_categorie_by_nom(session: Session, categorie_nom: str) -> Categorie | None:
    """Récupère une catégorie par son nom.

    Args:
        session (Session): La session SQLModel utilisée pour la requête.
        categorie_nom (str): Le nom de la catégorie à récupérer.

    Returns:
        Categorie | None: La catégorie correspondante, ou None si elle n'existe pas.
    """
    statement = select(Categorie).where(Categorie.nom == categorie_nom)
    return session.exec(statement).first()


# --- Update ---
def update_categorie(
    session: Session, categorie_id: int, data: CategorieUpdate
) -> Categorie | None:
    """Met à jour une catégorie existante avec de nouvelles données.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        categorie_id (int): L'identifiant de la catégorie à mettre à jour.
        data (CategorieUpdate): Les nouvelles valeurs à appliquer.

    Returns:
        Categorie | None: La catégorie mise à jour, ou None si elle n'existe pas.
    """
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(categorie, key, value)
    session.commit()
    session.refresh(categorie)
    return categorie


# --- Delete ---
def delete_categorie(session: Session, categorie_id: int) -> bool:
    """Supprime une catégorie existante par son identifiant.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        categorie_id (int): L'identifiant de la catégorie à supprimer.

    Returns:
        bool: True si la suppression a réussi, False si la catégorie n'existait pas.
    """
    categorie = session.get(Categorie, categorie_id)
    if not categorie:
        return False
    session.delete(categorie)
    session.commit()
    return True
