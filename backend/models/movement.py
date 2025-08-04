from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base
from utils.enums import MovementType


class Movement(Base):
    __tablename__ = "movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    value = Column(Numeric, nullable=False)

    item_id = Column(UUID(as_uuid=True), ForeignKey("materials.id"), nullable=False)
    item = relationship("Material", back_populates="movements")

    insert_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    inserted_by = relationship("User", back_populates="movements")

    type_insertion = Column(Enum(MovementType), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
