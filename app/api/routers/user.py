# app/api/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, User
from app.services.user import UserService
from app.api.dependencies import get_db, get_user_service

router = APIRouter(tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
) -> User:
    try:
        return service.create_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
) -> List[User]:
    return service.list_users()

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> User:
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: str,
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
) -> User:
    try:
        return service.update_user(user_id, user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
):
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
