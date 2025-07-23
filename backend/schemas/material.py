# schemas/material.py
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class MaterialCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category_id: UUID


class MaterialUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class MaterialRead(BaseModel):
    id: UUID
    name: str
    category_id: str
    created_at: datetime
    created_by: str

    class Config:
        orm_mode = True
