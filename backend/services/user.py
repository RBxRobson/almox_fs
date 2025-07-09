from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext
from uuid import UUID
from core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token, get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Criar novo usuário (apenas admin usa esse service)
def create_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso."
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        full_name=user_data.full_name,
        username=user_data.username,
        password_hash=hashed_password,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 🔹 Atualizar senha
def update_user_password(db: Session, user_id: str, new_password: str) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.password_hash = get_password_hash(new_password)
    db.commit()

# 🔹 Listar usuários (exibição pública)
def get_all_users(db: Session):
    return db.query(User).all()

# 🔹 Recupera o usuário autenticado a partir do token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise credentials_exception

    return user
