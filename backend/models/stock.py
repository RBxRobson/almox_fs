from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from core.database import Base


class Stock(Base):
    __tablename__ = "stocks"

    material_id = Column(UUID(as_uuid=True), ForeignKey("materials.id"), primary_key=True)
    material = relationship("Material", back_populates="stock", uselist=False)

    value = Column(Numeric(10, 2), nullable=False, default=0)
