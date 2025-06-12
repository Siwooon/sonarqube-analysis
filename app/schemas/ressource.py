# app/schemas/ressource.py

from enum import Enum
from pydantic import BaseModel, ConfigDict

class RessourceType(str, Enum):
    livre = "Livre"
    film = "Film"
    jeu = "Jeu"
    autre = "Autre"

class RessourceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    titre: str
    type: RessourceType
    auteur: str

class RessourceCreate(RessourceBase):
    pass

class Ressource(RessourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    disponible: bool
