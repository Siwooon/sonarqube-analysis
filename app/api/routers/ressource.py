# app/api/routers/ressource.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.schemas.ressource import RessourceCreate, Ressource, RessourceType
from app.services.ressource import RessourceService
from app.api.dependencies import get_ressource_service

router = APIRouter(tags=["ressources"])

@router.post("/", response_model=Ressource, status_code=status.HTTP_201_CREATED)
def create_ressource(
    res_in: RessourceCreate,
    service: RessourceService = Depends(get_ressource_service)
) -> Ressource:
    return service.create_ressource(res_in)

@router.get("/", response_model=List[Ressource])
def list_ressources(
    type: Optional[RessourceType] = Query(None, alias="type"),
    disponible: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: RessourceService = Depends(get_ressource_service)
) -> List[Ressource]:
    return service.list_ressources(
        type_filter=type.value if type else None,
        dispo_filter=disponible,
        skip=skip,
        limit=limit
    )

@router.get("/{ressource_id}", response_model=Ressource)
def get_ressource(
    res_id: str,
    service: RessourceService = Depends(get_ressource_service)
) -> Ressource:
    res = service.get_ressource(res_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ressource non trouvée")
    return res

@router.put("/{ressource_id}", response_model=Ressource)
def update_ressource(
    res_id: str,
    res_in: RessourceCreate,
    service: RessourceService = Depends(get_ressource_service)
) -> Ressource:
    try:
        return service.update_ressource(res_id, res_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{ressource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ressource(
    res_id: str,
    service: RessourceService = Depends(get_ressource_service)
):
    try:
        service.delete_ressource(res_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
