from uuid import UUID
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class StockRead(BaseModel):
    material_id: UUID
    material_name: str
    value: Decimal

    model_config = ConfigDict(from_attributes=True)
