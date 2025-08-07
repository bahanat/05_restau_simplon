from sqlmodel import Session

from app.models.commandes_et_produits import Commande, DetailCommande, Produit


def update_details_commande(
    session: Session, commande: Commande, details_data: list[dict]
) -> None:
    for detail in list(commande.details):
        session.delete(detail)
    session.flush()

    new_details = []
    for det_data in details_data:
        detail_instance = DetailCommande(
            commande_id=commande.id,
            produit_id=det_data["produit_id"],
            quantite=det_data["quantite"],
        )
        session.add(detail_instance)
        new_details.append(detail_instance)

    commande.details = new_details

    session.flush()

    montant_total = 0.0
    for detail in new_details:
        produit = session.get(Produit, detail.produit_id)
        if produit:
            montant_total += produit.prix * detail.quantite

    commande.montant_total = round(montant_total, 2)
    session.add(commande)
