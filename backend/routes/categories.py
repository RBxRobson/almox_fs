from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.category import CategoryCreate, CategoryRead
from services.category import (
    create_category as create_category_service,
    get_all_categories,
)
from services.user import get_current_user
from core.database import get_db
from models import User

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    return create_category_service(db, data, current_user)


@router.get("/", response_model=List[CategoryRead])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
     
):
    return get_all_categories(db)
