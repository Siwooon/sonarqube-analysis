# app/schemas/emprunt.py

from typing import Optional, List
from datetime import date
from pydantic import BaseModel, ConfigDict

class EmpruntBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: str
    ressource_id: str
    date_emprunt: date
    date_retour: date

class EmpruntCreate(EmpruntBase):
    pass

class Emprunt(EmpruntBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            date: lambda v: v.strftime("%d-%m-%Y") if v else None
        }
    )
    id: str
