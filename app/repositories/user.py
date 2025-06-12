from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_in: UserCreate) -> UserModel:
        user = UserModel(**user_in.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get(self, user_id: str) -> Optional[UserModel]:
        return (
            self.db
            .query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

    def list(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return (
            self.db
            .query(UserModel)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, user: UserModel, user_in: UserCreate) -> UserModel:
        for key, value in user_in.dict().items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
