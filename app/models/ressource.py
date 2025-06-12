from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from .utils import gen_uuid

class Ressource(Base):
    __tablename__ = "ressources"

    id = Column(String, primary_key=True, default=gen_uuid)
    titre = Column(String, nullable=False)
    type = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)

    emprunts = relationship(
        "Emprunt",
        back_populates="ressource",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
