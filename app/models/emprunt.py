# app/models/emprunt.py

import uuid
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

def gen_uuid() -> str:
    return str(uuid.uuid4())

class Emprunt(Base):
    __tablename__ = "emprunts"

    # UUID de l'emprunt
    id = Column(String, primary_key=True, default=gen_uuid)

    # clé interne vers users.pk (jamais exposée)
    user_pk = Column(
        Integer,
        ForeignKey("users.pk", ondelete="CASCADE"),
        nullable=False
    )

    # UUID de la ressource
    ressource_id = Column(
        String,
        ForeignKey("ressources.id", ondelete="CASCADE"),
        nullable=False
    )

    date_emprunt = Column(Date,  nullable=False)
    date_retour  = Column(Date,  nullable=False)

    # relations SQLAlchemy
    user      = relationship("User",     back_populates="emprunts")
    ressource = relationship("Ressource", back_populates="emprunts")

    @property
    def user_id(self) -> str:
        """
        Expose l'UUID public de l'utilisateur pour Pydantic.
        """
        return self.user.id
