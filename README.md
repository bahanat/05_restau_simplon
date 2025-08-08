# RESTau Simplon

## Système de gestion de commandes pour un restaurant

### Structure du projet
```bash
restausimplon/
│
├── app/
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── categorie.py            # Routes Catégories
│   │   │   ├── commande.py             # Routes Commandes
│   │   │   ├── produit.py              # Routes Produits
│   │   │   ├── role.py                 # Routes Rôles
│   │   │   ├── user.py                 # Routes Users
│   │   │
│   │   ├── deps.py                     # Dépendances réutilisables
│   │
│   ├── core/
│   │   ├── config.py                   # Variables d'environnement, paramètres app
│   │   ├── security.py                 # JWT, hashage mots de passe
│   │
│   ├── crud/
│   │   ├── categorie.py                # Fonctions CRUD Catégories
│   │   ├── commande.py                 # Fonctions CRUD Commandes
│   │   ├── details.py                  # Fonctions CRUD Détails
│   │   ├── produit.py                  # Fonctions CRUD Produits
│   │   ├── user.py                     # Fonctions CRUD Users
│   │
│   ├── db/
│   │   ├── session.py                  # Connexion DB (engine, session)
│   │   ├── base.py                     # Import global des modèles pour Alembic
│   │
│   ├── models/
│   │   ├── commandes_et_produits.py    # Modèles SQLModel pour les produits, commandes et leurs détails
│   │   ├── users_et_roles.py           # Modèles SQLModel pour les utilisateurs et leurs rôles
│   │
│   ├── schemas/
│   │   ├── categorie.py                # Pydantic : CategorieCreate, CategorieRead, etc.
│   │   ├── commande.py                 # Pydantic : CommandCreate, CommandRead, etc.
│   │   ├── detail.py                   # Pydantic : DetailUpdate, etc.
│   │   ├── produit.py                  # Pydantic : ProductCreate, ProductRead, etc.
│   │   ├── role.py                     # Pydantic : RoleCreate, RoleRead, etc.
│   │   ├── user.py                     # Pydantic : UserCreate, UserRead, etc.
│   │
│   ├── utils/
│   │   ├── helpers.py                  # Fonctions utilitaires
│   │
│   ├── db_creation.py                  # Script de création en local de la base et ses tables avec fausses données
│   ├── main.py                         # Point d'entrée FastAPI
│
├── .env                                # Variables d'environnement
├── requirements.txt                    # Dépendances Python
├── README.md
```

### Utilisation de l'app

1. Installation des dépendances
```bash
pip install -r requirements.txt
```

2. Renseignement des variables dans le `.env` (voir `template.env`)

3. Création de la base de données de test en local
```bash
python -m app.db_creation
```

4. Lancement de l'API
```bash
uvicorn app.main:app --reload
```

- Accès à l’API : http://127.0.0.1:8000  
- Documentation interactive Swagger : http://127.0.0.1:8000/docs