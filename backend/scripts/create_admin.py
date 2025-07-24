from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import User
from utils.enums import UserRole
from services.user import get_password_hash
import uuid

def create_default_admin():
    db: Session = SessionLocal()

    try:
        existing_admin = db.query(User).filter(User.role == UserRole.admin).first()
        if existing_admin:
            print("O usuário admin já foi criado.")
            return

        admin_user = User(
            id=uuid.uuid4(),
            full_name="Administrador do Sistema",
            username="admin",
            password_hash=get_password_hash("admin1234"),
            role=UserRole.admin,
        )

        db.add(admin_user)
        db.commit()
        print("Usuário admin criado com sucesso")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_admin()
