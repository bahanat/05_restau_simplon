from sqlmodel import Session

from app.crud.categorie import (
    create_categorie,
    delete_categorie,
    get_all_categories,
    get_categorie_by_id,
    get_categorie_by_nom,
    update_categorie,
)
from app.models.commandes_et_produits import Categorie
from app.schemas.categorie import CategorieCreate, CategorieUpdate


def test_create_category_persists(session: Session) -> None:
    """Teste la création et la persistance d'une catégorie dans la base.

    Vérifie que l'objet créé a un ID, que le nom correspond et que l'objet
    peut être relu depuis la base de données.
    """
    data = CategorieCreate(nom="Livres")
    created = create_categorie(session, data)

    assert created.id is not None
    assert created.nom == "Livres"

    fetched = session.get(Categorie, created.id)
    assert fetched is not None
    assert fetched.nom == "Livres"


def test_get_all_categories_returns_all(session: Session) -> None:
    """Teste la récupération de toutes les catégories.

    Insère des catégories et vérifie que get_all_categories retourne une liste
    contenant toutes les catégories insérées.
    """
    cat1 = Categorie(nom="Livres")
    cat2 = Categorie(nom="Musique")
    session.add_all([cat1, cat2])
    session.commit()

    result = get_all_categories(session)

    assert isinstance(result, list)
    assert len(result) != 0
    noms = [c.nom for c in result]
    assert "Livres" in noms
    assert "Musique" in noms


def test_get_category_by_id_returns_category(session: Session) -> None:
    """Teste la récupération d'une catégorie existante par ID."""
    result = get_categorie_by_id(session, 1)

    assert result is not None
    assert result.id == 1
    assert result.nom is not None


def test_get_category_by_id_returns_none_when_not_found(session: Session) -> None:
    """Teste la récupération d'une catégorie inexistante retourne None."""
    result = get_categorie_by_id(session, 999)
    assert result is None


def test_get_category_by_name_found(session: Session) -> None:
    """Teste la récupération d'une catégorie existante par nom."""
    categorie = Categorie(nom="Livres")
    session.add(categorie)
    session.commit()

    result = get_categorie_by_nom(session, "Livres")

    assert result is not None
    assert result.nom == "Livres"


def test_get_category_by_name_not_found(session: Session) -> None:
    """Teste la récupération d'une catégorie inexistante par nom retourne None."""
    result = get_categorie_by_nom(session, "Inexistant")
    assert result is None


def test_update_category_success(session: Session) -> None:
    """Teste la mise à jour d'une catégorie existante.

    Vérifie que les champs sont modifiés et que l'objet retourné correspond.
    """
    categorie = Categorie(nom="Ancien nom")
    session.add(categorie)
    session.commit()

    data = CategorieUpdate(nom="Nouveau nom")
    assert categorie.id is not None
    updated = update_categorie(session, categorie.id, data)

    assert updated is not None
    assert updated.nom == "Nouveau nom"


def test_update_category_not_found(session: Session) -> None:
    """Teste la mise à jour d'une catégorie inexistante retourne None."""
    data = CategorieUpdate(nom="Ne devrait pas exister")
    updated = update_categorie(session, 999, data)
    assert updated is None


def test_delete_category_success(session: Session) -> None:
    """Teste la suppression réussie d'une catégorie existante.

    Vérifie que delete_categorie retourne True et que la catégorie n'existe plus.
    """
    categorie = Categorie(nom="À supprimer", description="Catégorie temporaire")
    session.add(categorie)
    session.commit()
    assert categorie.id is not None

    result = delete_categorie(session, categorie.id)

    assert result is True
    assert session.get(Categorie, categorie.id) is None


def test_delete_category_not_found(session: Session) -> None:
    """Teste la suppression d'une catégorie inexistante retourne False."""
    result = delete_categorie(session, 999)
    assert result is False
