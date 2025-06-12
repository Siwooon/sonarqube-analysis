# app/api/main.py

from fastapi import FastAPI
from app.db.base import engine, Base
from app.api.routers.user import router as user_router
from app.api.routers.ressource import router as ressource_router
from app.api.routers.emprunt import router as emprunt_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Médiathèque API",
    description="API pour gérer une médiathèque (utilisateurs, ressources, emprunts)",
    version="1.0.0"
)

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """
    Crée les tables SQLAlchemy au démarrage de l'application.
    """
    Base.metadata.create_all(bind=engine)

# Inclusion des routers avec préfixes et tags
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(ressource_router, prefix="/ressources", tags=["ressources"])
app.include_router(emprunt_router, prefix="/emprunts", tags=["emprunts"])
