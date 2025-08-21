# RESTau Simplon

## Système de gestion de commandes pour un restaurant
Application FastAPI avec gestion des utilisateurs, rôles, catégories, produits et commandes.

## Structure du projet
```bash
restausimplon/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── categorie.py            # Routes Catégories
│   │   │   ├── commande.py             # Routes Commandes
│   │   │   ├── login.py                # Routes Login
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
│   │   ├── role.py                     # Fonctions CRUD Rôles
│   │   ├── user.py                     # Fonctions CRUD Users
│   │
│   ├── db
│   │   ├── scripts/
│   │   │   ├── Dockerfile.data         # Dockerfile pour la création et insertion des données test
│   │   │   ├── Dockerfile.init         # Dockerfile pour la création des tables
│   │   │   ├── fake_data.py            # Script de création et insertion des données test
│   │   │   ├── init.py                 # Script pour la création des tables (basées sur les SQL Models)
│   │   │
│   │   ├── base.py                     # Import global des modèles pour Alembic
│   │   ├── session.py                  # Connexion DB (engine, session)
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
│   ├── Dockerfile.api                  # Dockerfile pour l'image de l'API
│   ├── main.py                         # Point d'entrée FastAPI
│
├── static/
│   ├── logo.png
│
├── tests/                              # Fichiers de tests, même structure que l'app/
│   ├── api/
│   ├── crud/
│   ├── db/
│   ├── ...
│   ├── conftest.py                     # Fichier de fixtures pour les tests (session et engine spécifiques)
│
├── .dockerignore
├── .env                                # Variables d'environnement
├── .flake8                             # Config de Flake
├── .gitignore
├── docker-compose.test.yml             # Docker Compose spécifique aux tests (avec DB de test)
├── docker-compose.yml                  # Docker Compose de l'app en version prod
├── Dockerfile.test                     # Dockerfile pour l'image des fichiers tests/
├── LICENSE
├── Makefile                            # Makefile pour le formattage du code et tests
├── pyproject.toml                      # Configs de Black, isort, mypy
├── pytest.ini                          # Config de Pytest
├── README.md
├── requirements.txt                    # Dépendances Python
├── template.env                        # Fichier d'exemple pour le .env
```

## Installation & utilisation

### 0. Préparer l’environnement
1. Copier le fichier `.env` depuis le `template.env` et remplir les variables nécessaires.
```bash
cp template.env .env
```

<hr>

### Option 1 – Avec Docker seul
1. Créer le réseau Docker :
```bash
docker network create mynet
```

2. Télécharger l'image Postgres :
```bash
docker pull postgres:15.6
```

3. Lancer Postgres :
```bash
docker run -d \
  --name my-postgres \
  --env-file .env \
  --network mynet \
  -v pgdata:/var/lib/postgresql/data \
  postgres
```

4. Construire les images nécessaires :
- Pour le script de création des tables (en se basant sur les `SQL Models`) :
```bash
docker build -f app/db/scripts/Dockerfile.tables -t mytables .
docker build -f app/db/scripts/Dockerfile.data -t myfakedata .
docker build -f app/Dockerfile.api -t myapi .
```

5. Lancer les conteneurs dans l’ordre :
```bash
docker run -d --name mytables --env-file .env --network mynet mytables
docker run -d --name myfakedata --env-file .env --network mynet myfakedata
docker run -d --name myapi --env-file .env --network mynet -p 8000:8000  myapi
```

<hr>

### Option 2 – Avec Docker Compose
```bash
docker compose up --build
```

- Accès à l’API : http://127.0.0.1:8000  
- Documentation interactive Swagger : http://127.0.0.1:8000/docs

<hr>

## Tests

1. Lancer le conteneur Postgres de test :
```bash
docker compose -f docker-compose.test.yml up -d my-test-postgres
```

2. Initialiser la base de test et insérer des données fake :
```bash
docker compose -f docker-compose.test.yml run --rm db-init
```

3. Exécuter les tests :
```bash
docker compose -f docker-compose.test.yml run --rm tests
```

<hr>

## CI/CD

Le projet inclut un workflow GitHub Actions décomposé en :
- CI : branch `develop`
  - Lint, formatage, type-check, tests unitaires.
  - La fusion sur `develop` est bloquée tant que la CI ne passe pas (via branch protection rules).

- CD : branch `main`
  - Déploiement automatique via Docker Compose.

<hr>

## API Documentation

### Rôles
| Méthode | Endpoint           | Description                      | Paramètres                                | Retour                                       |
| ------- | ------------------ | -------------------------------- | ----------------------------------------- | -------------------------------------------- |
| POST    | `/roles/`          | Crée un nouveau rôle utilisateur | `role_data` (RoleCreate)                  | RoleRead                                     |
| GET     | `/roles/`          | Récupère tous les rôles          | —                                         | List\[RoleRead]                              |
| GET     | `/roles/{role_id}` | Récupère un rôle par ID          | `role_id` (int)                           | RoleRead                                     |
| PUT     | `/roles/{role_id}` | Met à jour un rôle existant      | `role_id` (int), `role_data` (RoleUpdate) | RoleRead                                     |
| DELETE  | `/roles/{role_id}` | Supprime un rôle par ID          | `role_id` (int)                           | dict: message, utilisateurs\_affectés, count |

### Users
| Méthode | Endpoint           | Description                    | Paramètres                                | Retour          |
| ------- | ------------------ | ------------------------------ | ----------------------------------------- | --------------- |
| POST    | `/users/`          | Crée un nouvel utilisateur     | `user_data` (UserCreate)                  | UserRead        |
| GET     | `/users/`          | Récupère tous les utilisateurs | —                                         | List\[UserRead] |
| GET     | `/users/{user_id}` | Récupère un utilisateur par ID | `user_id` (int)                           | UserRead        |
| PUT     | `/users/{user_id}` | Met à jour un utilisateur      | `user_id` (int), `user_data` (UserUpdate) | UserRead        |
| DELETE  | `/users/{user_id}` | Supprime un utilisateur        | `user_id` (int)                           | None            |

### Authentification / Login
| Méthode | Endpoint | Description                | Paramètres         | Retour            |
| ------- | -------- | -------------------------- | ------------------ | ----------------- |
| POST    | `/login` | Authentifie un utilisateur | `body` (UserLogin) | UserLoginResponse |


### Catégories
| Méthode | Endpoint                     | Description                 | Paramètres                                     | Retour               |
| ------- | ---------------------------- | --------------------------- | ---------------------------------------------- | -------------------- |
| POST    | `/categories/`               | Crée une catégorie          | `data` (CategorieCreate)                       | CategorieRead        |
| GET     | `/categories/`               | Liste toutes les catégories | —                                              | List\[CategorieRead] |
| GET     | `/categories/{categorie_id}` | Récupère une catégorie      | `categorie_id` (int)                           | CategorieRead        |
| PUT     | `/categories/{categorie_id}` | Met à jour une catégorie    | `categorie_id` (int), `data` (CategorieUpdate) | CategorieRead        |
| DELETE  | `/categories/{categorie_id}` | Supprime une catégorie      | `categorie_id` (int)                           | None                 |

### Produits
| Méthode | Endpoint                 | Description             | Paramètres                                 | Retour             |
| ------- | ------------------------ | ----------------------- | ------------------------------------------ | ------------------ |
| POST    | `/produits/`             | Crée un produit         | `data` (ProduitCreate)                     | ProduitRead        |
| GET     | `/produits/`             | Liste tous les produits | —                                          | List\[ProduitRead] |
| GET     | `/produits/{produit_id}` | Récupère un produit     | `produit_id` (int)                         | ProduitRead        |
| PUT     | `/produits/{produit_id}` | Met à jour un produit   | `produit_id` (int), `data` (ProduitUpdate) | ProduitRead        |
| DELETE  | `/produits/{produit_id}` | Supprime un produit     | `produit_id` (int)                         | None               |

### Commandes
| Méthode | Endpoint                   | Description                            | Paramètres                                              | Retour              |
| ------- | -------------------------- | -------------------------------------- | ------------------------------------------------------- | ------------------- |
| POST    | `/commandes/`              | Crée une commande                      | `commande_data` (CommandeCreate)                        | CommandeRead        |
| GET     | `/commandes/{commande_id}` | Récupère une commande par ID           | `commande_id` (int)                                     | CommandeRead        |
| GET     | `/commandes/`              | Liste toutes les commandes ou filtrées | `client_id`, `date_commande`, `statut`                  | List\[CommandeRead] |
| PATCH   | `/commandes/{commande_id}` | Met à jour une commande                | `commande_id` (int), `commande_update` (CommandeUpdate) | CommandeRead        |
| DELETE  | `/commandes/{commande_id}` | Supprime une commande                  | `commande_id` (int)                                     | None                |
