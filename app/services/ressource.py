from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.ressource import RessourceRepository
from app.schemas.ressource import RessourceCreate, Ressource

class RessourceService:
    def __init__(self, db: Session):
        self.res_repo = RessourceRepository(db)

    def list_ressources(
        self,
        type_filter: Optional[str] = None,
        dispo_filter: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Ressource]:
        all_res = self.res_repo.list(
            type_filter=type_filter,
            dispo_filter=dispo_filter,
            skip=skip,
            limit=limit
        )
        return [Ressource.from_orm(r) for r in all_res]

    def create_ressource(self, res_in: RessourceCreate) -> Ressource:
        r = self.res_repo.create(res_in)
        return Ressource.from_orm(r)

    def update_ressource(self, res_id: str, res_in: RessourceCreate) -> Ressource:
        r = self.res_repo.get(res_id)
        if not r:
            raise ValueError("Ressource non trouvée")
        updated = self.res_repo.update(r, res_in)
        return Ressource.from_orm(updated)

    def delete_ressource(self, res_id: str) -> Ressource:
        r = self.res_repo.get(res_id)
        if not r:
            raise ValueError("Ressource non trouvée")
        self.res_repo.delete(r)
        return Ressource.from_orm(r)
