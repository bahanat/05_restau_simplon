from fastapi import FastAPI

from app.api.v1 import user
from app.api.v1 import commande


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur votre API FastAPI !"}


app.include_router(user.router)
app.include_router(commande.router)
