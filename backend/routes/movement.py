from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models import User
from services.movement import create_movement, get_all_movements
from schemas.movement import MovementCreate, MovementRead
from services.user import get_current_user

router = APIRouter(prefix="/movements", tags=["Movements"])


# 🔹 Criar movimentação
@router.post("/", response_model=MovementRead, status_code=status.HTTP_201_CREATED)
def create_new_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_movement(db, data, current_user)


# 🔹 Listar movimentações
@router.get("/", response_model=List[MovementRead])
def list_movements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    return get_all_movements(db)