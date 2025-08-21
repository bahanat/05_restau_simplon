from typing import Sequence

from sqlmodel import Session

from app.models.commandes_et_produits import Commande, DetailCommande, Produit
from app.schemas.detail import DetailsUpdate


# --- Update ---
def update_details_commande(
    session: Session, commande: Commande, details_data: Sequence[DetailsUpdate]
) -> None:
    """Met à jour les détails d'une commande et recalcul le montant total.

    Cette fonction supprime les détails existants de la commande,
    ajoute les nouveaux détails fournis et met à jour le montant total
    de la commande en fonction des prix des produits.

    Args:
        session (Session): La session SQLModel utilisée pour la transaction.
        commande (Commande): La commande à mettre à jour.
        details_data (Sequence[DetailsUpdate]): Une séquence d'objets DetailsUpdate
            représentant les nouveaux détails de la commande.

    Returns:
        None
    """
    # Supprimer les détails existants
    for detail in list(commande.details):
        session.delete(detail)
    session.flush()

    # Ajouter les nouveaux détails
    new_details = []
    for det in details_data:
        detail_instance = DetailCommande(
            commande_id=commande.id,
            produit_id=det.produit_id,
            quantite=det.quantite,
        )
        session.add(detail_instance)
        new_details.append(detail_instance)

    commande.details = new_details

    # Recalculer le montant total
    montant_total = 0.0
    for detail in new_details:
        produit = session.get(Produit, detail.produit_id)
        if produit:
            montant_total += produit.prix * detail.quantite

    commande.montant_total = round(montant_total, 2)
    session.add(commande)
