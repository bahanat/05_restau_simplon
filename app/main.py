from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime

from app.api.v1 import categorie, produit
from app.api.v1 import user
from app.api.v1 import commande
from app.api.v1 import role


app = FastAPI(title="RESTAU_SIMPLON 🍽️")

# Inclusion des routes de l'API v1
app.include_router(categorie.router)
app.include_router(produit.router)
app.include_router(user.router)
app.include_router(commande.router)
app.include_router(role.router)


# Montre le dossier static à l'URL /static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    return f"""
    <html>
        <head>
            <title>RESTAU_SIMPLON</title>
            <style>
                body {{
                    background-color: #f8f9fa;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    text-align: center;
                    padding: 50px;
                    color: #333;
                }}
                img {{
                    width: 150px;
                    margin-bottom: 20px;
                }}
                h1 {{
                    font-size: 2.5em;
                    color: #e63946;
                }}
                p {{
                    font-size: 1.2em;
                    margin: 10px 0;
                }}
                a {{
                    color: #1d3557;
                    text-decoration: none;
                    font-weight: bold;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .card {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    display: inline-block;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <img src="/static/logo.png" alt="Logo RESTAU_SIMPLON"/>
                <h1>Bienvenue sur RESTAU_SIMPLON 🍽️</h1>
                <p><strong>Version :</strong> 1.0</p>
                <p><strong>Auteur :</strong> Izak | Anathole | HARLEY</p>
                <p><a href="/docs">📚 Accéder à la documentation Swagger</a></p>
                <p><em>Horodatage :</em> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
    </html>
    """
