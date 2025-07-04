from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from utils.enums import UserRole

# 🔹 Base compartilhado entre input/output
class UserBase(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3)
    username: str = Field(..., min_length=3)
    role: UserRole

# 🔹 Criação
class UserCreate(UserBase):
    full_name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)

# 🔹 Atualização de senha
class UserUpdatePassword(BaseModel):
    password: str = Field(..., min_length=8)

# 🔹 Login
class UserLogin(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)

# 🔹 Leitura 
class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True