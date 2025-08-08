from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialRead,
)
from services.material import (
    create_material,
    get_all_materials,
    update_material,
    delete_material,
)
from services.user import get_current_user
from core.database import get_db
from models import User
from utils.enums import UserRole

router = APIRouter(
    prefix="/materials",
    tags=["Materials"],
)


@router.get("/", response_model=List[MaterialRead])
def list_materials(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    name: Optional[str] = Query(None, description="Filtrar por nome do material"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_materials(db, category=category, name=name)


@router.post("/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_new_material(
    data: MaterialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem criar materiais.")
    return create_material(db, data, current_user)


@router.put("/{material_id}", response_model=MaterialRead)
def update_existing_material(
    material_id: UUID,
    data: MaterialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem atualizar materiais.")
    return update_material(db, material_id, data)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_material(
    material_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem deletar materiais.")
    delete_material(db, material_id)
