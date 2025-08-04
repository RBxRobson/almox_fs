from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from utils.enums import MovementType


class MovementCreate(BaseModel):
    description: str = Field(..., min_length=3, max_length=200)
    item_id: UUID
    value: int = Field(..., gt=0)
    type_insertion: MovementType


class MovementRead(BaseModel):
    id: UUID
    description: str
    item: str
    value: int
    type_insertion: MovementType
    created_at: datetime
    inserted_by: str 

    model_config = ConfigDict(from_attributes=True)
