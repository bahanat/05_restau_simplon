from sqlmodel import Session, select

from app.crud.details import update_details_commande
from app.models.commandes_et_produits import Commande
from app.schemas.detail import DetailsUpdate


def test_update_details_commande(session: Session) -> None:
    commande = session.exec(select(Commande)).first()
    assert commande is not None
    old_total = commande.montant_total

    new_details = [
        DetailsUpdate(produit_id=1, quantite=2),
        DetailsUpdate(produit_id=2, quantite=3),
    ]

    update_details_commande(session, commande, new_details)
    session.commit()
    session.refresh(commande)

    assert len(commande.details) == 2
    assert commande.montant_total != old_total

    produits_quantites = {(d.produit_id, d.quantite) for d in commande.details}
    assert produits_quantites == {(1, 2), (2, 3)}
