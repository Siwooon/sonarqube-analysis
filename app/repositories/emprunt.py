# app/repositories/emprunt.py

from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.emprunt import Emprunt as EmpruntModel

class EmpruntRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_pk: int,
        ressource_id: str,
        date_emprunt: date,
        date_retour: date
    ) -> EmpruntModel:
        """
        Crée un nouvel emprunt en base en utilisant la clé primaire interne de l'utilisateur.
        """
        em = EmpruntModel(
            user_pk=user_pk,
            ressource_id=ressource_id,
            date_emprunt=date_emprunt,
            date_retour=date_retour
        )
        self.db.add(em)
        self.db.commit()
        self.db.refresh(em)
        return em

    def get(self, emprunt_id: str) -> Optional[EmpruntModel]:
        return (
            self.db
            .query(EmpruntModel)
            .filter(EmpruntModel.id == emprunt_id)
            .first()
        )

    def list(self, skip: int = 0, limit: int = 100) -> List[EmpruntModel]:
        return (
            self.db
            .query(EmpruntModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(self, em: EmpruntModel) -> None:
        self.db.delete(em)
        self.db.commit()
