from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MaterialCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category_name: Optional[str] = None  # Agora é opcional

class MaterialUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class MaterialRead(BaseModel):
    id: UUID
    name: str
    category: str
    created_at: datetime
    created_by: str
   
    model_config = ConfigDict(from_attributes=True) 
