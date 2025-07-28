from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from core.security import create_access_token, verify_password

# 🔐 Autentica o usuário e retorna o token de acesso
def authenticate_user(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Retorna token JWT com o ID do usuário no campo 'sub'
    token = create_access_token(data={"sub": str(user.id)})
    return token
