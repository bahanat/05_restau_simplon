from fastapi import FastAPI
from app.api.v1.user import router as user_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur votre API FastAPI !"}


app.include_router(user_router)
