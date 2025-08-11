from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from services.stock import get_all_stock
from schemas.stock import StockRead
from services.user import get_current_user
from models.user import User

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/", response_model=List[StockRead], status_code=status.HTTP_200_OK)
def list_stocks(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    name: Optional[str] = Query(None, description="Filtrar por nome do material"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_stock(db, category=category, name=name)
