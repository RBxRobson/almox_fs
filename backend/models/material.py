from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from core.database import Base
 

class Material(Base):
    __tablename__ = "materials"

    movements = relationship("Movement", back_populates="item")
    stock = relationship("Stock", back_populates="material", uselist=False)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="materials")

    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="materials_created")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
