from sqlmodel import Session, create_engine
from faker import Faker
import random

from app.core.security import hash_mdp
from app.models.users_et_roles import User, Role, RoleEnum
from app.models.commandes_et_produits import (
    Categorie,
    Produit,
    Commande,
    DetailCommande,
    StatusEnum,
)

fake = Faker("fr_FR")

from app.core.config import (
    settings,
)

engine = create_engine(settings.DATABASE_URL, echo=False)


# Utilisation de Faker pour la création de fausses données pour notre DB de test
def create_fake_data():
    with Session(engine) as session:
        # --- 1. Créer quelques rôles ---
        role_admin = Role(nom=RoleEnum.admin)
        role_client = Role(nom=RoleEnum.client)
        role_serveur = Role(nom=RoleEnum.serveur)
        session.add_all([role_admin, role_client, role_serveur])
        session.commit()

        # --- 2. Créer quelques utilisateurs ---
        users = []
        for _ in range(5):
            user = User(
                nom=fake.last_name(),
                prenom=fake.first_name(),
                email=fake.unique.email(),
                adresse=fake.address(),
                telephone=fake.phone_number(),
                mot_de_passe=hash_mdp("group1start2025"),
                role_id=random.choice([role_admin.id, role_client.id, role_serveur.id]),
                date_creation=fake.date_time_this_year(),
            )
            users.append(user)
        session.add_all(users)
        session.commit()

        # --- 3. Créer des catégories ---
        categories = [
            Categorie(nom="Entrée"),
            Categorie(nom="Plat"),
            Categorie(nom="Dessert"),
            Categorie(nom="Boisson"),
            Categorie(nom="Autre"),
        ]
        session.add_all(categories)
        session.commit()

        # --- 4. Créer des produits ---
        produits = []
        for cat in categories:
            for _ in range(5):
                produit = Produit(
                    nom=fake.word().capitalize(),
                    description=fake.sentence(),
                    prix=round(random.uniform(1, 35), 2),
                    categorie_id=cat.id,
                    stock=random.randint(0, 25),
                )
                produits.append(produit)
        session.add_all(produits)
        session.commit()

        # --- 5. Créer des commandes ---
        for _ in range(10):
            client = random.choice(users)
            commande = Commande(
                client_id=client.id,
                date_commande=fake.date_time_this_year(),
                statut=random.choice(list(StatusEnum)),
                montant_total=0.0,
            )
            session.add(commande)
            session.commit()

            # --- 6. Ajouter des détails à la commande ---
            produits_selectionnes = random.sample(produits, k=random.randint(1, 4))
            montant_total = 0
            for prod in produits_selectionnes:
                quantite = random.randint(1, 3)
                detail = DetailCommande(
                    commande_id=commande.id, produit_id=prod.id, quantite=quantite
                )
                montant_total += prod.prix * quantite
                session.add(detail)

            # --- 7. Calcul automatique du montant total ---
            commande.montant_total = round(montant_total, 2)
            session.add(commande)
            session.commit()


if __name__ == "__main__":
    create_fake_data()
    print("Données de test insérées avec succès !")
