# app/services/emprunt.py

from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.emprunt import EmpruntRepository
from app.repositories.user import UserRepository
from app.repositories.ressource import RessourceRepository
from app.schemas.emprunt import EmpruntCreate, Emprunt

class EmpruntService:
    def __init__(self, db: Session):
        self.empr_repo = EmpruntRepository(db)
        self.user_repo = UserRepository(db)
        self.res_repo  = RessourceRepository(db)

    def list_emprunts(self, skip: int = 0, limit: int = 100) -> List[Emprunt]:
        all_e = self.empr_repo.list(skip=skip, limit=limit)
        return [Emprunt.from_orm(e) for e in all_e]

    def get_emprunt(self, empr_id: str) -> Optional[Emprunt]:
        e = self.empr_repo.get(empr_id)
        return Emprunt.from_orm(e) if e else None

    def create_emprunt(self, empr_in: EmpruntCreate) -> Emprunt:
        # 1. Vérifier que l'utilisateur existe (via UUID public)
        user = self.user_repo.get(empr_in.user_id)
        if not user:
            raise ValueError("Utilisateur non trouvé")

        # 2. Vérifier que la ressource existe et est disponible
        res = self.res_repo.get(empr_in.ressource_id)
        if not res:
            raise ValueError("Ressource non trouvée")
        if not res.disponible:
            raise ValueError("Ressource déjà empruntée")

        # 3. Créer l'emprunt en passant user.pk (la clé interne)
        e = self.empr_repo.create(
            user_pk=user.pk,
            ressource_id=empr_in.ressource_id,
            date_emprunt=empr_in.date_emprunt,
            date_retour=empr_in.date_retour
        )

        # 4. Mettre à jour la disponibilité de la ressource
        res.disponible = False
        # Persister ce changement
        self.res_repo.db.commit()

        return Emprunt.from_orm(e)

    def rendre_emprunt(self, empr_id: str) -> Emprunt:
        # 1. Récupérer l'emprunt
        e = self.empr_repo.get(empr_id)
        if not e:
            raise ValueError("Emprunt non trouvé")

        # 2. Remettre la ressource disponible
        res = self.res_repo.get(e.ressource_id)
        if res:
            res.disponible = True
            self.res_repo.db.commit()

        # 3. Supprimer l'emprunt
        self.empr_repo.delete(e)

        return Emprunt.from_orm(e)
