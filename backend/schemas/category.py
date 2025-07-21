from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


# Para criação de categoria via API (entrada)
class CategoryCreate(BaseModel):
    name: str


# Para leitura de categoria (resposta)
class CategoryRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True
