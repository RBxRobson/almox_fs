from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from services.user import get_current_user
from models import User
from utils.enums import UserRole
from schemas.user import UserCreate, UserRead, PasswordUpdate
from core.security import verify_password
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

# 🔹 Acesso: qualquer usuário autenticado, alterar senha
@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    user_service.update_user_password(db, current_user.id, data.new_password)

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
