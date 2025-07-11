from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from services.user import get_current_user
from models.user import User, UserRole
from schemas.user import UserCreate, UserRead
from services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])

# 🔹 Acesso: qualquer usuário autenticado
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return {  
        "id": current_user.id,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "role": current_user.role,
        "created_at": current_user.created_at,
    }

# 🔹 Acesso: apenas admin pode criar usuários
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise PermissionError("Apenas administradores podem criar usuários.")
    
    return user_service.create_user(db, user_data)

# 🔹 Acesso: admin e supervisor
@router.get("/", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise PermissionError("Você não tem permissão para visualizar os usuários.")
    
    return user_service.get_all_users(db)
