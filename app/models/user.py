from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from .utils import gen_uuid

class User(Base):
    __tablename__ = "users"

    # IDENTIFIANT INTERNE (jamais exposé dans Swagger)
    pk = Column(Integer, primary_key=True, index=True)
    # UUID PUBLIC (ce que tu expose dans tes schémas / Swagger)
    id = Column(String, unique=True, default=gen_uuid, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    numero_telephone = Column(String, nullable=False)
    nationalite = Column(String, nullable=False)

    emprunts = relationship(
        "Emprunt",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )