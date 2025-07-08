from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import UserLogin
from schemas.token import Token
from core.security import verify_password, create_access_token
from models.user import User
from core.database import get_db

router = APIRouter()

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
