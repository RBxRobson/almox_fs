from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from services.stock import get_all_stocks
from schemas.stock import StockRead
from services.user import get_current_user
from models.user import User

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)

@router.get("/", response_model=List[StockRead], status_code=status.HTTP_200_OK)
def list_stocks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_stocks(db)
