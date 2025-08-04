# RESTau Simplon

## Système de gestion de commandes pour un restaurant

### Structure du projet
```bash
restausimplon/
│
├── app/
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                 # Dépendances réutilisables (ex : get_current_user)
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── commande.py         # Routes Commandes
│   │       ├── detail.py           # Routes Détails des commandes
│   │       ├── produit.py          # Routes Produits
│   │       ├── user.py             # Routes Users
│   │
│   ├── core/
│   │   ├── config.py               # Variables d'environnement, paramètres app
│   │   ├── security.py             # JWT, hashage mots de passe
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── commande.py             # Fonctions CRUD Commandes + Détails
│   │   ├── produit.py              # Fonctions CRUD Produits
│   │   ├── user.py                 # Fonctions CRUD Users
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py              # Connexion DB (engine, session)
│   │   ├── base.py                 # Import global des modèles pour Alembic
│   │   ├── migrations/             # Fichiers Alembic
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── commande.py             # Modèle SQLModel pour Commandes + Détails
│   │   ├── produit.py              # Modèle SQLModel pour Produits
│   │   ├── user.py                 # Modèle SQLModel pour Users
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── commande.py             # Pydantic : UserCreate, UserRead, etc.
│   │   ├── produit.py              # Pydantic : UserCreate, UserRead, etc.
│   │   ├── user.py                 # Pydantic : UserCreate, UserRead, etc.
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py              # Fonctions utilitaires
│   │
│   ├── __init__.py
│   ├── main.py                     # Point d'entrée FastAPI
│
├── .env                            # Variables d'environnement
├── requirements.txt                # Dépendances Python
├── README.md
```

### Utilisation de l'app

1. Installation des dépendances
```bash
pip install -r requirements.txt
```

2. Lancement de l'API (depuis le dossier `app/`)
```bash
uvicorn main:app --reload
```

- Accès à l’API : http://127.0.0.1:8000  
- Documentation interactive Swagger : http://127.0.0.1:8000/docs