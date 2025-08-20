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
│   ├── db
│   │   ├── scripts/
│   │   │   ├── Dockerfile.data         # Dockerfile pour la création et insertion des données test
│   │   │   ├── Dockerfile.init         # Dockerfile pour la création des tables
│   │   │   ├── fake_data.py            # Script de création et insertion des données test
│   │   │   ├── init.py                 # Script pour la création des tables (basées sur les SQL Models)
│   │   │
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
│   ├── Dockerfile.api                  # Dockerfile pour l'image de l'API
│   ├── main.py                         # Point d'entrée FastAPI
│
├── tests/                              # Fichiers de tests, même structure que l'app/
│   │
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
├── pytest.ini                          # Configs de Black, isort, mypy
├── README.md
├── requirements.txt                    # Dépendances Python
├── template.env                        # Fichier d'exemple pour le .env
```

### Utilisation de l'application

0. Créer et remplir le fichier `.env`, voir le `template.env`

<hr>

#### Option 1 - Lancement avec `Docker` (sans utiliser de docker-compose)

1. Création du réseau pour les conteneurs Docker
```bash
docker network create mynet
```

2. Téléchargement de la dernière version de l'image `Postgres` officielle
```bash
docker pull postgres:15.6
```

3. Lancement de l'image Postgres avec les bons paramètres
```bash
docker run -d \
  --name my-postgres \
  --env-file .env \
  --network mynet \
  -v pgdata:/var/lib/postgresql/data \
  postgres
```
Possibilité d'ajouter la ligne `-p 5432:5432` si vous comptez consulter la BDD depuis DBeaver ou autre outil (en dehors du réseau Docker `mynet`), elle peut d'ailleurs causer des problèmes de ports si vous avez déjà un `Postgres` en local ou de sécurité.

4. Construction des images à partir des différents `Dockerfiles`
- Pour le script de création des tables (en se basant sur les `SQL Models`) :
```bash
docker build -f app/db/scripts/Dockerfile.tables -t mytables .
```

- Pour le script de création et insertion de données de test (avec `Faker`) :
```bash
docker build -f app/db/scripts/Dockerfile.data -t myfakedata .
```

- Puis pour l'API :
```bash
docker build -f app/Dockerfile.api -t myapi .
```

5. Lancement des images précédemment construites (ordre à respecter ici)
```bash
docker run -d --name mytables --env-file .env --network mynet mytables
```

```bash
docker run -d --name myfakedata --env-file .env --network mynet myfakedata
```

```bash
docker run -d --name myapi --env-file .env --network mynet -p 8000:8000  myapi
```

<hr>

#### Option 2 - Lancement avec un `docker-compose.yml`

1. Lancement du `docker-compose` qui orchestre la construction et le lancement des différentes images
```bash
docker compose up --build
```

<hr>

- Accès à l’API : http://127.0.0.1:8000  
- Documentation interactive Swagger : http://127.0.0.1:8000/docs