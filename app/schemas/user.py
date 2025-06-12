# app/schemas/user.py

from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str
    prenom: str
    mail: EmailStr
    numero_telephone: str
    nationalite: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
