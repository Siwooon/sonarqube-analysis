# app/schemas/user.py

from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic_extra_types.country import CountryAlpha2

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: str
    prenom: str
    mail: EmailStr
    numero_telephone: str
    nationalite: CountryAlpha2

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
