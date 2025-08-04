# RESTau Simplon

## Système de gestion de commandes pour un restaurant

### Structure du projet
```bash
.
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── requirements.txt
```

### Utilisation de l'app

1. Installation des dépendances
```bash
pip install -r requirements.txt
```

2. Lancement de l'API
```bash
uvicorn main:app --reload
```

- Accès à l’API : http://127.0.0.1:8000  
- Documentation interactive Swagger : http://127.0.0.1:8000/docs