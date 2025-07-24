from uuid import UUID
from pydantic import BaseModel, ConfigDict
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

       
    model_config = ConfigDict(from_attributes=True) 
