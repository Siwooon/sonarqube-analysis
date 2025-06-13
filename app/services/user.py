from typing import List, Optional
from sqlalchemy.orm import Session
from pydantic_extra_types.country import CountryShortName
from app.repositories.user import UserRepository
from app.repositories.emprunt import EmpruntRepository
from app.schemas.user import UserCreate, User


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.emprunt_repo = EmpruntRepository(db)

    def _to_user_model(self, u) -> User:
        return User.model_validate({
            "id": u.id,
            "nom": u.nom,
            "prenom": u.prenom,
            "mail": u.mail,
            "numero_telephone": u.numero_telephone,
            "nationalite": u.nationalite,
        })


    def list_users(self) -> List[User]:
        users = self.user_repo.list()
        return [self._to_user_model(u) for u in users]

    def create_user(self, user_in: UserCreate) -> User:
        u = self.user_repo.create(user_in)
        return self._to_user_model(u)

    def delete_user(self, user_id: str) -> User:
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Utilisateur non trouvé")
        # Logique métier : ne pas supprimer s'il a un emprunt en cours
        emprunts = self.emprunt_repo.list()
        in_progress = [e for e in emprunts if e.user_id == user_id]
        if in_progress:
            raise ValueError("Impossible de supprimer un utilisateur avec des emprunts en cours")
        self.user_repo.delete(user)
        return self._to_user_model(user)
