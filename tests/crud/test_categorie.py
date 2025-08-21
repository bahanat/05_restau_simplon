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

# --- test_Create ---


def test_create_categorie_persiste(session: Session) -> None:
    # Arrange
    data = CategorieCreate(nom="Livres")  # description="Catégorie de livres")

    # Act
    created = create_categorie(session, data)

    # Assert
    assert created.id is not None
    assert created.nom == "Livres"
    # assert created.description == "Catégorie de livres"

    # Relire depuis la base
    fetched = session.get(Categorie, created.id)
    assert fetched is not None
    assert fetched.nom == "Livres"


# ---test_Read ---


def test_get_all_categories_retourne_toutes(session: Session) -> None:
    # Arrange – insérestion des données
    cat1 = Categorie(nom="Livres")
    cat2 = Categorie(nom="Musique")
    session.add_all([cat1, cat2])
    session.commit()

    # Act – appeler la fonction à tester
    result = get_all_categories(session)

    # Assert – vérification du contenue
    assert isinstance(result, list)
    assert len(result) != 0
    noms = [c.nom for c in result]
    assert "Livres" in noms
    assert "Musique" in noms


def test_get_categorie_by_id_returns_categorie(session: Session) -> None:
    # Arrange
    # Déjà fait par faker

    # Act
    result = get_categorie_by_id(session, 1)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.nom is not None


def test_get_categorie_by_id_returns_none_when_not_found(session: Session) -> None:
    # Arrange
    # (aucune catégorie insérée)

    # Act
    result = get_categorie_by_id(session, 999)

    # Assert
    assert result is None


def test_get_categorie_by_nom_found(session: Session) -> None:
    # Arrange : insérer une catégorie avec un nom spécifique
    categorie = Categorie(nom="Livres")
    session.add(categorie)
    session.commit()

    # Act : rechercher par nom
    result = get_categorie_by_nom(session, "Livres")

    # Assert : vérifier que l'objet est bien trouvé
    assert result is not None
    assert result.nom == "Livres"


def test_get_categorie_by_nom_not_found(session: Session) -> None:
    # Arrange : ne rien insérer

    # Act : rechercher un nom inexistant
    result = get_categorie_by_nom(session, "Inexistant")

    # Assert : vérifier que le résultat est None
    assert result is None


# --- test_Update ---
def test_update_categorie_success(session: Session) -> None:
    # Arrange : créer une catégorie existante
    categorie = Categorie(nom="Ancien nom")
    session.add(categorie)
    session.commit()

    # Act : mettre à jour avec un nouveau nom et description
    data = CategorieUpdate(nom="Nouveau nom")
    assert categorie.id is not None
    updated = update_categorie(session, categorie.id, data)

    # Assert : vérifier que les champs sont bien mis à jour
    assert updated is not None
    assert updated.nom == "Nouveau nom"


def test_update_categorie_not_found(session: Session) -> None:
    # Arrange : ne pas insérer de catégorie correspondante

    # Act : essayer de mettre à jour un ID inexistant
    data = CategorieUpdate(nom="Ne devrait pas exister")
    updated = update_categorie(session, 999, data)

    # Assert : aucun objet n'est retourné
    assert updated is None


# --- test_Delete ---
def test_delete_categorie_success(session: Session) -> None:
    # Arrange : créer et insérer une catégorie à supprimer
    categorie = Categorie(nom="À supprimer", description="Catégorie temporaire")
    session.add(categorie)
    session.commit()
    assert categorie.id is not None
    # Act : supprimer la catégorie existante
    result = delete_categorie(session, categorie.id)

    # Assert : vérifier que la suppression a réussi et que la catégorie n'existe plus
    assert result is True
    assert session.get(Categorie, categorie.id) is None


def test_delete_categorie_not_found(session: Session) -> None:
    # Arrange : ne pas insérer de catégorie avec cet ID

    # Act : tenter de supprimer un ID inexistant
    result = delete_categorie(session, 999)

    # Assert : suppression échouée, résultat False
    assert result is False
