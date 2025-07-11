from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import UserLogin
from schemas.token import Token
from core.database import get_db
from services.login import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, data.username, data.password)
    return {"access_token": token, "token_type": "bearer"}
