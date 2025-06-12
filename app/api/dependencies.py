# app/api/dependencies.py

from fastapi import Depends
from sqlalchemy.orm import Session

from typing import Generator
from app.db.base import SessionLocal
from app.services.user import UserService
from app.services.ressource import RessourceService
from app.services.emprunt import EmpruntService

def get_db() -> Generator[Session, None, None]:

    """
    Fournit une session SQLAlchemy, et s'assure de la fermer après usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(
    db: Session = Depends(get_db)
) -> UserService:
    """
    Injection du UserService avec sa dépendance en DB.
    """
    return UserService(db)

def get_ressource_service(
    db: Session = Depends(get_db)
) -> RessourceService:
    """
    Injection du RessourceService avec sa dépendance en DB.
    """
    return RessourceService(db)

def get_emprunt_service(
    db: Session = Depends(get_db)
) -> EmpruntService:
    """
    Injection du EmpruntService avec sa dépendance en DB.
    """
    return EmpruntService(db)
