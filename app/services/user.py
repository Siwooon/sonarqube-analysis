from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.repositories.emprunt import EmpruntRepository
from app.schemas.user import UserCreate, User

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.emprunt_repo = EmpruntRepository(db)

    def list_users(self) -> List[User]:
        users = self.user_repo.list()
        return [User.from_orm(u) for u in users]

    def create_user(self, user_in: UserCreate) -> User:
        # tu peux vérifier unicité email ici ou via exception SQLAlchemy
        u = self.user_repo.create(user_in)
        return User.from_orm(u)

    def delete_user(self, user_id: str) -> User:
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Utilisateur non trouvé")
        # **Logique métier**: on ne supprime pas s'il a un emprunt en cours
        emprunts = self.emprunt_repo.list()
        in_progress = [e for e in emprunts if e.user_id == user_id]
        if in_progress:
            raise ValueError("Impossible de supprimer un utilisateur avec des emprunts en cours")
        self.user_repo.delete(user)
        return User.from_orm(user)
