from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext
from uuid import UUID
from core.security import create_access_token, verify_access_token
from core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# 🔹 Login do usuário
def authenticate_user(db: Session, username: str, password: str) -> str:
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Retorna token JWT com id no sub
    token = create_access_token(data={"sub": str(user.id)})
    return token

# 🔹 Recupera o usuário autenticado a partir do token JWT
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